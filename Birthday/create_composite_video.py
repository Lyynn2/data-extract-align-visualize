
############
#
# Copyright (c) 2023 Joseph DelPreto / MIT CSAIL and Project CETI
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR
# IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
# Created 2023 by Joseph DelPreto [https://josephdelpreto.com].
# [can add additional updates and authors as desired]
#
############

# A few notable design choices for speed:
#  Use custom subplotting via matrix slicing.
#   This is significantly faster than using a framework such as Matplotlib or PyQtGraph and then exporting plots as images.
#  Use Decord instead of OpenCV for reading videos.
#   This is faster, more accurate for fetching a target frame index, and can scale images during the load.
#  Use PIL instead of OpenCV for loading images.
#   This is faster, and allows for scaling images during the load to get closer to the target size.
#  Using the custom ImagePlot class for graphing, instead of a framework such as Matplotlib or PyQtGraph.
#   This edits an image matrix directly (with quite a few speed considerations),
#   which avoids the need to export a plot as an image.
#  Using the custom ThreadedVideoWriter class, which allows frames to be written to a video in the background.
#   This buffers frames to write, allowing the main loop to create the next frame while the previous one is being written.
#  Only updating parts of the composite frame that have changed, instead of starting from an empty frame each iteration.
#   For example, if a camera image or video frame are active for multiple output frames, can avoid updating that subplot.
#  Compute spectrograms for each file at the beginning, and then scroll through that image matrix.
#   This avoids computing a spectrogram of an audio snippet for each output frame.
#  For large lists such as timestamps that are known to be sorted,
#    using np.searchsorted instead of np.where and using first/last indexes instead of min/max.
#  Avoid making copies of large numpy matrices when possible, and of assigning large segments of a matrix.

import os
import glob
import re
import time
from collections import OrderedDict

import numpy as np
from scipy import signal
from scipy.io import wavfile
from scipy import interpolate
from scipy import spatial
from moviepy.editor import VideoFileClip, AudioFileClip, CompositeAudioClip
import proglog

import cv2
import decord
from ThreadedVideoWriter import ThreadedVideoWriter

from ImagePlot import ImagePlot
import pyqtgraph
import distinctipy

from helpers_synchronization import *
from helpers_data_extraction import *
from helpers_various import *

######################################################
# CONFIGURATION
######################################################

# Specify the root data directory, which contains subfolders for each device.
# The output video will also be saved in this folder.
data_dir_root = 'C:/Users/jdelp/Desktop/_whale_birthday_s3_data'

# Specify the subplot layout of device streams in the output video.
# Each value is (row, column, rowspan, colspan).
composite_layout = OrderedDict([
  # ('Mavic (CETI)'         , (0, 0, 2, 2)),
  # ('Mavic (DSWP)'         , (0, 2, 2, 2)),
  # ('Canon (Gruber)'       , (2, 0, 1, 1)),
  # ('Canon (DelPreto)'     , (2, 1, 1, 1)),
  # ('Phone (DelPreto)'     , (2, 1, 1, 1)),
  # ('GoPro (DelPreto)'     , (2, 1, 1, 1)),
  # ('Canon (DSWP)'         , (2, 2, 1, 1)),
  # ('Drone Positions'      , (2, 3, 1, 1)),
  # ('Phone (Baumgartner)'  , (3, 0, 1, 1)),
  # ('Phone (Pagani)'       , (3, 1, 1, 1)),
  # ('Phone (Salino-Hugg)'  , (3, 2, 1, 1)),
  # ('Phone (Aluma)'        , (3, 3, 1, 1)),
  ('Hydrophone (Mevorach)', (4, 0, 1, 4)),
  # ('Codas Haifa (ICI)'    , (5, 0, 1, 4)),
  # ('Codas Haifa (TFS)'    , (5, 0, 1, 4)),
  # ('Codas Biology (ICI)'  , (6, 0, 1, 4)),
  # ('Codas Biology (TFS)'  , (6, 0, 1, 4)),
])

# Specify friendly names for each device, which will be printed on the output video.
# This also specifies the device IDs that exist, and directories will be searched accordingly.
# For Misc devices, the keyword after "Misc/" will be used to find matching files in the Misc directory.
device_friendlyNames = {
  'CETI-DJI_MAVIC3-1'          : 'Mavic (CETI)',
  'DSWP-DJI_MAVIC3-2'          : 'Mavic (DSWP)',
  'DG-CANON_EOS_1DX_MARK_III-1': 'Canon (Gruber)',
  'JD-CANON_REBEL_T5I'         : 'Canon (DelPreto)',
  'DSWP-CANON_EOS_70D-1'       : 'Canon (DSWP)',
  'DSWP-KASHMIR_MIXPRE6-1'     : 'Hydrophone (Mevorach)',
  'Misc/Aluma'                 : 'Phone (Aluma)',
  'Misc/Baumgartner'           : 'Phone (Baumgartner)',
  'Misc/Pagani'                : 'Phone (Pagani)',
  'Misc/SalinoHugg'            : 'Phone (Salino-Hugg)',
  'Misc/DelPreto_Pixel5'       : 'Phone (DelPreto)',
  'Misc/DelPreto_GoPro'        : 'GoPro (DelPreto)',
  'Drone_Positions'            : 'Drone Positions',
  '_coda_annotations_biology'  : 'Codas Biology', # will catch "Codas Biology (ICI)" and "Codas Biology (TFS)" from the above subplot layout specification
  '_coda_annotations_haifa'    : 'Codas Haifa',   # will catch "Codas Biology (ICI)" and "Codas Biology (TFS)" from the above subplot layout specification
}

# Define the start/end time of the video.
# Some notable times are below for reference:
#   10:20:12.514 + 0.7986 start of CETI Mavic
#   10:51:16.972 + 2.1083 start of DSWP Mavic
#   10:53:46.000 + 32.7085 start of hydrophone
#   15:19:15.834 + 0.7986 end of CETI Mavic
#   14:14:32.143 + 2.1083 end of DSWP Mavic
#   15:29:10.000 + 1008 + 32.7085 end of hydrophone
#   10:20:13.3126 overall start
#   15:46:30.7085 overall end
#   19577.3959 overall duration
#
#   11:45:15 see baby in mom
#   11:45:48 see blood in water
#   11:53:30 whales nearing the boat
#   11:54:55 whales on other side of the boat
#
# # Full span:
# output_video_start_time_str = '2023-07-08 10:20:13 -0400'
# output_video_duration_s = 19579
# #
# # Haifa annotations:
# output_video_start_time_str = '2023-07-08 11:40:30 -0400'
# output_video_duration_s = 9949 # 9931
# #
# Hydrophone file 280:
output_video_start_time_str = '2023-07-08 11:53:34.72 -0400' #'2023-07-08 11:53:34.7085 -0400' (after adding an offset of 32.7085)
output_video_duration_s = 184.32
#
# # Testing for hydrophone file 280:
# output_video_start_time_str = '2023-07-08 11:55:10 -0400'
# output_video_duration_s = 60
#
# # Testing spanning annotation files including 280:
# output_video_start_time_str = '2023-07-08 11:50:10 -0400'
# output_video_duration_s = 20*60
#
# # Testing for spanning hydrophone files 279-280:
# output_video_start_time_str = '2023-07-08 11:53:00 -0400'
# output_video_duration_s = 60
# # Testing for spanning hydrophone files 279-280:
# output_video_start_time_str = '2023-07-08 11:53:30 -0400'
# output_video_duration_s = 5

# Define the frame rate of the output video.
output_video_fps = 25

# Define the output video size and resolution.
composite_layout_column_width = 600 # also defines the scaling/resolution of photos/videos
subplot_border_size = 8 # the padding between subplots
composite_layout_row_height = round(composite_layout_column_width/(1+7/9)) # Drone videos have an aspect ratio of 1.7777

# Specify whether the output video should be compressed.
# This will add an extra compression stage after the output video is generated.
# Note that the video will be implicitly compressed if audio is added to it,
#  so if add_audio_track_to_output_video_original is True then the below compression may be skippable.
output_video_compressed_rate_MB_s = None # None to not compress the video # 0.5

# Define the audio track added to the output video.
# Note that the process of adding audio will implictly compress the video too.
save_audio_track_as_separate_file = True
output_audio_track_volume_gain_factor = 50 # 1 to not change the volume
add_audio_track_to_output_video_original = True   # Add audio to the raw output video.
add_audio_track_to_output_video_compressed = True # Add audio to a version that was explicitly compressed via output_video_compressed_rate_MB_s
delete_output_video_withoutAudio = True # Delete the raw output video without audio, which may be quite large

# Configure device and timestamp labels on the output video.
output_video_banner_height_fraction = 0.03 # fraction of the final composite frame height
output_video_banner_bg_color   = [100, 100, 100] # RGB
output_video_banner_text_color = [0,   255, 255] # RGB
# Configure the labels that identify device streams on the output video.
output_video_subplot_labels_text_color = [255, 255, 255] # RGB
output_video_subplot_labels_bg_color = [100, 100, 100] # RGB
output_video_subplot_labels_font_size = 0.9
output_video_subplot_labels_font_thickness = 1
output_video_subplot_labels_font = cv2.FONT_HERSHEY_SIMPLEX

# Configure audio parsing and plotting.
audio_resample_rate_hz = 96000 # original rate is 96000
audio_plot_duration_beforeCurrentTime_s = 5
audio_plot_duration_afterCurrentTime_s  = 10
audio_num_channels_toPlot = 1
audio_plot_type = 'spectrogram' # 'spectrogram' or 'waveform'
audio_plot_x_tick_spacing = {'major':2, 'minor':1} # will only show major ticks
audio_plot_grid_thickness = {'major': 2, 'minor': 2}
audio_plot_font_size = 0.9
audio_plot_label_color = (150, 150, 150) # RGB
# Configure audio waveform plotting.
audio_waveform_plot_colors = [(255, 255, 255), (255, 0, 255)] # RGB for each channel
audio_waveform_line_thicknesses = [4, 1] # an entry for each channel
audio_waveform_plot_currentTime_color = (255, 255, 255) # RGB
audio_waveform_plot_currentTime_thickness = 2
# Configure audio spectrogram plotting.
audio_spectrogram_frequency_range = [0e3, min(40e3, audio_resample_rate_hz//2)] # Will be adjusted to match the achieved min/max after the first spectrogram is computed
audio_spectrogram_frequency_tick_spacing_khz = 10
audio_spectrogram_target_window_s = 0.03 # note that the achieved window may be a bit different
audio_spectrogram_colormap = pyqtgraph.colormap.get('gist_stern', source='matplotlib', skipCache=True) # some other promising ones: 'nipy_spectral', 'turbo'
audio_spectrogram_colorbar_levels = [0, 0.4]
audio_spectrogram_colorbar_width_ratio = 0.0125 # fraction of plot image width
audio_spectrogram_plot_currentTime_color = (255, 255, 255) # RGB
audio_spectrogram_plot_currentTime_thickness = 2

# Configure coda annotations plotting.
codas_uncertain_whale_index = 20 # whale indexes >= this number represent uncertain annotations
codas_plot_yrange = {'ici': [-25, 625],
                     'tfs': [-0.2, 2.0]}
codas_plot_line_thickness = 3
codas_plot_marker_edge_width = lambda whale_index: 1 if whale_index < codas_uncertain_whale_index \
                                                   else 2
codas_plot_marker_edge_color = lambda whale_index: (150, 150, 150) if whale_index < codas_uncertain_whale_index \
                                                   else (255, 0, 0) # RGB
codas_plot_marker_symbol = lambda whale_index: 'circle' if whale_index < codas_uncertain_whale_index \
                                               else 'diamond'
codas_plot_marker_symbol_endClick = lambda whale_index: 'square' if whale_index < codas_uncertain_whale_index \
                                                        else 'triangle'
codas_plot_marker_size = lambda whale_index: 16 if whale_index < codas_uncertain_whale_index else 14
codas_plot_currentTime_thickness = 2
codas_plot_currentTime_color = (255, 255, 255) # RGB
codas_plot_font_size = 0.9
codas_plot_x_tickSpacing_s = {'ici': audio_plot_x_tick_spacing,
                              'tfs': audio_plot_x_tick_spacing}
codas_plot_y_tickSpacing = {'ici': {'major':150, 'minor':1}, # will only show major ticks
                            'tfs': {'major':0.3, 'minor':1}} # will only show major ticks
codas_plot_duration_beforeCurrentTime_s = audio_plot_duration_beforeCurrentTime_s #+ 0.325
codas_plot_duration_afterCurrentTime_s = audio_plot_duration_afterCurrentTime_s #+ 0.325
codas_plot_label_color = (150, 150, 150) # RGB
codas_plot_grid_thickness = {'major': 2, 'minor': 2}
codas_plot_grid_color = {'major': (50, 50, 50), 'minor': (25, 25, 25)} # RGB
codas_plot_unique_whale_colors = None # Will be computed later, once the number of whales is known
codas_plot_whale_color = None # Will be a lambda function assigned later, once whale colors are computed
# Configuration specific to TFS version of plot.
codas_plot_tfs_scaleFactor = 1

# Configuration for aligning spectrogram/waveform plots with coda plots.
audio_plots_left_axis_position_ratio = 0.05  # fraction of plot image width at which the leftmost edge of the axis will be plotted
audio_plots_right_axis_position_ratio = 0.95 # fraction of plot image width at which the rightmost edge of the axis will be plotted
audio_plot_horizontal_alignment = 0 # fraction of composite image width at which to place the leftmost edge of the image plot inside the subplot
codas_plot_hide_xlabels = {'biology': {'ici': False, 'tfs': False},
                           'haifa':   {'ici': False,  'tfs': False}}
audio_plot_hide_xlabels = True

# Configure drone plotting.
drone_plot_reference_location_lonLat = [-61.373179, 15.306914] # will plot meters from this location (the Mango house)
conversion_factor_lat_to_km = (111.32) # From simplified Haversine formula: https://stackoverflow.com/a/39540339
conversion_factor_lon_to_km = (40075 * np.cos(np.radians(drone_plot_reference_location_lonLat[1])) / 360) # From simplified Haversine formula: https://stackoverflow.com/a/39540339
drone_lat_to_km = lambda lat:  (lat - drone_plot_reference_location_lonLat[1])*conversion_factor_lat_to_km
drone_lon_to_km = lambda lon: -(lon - drone_plot_reference_location_lonLat[0])*conversion_factor_lon_to_km
drone_plot_rangeRatio_bounds = [1, 3] # min/max ratio that the plot range can be, relative to the distance between the drones, before starting to zoom in/out
drone_plot_minRange_km = 250/1000 # minimum range of x or y axis; but if drones are far from each other, range can dynamically expand
drone_plot_rangePad_km = 75/1000  # minimum distance from a drone to the edge of the plot
drone_plot_tickSpacing_km = {'minor':25/1000, 'major':100/1000}
drone_plot_colors = [(210, 0, 210), (0, 190, 190)] # RGB for each drone; used for position plot and for outline on video labels
drone_plot_marker_edge_thickness = 5 # outline of markers that will indicate which drone it is
drone_plot_colorbar_levels_m = [0, 150] # altitude colorbar limits
drone_plot_colorbar_tickSpacing_m = 25
drone_plot_colormap = pyqtgraph.colormap.get('gist_stern', source='matplotlib', skipCache=True)
drone_plot_colorbar_width_ratio = 0.033 # fraction of plot image width
drone_plot_grid_thickness = {'major': 2, 'minor': 2}
drone_plot_label_color = (150, 150, 150) # RGB
drone_plot_symbolSize = round(0.05 * composite_layout_column_width)
drone_plot_font_size = 0.8

# Configure how device timestamps are matched with output video frame timestamps.
# For each output video frame timestamp, will look for a device timestamp that is
#  within a certain distance of that target time.
# Each entry below specifies this window as (time_before_target_timestamp, time_after_target_timestamp).
# Being strict would use 1/output_video_fps*0.5, which enforces that a device time must be within half of an output frame duration.
#  In other words, finding the output frame that is the best match for a device time.
# To add some leeway and avoid black frames if a device timestamps are slightly inconsistent though,
#  the windows will be expanded slightly.
timestamp_to_target_thresholds_s = {
  'video': (1/output_video_fps*0.6, 1/output_video_fps*0.6),
  'audio': (1/output_video_fps*0.6, 1/output_video_fps*0.6),
  'image': (1,                      1/output_video_fps*0.6), # first entry controls how long an image will be shown
  'drone': (1/output_video_fps*0.6, 1/output_video_fps*0.6),
  'codas': (1/output_video_fps*0.6, 1/output_video_fps*0.6),
}

# Visualization debugging options.
show_visualization_window = False
debug_composite_layout = False # Will show the layout with dummy data and then exit

# Derived configurations.
if audio_plot_type == 'waveform':
  audio_plot_length_beforeCurrentTime = int(audio_resample_rate_hz * audio_plot_duration_beforeCurrentTime_s)
  audio_plot_length_afterCurrentTime = int(audio_resample_rate_hz * audio_plot_duration_afterCurrentTime_s)
  audio_plot_length = 1 + audio_plot_length_beforeCurrentTime + audio_plot_length_afterCurrentTime
  audio_timestamps_toPlot_s = np.arange(start=0, stop=audio_plot_length)/audio_resample_rate_hz - audio_plot_duration_beforeCurrentTime_s
elif audio_plot_type == 'spectrogram':
  # Plot lengths will be derived later once the achieved spectrogram window size is known
  audio_plot_length_beforeCurrentTime = None
  audio_plot_length_afterCurrentTime = None
  audio_plot_length = None
audio_spectrogram_window_s = None
audio_plot_duration_s = (audio_plot_duration_beforeCurrentTime_s + audio_plot_duration_afterCurrentTime_s)

drone_plot_color_lookup = drone_plot_colormap.getLookupTable(start=0, stop=1, nPts=1000)
drone_plot_color_lookup_keys = np.linspace(start=drone_plot_colorbar_levels_m[0], stop=drone_plot_colorbar_levels_m[1], num=1000)

output_video_num_rows = max([layout_specs[0] + layout_specs[2] for layout_specs in composite_layout.values()])
output_video_num_cols = max([layout_specs[1] + layout_specs[3] for layout_specs in composite_layout.values()])
output_video_width = composite_layout_column_width*output_video_num_cols + subplot_border_size*(output_video_num_cols+1)
output_video_height = composite_layout_row_height*output_video_num_rows + subplot_border_size*(output_video_num_rows+1)
# Create a blank image to use as the background.
def get_composite_img_blank():
  return np.zeros(shape=(output_video_height, output_video_width, 3), dtype=np.uint8)

output_video_banner_fontScale = None # will be determined later based on the size of the banner
output_video_banner_textSize  = None # will be determined later once the font scale is computed
output_video_banner_height = int(output_video_banner_height_fraction*output_video_height)
output_video_banner_font = cv2.FONT_HERSHEY_SIMPLEX

output_video_start_time_s = time_str_to_time_s(output_video_start_time_str)

output_video_filepath = os.path.join(data_dir_root,
                                     'composite_video_TEST_fps%d_duration%d_start%d_colWidth%d_audio%d%s%s.mp4'
                                     % (output_video_fps, output_video_duration_s,
                                        1000*output_video_start_time_s,
                                        composite_layout_column_width,
                                        audio_resample_rate_hz, audio_plot_type,
                                        ''.join(['_codasICI' if True in ['(ICI)' in x for x in list(composite_layout.keys())] else '',
                                                 '_codasTFS' if True in ['(TFS)' in x for x in list(composite_layout.keys())] else '',
                                                 '_codasBio' if True in ['Codas Biology' in x for x in list(composite_layout.keys())] else '',
                                                 '_codasHaifa' if True in ['Codas Haifa' in x for x in list(composite_layout.keys())] else '',
                                                 ])))


######################################################
# HELPERS
######################################################

# Convert a device friendly name to a device ID.
def device_friendlyName_to_id(device_friendlyName_toFind):
  if 'Codas Biology (' in device_friendlyName_toFind:
    device_friendlyName_toFind = 'Codas Biology'
  if 'Codas Haifa (' in device_friendlyName_toFind:
    device_friendlyName_toFind = 'Codas Haifa'
  for (device_id, device_friendlyName) in device_friendlyNames.items():
    if device_friendlyName == device_friendlyName_toFind:
      return device_id
  return None

# Add a banner to the output frame that displays the current timestamp.
def add_timestamp_banner(img, timestamp_s):
  global output_video_banner_fontScale, output_video_banner_textSize
  
  # Add the bottom banner shading.
  img = cv2.copyMakeBorder(img, 0, output_video_banner_height, 0, 0,
                           cv2.BORDER_CONSTANT, value=output_video_banner_bg_color)
  
  # Specify the text to write.
  timestamp_str = '%s (%0.3f)' % (time_s_to_str(timestamp_s, localtime_offset_s, localtime_offset_str),
                                  timestamp_s)
  
  # Compute the size of the text that will be drawn on the image.
  fontFace = output_video_banner_font
  fontThickness = 2 if output_video_banner_height > 25 else 1
  if output_video_banner_fontScale is None:
    # If this is the first time, compute a font size to use.
    target_height = 0.5*output_video_banner_height
    target_width = 1e6 # don't filter on the width for now
    fontScale = 0
    textsize = None
    while (textsize is None) or ((textsize[1] < target_height) and (textsize[0] < target_width)):
      fontScale += 0.2
      textsize = cv2.getTextSize(timestamp_str, fontFace, fontScale, fontThickness)[0]
    fontScale -= 0.2
    textsize = cv2.getTextSize(timestamp_str, fontFace, fontScale, fontThickness)[0]
    output_video_banner_fontScale = fontScale
    output_video_banner_textSize = textsize
  else:
    # Otherwise, use the previously computed font size.
    output_video_banner_textSize = cv2.getTextSize(timestamp_str, fontFace, output_video_banner_fontScale, fontThickness)[0]
  
  # Compute a position that will center the text in the banner.
  text_position = [int(img.shape[1]/2 - output_video_banner_textSize[0]/2),
                   int(img.shape[0] - output_video_banner_height/2 + output_video_banner_textSize[1]/3)]
  
  # Draw the text on the image.
  img = cv2.putText(img, timestamp_str, text_position,
                    fontFace=fontFace, fontScale=output_video_banner_fontScale,
                    color=output_video_banner_text_color, thickness=fontThickness)
  return img


# Get slice indexes into the main composite image that represent a desired subplot region.
# Returned indexes will be inclusive of start indexes but exclusive of end indexes
#  so they can be used to directly index an array.
# layout_specs is (row, column, rowspan, colspan).
# If subplot_img is None, will return the entire subplot area.
# If subplot_img is provided, will use its size and place it within the subplot.
#   If horizontal_alignment controls how the image is positioned within the larger subplot area.
#     Can be 'center', 'left', 'right', or a number between 0 and 1.
#     If a number is provided, will place the left edge of the subplot image at that fraction of the overall subplot area.
def get_slice_indexes_for_subplot_update(layout_specs, subplot_img=None, horizontal_alignment='center'):
  (row, col, rowspan, colspan) = layout_specs
  # Get the indexes of the total space allocated to this subplot.
  start_col_index = subplot_border_size*(col+1) + composite_layout_column_width*(col)
  end_col_index = start_col_index + composite_layout_column_width*(colspan) + subplot_border_size*(colspan-1) - 1
  start_row_index = subplot_border_size*(row+1) + composite_layout_row_height*(row)
  end_row_index = start_row_index + composite_layout_row_height*(rowspan) + subplot_border_size*(rowspan-1) - 1
  # Position the desired image in the subplot.
  if subplot_img is not None:
    subplot_width = end_col_index - start_col_index + 1
    if horizontal_alignment == 'center':
      pad_left = (subplot_width - subplot_img.shape[1])//2
      pad_right = (subplot_width - subplot_img.shape[1]) - pad_left
    elif horizontal_alignment == 'left':
      pad_left = 0
      pad_right = (subplot_width - subplot_img.shape[1]) - pad_left
    elif horizontal_alignment == 'right':
      pad_right = 0
      pad_left = (subplot_width - subplot_img.shape[1]) - pad_right
    elif isinstance(horizontal_alignment, float): # fractional shift from the left
      pad_left = round(subplot_width*horizontal_alignment)
      pad_right = (subplot_width - subplot_img.shape[1]) - pad_left
    else:
      raise AssertionError('Unknown subplot alignment option [%s]' % horizontal_alignment)
    start_col_index += pad_left
    end_col_index -= pad_right
    subplot_height = end_row_index - start_row_index + 1
    pad_top = (subplot_height - subplot_img.shape[0])//2
    pad_bottom = (subplot_height - subplot_img.shape[0]) - pad_top
    start_row_index += pad_top
    end_row_index -= pad_bottom
  # Return the slice indexes.
  # Increment end indexes since the end indexes computed above were considered inclusive,
  #  but slicing will be exclusive of the end indexes.
  return (start_row_index, end_row_index+1, start_col_index, end_col_index+1)

# Get the size of a subplot area.
def get_subplot_size(layout_specs):
  (start_row_index, end_row_index, start_col_index, end_col_index) = get_slice_indexes_for_subplot_update(layout_specs)
  subplot_width = end_col_index - start_col_index
  subplot_height = end_row_index - start_row_index
  return (subplot_width, subplot_height)
  
######################################################
# LOAD TIMESTAMPS AND DATA POINTERS
######################################################

# Will create a dictionary with following structure:
#   [device_id][filepath] = (timestamps_s, data)
#   If filepath points to a video:
#     timestamps_s is a numpy array of epoch timestamps for every frame
#     data is a video reader object
#   If filepath points to a wav file:
#     timestamps_s is a numpy array of epoch timestamps for every sample
#     if requesting waveforms, data is an [num_samples x num_channels] matrix of audio data
#     if requesting spectrograms, data is a tuple with (spectrogram, spectrogram_t, spectrogram_f).
#   If filepath points to an image:
#     timestamps_s is a single-element numpy array with the epoch timestamps of the image
#     data is the filepath again
media_infos = OrderedDict()

print()
print('Getting timestamps and pointers to video/image/audio data for every frame/photo/sample')
for (device_friendlyName, layout_specs) in composite_layout.items():
  (row, col, rowspan, colspan) = layout_specs
  device_id = device_friendlyName_to_id(device_friendlyName)
  (subplot_width, subplot_height) = get_subplot_size(layout_specs)
  
  # Extract the timestamped data for this device.
  media_info = get_timestamped_data_audioVideoImage(
                data_dir_root, [device_id], device_friendlyNames=[device_friendlyName],
                audio_type=audio_plot_type, audio_resample_rate_hz=audio_resample_rate_hz,
                audio_spectrogram_target_window_s=audio_spectrogram_target_window_s,
                video_target_width=subplot_width, video_target_height=subplot_height,
                start_time_cutoff_s=output_video_start_time_s, end_time_cutoff_s=(output_video_start_time_s+output_video_duration_s),
                suppress_printing=False)
    
  # Perform any additional processing on the data,
  #  then store it in the appropriate dictionary.
  if device_id in media_info:
    media_infos[device_id] = {}
    for (filepath, (timestamps_s, data)) in media_info[device_id].items():
      if is_video(filepath):
        media_infos[device_id][filepath] = (timestamps_s, data)
      elif is_image(filepath):
        media_infos[device_id][filepath] = (timestamps_s, data)
      elif is_audio(filepath) and audio_plot_type == 'spectrogram':
        # Get the computed spectrogram of the entire file.
        (spectrogram, spectrogram_t, spectrogram_f) = data
        # Determine epoch timestamps of each entry in the spectrogram.
        timestamps_s = spectrogram_t + timestamps_s[0]
        # Truncate to the desired frequency range.
        min_f_index = spectrogram_f.searchsorted(audio_spectrogram_frequency_range[0])
        max_f_index = spectrogram_f.searchsorted(audio_spectrogram_frequency_range[-1])
        spectrogram_f = spectrogram_f[min_f_index:(max_f_index+1)]
        spectrogram = spectrogram[min_f_index:max_f_index, :]
        # If this is the first spectrogram computed:
        #   Update the plot frequency range to match the achieved range after discretization.
        # Otherwise, check that the achieved window size and frequency range are the same for all files.
        #  (If not, will need to store these settings for each file.)
        if audio_spectrogram_window_s is None:
          audio_spectrogram_frequency_range = [spectrogram_f[0], spectrogram_f[-1]]
        else:
          assert(audio_spectrogram_window_s == np.round(np.mean(np.diff(spectrogram_t)), 6))
          assert(audio_spectrogram_frequency_range == [spectrogram_f[0], spectrogram_f[-1]])
        # Compute the audio plot range based on the achieved window size.
        audio_spectrogram_window_s = np.round(np.mean(np.diff(spectrogram_t)), 6)
        audio_plot_length_beforeCurrentTime = int(audio_plot_duration_beforeCurrentTime_s/audio_spectrogram_window_s)
        audio_plot_length_afterCurrentTime = int(audio_plot_duration_afterCurrentTime_s/audio_spectrogram_window_s)
        audio_plot_length = 1 + audio_plot_length_beforeCurrentTime + audio_plot_length_afterCurrentTime
        # Convert spectrogram magnitudes to colors.
        # Also convert from BGR to RGB.
        spectrogram_colormapped = audio_spectrogram_colormap.map(spectrogram/audio_spectrogram_colorbar_levels[1])[:,:,(2,1,0)]
        # Save the information
        media_infos[device_id][filepath] = (timestamps_s, spectrogram_colormapped)
    
# For drone data, will create a dictionary of the same format
#   [device_id][filepath] = (timestamps_s, data) where
#   timestamps_s is a numpy array of epoch timestamps for every frame
#   data is a dictionary returned by helpers.get_drone_srt_data()
drone_datas = OrderedDict()
print()
print('Getting timestamps and pointers to data for every drone frame')
for (device_friendlyName, layout_specs) in composite_layout.items():
  (row, col, rowspan, colspan) = layout_specs
  device_id = device_friendlyName_to_id(device_friendlyName)
  (subplot_width, subplot_height) = get_subplot_size(layout_specs)
  
  # Extract the timestamped data for this device.
  drone_data = get_timestamped_data_drones(
                  data_dir_root, [device_id], [device_friendlyName],
                  end_time_cutoff_s=(output_video_start_time_s+output_video_duration_s),
                  suppress_printing=False)
  
  # Perform any additional processing on the data,
  #  then store it in the appropriate dictionary.
  if device_id in drone_data:
    drone_datas[device_id] = {}
    for (filepath, (timestamps_s, data)) in drone_data[device_id].items():
      drone_datas[device_id][filepath] = (timestamps_s, data)

# For coda annotations, will create one combined dictionary from all files.
codas_data = dict([(source, {'coda_start_times_s': [],
                             'coda_end_times_s': [],
                             'click_icis_s': [],
                             'click_times_s': [],
                             'whale_indexes': [],
                             }) for source in ['biology', 'haifa']])
codas_files_start_times_s = dict([(source, []) for source in ['biology', 'haifa']])
codas_files_end_times_s = dict([(source, []) for source in ['biology', 'haifa']])
print()
print('Getting coda annotations')
for (device_friendlyName, layout_specs) in composite_layout.items():
  (row, col, rowspan, colspan) = layout_specs
  device_id = device_friendlyName_to_id(device_friendlyName)
  (subplot_width, subplot_height) = get_subplot_size(layout_specs)
  
  # Extract the timestamped data for this device.
  coda_data = get_timestamped_data_codas(
                data_dir_root, device_ids=[device_id], device_friendlyNames=[device_friendlyName],
                suppress_printing=False)
  
  # Perform any additional processing on the data,
  #  then store it in the appropriate dictionary.
  for (source, data) in coda_data.items():
    codas_data[source] = data
    
print()

######################################################
# VISUALIZATION FUNCTIONS
######################################################

# Update a subplot with new image data.
# composite_img is the composite frame image to update.
# layout_specs is (row, col, rowspan, colspan) of the subplot location.
# data is the image to place in its subplot.
# subplot_label is text to write on the image if desired.
#   subplot_label_color is the text color in RGB format.
# subplot_horizontal_alignment controls how the image is positioned within the larger subplot area.
#   Can be 'center', 'left', 'right', or a number between 0 and 1.
#   If a number is provided, will place the left edge of the subplot image at that fraction of the overall subplot area.
# Returns the updated composite image.
def update_image_subplot(composite_img, layout_specs, data,
                         subplot_label=None, subplot_label_outline_color=None,
                         subplot_horizontal_alignment='center'):
  # Update the subplot within the image.
  image_slice_indexes = get_slice_indexes_for_subplot_update(layout_specs, data, horizontal_alignment=subplot_horizontal_alignment)
  composite_img[image_slice_indexes[0]:image_slice_indexes[1], image_slice_indexes[2]:image_slice_indexes[3]] = data
  # Add a label to the subplot if desired.
  if subplot_label is not None and len(subplot_label) > 0:
    # Get the indexes of the entire subplot area and to the region for the placed image.
    subplot_slice_indexes = get_slice_indexes_for_subplot_update(layout_specs)
    subplot_width = subplot_slice_indexes[3] - subplot_slice_indexes[2]
    subplot_height = subplot_slice_indexes[1] - subplot_slice_indexes[0]
    # Determine the size and position of the text on the image/subplot.
    (text_w, text_h, _, text_pos) = draw_text_on_image(np.zeros_like(data), subplot_label,
                                       pos=(0, -1), # bottom left corner
                                       font_scale=output_video_subplot_labels_font_size,
                                       font_thickness=output_video_subplot_labels_font_thickness,
                                       font=output_video_subplot_labels_font,
                                       text_width_ratio=None,
                                       text_bg_color_bgr=output_video_subplot_labels_bg_color,
                                       text_bg_outline_color_bgr=subplot_label_outline_color,
                                       text_color_bgr=output_video_subplot_labels_text_color,
                                       preview_only=True)
    # If the text can fit on the data image, draw it in its bottom-left corner.
    if text_w <= data.shape[1]:
      draw_text_on_image(composite_img, subplot_label,
                         pos=(text_pos[0]+image_slice_indexes[2],  # x position of text in data, plus left of data in composite frame
                              text_pos[1]+image_slice_indexes[0]), # y position of text in data, plus top of data in composite frame
                         font_scale=output_video_subplot_labels_font_size,
                         font_thickness=output_video_subplot_labels_font_thickness,
                         font=output_video_subplot_labels_font,
                         text_width_ratio=None,
                         text_bg_color_bgr=output_video_subplot_labels_bg_color,
                         text_bg_outline_color_bgr=subplot_label_outline_color,
                         text_color_bgr=output_video_subplot_labels_text_color)
    # Otherwise, center it over the data image but allow it to extend beyond its bounds.
    else:
      # If the text is larger than the subplot, scale it to fit.
      if text_w > subplot_width:
        text_width_ratio = 0.95
      else:
        text_width_ratio = None
      # Determine the size and position of the scaled centered text on the subplot area.
      (text_w, text_h, font_scale, text_pos) = draw_text_on_image(np.zeros(shape=(subplot_height, subplot_width, 3), dtype=np.uint8),
                                                 subplot_label,
                                                 pos=(0.5, -1), # centered left/right, bottom
                                                 font_scale=output_video_subplot_labels_font_size,
                                                 font_thickness=output_video_subplot_labels_font_thickness,
                                                 font=output_video_subplot_labels_font,
                                                 text_width_ratio=text_width_ratio,
                                                 text_bg_color_bgr=output_video_subplot_labels_bg_color,
                                                 text_bg_outline_color_bgr=subplot_label_outline_color,
                                                 text_color_bgr=output_video_subplot_labels_text_color,
                                                 preview_only=True)
      # Draw the text on the full composite image.
      draw_text_on_image(composite_img, subplot_label,
                         pos=(text_pos[0]+subplot_slice_indexes[2],  # x position of text in subplot, plus left of subplot in composite frame
                              text_pos[1]+subplot_slice_indexes[0]), # y position of text in subplot, plus top of subplot in composite frame
                         font_scale=font_scale,
                         font_thickness=output_video_subplot_labels_font_thickness,
                         font=output_video_subplot_labels_font,
                         text_width_ratio=None,
                         text_bg_color_bgr=output_video_subplot_labels_bg_color,
                         text_bg_outline_color_bgr=subplot_label_outline_color,
                         text_color_bgr=output_video_subplot_labels_text_color)
  # Return the updated composite image.
  return composite_img


# Update a subplot with new audio data.
# composite_img is the composite frame image to update.
# layout_specs is (row, col, rowspan, colspan) of the subplot location.
# data is the spectrogram image matrix or waveform data.
# subplot_horizontal_alignment controls how the image is positioned within the larger subplot area.
#   Can be 'center', 'left', 'right', or a number between 0 and 1.
#   If a number is provided, will place the left edge of the subplot image at that fraction of the overall subplot area.
# audio_imagePlot is the ImagePlot object to update.
# Returns the updated composite image.
def update_audio_subplot(composite_img, layout_specs, data,
                         audio_imagePlot,
                         subplot_horizontal_alignment='center'):
  if audio_plot_type == 'waveform':
    # Reset the plot to an empty state.
    audio_imagePlot.clear_plot()
    # Update the y limits.
    upper_data_value = np.quantile(data, 0.95)
    if upper_data_value < 50:
      y_limits = [-50, 50] # avoid zooming in to an empty plot
    else:
      y_limits = upper_data_value*np.array([-1, 1])
    audio_imagePlot.set_y_ticks_major(y_limits[1]*np.array([-1, 0, 1]))
    audio_imagePlot.set_y_limits(y_limits)
    audio_imagePlot.render_empty()
    for channel_index in range(audio_num_channels_toPlot):
      audio_imagePlot.plot(audio_timestamps_toPlot_s, data[:,channel_index],
                            line_thickness=audio_waveform_line_thicknesses[channel_index],
                            color=audio_waveform_plot_colors[channel_index],
                            marker_symbols=None)
    # Plot a vertical current time marker.
    if upper_data_value < 50:
      audio_imagePlot.plot([0, 0], [-50, 50], marker_symbols=None,
                            line_thickness=audio_waveform_plot_currentTime_thickness,
                            color=audio_waveform_plot_currentTime_color)
    else:
      audio_imagePlot.plot([0, 0], upper_data_value*np.array([-1, 1]), marker_symbols=None,
                            line_thickness=audio_waveform_plot_currentTime_thickness,
                            color=audio_waveform_plot_currentTime_color)
    # Update the subplot with the image.
    composite_img = update_image_subplot(composite_img, layout_specs,
                                         audio_imagePlot.get_plot_image(),
                                         subplot_label=None, subplot_label_outline_color=None,
                                         subplot_horizontal_alignment=subplot_horizontal_alignment)
  
  elif audio_plot_type == 'spectrogram':
    # Reset the plot to an empty axis.
    audio_imagePlot.clear_plot()
    # Add the spectrogram image,
    #  and stretch it to fill the axis limits.
    audio_imagePlot.plot_image(data, flip_image_upDown=True)
    # Add the current-time marker.
    audio_imagePlot.plot([0, 0], audio_imagePlot.get_y_limits(), marker_symbols=None,
                                line_thickness=audio_spectrogram_plot_currentTime_thickness,
                                color=audio_spectrogram_plot_currentTime_color)
    # Update the subplot with the image.
    composite_img = update_image_subplot(composite_img, layout_specs,
                                         audio_imagePlot.get_plot_image(),
                                         subplot_label=None, subplot_label_outline_color=None,
                                         subplot_horizontal_alignment=subplot_horizontal_alignment)
  
  else:
    raise AssertionError('Unknown audio plot type [%s]' % audio_plot_type)
  
  # Return the updated composite image.
  return composite_img

# Update a subplot with new coda annotation data.
# composite_img is the composite frame image to update.
# layout_specs is (row, col, rowspan, colspan) of the subplot location.
# coda_data is a dictionary of coda annotation information to plot.
# current_time_s is the current epoch time for the plot.
# coda_plot_type is 'ici' or 'tfs'.
# codas_imagePlot is the ImagePlot object to update.
# subplot_horizontal_alignment controls how the image is positioned within the larger subplot area.
#   Can be 'center', 'left', 'right', or a number between 0 and 1.
#   If a number is provided, will place the left edge of the subplot image at that fraction of the overall subplot area.
# Returns the updated composite image.
def update_codas_subplot(composite_img, layout_specs,
                         coda_data, current_time_s, coda_plot_type, codas_imagePlot,
                         subplot_horizontal_alignment='center'):
  # Reset the plot to an empty axis.
  codas_imagePlot.clear_plot()
  # Plot all codas in the given window.
  max_y_value = 0
  for coda_index in range(len(coda_data['click_times_s'])):
    click_times_s = coda_data['click_times_s'][coda_index]
    click_icis_s = coda_data['click_icis_s'][coda_index]
    whale_index = coda_data['whale_indexes'][coda_index]
    # Create a series of symbols for each click marker.
    symbols = [codas_plot_marker_symbol(whale_index)] * len(click_times_s)
    if coda_plot_type == 'ici':
      # The last click will be plotted at a fictitious ICI that copies the previous one.
      # Use a different symbol for the last click, as a reminder that it is a fictitious ICI.
      if len(click_icis_s) > 0:
        click_icis_s = click_icis_s + [click_icis_s[-1]]
      else:
        click_icis_s = [0.0] # plot single clicks at the bottom of the graph
      symbols[-1] = codas_plot_marker_symbol_endClick(whale_index)
      # Plot the series of clicks at their subsequent ICI.
      click_icis_ms = np.array(click_icis_s)*1000
      codas_imagePlot.plot(click_times_s - current_time_s, # make time relative to current time
                            click_icis_ms,
                            line_thickness=codas_plot_line_thickness,
                            color=codas_plot_whale_color(whale_index),
                            marker_symbols=symbols,
                            marker_size=codas_plot_marker_size(whale_index),
                            marker_edge_thickness=codas_plot_marker_edge_width(whale_index),
                            marker_edge_color=codas_plot_marker_edge_color(whale_index),
                            )
      max_y_value = max(max_y_value, max(click_icis_ms))
    elif coda_plot_type == 'tfs':
      # Plot the series of clicks at their time since coda start.
      click_tfs_s = (click_times_s - click_times_s[0]) * codas_plot_tfs_scaleFactor
      codas_imagePlot.plot(click_times_s - current_time_s,  # make time relative to current time
                            click_tfs_s,
                            line_thickness=codas_plot_line_thickness,
                            color=codas_plot_whale_color(whale_index),
                            marker_symbols=symbols,
                            marker_size=codas_plot_marker_size(whale_index),
                            marker_edge_thickness=codas_plot_marker_edge_width(whale_index),
                            marker_edge_color=codas_plot_marker_edge_color(whale_index),
                            )
      max_y_value = max(max_y_value, max(click_tfs_s))
  # Update the y range if using auto scaling.
  # Note that this will take effect on the plot update rather than this one
  #  (it will redraw the empty plot now, but the above codas have already been plotted).
  if codas_plot_yrange[coda_plot_type] == 'auto' and len(coda_data['click_times_s']) > 0:
    codas_imagePlot.set_y_limits([0, max_y_value*1.05])
    codas_imagePlot.render_empty()
  # Plot the current-time marker.
  codas_imagePlot.plot([0, 0], codas_imagePlot.get_y_limits(), marker_symbols=None,
                                line_thickness=codas_plot_currentTime_thickness,
                                color=codas_plot_currentTime_color)
  # Update the subplot with the image.
  composite_img = update_image_subplot(composite_img, layout_specs,
                                       codas_imagePlot.get_plot_image(),
                                       subplot_label=None, subplot_label_outline_color=None,
                                       subplot_horizontal_alignment=subplot_horizontal_alignment)
  # Return the updated composite image.
  return composite_img

# Update a subplot with new drone data.
# composite_img is the composite frame image to update.
# layout_specs is (row, col, rowspan, colspan) of the subplot location.
# data is a list of dictionaries, each with data to plot for a drone.
# subplot_horizontal_alignment controls how the image is positioned within the larger subplot area.
#   Can be 'center', 'left', 'right', or a number between 0 and 1.
#   If a number is provided, will place the left edge of the subplot image at that fraction of the overall subplot area.
# drone_imagePlot is the ImagePlot object to update.
# Returns the updated composite image.
def update_drone_subplot(composite_img, layout_specs, data,
                         drone_imagePlot,
                         subplot_horizontal_alignment='center'):
  # Reset the plot to an empty axis.
  drone_imagePlot.clear_plot()
  # Get a list of coordinates for all drones.
  drone_coordinates = []
  for (drone_index, drone_data) in enumerate(data):
    if drone_data is not None:
      x = drone_lon_to_km(drone_data['longitude'])
      y = drone_lat_to_km(drone_data['latitude'])
      drone_coordinates.append([x, y])
  if len(drone_coordinates) > 0:
    drone_coordinates = np.array(drone_coordinates)
    # Compute the maximum distance between any pair of drones.
    # This will be used as a reference length when considering the plot bounds.
    max_distance_km = np.amax(spatial.distance.cdist(drone_coordinates, drone_coordinates))
    # Check if the existing plot limits are sufficient, and if so avoid overhead of re-rendering the empty plot.
    x_extremes = [np.amin(drone_coordinates[:,0]), np.amax(drone_coordinates[:,0])]
    y_extremes = [np.amin(drone_coordinates[:,1]), np.amax(drone_coordinates[:,1])]
    x_limits = drone_imagePlot.get_x_limits()
    y_limits = drone_imagePlot.get_y_limits()
    x_range = drone_imagePlot.get_x_range()
    y_range = drone_imagePlot.get_y_range()
    existing_range_good =     x_extremes[0] >= x_limits[0] + drone_plot_rangePad_km \
                          and x_extremes[1] <= x_limits[1] - drone_plot_rangePad_km \
                          and y_extremes[0] >= y_limits[0] + drone_plot_rangePad_km \
                          and y_extremes[1] <= y_limits[1] - drone_plot_rangePad_km
    if max_distance_km > 0:
      existing_range_good = existing_range_good \
                            and (x_range >= drone_plot_rangeRatio_bounds[0]*max_distance_km
                              or y_range >= drone_plot_rangeRatio_bounds[0]*max_distance_km) \
                            and (x_range <= drone_plot_rangeRatio_bounds[1]*max_distance_km
                              or y_range <= drone_plot_rangeRatio_bounds[1]*max_distance_km)
    else:
      existing_range_good = existing_range_good \
                            and (x_range >= drone_plot_minRange_km
                              or y_range >= drone_plot_minRange_km)
    if not existing_range_good:
      # Compute a plot range using the distance between drones as a reference length.
      plot_range = max(drone_plot_minRange_km, np.mean(drone_plot_rangeRatio_bounds)*max_distance_km)
      # Keep the plot center the same, but zoom in/out according to the above range.
      x_center = np.mean(drone_imagePlot.get_x_limits())
      y_center = np.mean(drone_imagePlot.get_y_limits())
      x_limits = x_center + np.array([-plot_range/2, plot_range/2])
      y_limits = y_center + np.array([-plot_range/2, plot_range/2])
      # Adjust limits if needed to keep the drones away from the edges by the desired padding size.
      if x_extremes[0] < x_limits[0] + drone_plot_rangePad_km:
        x_limits[0] = (x_extremes[0]-drone_plot_rangePad_km)
        x_limits[1] = x_limits[0] + plot_range
      if x_extremes[1] > x_limits[1] - drone_plot_rangePad_km:
        x_limits[1] = (x_extremes[1]+drone_plot_rangePad_km)
        x_limits[0] = x_limits[1] - plot_range
      if y_extremes[0] < y_limits[0] + drone_plot_rangePad_km:
        y_limits[0] = (y_extremes[0]-drone_plot_rangePad_km)
        y_limits[1] = y_limits[0] + plot_range
      if y_extremes[1] > y_limits[1] - drone_plot_rangePad_km:
        y_limits[1] = (y_extremes[1]+drone_plot_rangePad_km)
        y_limits[0] = y_limits[1] - plot_range
      # Update the plot limits.
      if np.any(x_limits != drone_imagePlot.get_x_limits()) or \
          np.any(y_limits != drone_imagePlot.get_y_limits()):
        drone_imagePlot.set_x_limits(x_limits)
        drone_imagePlot.set_y_limits(y_limits)
        drone_imagePlot.render_empty()
  # Plot the drones.
  for (drone_index, drone_data) in enumerate(data):
    if drone_data is not None:
      x = drone_lon_to_km(drone_data['longitude'])
      y = drone_lat_to_km(drone_data['latitude'])
      drone_plot_color_index = drone_plot_color_lookup_keys.searchsorted(drone_data['altitude_relative_m'])
      drone_plot_color_index = min(drone_plot_color_index, drone_plot_color_lookup.shape[0]-1)
      drone_imagePlot.plot(x, y,
                           color=drone_plot_color_lookup[drone_plot_color_index],
                           marker_symbols='circle',
                           marker_size=drone_plot_symbolSize,
                           marker_edge_thickness=drone_plot_marker_edge_thickness,
                           marker_edge_color=drone_plot_colors[drone_index])
  # Update the subplot with the image.
  composite_img = update_image_subplot(composite_img, layout_specs,
                                       drone_imagePlot.get_plot_image(),
                                       subplot_label=None, subplot_label_outline_color=None,
                                       subplot_horizontal_alignment=subplot_horizontal_alignment)
  # Return the updated composite image.
  return composite_img


######################################################
# INITIALIZE PLOTS
######################################################

print()
print('Initializing plots for audio, codas, and drone data')

# Will store pointers to ImagePlot objects for each device stream that needs it.
# Will index the dictionary by layout_specs tuples since a single plot will be needed for each subplot.
imagePlots = {}
# Will also store the media type of each subplot.
media_types = {}

# Initialize audio visualizations.
for (device_friendlyName, layout_specs) in composite_layout.items():
  device_id = device_friendlyName_to_id(device_friendlyName)
  (row, col, rowspan, colspan) = layout_specs
  # If a plot has already been created for this subplot location, just use that one for this device too.
  if layout_specs in imagePlots:
    continue
  # Skip if no media information is stored for this device (e.g. a synthetic device such as drones)
  if device_id not in media_infos:
    continue
  # Load information about the stream.
  media_file_infos = media_infos[device_id]
  example_filepath = list(media_file_infos.keys())[0]
  (example_timestamps_s, example_data) = media_file_infos[example_filepath]
  # Store the media type if it is image, video, or audio:
  if is_video(example_filepath):
    media_types[layout_specs] = 'image'
  elif is_image(example_filepath):
    media_types[layout_specs] = 'image'
  elif is_audio(example_filepath):
    media_types[layout_specs] = 'audio'
  # Only continue if it is an audio stream.
  if not is_audio(example_filepath):
    continue
  # Create a plot for the audio data, that is set to the target size so no rescaling will be needed.
  plt = ImagePlot(auto_update_empty_plot=False)
  (subplot_width, subplot_height) = get_subplot_size(layout_specs)
  plt.set_plot_size(width=subplot_width, height=subplot_height)
  
  # Format the plot.
  plt.set_padding(left=0, top=subplot_border_size, right=0, bottom=subplot_border_size)
  plt.set_axis_left_position(width_ratio=audio_plots_left_axis_position_ratio)
  plt.set_axis_right_position(width_ratio=audio_plots_right_axis_position_ratio)
  plt.set_x_limits([-audio_plot_duration_beforeCurrentTime_s, audio_plot_duration_afterCurrentTime_s])
  plt.set_x_ticks_spacing(audio_plot_x_tick_spacing['major'], audio_plot_x_tick_spacing['minor'], value_to_include=0)
  plt.show_grid_major(x=False, y=False, thickness=audio_plot_grid_thickness['major'])
  plt.show_tick_labels(x=(not audio_plot_hide_xlabels), y=True)
  plt.set_x_label('Time [s]' if not audio_plot_hide_xlabels else '')
  plt.show_box(False)
  plt.set_font_size(size=audio_plot_font_size, yLabelHeightRatio=None)
  plt.set_font_color(audio_plot_label_color)
  if audio_plot_type == 'waveform':
    plt.set_y_label('')
  elif audio_plot_type == 'spectrogram':
    plt.set_y_label('Frequency [kHz]')
    plt.set_y_limits(np.array(audio_spectrogram_frequency_range)/1000)
    plt.set_y_ticks_spacing_major(audio_spectrogram_frequency_tick_spacing_khz)
    # Add a color bar.
    plt.add_colorbar(audio_spectrogram_colormap,
                     audio_spectrogram_colorbar_width_ratio,
                     limits=audio_spectrogram_colorbar_levels,
                     ticks=np.linspace(start=audio_spectrogram_colorbar_levels[0], stop=audio_spectrogram_colorbar_levels[1],
                                       num=5),
                     tick_label_format='%0.1f')
  
  # Render all updates to the plot formatting.
  plt.render_empty()
  # Store the plot to update later.
  imagePlots[layout_specs] = plt
  # Show the window if desired.
  if show_visualization_window:
    plt.show_plot(block=False, window_title=device_friendlyName)
    cv2.imwrite('test_plot_audio_%s.jpg' % device_id, plt.get_plot_image())


# Initialize coda visualizations.
whale_indexes_all = None
for coda_source in ['biology', 'haifa']:
  for coda_plot_type in ['ici', 'tfs']:
    if len(codas_data[coda_source]['coda_start_times_s']) > 0 and 'Codas %s (%s)' % (coda_source.title(), coda_plot_type.upper()) in composite_layout:
      # Find the layout for the coda plot.
      layout_specs = composite_layout['Codas %s (%s)' % (coda_source.title(), coda_plot_type.upper())]
      (row, col, rowspan, colspan) = layout_specs
      # Store the media type.
      media_types[layout_specs] = 'codas'
      # Create a plot for the data, that is set to the target size so no rescaling will be needed.
      plt = ImagePlot(auto_update_empty_plot=False)
      (subplot_width, subplot_height) = get_subplot_size(layout_specs)
      plt.set_plot_size(width=subplot_width, height=subplot_height)
      # Format the plot.
      plt.set_padding(left=0, top=subplot_border_size, right=0, bottom=subplot_border_size)
      plt.set_axis_left_position(width_ratio=audio_plots_left_axis_position_ratio)
      plt.set_axis_right_position(width_ratio=audio_plots_right_axis_position_ratio)
      plt.set_x_limits([-codas_plot_duration_beforeCurrentTime_s, codas_plot_duration_afterCurrentTime_s])
      plt.set_y_limits(codas_plot_yrange[coda_plot_type])
      plt.show_grid_major(x=False, y=True, thickness=codas_plot_grid_thickness['major'], color=codas_plot_grid_color['major'])
      plt.show_grid_minor(x=False, y=False, thickness=codas_plot_grid_thickness['minor'], color=codas_plot_grid_color['minor'])
      plt.set_x_ticks_spacing(codas_plot_x_tickSpacing_s[coda_plot_type]['major'], codas_plot_x_tickSpacing_s[coda_plot_type]['minor'],
                              value_to_include=0)
      plt.set_y_ticks_spacing(codas_plot_y_tickSpacing[coda_plot_type]['major'], codas_plot_y_tickSpacing[coda_plot_type]['minor'],
                              value_to_include=0)
      plt.show_tick_labels(x=(not codas_plot_hide_xlabels[coda_source][coda_plot_type]), y=True)
      plt.set_x_label('Time [s]' if not codas_plot_hide_xlabels[coda_source][coda_plot_type] else '')
      plt.show_box(False)
      if coda_plot_type == 'ici':
        plt.set_y_label('ICI [ms] %s' % coda_source.title())
      elif coda_plot_type == 'tfs':
        plt.set_y_label('TfS [ms] %s' % coda_source.title())
      plt.set_font_size(size=codas_plot_font_size, yLabelHeightRatio=None)
      plt.set_font_color(codas_plot_label_color)
      
      # Get visibly distinct colors for each whale index.
      # Note that this could be done with a single simple distinctipy call,
      #  but the below were manually tweaked to get colors that look nice and that
      #  use more red colors for uncertain annotations.
      if whale_indexes_all is None:
        whale_indexes_all = codas_data[coda_source]['whale_indexes']
      else:
        whale_indexes_all.extend(codas_data[coda_source]['whale_indexes'])
      unique_whale_indexes = sorted(list(OrderedDict(zip(whale_indexes_all, whale_indexes_all)).keys()))
      unique_whale_indexes_uncertain = [x for x in unique_whale_indexes if x >= codas_uncertain_whale_index]
      # Get colors for more 'certain' whales, which avoid red colors.
      whale_colors_certain = [(0, 1, 0), (1, 0, 1), (1, 1, 0), (0, 1, 1), (1, 1, 1)]
      whale_colors_certain_extra = distinctipy.get_colors(len(unique_whale_indexes) - len(unique_whale_indexes_uncertain) - len(whale_colors_certain),
                                                          exclude_colors=[(1, 0, 0), (0, 0, 0)] + whale_colors_certain,
                                                          rng=3,
                                                          pastel_factor=0.5,
                                                          n_attempts=1000)
      whale_colors_certain_extra.reverse()
      whale_colors_certain += whale_colors_certain_extra
      # Get colors for 'uncertain' whales that avoids green and colors already chosen.
      whale_colors_uncertain = distinctipy.get_colors(len(unique_whale_indexes_uncertain),
                                                      exclude_colors=[(0, 0, 0), (0, 1, 0), (1, 1, 1)]
                                                                     + whale_colors_certain,
                                                      rng=6,
                                                      pastel_factor=0.8,
                                                      n_attempts=1000)
      # Get a full list of whale colors, with RGB values scaled to 255 instead of 1.
      codas_plot_unique_whale_colors = [distinctipy.get_rgb256(c) for c in whale_colors_certain + whale_colors_uncertain]
      # Store a function that gets a whale color for a given index.
      codas_plot_whale_color = lambda whale_index: codas_plot_unique_whale_colors[unique_whale_indexes.index(whale_index)]
      
      # Render all updates to the plot formatting.
      plt.render_empty()
      # Store the plot to update later.
      imagePlots[layout_specs] = plt
      # Show the window if desired.
      if show_visualization_window:
        plt.show_plot(block=False, window_title='Codas (%s)' % coda_plot_type.upper())
        cv2.imwrite('test_plot_codas_%s.jpg' % coda_plot_type, plt.get_plot_image())
      

# Initialize drone data visualizations.
if len(drone_datas) > 0 and 'Drone Positions' in composite_layout:
  # Find the layout for the drone plot.
  layout_specs = composite_layout['Drone Positions']
  (row, col, rowspan, colspan) = layout_specs
  # Store the media type.
  media_types[layout_specs] = 'drones'
  
  # Create a plot for the data, that is set to the target size so no rescaling will be needed.
  plt = ImagePlot(auto_update_empty_plot=False)
  (subplot_width, subplot_height) = get_subplot_size(layout_specs)
  plt.set_plot_size(width=subplot_width, height=subplot_height)
  
  # Format the plot.
  plt.set_padding(left=0, top=subplot_border_size, right=0, bottom=subplot_border_size)
  plt.set_equal_aspect_ratio(True)
  plt.show_grid_major(x=True, y=True, thickness=drone_plot_grid_thickness['major'])
  plt.show_grid_minor(x=True, y=True, thickness=drone_plot_grid_thickness['minor'])
  plt.show_box(True)
  plt.show_tick_labels(x=True, y=True)
  plt.set_x_label('X From Home [km]')
  plt.set_y_label('Y From Home [km]')
  plt.set_x_tick_label_format('%0.1f')
  plt.set_y_tick_label_format('%0.1f')
  plt.set_font_size(size=drone_plot_font_size, yLabelHeightRatio=None)
  plt.set_font_color(drone_plot_label_color)
  # Set the plot bounds and ticks.
  (x_center, y_center) = drone_plot_reference_location_lonLat
  x_center = drone_lon_to_km(x_center)/1000.0
  y_center = drone_lat_to_km(y_center)/1000.0
  x_limits = x_center + np.array([-drone_plot_minRange_km/2, drone_plot_minRange_km/2])
  y_limits = y_center + np.array([-drone_plot_minRange_km/2, drone_plot_minRange_km/2])
  plt.set_x_limits(x_limits)
  plt.set_y_limits(y_limits)
  plt.set_x_ticks_spacing(drone_plot_tickSpacing_km['major'], drone_plot_tickSpacing_km['minor'])
  plt.set_y_ticks_spacing(drone_plot_tickSpacing_km['major'], drone_plot_tickSpacing_km['minor'])
  
  # Add a color bar.
  plt.add_colorbar(drone_plot_colormap, width=drone_plot_colorbar_width_ratio,
                   limits=drone_plot_colorbar_levels_m,
                   ticks=np.arange(start=drone_plot_colorbar_levels_m[0], stop=drone_plot_colorbar_levels_m[1]*1.1,
                                   step=drone_plot_colorbar_tickSpacing_m),
                   tick_label_format='%d',
                   label='Altitude [m]')
  
  # Render all updates to the plot formatting.
  plt.render_empty()
  # Store the plot to update later.
  imagePlots[layout_specs] = plt
  # Show the window if desired.
  if show_visualization_window:
    plt.show_plot(block=False, window_title='Drone Positions')
    cv2.imwrite('test_plot_drones.jpg', plt.get_plot_image())

######################################################
# DUMMY COMPOSITE FRAME FOR DEBUGGING THE LAYOUT
######################################################

print()
print('Creating a sample composite frame')

# Create a dummy image that can be used to debug the visualization layout.
composite_img_dummy = get_composite_img_blank()

# Store 'blank' image data for each subplot, in case we want to use it later to clear the composite frame.
# Not currently used, but an earlier structure of the main visualization loop used it.
# Will use layout_specs as the key, in case multiple devices are in the same subplot.
blank_subplot_datas = {}

# Update video, image, and audio visualizations.
for (device_friendlyName, layout_specs) in composite_layout.items():
  device_id = device_friendlyName_to_id(device_friendlyName)
  # If this subplot has already been updated, just use that one for this device too.
  if layout_specs in blank_subplot_datas:
    continue
  # Skip if no media information is stored for this device (e.g. a synthetic device such as drones)
  if device_id not in media_infos:
    continue
  # Load information about the stream.
  media_file_infos = media_infos[device_id]
  example_filepath = list(media_file_infos.keys())[0]
  (example_timestamps_s, example_data) = media_file_infos[example_filepath]
  # Create and show dummy data based on the stream type.
  if is_video(example_filepath) or is_image(example_filepath):
    (subplot_width, subplot_height) = get_subplot_size(layout_specs)
    if is_video(example_filepath):
      example_image = load_frame(example_data, 0,
                                 target_width=subplot_width,
                                 target_height=subplot_height)
    elif is_image(example_filepath):
      example_image = load_image(example_filepath,
                                 target_width=subplot_width,
                                 target_height=subplot_height)
    else:
      raise AssertionError('Thought it was a video or image, but apparently not')
    # Update the dummy composite image with the dummy image.
    update_image_subplot(composite_img_dummy, layout_specs, example_image,
                         subplot_label=device_friendlyName,
                         subplot_label_outline_color=drone_plot_colors[list(drone_datas.keys()).index(device_id)]
                                                      if device_id in drone_datas else None,
                         )
    # Store a black image as dummy data.
    # Make it the full size of the subplot, rather than the size of the example image,
    #  since other data for this subplot may be a different size than this first example
    #  (for example, if a camera has both audio and video of different sizes/orientations).
    blank_subplot_datas[layout_specs] = np.zeros((subplot_height, subplot_width, 3), dtype=np.uint8)
  elif is_audio(example_filepath):
    # Generate random noise that can be used to preview the visualization.
    random_audio = 500*np.random.normal(size=(1+int(audio_plot_duration_s*audio_resample_rate_hz), audio_num_channels_toPlot))
    if audio_plot_type == 'waveform':
      # Update the example composite image.
      update_audio_subplot(composite_img_dummy, layout_specs, random_audio, imagePlots[layout_specs])
      # Store a blank plot.
      blank_subplot_datas[str(layout_specs)] = imagePlots[layout_specs].get_empty_plot_image()
    elif audio_plot_type == 'spectrogram':
      # Create a random-noise spectrogram.
      spectrogram_f, spectrogram_t, spectrogram = \
        signal.spectrogram(random_audio[:,0], audio_resample_rate_hz,
                           window=signal.get_window('tukey', int(audio_spectrogram_target_window_s * audio_resample_rate_hz)),
                           scaling='density',  # density or spectrum (default is density)
                           nperseg=None)
      spectrogram_colormapped = audio_spectrogram_colormap.map(spectrogram/audio_spectrogram_colorbar_levels[1])[:,:,0:3]
      # Update the plot now with dummy data.
      update_audio_subplot(composite_img_dummy, layout_specs, spectrogram_colormapped, imagePlots[layout_specs])
      # Store a blank plot.
      blank_subplot_datas[str(layout_specs)] = imagePlots[layout_specs].get_empty_plot_image()

# Update drone visualizations.
# Do the same as above but for drone data visualizations.
if len(drone_datas) > 0 and 'Drone Positions' in composite_layout:
  # Find the layout for the drone plot.
  layout_specs = composite_layout['Drone Positions']
  # Generate dummy data for each drone.
  def get_example_drone_data():
    return {
      'latitude': (np.random.rand()-0.5)*0.0001 + (15.38146),
      'longitude': (np.random.rand()-0.5)*0.0001 + (-61.48562),
      'altitude_relative_m': (np.random.rand()-0.5)*10 + (20),
    }
  drone_dummy_data = [get_example_drone_data() for i in range(len(drone_datas))]
  # Update the example composite image with the dummy data plot.
  update_drone_subplot(composite_img_dummy, layout_specs, drone_dummy_data, imagePlots[layout_specs])
  # Store a blank plot.
  blank_subplot_datas[layout_specs] = imagePlots[layout_specs].get_empty_plot_image()

# Update coda visualizations.
for coda_source in ['biology', 'haifa']:
  for coda_plot_type in ['ici', 'tfs']:
    if len(codas_data[coda_source]['coda_start_times_s']) > 0 and 'Codas %s (%s)' % (coda_source.title(), coda_plot_type.upper()) in composite_layout:
      # Find the layout for the coda plot.
      layout_specs = composite_layout['Codas %s (%s)' % (coda_source.title(), coda_plot_type.upper())]
      # Set dummy data as not having any codas (dict of empty lists)
      #  at an epoch time that won't exist (0).
      codas_dummy_data = dict([(key, []) for key in codas_data[coda_source]])
      # Update the example composite image.
      update_codas_subplot(composite_img_dummy, layout_specs,
                           codas_dummy_data, 0, coda_plot_type, imagePlots[layout_specs])
      # Store a blank plot.
      blank_subplot_datas[str(layout_specs)] = imagePlots[layout_specs].get_empty_plot_image()

# Show the dummy visualization frame if desired.
if show_visualization_window or debug_composite_layout:
  cv2.imwrite('dummy_composite_visualization_frame.jpg', cv2.cvtColor(composite_img_dummy, cv2.COLOR_BGR2RGB))
  # Scale it to fit on more monitors.
  cv2.imshow('Happy Birthday!', cv2.cvtColor(scale_image(composite_img_dummy, target_width=600, target_height=600), cv2.COLOR_BGR2RGB))
  cv2.waitKey(1)
  if debug_composite_layout:
    cv2.waitKey(0)
    import sys
    sys.exit()


######################################################
# CREATE THE VIDEO!
######################################################

# Generate timestamps for the output video frames.
output_video_num_frames = np.ceil(output_video_duration_s * output_video_fps)
output_video_frame_duration_s = 1/output_video_fps
output_video_timestamps_s = output_video_start_time_s \
                            + np.arange(start=0,
                                        stop=output_video_num_frames)*output_video_frame_duration_s

print()
print('Generating an output video with %d frames' % output_video_timestamps_s.shape[0])

# Will store some timing information for finding processing bottlenecks.
duration_s_updateSubplots_total = 0
duration_s_updateSubplots_audio = 0
duration_s_updateSubplots_codas = 0
duration_s_updateSubplots_images = 0
duration_s_updateSubplots_videos = 0
duration_s_updateSubplots_drones = 0
duration_s_showVisualization = 0
duration_s_getIndex = 0
duration_s_readImages = 0
duration_s_readVideos = 0
readImages_count = 0
readVideos_count = 0
duration_s_audioParsing = 0
duration_s_codasParsing = 0
duration_s_addTimestampBanner = 0
duration_s_exportFrame = 0
duration_s_writeFrame = 0
duration_s_writeFlush = 0
duration_s_getBlankFrame = 0

# Will use a buffer of frames to reduce overhead.
# The ThreadedVideoWriter class will add a new frame to the buffer and then write it to video in the background.
#   This allows the main loop below to work on generating the next frame while the previous one is being written.
#   But by default, the ThreadedVideoWriter will need to make a copy of the frame since otherwise
#     the main loop will edit the same pointer that is in the writing buffer.
#     This is fine, but incurs a non-trivial processing cost of copying the frame (a large numpy matrix).
#   To avoid this, we can keep a buffer of frames to edit.
#     We can check that the video writer is done with a frame before editing it and wait if needed,
#     but if the buffer is long enough and the writing fast enough it is likely that we will avoid this delay as well.
frame_buffer_length = 200
# Create a video writer that will use threading to reduce overhead.
if output_video_filepath is not None:
  composite_video_writer = ThreadedVideoWriter(
                              output_filepath=output_video_filepath,
                              frame_rate=output_video_fps, max_buffered_frames=frame_buffer_length,
                              copy_added_frames=False,
                              overwrite_existing_video=True)
else:
  composite_video_writer = None
# Create a buffer of frames that aligns with the buffered video writer.
# This will allow us to avoid making a copy of every frame when adding it to the write buffer.
composite_img_buffer = [None]*frame_buffer_length
composite_img_buffer_index = 0

# Store the previous state of each subplot, to reduce overhead if nothing has changed.
layouts_prevState = dict([(layout_specs, None) for layout_specs in composite_layout.values()])
layouts_prevImages = dict([(layout_specs, None) for layout_specs in composite_layout.values()])

# Initialize state for printing status updates.
last_status_time_s = time.time()
last_status_frame_index = 0
start_loop_time_s = time.time()

# Loop through the video!
for (frame_index, current_time_s) in enumerate(output_video_timestamps_s):
  # Print periodic status updates.
  if time.time() - last_status_time_s > 10:
    print(' Processing frame %6d/%6d (%0.2f%%) for time %14.3f (%s) | FPS %0.1f Avg %0.1f' %
          (frame_index+1, output_video_num_frames, 100*(frame_index+1)/output_video_num_frames,
           current_time_s, time_s_to_str(current_time_s, localtime_offset_s, localtime_offset_str),
           (frame_index - last_status_frame_index)/(time.time() - last_status_time_s),
           frame_index/(time.time() - start_loop_time_s)))
    last_status_time_s = time.time()
    last_status_frame_index = frame_index
  
  # Wait for the frame previously stored at this buffer location to be written to video.
  t0 = time.time()
  while composite_video_writer.frame_is_pending_write(composite_img_buffer_index):
    time.sleep(0.001)
  duration_s_writeFrame += time.time() - t0
  # Create a blank frame.
  t0 = time.time()
  composite_img_buffer[composite_img_buffer_index] = get_composite_img_blank()
  composite_img_current = composite_img_buffer[composite_img_buffer_index]
  duration_s_getBlankFrame += time.time() - t0
  
  # Loop through each specified device stream.
  # Note that multiple devices may be mapped to the same layout position;
  #  in that case the first device with data for this timestep will be used.
  
  # Update video, image, and audio visualizations.
  for (device_friendlyName, layout_specs) in composite_layout.items():
    device_id = device_friendlyName_to_id(device_friendlyName)
    (row, col, rowspan, colspan) = layout_specs
    (subplot_width, subplot_height) = get_subplot_size(layout_specs)
    if device_id not in media_infos:
      continue
    # For each media file associated with this device, see if it has data for this timestep.
    # Note that the device may have multiple images that match this timestamp, but only the first will be used.
    for (filepath, (timestamps_s, data)) in media_infos[device_id].items():
      # Handle videos.
      if is_video(filepath):
        # Find the data index closest to the current time (if any).
        t0 = time.time()
        data_index = get_index_for_time_s(timestamps_s, current_time_s, timestamp_to_target_thresholds_s['video'])
        duration_s_getIndex += time.time() - t0
        if data_index is not None:
          # Only spend time loading a frame if it would be a different one than last frame.
          if (filepath, data_index) == layouts_prevState[layout_specs]:
            t0 = time.time()
            update_image_subplot(composite_img_current, layout_specs, layouts_prevImages[layout_specs],
                                 subplot_label=device_friendlyName,
                                 subplot_label_outline_color=drone_plot_colors[list(drone_datas.keys()).index(device_id)] if device_id in drone_datas else None,
                                 subplot_horizontal_alignment='center')
            duration_s_updateSubplots_videos += time.time() - t0
            duration_s_updateSubplots_total += time.time() - t0
            break # don't check any more media for this device
          # Read the video frame at the desired index.
          t0 = time.time()
          img = load_frame(data, data_index, target_width=subplot_width, target_height=subplot_height)
          duration_s_readVideos += time.time() - t0
          if img is not None:
            readVideos_count += 1
            # Update the subplot with the video frame.
            t0 = time.time()
            update_image_subplot(composite_img_current, layout_specs, img,
                                 subplot_label=device_friendlyName,
                                 subplot_label_outline_color=drone_plot_colors[list(drone_datas.keys()).index(device_id)] if device_id in drone_datas else None,
                                 subplot_horizontal_alignment='center')
            layouts_prevState[layout_specs] = (filepath, data_index)
            layouts_prevImages[layout_specs] = img
            duration_s_updateSubplots_total += time.time() - t0
            duration_s_updateSubplots_videos += time.time() - t0
            break # don't check any more media for this device
      
      # Handle images.
      elif is_image(filepath):
        # Find the data index closest to the current time (if any).
        t0 = time.time()
        data_index = get_index_for_time_s(timestamps_s, current_time_s, timestamp_to_target_thresholds_s['image'])
        duration_s_getIndex += time.time() - t0
        if data_index is not None:
          # Only spend time loading the image if it would be a different one than last frame.
          if (filepath, data_index) == layouts_prevState[layout_specs]:
            t0 = time.time()
            update_image_subplot(composite_img_current, layout_specs, layouts_prevImages[layout_specs],
                                 subplot_label=device_friendlyName,
                                 subplot_label_outline_color=drone_plot_colors[list(drone_datas.keys()).index(device_id)] if device_id in drone_datas else None,
                                 subplot_horizontal_alignment='center')
            duration_s_updateSubplots_images += time.time() - t0
            duration_s_updateSubplots_total += time.time() - t0
            break # don't check any more media for this device
          # Read the desired photo.
          t0 = time.time()
          img = load_image(filepath, target_width=subplot_width, target_height=subplot_height)
          duration_s_readImages += time.time() - t0
          readImages_count += 1
          # Update the subplot with the photo.
          t0 = time.time()
          update_image_subplot(composite_img_current, layout_specs, img,
                               subplot_label=device_friendlyName,
                               subplot_label_outline_color=drone_plot_colors[list(drone_datas.keys()).index(device_id)] if device_id in drone_datas else None,
                               subplot_horizontal_alignment='center')
          layouts_prevState[layout_specs] = (filepath, data_index)
          layouts_prevImages[layout_specs] = img
          duration_s_updateSubplots_total += time.time() - t0
          duration_s_updateSubplots_images += time.time() - t0
          break # don't check any more media for this device
      
      # Handle audio.
      elif is_audio(filepath):
        # Find the data index closest to the current time (if any).
        t0 = time.time()
        data_index = get_index_for_time_s(timestamps_s, current_time_s, timestamp_to_target_thresholds_s['audio'])
        duration_s_getIndex += time.time() - t0
        if data_index is not None:
          # Only spend time loading data if it would be different than last frame.
          if (filepath, data_index) == layouts_prevState[layout_specs]:
            t0 = time.time()
            update_audio_subplot(composite_img_current, layout_specs, layouts_prevImages[layout_specs],
                                 imagePlots[layout_specs],
                                 subplot_horizontal_alignment='center')
            duration_s_updateSubplots_audio += time.time() - t0
            duration_s_updateSubplots_total += time.time() - t0
            break # don't check any more media for this device
          t0 = time.time()
          # Get the start/end indexes of the data to plot.
          # Note that these may be negative or beyond the bounds of the data, indicating padding is needed.
          start_index = data_index - audio_plot_length_beforeCurrentTime
          end_index = data_index + audio_plot_length_afterCurrentTime + 1
          # Determine how much silence should be added to the data to fill the plot.
          data_t_length = data.shape[0] if audio_plot_type == 'waveform' else data.shape[1]
          num_toPad_pre = 0 if start_index >= 0 else -start_index
          num_toPad_post = 0 if end_index <= data_t_length else end_index - data_t_length
          # Adjust the start/end indexes to be within the data bounds.
          start_index = max(0, start_index)
          end_index = min(data_t_length, end_index)
          # Get the data and pad it as needed.
          if audio_plot_type == 'waveform':
            audio_num_channels = data.shape[1]
            data_toPlot = data[start_index:end_index, :]
            if num_toPad_pre > 0 or num_toPad_post > 0:
              data_toPlot = np.vstack([np.zeros((num_toPad_pre, audio_num_channels)),
                                       data_toPlot,
                                       np.zeros((num_toPad_post, audio_num_channels))])
          if audio_plot_type == 'spectrogram':
            data_toPlot = data[:, start_index:end_index, :]
            if num_toPad_pre > 0 or num_toPad_post > 0:
              data_toPlot = np.hstack([np.zeros((data.shape[0], num_toPad_pre, 3)),
                                       data_toPlot,
                                       np.zeros((data.shape[0], num_toPad_post, 3))])
          duration_s_audioParsing += time.time() - t0
          # Update the subplot with the waveform or spectrogram segment.
          t0 = time.time()
          update_audio_subplot(composite_img_current, layout_specs, data_toPlot,
                               imagePlots[layout_specs],
                               subplot_horizontal_alignment='center')
          layouts_prevState[layout_specs] = (filepath, data_index)
          layouts_prevImages[layout_specs] = imagePlots[layout_specs].get_plot_image()
          duration_s_updateSubplots_total += time.time()- t0
          duration_s_updateSubplots_audio += time.time()- t0
          break # don't check any more media for this device
  
  # Update drone data visualizations.
  for (device_friendlyName, layout_specs) in composite_layout.items():
    device_id = device_friendlyName_to_id(device_friendlyName)
    if device_id != 'Drone_Positions':
      continue
    drone_data_toPlot = [None]*len(drone_datas)
    layout_curState = [None]*len(drone_datas)
    for (drone_index, drone_device_id) in enumerate(drone_datas.keys()):
      for (filepath, (timestamps_s, drone_data)) in drone_datas[drone_device_id].items():
        # Find the data index closest to the current time (if any).
        t0 = time.time()
        data_index = get_index_for_time_s(timestamps_s, current_time_s, timestamp_to_target_thresholds_s['drone'])
        duration_s_getIndex += time.time() - t0
        if data_index is not None:
          drone_data_toPlot[drone_index] = {
            'latitude': drone_data['latitude'][data_index],
            'longitude': drone_data['longitude'][data_index],
            'altitude_relative_m': drone_data['altitude_relative_m'][data_index],
          }
          layout_curState[drone_index] = (filepath, data_index)
          break # don't check any more media for this device
    # Only spend time updating the plot if the data changed since last frame.
    if layout_curState == layouts_prevState[layout_specs]:
      pass
    elif True in [data is not None for data in drone_data_toPlot]:
      t0 = time.time()
      update_drone_subplot(composite_img_current, layout_specs, drone_data_toPlot,
                           imagePlots[layout_specs],
                           subplot_horizontal_alignment='center')
      layouts_prevState[layout_specs] = layout_curState
      layouts_prevImages[layout_specs] = imagePlots[layout_specs].get_plot_image()
      duration_s_updateSubplots_drones += time.time() - t0
      duration_s_updateSubplots_total += time.time() - t0
  
  # Update coda visualizations.
  for (device_friendlyName, layout_specs) in composite_layout.items():
    device_id = device_friendlyName_to_id(device_friendlyName)
    if device_id not in ['_coda_annotations_biology', '_coda_annotations_haifa']:
      continue
    if '_coda_annotations_biology' in device_id:
      coda_source = 'biology'
    elif '_coda_annotations_haifa' in device_id:
      coda_source = 'haifa'
    # Find codas within the current plot window.
    t0 = time.time()
    plot_start_time_s = current_time_s - codas_plot_duration_beforeCurrentTime_s
    plot_end_time_s = current_time_s + codas_plot_duration_afterCurrentTime_s
    coda_data_toPlot = dict([(key, []) for key in codas_data[coda_source]])
    found_active_annotation_file = False
    for coda_index in range(len(codas_data[coda_source]['coda_start_times_s'])):
      coda_start_time_s = codas_data[coda_source]['coda_start_times_s'][coda_index]
      coda_end_time_s = codas_data[coda_source]['coda_end_times_s'][coda_index]
      click_times_s = codas_data[coda_source]['click_times_s'][coda_index]
      if (coda_start_time_s >= plot_start_time_s and coda_start_time_s <= plot_end_time_s) \
        or (coda_end_time_s >= plot_start_time_s and coda_end_time_s <= plot_end_time_s):
          for key in codas_data[coda_source]:
            coda_data_toPlot[key].append(codas_data[coda_source][key][coda_index])
          found_active_annotation_file = True
    # If there were no codas, determine whether an annotations file is still active and there were just no clicks for this plot.
    if not found_active_annotation_file:
      for coda_file_index in range(len(codas_files_start_times_s[coda_source])):
        if current_time_s >= codas_files_start_times_s[coda_source][coda_file_index] \
            and current_time_s <= codas_files_end_times_s[coda_source][coda_file_index]:
          found_active_annotation_file = True
          break
    duration_s_codasParsing += time.time() - t0
    # If there is an active annotations file at this time, update the plot.
    if found_active_annotation_file:
      t0 = time.time()
      coda_plot_type = 'ici' if '(ICI)' in device_friendlyName else 'tfs'
      update_codas_subplot(composite_img_current, layout_specs,
                           coda_data_toPlot, current_time_s, coda_plot_type, imagePlots[layout_specs],
                           subplot_horizontal_alignment='center')
      duration_s_updateSubplots_codas += time.time() - t0
      duration_s_updateSubplots_total += time.time() - t0

  # Add a banner with the current timestamp.
  t0 = time.time()
  composite_img_current = add_timestamp_banner(composite_img_current, current_time_s)
  duration_s_addTimestampBanner = time.time() - t0
  
  # Show the updated composite frame if desired.
  if show_visualization_window:
    t0 = time.time()
    cv2.imshow('Happy Birthday!', cv2.cvtColor(scale_image(composite_img_dummy, target_width=600, target_height=600), cv2.COLOR_BGR2RGB))
    cv2.waitKey(1)
    duration_s_showVisualization += time.time() - t0
  
  # Add the frame to the buffer of frames to write to the output video.
  if composite_video_writer is not None:
    t0 = time.time()
    composite_video_writer.add_frame(cv2.cvtColor(composite_img_current, cv2.COLOR_BGR2RGB))
    composite_img_buffer_index = (composite_img_buffer_index+1) % frame_buffer_length
    duration_s_writeFrame += time.time() - t0

# Release the output video.
# This will also write any frames that are remaining in the write buffer.
if composite_video_writer is not None:
  t0 = time.time()
  composite_video_writer.release()
  duration_s_writeFlush += time.time() - t0

# Release video readers.
for (device_id, media_file_infos) in media_infos.items():
  for (filepath, (timestamps_s, data)) in media_file_infos.items():
    if isinstance(data, cv2.VideoCapture):
      data.release()

# All done!
total_duration_s = time.time() - start_loop_time_s
file_size_bytes_original = os.path.getsize(output_video_filepath)
print()
print('Generated composite video in %d seconds' % total_duration_s)
print('  File size: %0.2f GiB (%0.2f MiB) (%d bytes)' % (file_size_bytes_original/1024/1024/1024, file_size_bytes_original/1024/1024, file_size_bytes_original))
print()

# Print timing information.
print()
print('Configuration:')
print('  Audio rate     : %d Hz' % audio_resample_rate_hz)
print('  Audio plot duration: [-%d %d] seconds' % (audio_plot_duration_beforeCurrentTime_s, audio_plot_duration_afterCurrentTime_s))
print('  Column width   : %d' % composite_layout_column_width)
print('  Output duration: %d' % output_video_duration_s)
print('  Output rate    : %d' % output_video_fps)
print('  Show visualization window: %s' % show_visualization_window)
print('  Composite layout:', composite_layout)
print()
print('Processing duration: ')
print('  Total duration: %0.3f seconds' % total_duration_s)
print('  Frame count   : %d' % output_video_timestamps_s.shape[0])
print('  Frame rate    : %0.1f frames per second' % (output_video_timestamps_s.shape[0]/total_duration_s))
print('  Speed factor  : %0.2f x real time' % (output_video_duration_s/total_duration_s))
print('Processing breakdown: ')
print('  Update subplots (total)    : %6.2f%% (%0.3f seconds)'%(100*duration_s_updateSubplots_total/total_duration_s, duration_s_updateSubplots_total))
print('    Update subplots (audio)  :       %6.2f%% (%0.3f seconds)'%(100*duration_s_updateSubplots_audio/total_duration_s, duration_s_updateSubplots_audio))
print('    Update subplots (codas)  :       %6.2f%% (%0.3f seconds)'%(100*duration_s_updateSubplots_codas/total_duration_s, duration_s_updateSubplots_codas))
print('    Update subplots (drones) :       %6.2f%% (%0.3f seconds)'%(100*duration_s_updateSubplots_drones/total_duration_s, duration_s_updateSubplots_drones))
print('    Update subplots (videos) :       %6.2f%% (%0.3f seconds)'%(100*duration_s_updateSubplots_videos/total_duration_s, duration_s_updateSubplots_videos))
print('    Update subplots (images) :       %6.2f%% (%0.3f seconds)'%(100*duration_s_updateSubplots_images/total_duration_s, duration_s_updateSubplots_images))
print('  Get index for timestamp    : %6.2f%% (%0.3f seconds)' % (100*duration_s_getIndex/total_duration_s, duration_s_getIndex))
print('  Load images                : %6.2f%% (%0.3f seconds) (%d calls)' % (100*duration_s_readImages/total_duration_s, duration_s_readImages, readImages_count))
print('  Load video frames          : %6.2f%% (%0.3f seconds) (%d calls)' % (100*duration_s_readVideos/total_duration_s, duration_s_readVideos, readVideos_count))
print('  Parse audio                : %6.2f%% (%0.3f seconds)' % (100*duration_s_audioParsing/total_duration_s, duration_s_audioParsing))
print('  Parse codas                : %6.2f%% (%0.3f seconds)' % (100*duration_s_codasParsing/total_duration_s, duration_s_codasParsing))
print('  Export frame               : %6.2f%% (%0.3f seconds)' % (100*duration_s_exportFrame/total_duration_s, duration_s_exportFrame))
print('  Write frame                : %6.2f%% (%0.3f seconds)' % (100*duration_s_writeFrame/total_duration_s, duration_s_writeFrame))
print('  Write flush                : %6.2f%% (%0.3f seconds)' % (100*duration_s_writeFlush/total_duration_s, duration_s_writeFlush))
print('  Draw text                  : %6.2f%% (%0.3f seconds)' % (100*get_duration_s_drawText()/total_duration_s, get_duration_s_drawText()))
print('  Add timestamp banner       : %6.2f%% (%0.3f seconds)' % (100*duration_s_addTimestampBanner/total_duration_s, duration_s_addTimestampBanner))
print('  Scale images               : %6.2f%% (%0.3f seconds)' % (100*get_duration_s_scaleImage()/total_duration_s, get_duration_s_scaleImage()))
print('  Show visualization         : %6.2f%% (%0.3f seconds)' % (100*duration_s_showVisualization/total_duration_s, duration_s_showVisualization))
print('  Get blank frame            : %6.2f%% (%0.3f seconds)' % (100*duration_s_getBlankFrame/total_duration_s, duration_s_getBlankFrame))
print()
print()

######################################################
# COMPRESS THE VIDEO
######################################################

output_video_compressed_filepath = None
if output_video_compressed_rate_MB_s is not None:
  print('Compressing the output video to %0.2f MB (target rate %g MB/s)'
        % (output_video_compressed_rate_MB_s*output_video_duration_s, output_video_compressed_rate_MB_s))
  t0 = time.time()
  output_video_compressed_filepath = '%s_compressed%sMBs%s' \
                                     % (os.path.splitext(output_video_filepath)[0],
                                        ('%0.2f' % output_video_compressed_rate_MB_s).replace('.','-'),
                                        os.path.splitext(output_video_filepath)[1])
  compress_video(output_video_filepath, output_video_compressed_filepath,
                 output_video_compressed_rate_MB_s*1024*1024*8)
  file_size_bytes_compressed = os.path.getsize(output_video_compressed_filepath)
  print('  Compression completed in %0.3f seconds' % (time.time() - t0))
  print('  File size: %0.2f GiB (%0.2f MiB) (%d bytes)' % (file_size_bytes_compressed/1024/1024/1024, file_size_bytes_compressed/1024/1024, file_size_bytes_compressed))
  print('    Compression ratio: %0.2f' % (file_size_bytes_original/file_size_bytes_compressed))
  print()

######################################################
# ADD AUDIO TO THE VIDEO
######################################################

output_video_filepaths_toAddAudio = []
if add_audio_track_to_output_video_original:
  output_video_filepaths_toAddAudio.append(output_video_filepath)
if add_audio_track_to_output_video_compressed:
  output_video_filepaths_toAddAudio.append(output_video_compressed_filepath)
saved_audio_file = False

for output_video_filepath_toAddAudio in output_video_filepaths_toAddAudio:
  if output_video_filepath_toAddAudio is None:
    continue
  print('Adding aligned audio track to %s' % os.path.basename(output_video_filepath_toAddAudio))
  
  # Open a handle to the newly created composite video.
  output_video_clip = VideoFileClip(output_video_filepath_toAddAudio, audio=False)
  
  # Find audio files that overlap with the video.
  print('  Searching for audio files that overlap with the composite video')
  audio_clips = []
  for (device_id, media_file_infos) in media_infos.items():
    for filepath in media_file_infos.keys():
      if not is_audio(filepath):
        continue
      # Get the start/end/duration of the audio file.
      audio_filename = os.path.basename(filepath)
      audio_start_time_ms = int(re.search('\d{13}', audio_filename)[0])
      audio_start_time_s = audio_start_time_ms/1000.0
      audio_start_time_s = adjust_start_time_s(audio_start_time_s, device_id)
      (audio_rate, audio_data) = wavfile.read(filepath)
      audio_duration_s = audio_data.shape[0]/audio_rate
      audio_end_time_s = audio_start_time_s + audio_duration_s
      
      audio_clip = None
      # Compute how far into the audio clip the video clip starts.
      # Being negative would imply the audio starts inside video, so the audio start should not be clipped.
      audio_clip_start_offset_s = max(0.0, output_video_start_time_s - audio_start_time_s)
      # Compute the duration of the audio that would align it with the end of the video.
      # Being longer than the audio duration implies the audio ends inside the video, so the audio end should not be clipped.
      audio_clip_duration_s = min(audio_duration_s, (output_video_start_time_s+output_video_duration_s) - audio_start_time_s)
      audio_clip_duration_s -= audio_clip_start_offset_s
      # Load the audio segment if it is valid (if the audio file overlaps with the video).
      if audio_clip_duration_s > 0:
        audio_clip = AudioFileClip(filepath).subclip(t_start=audio_clip_start_offset_s,
                                                     t_end=audio_clip_start_offset_s+audio_clip_duration_s)
        
        # Compute the video time at which this audio clip should start.
        audio_clip_start_time_s = audio_start_time_s + audio_clip_start_offset_s
        audio_video_start_offset_s = audio_clip_start_time_s - output_video_start_time_s
        audio_clip = audio_clip.set_start(audio_video_start_offset_s)
        print('  Found %s spanning [%d, %d] > placed segment [%6.1f, %6.1f] at video time %5ds'
              % (audio_filename, audio_start_time_s, audio_end_time_s,
                 audio_clip_start_offset_s, audio_clip_start_offset_s+audio_clip_duration_s,
                 audio_video_start_offset_s))
        
        # Store the audio clip.
        audio_clips.append(audio_clip)
  
  # Create the composite audio.
  if len(audio_clips) == 0:
    print('  No audio clips were found that overlap with the generated video')
    # Close handle to the video clip.
    output_video_clip.close()
  else:
    print('  Adding %d audio clips to the video' % (len(audio_clips)))
    t0 = time.time()
    composite_audio_clip = CompositeAudioClip(audio_clips)
    composite_audio_clip = composite_audio_clip.volumex(output_audio_track_volume_gain_factor)
    output_video_clip = output_video_clip.set_audio(composite_audio_clip)
    output_video_withAudio_filepath = '%s_withAudio%s' % os.path.splitext(output_video_filepath_toAddAudio)
    output_audio_filepath = '%s_audio.m4a' % os.path.splitext(output_video_filepath_toAddAudio)[0]
    output_video_clip.write_videofile(output_video_withAudio_filepath,
                                      verbose=False,
                                      logger=proglog.TqdmProgressBarLogger(print_messages=False),
                                      # codec='libx264',
                                      audio_codec='aac',
                                      temp_audiofile=output_audio_filepath,
                                      remove_temp=(not save_audio_track_as_separate_file) or saved_audio_file,
                                      )
    saved_audio_file = save_audio_track_as_separate_file
    file_size_bytes_withAudio = os.path.getsize(output_video_withAudio_filepath)
    print('  Audio track added in %0.3f seconds' % (time.time() - t0))
    print('  File size: %0.2f GiB (%0.2f MiB) (%d bytes)' % (file_size_bytes_withAudio/1024/1024/1024, file_size_bytes_withAudio/1024/1024, file_size_bytes_withAudio))
    print('    Compression ratio: %0.2f' % ((os.path.getsize(output_video_filepath_toAddAudio))/file_size_bytes_withAudio))
    # Close handles to the audio files.
    for audio_clip in audio_clips:
      audio_clip.close()
    # Close handle to the video clip.
    output_video_clip.close()
    # Delete the original version without audio.
    if delete_output_video_withoutAudio:
      print('  Deleting the original version without audio')
      os.remove(output_video_filepath_toAddAudio)
    print()

######################################################
# EXIT
######################################################

print()
print('Done!')
print()
print()

# Wait until the visualization window is closed.
if show_visualization_window:
  cv2.waitKey(0)












