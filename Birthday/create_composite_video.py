
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
import pyqtgraph
from pyqtgraph.Qt import QtCore, QtGui, QtWidgets
from pyqtgraph.Qt.QtGui import QPixmap, QImage
import pyqtgraph.exporters

from helpers import *

######################################################
# CONFIGURATION
# Note that some of the below could be loaded
#  from metadata files in the future.
######################################################

# Specify the root data directory, which contains subfolders for each device
data_dir_root = 'C:/Users/jdelp/Desktop/_whale_birthday_s3_data'

# Specify the layout of devices streams in the output video.
# Each value is (row, column, rowspan, colspan).
composite_layout = OrderedDict([
  ('Mavic (CETI)'         , (0, 0, 2, 2)),
  ('Mavic (DSWP)'         , (0, 2, 2, 2)),
  ('Canon (Gruber)'       , (2, 0, 1, 1)),
  ('Canon (DelPreto)'     , (2, 1, 1, 1)),
  ('Phone (DelPreto)'     , (2, 1, 1, 1)),
  ('GoPro (DelPreto)'     , (2, 1, 1, 1)),
  ('Canon (DSWP)'         , (2, 2, 1, 1)),
  ('Drone Positions'      , (2, 3, 1, 1)),
  ('Phone (Baumgartner)'  , (3, 0, 1, 1)),
  ('Phone (Pagani)'       , (3, 1, 1, 1)),
  ('Phone (SalinoHugg)'   , (3, 2, 1, 1)),
  ('Phone (Aluma)'        , (3, 3, 1, 1)),
  ('Hydrophone (Mevorach)', (4, 0, 1, 4)),
  # ('Hydrophone (Mevorach)', (0, 0, 1, 1)),
])

# Specify the time zone offset to get local time of this data collection day from UTC.
# Note that in the future this could probably be determined automatically.
localtime_offset_s = -4*3600
localtime_offset_str = '-0400'

# Specify offsets to add to timestamps extracted from filenames.
epoch_offsets_toAdd_s = {
  'CETI-DJI_MAVIC3-1'          : 0.7986,
  'DSWP-DJI_MAVIC3-2'          : 2.1083,
  'DG-CANON_EOS_1DX_MARK_III-1': 14603.8151,
  'JD-CANON_REBEL_T5I'         : 14.3797,
  'DSWP-CANON_EOS_70D-1'       : 14486.213,
  'DSWP-KASHMIR_MIXPRE6-1'     : 32.7085,
  'Misc/Aluma'                 : -0.5595,
  'Misc/Baumgartner'           : 3.303,
  'Misc/Pagani'                : 0, # used as reference time
  'Misc/SalinoHugg'            : -0.1383,
  'Misc/DelPreto_Pixel5'       : 0,
  'Misc/DelPreto_GoPro'        : 0,
}
drone_timestamps_are_local_time = {
  'CETI-DJI_MAVIC3-1'          : False,
  'DSWP-DJI_MAVIC3-2'          : True,
}

# Specify friendly names for each device that will be printed on the output video.
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
  'Misc/SalinoHugg'            : 'Phone (SalinoHugg)',
  'Misc/DelPreto_Pixel5'       : 'Phone (DelPreto)',
  'Misc/DelPreto_GoPro'        : 'GoPro (DelPreto)',
  'Drone_Positions'            : 'Drone Positions',
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
# output_video_start_time_str = '2023-07-08 11:44:00 -0400'
# output_video_start_time_str = '2023-07-08 11:45:00 -0400'
# output_video_start_time_str = '2023-07-08 11:48:45 -0400'
# output_video_start_time_str = '2023-07-08 11:49:00 -0400'
# output_video_start_time_str = '2023-07-08 11:53:53 -0400'
# output_video_start_time_str = '2023-07-08 11:53:00 -0400'
# output_video_start_time_str = '2023-07-08 11:35:00 -0400'
# output_video_start_time_str = '2023-07-08 11:37:52 -0400'
# output_video_start_time_str = '2023-07-08 11:52:00 -0400'
# output_video_start_time_str = '2023-07-08 11:53:38 -0400'
# output_video_start_time_str = '2023-07-08 11:53:46 -0400'
# output_video_start_time_str = '2023-07-08 11:54:32 -0400'
# output_video_start_time_str = '2023-07-08 11:53:53 -0400'
# output_video_start_time_str = '2023-07-08 11:54:55 -0400'
# output_video_start_time_str = '2023-07-08 11:54:00 -0400'
output_video_start_time_str = '2023-07-08 10:20:13 -0400'
output_video_duration_s = 195780
# output_video_duration_s = 1#60*60
output_video_fps = 30

# Define the output video size/resolution and compression.
composite_layout_column_width = 400 # also defines the scaling/resolution of photos/videos
subplot_border_size = 5 # ignored if the pyqtgraph subplot method is used
composite_layout_row_height = round(composite_layout_column_width/(1+7/9)) # Drone videos have an aspect ratio of 1.7777
output_video_compressed_rate_MB_s = 0.5 # None to not compress the video

# Define audio track added to the output video.
add_audio_track_to_output_video_original = True
add_audio_track_to_output_video_compressed = True
delete_output_video_withoutAudio = False
output_audio_track_volume_gain_factor = 50 # 1 to not change volume
save_audio_track_as_separate_file = True

# Specify annotations on the output video.
output_video_banner_height_fraction = 0.04 # fraction of the final composite frame
output_video_banner_bg_color   = [100, 100, 100] # BGR
output_video_banner_text_color = [255, 255,   0] # BGR

# Configure audio plotting
audio_resample_rate_hz = 96000 # original rate is 96000
audio_plot_duration_beforeCurrentTime_s = 5
audio_plot_duration_afterCurrentTime_s  = 10
audio_num_channels_toPlot = 1
audio_plot_waveform = False
audio_plot_spectrogram = True # Will force audio_num_channels_toPlot = 1 for now
audio_waveform_plot_pens = [pyqtgraph.mkPen([255, 255, 255], width=4),
                            pyqtgraph.mkPen([255, 0, 255], width=1)]
audio_spectrogram_frequency_range = [0e3, min(40e3, audio_resample_rate_hz//2)]
audio_spectrogram_window_s = 0.03
# audio_spectrogram_colormap = 'CET-L16' # 'inferno', 'CET-CBTL1', 'CET-L1', 'CET-L16', 'CET-L3', 'CET-R1'
audio_spectrogram_colormap = pyqtgraph.colormap.get('gist_stern', source='matplotlib', skipCache=True)
# audio_spectrogram_colormap = pyqtgraph.colormap.get('nipy_spectral', source='matplotlib', skipCache=True)
# audio_spectrogram_colormap = pyqtgraph.colormap.get('turbo', source='matplotlib', skipCache=True)

# Configure drone plotting.
drone_plot_reference_location_lonLat = [-61.373179, 15.306914]
conversion_factor_lat_to_m = (111.32)*1000
conversion_factor_lon_to_m = (40075 * np.cos(np.radians(drone_plot_reference_location_lonLat[1])) / 360) * 1000
drone_lat_to_m = lambda lat: (lat - drone_plot_reference_location_lonLat[1]) * conversion_factor_lat_to_m
drone_lon_to_m = lambda lon: (lon - drone_plot_reference_location_lonLat[0]) * conversion_factor_lon_to_m
drone_plot_minRange_m = 400
drone_plot_rangePad = 40
drone_plot_tickSpacing_m = {'minor':20, 'major':200}
# drone_plot_colors = [(180, 20, 180), (180, 180, 20)] # BGR (but will be flipped to RGB for pyqtgraph pen below)
drone_plot_colors = [(255, 50, 255), (255, 255, 50)] # BGR (but will be flipped to RGB for pyqtgraph pen below)
drone_plot_symbolPens = [pyqtgraph.mkPen(np.flip(drone_plot_colors[drone_index]), width=4) for drone_index in range(len(drone_plot_colors))]
drone_plot_colormap = pyqtgraph.colormap.get('gist_stern', source='matplotlib', skipCache=True)
drone_plot_color_lookup = drone_plot_colormap.getLookupTable(start=0, stop=1, nPts=500)
drone_plot_color_lookup_keys = np.linspace(start=0, stop=125, num=500)
drone_colorbar_tickSpacing_m = {'major':25, 'minor':25}
drone_plot_symbolSize = 15

# Configure how device timestamps are matched with output video frame timestamps.
timestamp_to_target_thresholds_s = { # each entry is the allowed time (before_current_frame, after_current_frame)
  'video': (1/output_video_fps*0.6, 1/output_video_fps*0.6),
  'audio': (1/output_video_fps*0.6, 1/output_video_fps*0.6),
  'image': (1, 1/output_video_fps), # first entry controls how long an image will be shown
  'drone': (1/output_video_fps*0.6, 1/output_video_fps*0.6),
}

# Method of creating the composite visualization frame.
use_pyqtgraph_subplots = False
use_opencv_subplots = True

# Visualization debugging options.
show_visualization_window = False
debug_composite_layout = False # Will show the layout with dummy data and then exit

# Derived configurations.
if audio_plot_waveform:
  audio_plot_length_beforeCurrentTime = int(audio_resample_rate_hz * audio_plot_duration_beforeCurrentTime_s)
  audio_plot_length_afterCurrentTime = int(audio_resample_rate_hz * audio_plot_duration_afterCurrentTime_s)
  audio_plot_length = 1 + audio_plot_length_beforeCurrentTime + audio_plot_length_afterCurrentTime
  audio_timestamps_toPlot_s = np.arange(start=0, stop=audio_plot_length)/audio_resample_rate_hz - audio_plot_duration_beforeCurrentTime_s
elif audio_plot_spectrogram:
  audio_plot_length_beforeCurrentTime = int(audio_plot_duration_beforeCurrentTime_s/audio_spectrogram_window_s)
  audio_plot_length_afterCurrentTime = int(audio_plot_duration_afterCurrentTime_s/audio_spectrogram_window_s)
  audio_plot_length = 1 + audio_plot_length_beforeCurrentTime + audio_plot_length_afterCurrentTime
audio_plot_duration_s = (audio_plot_duration_beforeCurrentTime_s + audio_plot_duration_afterCurrentTime_s)

output_video_banner_fontScale = None # will be determined later based on the size of the banner
output_video_banner_textSize  = None # will be determined later once the font scale is computed

output_video_num_rows = max([layout_specs[0] + layout_specs[2] for layout_specs in composite_layout.values()])
output_video_num_cols = max([layout_specs[1] + layout_specs[3] for layout_specs in composite_layout.values()])
if use_opencv_subplots:
  output_video_width = composite_layout_column_width*output_video_num_cols + subplot_border_size*(output_video_num_cols+1)
  output_video_height = composite_layout_row_height*output_video_num_rows + subplot_border_size*(output_video_num_rows+1)
if use_pyqtgraph_subplots:
  output_video_width = composite_layout_column_width*output_video_num_cols
  output_video_height = composite_layout_row_height*output_video_num_rows

output_video_start_time_s = time_str_to_time_s(output_video_start_time_str)

output_video_filepath = os.path.join(data_dir_root,
                                     'composite_video_fps%d_duration%d_start%d_colWidth%d_audio%d%s.mp4'
                                     % (output_video_fps, output_video_duration_s,
                                        1000*output_video_start_time_s,
                                        composite_layout_column_width,
                                        audio_resample_rate_hz, 'spectrogram' if audio_plot_spectrogram else 'waveform'))


######################################################
# HELPERS
######################################################

# Convert a device friendly name to a device ID.
def device_friendlyName_to_id(device_friendlyName_toFind):
  for (device_id, device_friendlyName) in device_friendlyNames.items():
    if device_friendlyName == device_friendlyName_toFind:
      return device_id
  return None

# Find a timestamp from a device that most closely matches a target timestamp.
# Will return the index of that matched timestamp within the device's array of timestamps.
# If there is no such timestamp within a specified threshold of the target, return None.
def get_index_for_time_s(timestamps_s, target_time_s, timestamp_to_target_thresholds_s):
  # Find the timestamp closest to the target.
  if timestamps_s.shape[0] == 1:
    # If there is only one timestamp, consider that the best one.
    best_index = 0
  else:
    # Find the index where the target timestamp would be inserted without changing the sort order.
    # This is much faster than using something like numpy.where(), since it can assume the input is sorted.
    next_index_pastTarget = timestamps_s.searchsorted(target_time_s)
    if next_index_pastTarget == timestamps_s.shape[0]:
      next_index_pastTarget -= 1
    # The above placed the target between two device timestamps.
    # Now see which one of those two is closer to the target.
    index_candidates = np.array([next_index_pastTarget-1, next_index_pastTarget])
    dt_candidates = abs(timestamps_s[index_candidates] - target_time_s)
    if dt_candidates[0] < dt_candidates[1]:
      best_index = index_candidates[0]
    else:
      best_index = index_candidates[1]
  # Check if the closest timestamp is within the threshold region of the target.
  if timestamps_s[best_index] < (target_time_s - timestamp_to_target_thresholds_s[0]):
    return None
  if timestamps_s[best_index] > (target_time_s + timestamp_to_target_thresholds_s[1]):
    return None
  # We found a good timestamp! Return its index.
  return best_index

# Add a banner to the output frame that displays the current timestamp.
def add_timestamp_banner(img, timestamp_s):
  global output_video_banner_height_fraction, output_video_banner_bg_color, output_video_banner_fontScale, output_video_banner_textSize
  
  # Add the bottom banner shading.
  output_video_banner_height = int(output_video_banner_height_fraction*img.shape[0])
  img = cv2.copyMakeBorder(img, 0, output_video_banner_height, 0, 0,
                           cv2.BORDER_CONSTANT, value=output_video_banner_bg_color)
  
  # Specify the text to write.
  timestamp_str = '%s (%0.3f)' % (time_s_to_str(timestamp_s, localtime_offset_s, localtime_offset_str),
                                  timestamp_s)
  
  # Compute the size of the text that will be drawn on the image.
  fontFace = cv2.FONT_HERSHEY_DUPLEX # cv2.FONT_HERSHEY_SIMPLEX
  fontThickness = 1 #2 if output_video_banner_height > 25 else 1
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



######################################################
# LOAD TIMESTAMPS AND DATA POINTERS
######################################################

# Will create a dictionary with following structure:
#   [device_id][filepath] = (timestamps_s, data)
#   If filepath points to a video:
#     timestamps_s is a numpy array of epoch timestamps for every frame
#     data is a cv2.VideoCapture object
#   If filepath points to a wav file:
#     timestamps_s is a numpy array of epoch timestamps for every sample
#     data is a num_samples x num_channels matrix of audio data
#   If filepath points to an image:
#     timestamps_s is a single-element numpy array with the epoch timestamps of the image
#     data is the filepath again
media_infos = OrderedDict()
drone_datas = OrderedDict()

print()
print('Extracting timestamps and pointers to data for every frame/photo/audio')
for (device_friendlyName, layout_specs) in composite_layout.items():
  (row, col, rowspan, colspan) = layout_specs
  device_id = device_friendlyName_to_id(device_friendlyName)
  # Find data files for this device.
  if 'Misc' in device_id:
    data_dir = os.path.join(data_dir_root, 'Misc')
    filename_keyword = device_id.split('/')[1]
    filepaths = glob.glob(os.path.join(data_dir, '*%s*' % filename_keyword))
  else:
    data_dir = os.path.join(data_dir_root, device_id)
    filepaths = glob.glob(os.path.join(data_dir, '*'))
  filepaths = [filepath for filepath in filepaths if not os.path.isdir(filepath)]
  if len(filepaths) == 0:
    continue
  media_infos[device_id] = {}
  # Skip files that start after the composite video ends.
  # Do this now, so the below loop can know how many files there are (for printing purposes and whatnot).
  filepaths_toKeep = []
  for (file_index, filepath) in enumerate(filepaths):
    # Get the start time in epoch time
    filename = os.path.basename(filepath)
    start_time_ms = int(re.search('\d{13}', filename)[0])
    start_time_s = start_time_ms/1000.0
    start_time_s += epoch_offsets_toAdd_s[device_id]
    if start_time_s <= (output_video_start_time_s+output_video_duration_s):
      filepaths_toKeep.append(filepath)
  print('  Found %4d files for device [%s] (ignored %d files starting after the composite video)' % (len(filepaths_toKeep), device_friendlyName, len(filepaths) - len(filepaths_toKeep)))
  filepaths = filepaths_toKeep
  
  # Loop through each file to extract its timestamps and data pointers.
  for (file_index, filepath) in enumerate(filepaths):
    # Get the start time in epoch time
    filename = os.path.basename(filepath)
    start_time_ms = int(re.search('\d{13}', filename)[0])
    start_time_s = start_time_ms/1000.0
    start_time_s += epoch_offsets_toAdd_s[device_id]
    # Process the data/timestamps.
    if is_video(filepath):
      (video_reader, frame_rate, num_frames) = get_video_reader(filepath,
                                                                target_width=colspan*composite_layout_column_width)
      # Extract frame timestamps from an SRT file if one exists.
      # Otherwise, generate timestamps assuming a constant frame rate.
      drone_data = get_drone_data(filepath, timezone_offset_str=localtime_offset_str)
      if drone_data is not None:
        timestamps_s = drone_data['timestamp_s']
        timestamps_s = timestamps_s + epoch_offsets_toAdd_s[device_id]
        if not drone_timestamps_are_local_time[device_id]:
          timestamps_s = timestamps_s + localtime_offset_s
        drone_datas.setdefault(device_id, {})
        drone_datas[device_id][filepath] = (timestamps_s, drone_data)
      else:
        frame_duration_s = 1/frame_rate
        timestamps_s = start_time_s + np.arange(start=0, stop=num_frames)*frame_duration_s
      media_infos[device_id][filepath] = (timestamps_s, video_reader)
    elif is_image(filepath):
      timestamps_s = np.array([start_time_s])
      media_infos[device_id][filepath] = (timestamps_s, filepath)
    elif is_audio(filepath):
      if file_index > 0:
        print('\r', end='')
      print('    Loading file %2d/%2d %s' % (file_index+1, len(filepaths), ' '*15), end='')
      (audio_rate, audio_data) = wavfile.read(filepath)
      num_samples = audio_data.shape[0]
      timestamps_s = start_time_s + np.arange(start=0, stop=num_samples)/audio_rate
      # Only process/store it if it will be needed for the composite video.
      audio_start_time_s = timestamps_s[0]
      audio_end_time_s = timestamps_s[-1]
      if audio_end_time_s < output_video_start_time_s \
          or audio_start_time_s > (output_video_start_time_s+output_video_duration_s):
        if file_index == len(filepaths)-1:
          print()
        continue
      # Resample the data.
      if audio_resample_rate_hz != audio_rate:
        print('\r', end='')
        print('    Resampling file %2d/%2d %s' % (file_index+1, len(filepaths), ' '*15), end='')
        fn_interpolate_audio = interpolate.interp1d(
            timestamps_s,  # x values
            audio_data,    # y values
            axis=0,        # axis of the data along which to interpolate
            kind='linear', # interpolation method, such as 'linear', 'zero', 'nearest', 'quadratic', 'cubic', etc.
            fill_value='extrapolate' # how to handle x values outside the original range
        )
        num_samples = int(num_samples * (audio_resample_rate_hz/audio_rate))
        timestamps_s_resampled = start_time_s + np.arange(start=0, stop=num_samples)/audio_resample_rate_hz
        audio_data_resampled = fn_interpolate_audio(timestamps_s_resampled)
        audio_data = audio_data_resampled
        timestamps_s = timestamps_s_resampled
      # Compute a spectrogram of the entire file.
      if audio_plot_spectrogram:
        print('\r', end='')
        print('    Computing spectrogram for file %2d/%2d     ' % (file_index+1, len(filepaths)), end='')
        spectrogram_f, spectrogram_t, spectrogram = \
          signal.spectrogram(audio_data[:,0], audio_resample_rate_hz,
                             window=signal.get_window('tukey', int(audio_spectrogram_window_s*audio_resample_rate_hz)),
                             scaling='density', # density or spectrum (default is density)
                             nperseg=None)
        # Truncate to the desired frequency range.
        min_f_index = spectrogram_f.searchsorted(audio_spectrogram_frequency_range[0])
        max_f_index = spectrogram_f.searchsorted(audio_spectrogram_frequency_range[-1])
        spectrogram_f = spectrogram_f[min_f_index:max_f_index]
        spectrogram = spectrogram[min_f_index:max_f_index, :]
        # Determine colorbar levels.
        colorbar_levels = [0, 0.4] #[0, np.quantile(spectrogram, 0.99)]
        # Determine epoch timestamps of each entry in the spectrogram.
        timestamps_s = spectrogram_t + timestamps_s[0]
        # Determine frequency tick labels.
        f_tick_targets = np.arange(start=np.floor(spectrogram_f[0]/1000), stop=np.ceil(spectrogram_f[-1]/1000), step=np.ceil(audio_spectrogram_frequency_range[-1]/1000/5))
        f_tick_indexes = [spectrogram_f.searchsorted(f_tick_target*1000) for f_tick_target in f_tick_targets]
        f_ticks = [(f_tick_index, '%0.0f' % (spectrogram_f[f_tick_index]/1000)) for f_tick_index in f_tick_indexes]
        # Determine time tick labels using a sample portion of the spectrogram.
        t_tick_values = list(np.arange(start=-audio_plot_duration_beforeCurrentTime_s, stop=0, step=2)) \
                        + list(np.arange(start=0, stop=audio_plot_duration_afterCurrentTime_s, step=2))
        t_tick_values = np.array([round(t_tick_value) for t_tick_value in t_tick_values])
        sample_spectrogram_t = np.arange(start=0, stop=audio_plot_length, step=1)*audio_spectrogram_window_s
        sample_spectrogram_t -= audio_plot_duration_beforeCurrentTime_s
        t_ticks = []
        for t_tick_value in t_tick_values:
          spectrogram_t_index = sample_spectrogram_t.searchsorted(t_tick_value)
          t_ticks.append((spectrogram_t_index, '%0.0f' % t_tick_value))
        # Save the information
        media_infos[device_id][filepath] = (timestamps_s, (spectrogram, t_ticks, f_ticks, colorbar_levels))
      elif audio_plot_waveform:
        media_infos[device_id][filepath] = (timestamps_s, audio_data)
      if file_index == len(filepaths)-1:
        print()

# Remove devices with no data for the composite video.
device_ids_to_remove = []
for (device_id, device_friendlyName) in device_friendlyNames.items():
  if device_id in media_infos and len(media_infos[device_id]) == 0:
    device_ids_to_remove.append(device_id)
if len(device_ids_to_remove) > 0:
  print('Ignoring the following %d devices that have no data for the composite video: %s' % (len(device_ids_to_remove), str(device_ids_to_remove)))
  for device_id in device_ids_to_remove:
    del composite_layout[device_friendlyNames[device_id]]
    del device_friendlyNames[device_id]
    del media_infos[device_id]

######################################################
# INITIALIZE THE OUTPUT VIDEO
######################################################

# Generate timestamps for the output video frames.
output_video_num_frames = output_video_duration_s * output_video_fps
output_video_frame_duration_s = 1/output_video_fps
output_video_timestamps_s = output_video_start_time_s \
                            + np.arange(start=0,
                                        stop=output_video_num_frames)*output_video_frame_duration_s

if use_pyqtgraph_subplots:
  # # The below will make the background white if desired (the default is black).
  # pyqtgraph.setConfigOption('background', 'w')
  # pyqtgraph.setConfigOption('foreground', 'k')

  # Define a helper to update a subplot with new device data.
  # layout_widget is the item to update, such as an image view or an audio plot.
  # layout_specs is (row, col, rowspan, colspan) of the subplot location.
  # data is an image or audio data.
  # label is text to write on an image if desired.
  def update_subplot(layout_widget, layout_specs, data, label=None):
    if is_image(data[0]):
      data = data[0]
      # Draw text on the image if desired.
      # Note that this is done after scaling, since scaling the text could make it unreadable.
      if label is not None:
        draw_text_on_image(data, label, pos=(0,-1),
                           font_scale=0.5, font_thickness=1, font=cv2.FONT_HERSHEY_DUPLEX)
      # Update the subplot with the image.
      pixmap = cv2_to_pixmap(data)
      layout_widget.setPixmap(pixmap)

    elif is_audio(data[0]):
      if audio_plot_waveform:
        data = data[0]
        (audio_plotWidget, h_lines) = layout_widget
        # Update the line items with the new data.
        for channel_index in range(audio_num_channels_toPlot):
          h_lines[channel_index].setData(audio_timestamps_toPlot_s, data[:,channel_index])
        # Plot a vertical current time marker, and update the y range.
        if np.amax(data) < 50:
          h_lines[-1].setData([0, 0], np.amax(data)*np.array([-50, 50]))
          audio_plotWidget.setYRange(-50, 50) # avoid zooming into an empty plot
        else:
          h_lines[-1].setData([0, 0], np.amax(data)*np.array([-1, 1]))
          audio_plotWidget.enableAutoRange(enable=0.9) # allow automatic scaling that shows 90% of the data
      elif audio_plot_spectrogram:
        (audio_plotWidget, h_heatmap, h_colorbar) = layout_widget
        (spectrogram, t_ticks, f_ticks, colorbar_levels) = data
        colorbar_levels = colorbar_levels.copy()
        colorbar_levels[-1] = min(np.amax(spectrogram), colorbar_levels[-1])
        # Add the current-time marker.
        spectrogram_toPlot = spectrogram.copy()
        spectrogram_toPlot[:, audio_plot_length_beforeCurrentTime] = colorbar_levels[-1]
        # Update the heatmap and colorbar.
        h_heatmap.setImage(spectrogram_toPlot.T)
        h_colorbar.setLevels(colorbar_levels)

  # Create the plotting layout.

  # Store the widgets/plots, and dummy data for each one so it can be cleared when no device data is available.
  # Will use layout_specs as the key, in case multiple devices are in the same subplot.
  layout_widgets = {}
  dummy_datas = {}
  # Initialize the layout.
  # The top level will be a GraphicsLayout, since that seems easier to export to an image.
  # Then the main level will be a GridLayout to flexibly arrange the visualized data streams.
  app = QtWidgets.QApplication([])
  graphics_layout = pyqtgraph.GraphicsLayoutWidget()
  grid_layout = QtWidgets.QGridLayout()
  graphics_layout.setLayout(grid_layout)
  # Initialize the visualizations for each stream.
  for (device_friendlyName, layout_specs) in composite_layout.items():
    device_id = device_friendlyName_to_id(device_friendlyName)
    (row, col, rowspan, colspan) = layout_specs
    # If a widget has already been created for this subplot location, just use that one for this device too.
    if str(layout_specs) in layout_widgets:
      continue
    # Load information about the stream.
    media_file_infos = media_infos[device_id]
    example_filepath = list(media_file_infos.keys())[0]
    (example_timestamps_s, example_data) = media_file_infos[example_filepath]
    # Create a layout based on the data type.
    if is_video(example_filepath) or is_image(example_filepath):
      if is_video(example_filepath):
        success, example_image = load_frame(example_data, 0,
                                            target_width=composite_layout_column_width*colspan,
                                            target_height=composite_layout_row_height*rowspan)
      elif is_image(example_filepath):
        example_image = load_image(example_filepath,
                                   target_width=composite_layout_column_width*colspan,
                                   target_height=composite_layout_row_height*rowspan)
      else:
        raise AssertionError('Thought it was a video or image, but apparently not')
      # Create a gray image the size of the real image that can be used to see the composite layout.
      blank_image = 100*np.ones_like(example_image)
      # Create a widget to show the image, that is set to the target height.
      image_labelWidget = QtWidgets.QLabel()
      grid_layout.addWidget(image_labelWidget, *layout_specs,
                            alignment=pyqtgraph.QtCore.Qt.AlignmentFlag.AlignCenter)
      grid_layout.setRowMinimumHeight(layout_specs[0], composite_layout_row_height)
      update_subplot(image_labelWidget, layout_specs, [blank_image])
      # Store the widget and a black image as dummy data.
      layout_widgets[str(layout_specs)] = image_labelWidget
      dummy_datas[str(layout_specs)] = [0*blank_image]
    elif is_audio(example_filepath):
      # Create a plot for the audio data, that is set to the target height.
      audio_plotWidget = pyqtgraph.PlotWidget()
      grid_layout.addWidget(audio_plotWidget, *layout_specs, alignment=pyqtgraph.QtCore.Qt.AlignmentFlag.AlignCenter)
      grid_layout.setRowMinimumHeight(layout_specs[0], composite_layout_row_height)
      # Generate random noise that can be used to preview the visualization layout.
      random_audio = 500*np.random.normal(size=(1+int(audio_plot_duration_s*audio_resample_rate_hz), audio_num_channels_toPlot))
      # Ensure the widget fills the width of the entire allocated region of subplots.
      audio_plotWidget.setMinimumWidth(composite_layout_column_width*layout_specs[3])
      # Plot the dummy data, and store handles so the plot can be updated later.
      if audio_plot_waveform:
        h_lines = []
        for channel_index in range(audio_num_channels_toPlot):
          h_lines.append(audio_plotWidget.plot(audio_timestamps_toPlot_s, random_audio[:,channel_index],
                                               pen=audio_waveform_plot_pens[channel_index]))
        h_lines.append(audio_plotWidget.plot([0, 0], [-500, 500], pen=pyqtgraph.mkPen([0, 150, 150], width=7)))
        # Store the plot and line handles.
        layout_widgets[str(layout_specs)] = (audio_plotWidget, h_lines)
        # Store dummy data.
        dummy_datas[str(layout_specs)] = [0*random_audio]
      elif audio_plot_spectrogram:
        # Assumes one channel for now
        # Create a random-noise spectrogram.
        spectrogram_f, spectrogram_t, spectrogram = \
          signal.spectrogram(random_audio[:,0], audio_resample_rate_hz,
                             window=signal.get_window('tukey', int(audio_spectrogram_window_s*audio_resample_rate_hz)),
                             scaling='density', # density or spectrum (default is density)
                             nperseg=None)
        # Use the formatting from the example spectrogram.
        (_, t_ticks, f_ticks, colorbar_levels) = example_data
        # Plot the spectrogram.
        h_heatmap = pyqtgraph.ImageItem(image=spectrogram.T, hoverable=False)
        audio_plotWidget.addItem(h_heatmap)
        audio_plotWidget.showAxis('bottom')
        audio_plotWidget.showAxis('left')
        audio_plotWidget.getAxis('left').setTicks([f_ticks])
        audio_plotWidget.getAxis('bottom').setTicks([t_ticks])
        audio_plotWidget.getAxis('bottom').setLabel('Time [s]')
        audio_plotWidget.getAxis('left').setLabel('Frequency [kHz]')
        # Force an update of the window size (double-check if this is needed?)
        graphics_layout.show()
        graphics_layout.hide()
        # h_plot.setAspectLocked(True)
        h_colorbar = audio_plotWidget.addColorBar(h_heatmap, colorMap=audio_spectrogram_colormap, interactive=False)
        # Store the various handles to update later.
        layout_widgets[str(layout_specs)] = (audio_plotWidget, h_heatmap, h_colorbar)
        # Update the plot now, to set formatting such as colorbar levels.
        update_subplot(layout_widgets[str(layout_specs)], layout_specs, (spectrogram, t_ticks, f_ticks, colorbar_levels))
        # Store dummy data.
        dummy_datas[str(layout_specs)] = (0*spectrogram, t_ticks, f_ticks, colorbar_levels)

  # Draw the visualization with dummy data.
  QtCore.QCoreApplication.processEvents()
  graphics_layout.setWindowTitle('Happy Birthday!')
  if show_visualization_window or debug_composite_layout:
    graphics_layout.show()
    if debug_composite_layout:
      app.exec()
      import sys
      sys.exit()

######################################################
# Alternative option using OpenCV instead of PyQtGraph for the subplotting/layout

if use_opencv_subplots:
  def get_slice_indexes_for_subplot_update(layout_specs, subplot_img=None):
    (row, col, rowspan, colspan) = layout_specs
    # Get the indexes of the total space allocated to this subplot.
    start_col_index = subplot_border_size*(col+1) + composite_layout_column_width*(col)
    end_col_index = start_col_index + composite_layout_column_width*(colspan) + subplot_border_size*(colspan-1) - 1
    start_row_index = subplot_border_size*(row+1) + composite_layout_row_height*(row)
    end_row_index = start_row_index + composite_layout_row_height*(rowspan) + subplot_border_size*(rowspan-1) - 1
    # Center the desired image in the subplot.
    if subplot_img is not None:
      subplot_width = end_col_index - start_col_index + 1
      pad_left = (subplot_width - subplot_img.shape[1])//2
      pad_right = (subplot_width - subplot_img.shape[1]) - pad_left
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
  
  # Define a helper to update a subplot with new device data.
  # composite_img is the composite frame image to update.
  # layout_specs is (row, col, rowspan, colspan) of the subplot location.
  # data is an image or audio data.
  # image_label is text to write on an image if desired.
  # audio_graphics_layout and plot_handles are the audio/drone plot items if updating audio/drones.
  def update_subplot(composite_img, layout_specs, data,
                     subplot_label=None, subplot_label_color=None,
                     plot_handles=None):
    
    if is_image(data[0]):
      data = data[0]
      # Update the subplot within the image.
      subplot_indexes = get_slice_indexes_for_subplot_update(layout_specs, data)
      composite_img[subplot_indexes[0]:subplot_indexes[1], subplot_indexes[2]:subplot_indexes[3]] = data
      # Draw text on the subplot if desired.
      # Note that this is done after scaling, since scaling the text could make it unreadable.
      if subplot_label is not None:
        subplot_indexes = get_slice_indexes_for_subplot_update(layout_specs)
        subplot_img = composite_img[subplot_indexes[0]:subplot_indexes[1], subplot_indexes[2]:subplot_indexes[3]]
        # Test the width of the text on the image/subplot.
        pos = (0, -1) # bottom left corner
        text_width_ratio = None # use the specified font instead of scaling based on width
        font_thickness = 1#2 if subplot_label_color is not None else 1
        (text_w, text_h) = draw_text_on_image(subplot_img, subplot_label, pos=pos,
                           font_scale=0.7, font_thickness=font_thickness,
                           font=cv2.FONT_HERSHEY_DUPLEX,
                           text_width_ratio=text_width_ratio,
                           text_bg_color=None,
                           text_color=subplot_label_color,
                           # text_bg_color=subplot_label_color,
                           # text_color=None if subplot_label_color is None else (0, 0, 0),
                           preview_only=True)
        # If the text can fit on the data image, draw it there directly.
        if text_w <= subplot_img.shape[1] and text_w <= data.shape[1]:
          draw_text_on_image(data, subplot_label, pos=pos,
                             font_scale=0.7, font_thickness=font_thickness,
                             font=cv2.FONT_HERSHEY_DUPLEX,
                             text_width_ratio=text_width_ratio,
                             text_bg_color=None,
                             text_color=subplot_label_color)
                             # text_bg_color=subplot_label_color,
                             # text_color=None if subplot_label_color is None else (0, 0, 0))
          # Update the composite image with the new subplot image.
          subplot_indexes = get_slice_indexes_for_subplot_update(layout_specs, data)
          composite_img[subplot_indexes[0]:subplot_indexes[1], subplot_indexes[2]:subplot_indexes[3]] = data
        # Otherwise, draw it on the subplot so there is more room.
        else:
          # If the text is larger than the subplot, scale it to fit.
          if text_w > subplot_img.shape[1]:
            text_width_ratio = 0.9
          # If the text is larger than the image, center it in the subplot.
          elif text_w > data.shape[1]:
            pos = (0.5, -1)
          # Add the text.
          draw_text_on_image(subplot_img, subplot_label, pos=pos,
                             font_scale=0.7, font_thickness=font_thickness,
                             font=cv2.FONT_HERSHEY_DUPLEX,
                             text_width_ratio=text_width_ratio,
                             text_bg_color=None,
                             text_color=subplot_label_color)
                             # text_bg_color=subplot_label_color,
                             # text_color=None if subplot_label_color is None else (0, 0, 0))
          # Update the composite image with the new subplot image.
          composite_img[subplot_indexes[0]:subplot_indexes[1], subplot_indexes[2]:subplot_indexes[3]] = subplot_img
    
    elif is_audio(data[0]):
      if audio_plot_waveform:
        data = data[0]
        (audio_plotWidget, audio_graphics_layout, audio_line_handles) = plot_handles
        # Update the line items with the new data.
        for channel_index in range(audio_num_channels_toPlot):
          audio_line_handles[channel_index].setData(audio_timestamps_toPlot_s, data[:,channel_index])
        # Plot a vertical current time marker, and update the y range.
        if np.amax(data) < 50:
          audio_line_handles[-1].setData([0, 0], np.amax(data)*np.array([-50, 50]))
          audio_plotWidget.setYRange(-50, 50) # avoid zooming into an empty plot
        else:
          audio_line_handles[-1].setData([0, 0], np.amax(data)*np.array([-1, 1]))
          audio_plotWidget.enableAutoRange(enable=0.9) # allow automatic scaling that shows 90% of the data
        # Grab the plot as an image.
        img = audio_graphics_layout.grab().toImage()
        img = qimage_to_numpy(img)
        img = np.array(img[:,:,0:3])
        (_, _, rowspan, colspan) = layout_specs
        img = scale_image(img, target_width=composite_layout_column_width*colspan,
                               target_height=composite_layout_row_height*rowspan)
        # Update the subplot with the image.
        composite_img = update_subplot(composite_img, layout_specs, [img], subplot_label=subplot_label)
      elif audio_plot_spectrogram:
        (audio_plotWidget, audio_graphics_exporter, h_heatmap, h_colorbar) = plot_handles
        (spectrogram, t_ticks, f_ticks, colorbar_levels) = data
        colorbar_levels = colorbar_levels.copy()
        colorbar_levels[-1] = min(np.amax(spectrogram), colorbar_levels[-1])
        # Add the current-time marker.
        spectrogram_toPlot = spectrogram.copy()
        spectrogram_toPlot[:, audio_plot_length_beforeCurrentTime] = colorbar_levels[-1]
        # Update the heatmap and colorbar.
        h_heatmap.setImage(spectrogram_toPlot.T)
        h_colorbar.setLevels(colorbar_levels)
        # Grab the plot as an image.
        img = audio_graphics_exporter.export(toBytes=True)
        img = qimage_to_numpy(img)
        img = np.array(img[:,:,0:3])
        (_, _, rowspan, colspan) = layout_specs
        img = scale_image(img, target_width=composite_layout_column_width*colspan,
                               target_height=composite_layout_row_height*rowspan)
        # Update the subplot with the image.
        composite_img = update_subplot(composite_img, layout_specs, [img], subplot_label=subplot_label)
    
    elif is_drone_data(data[0]):
      # Set the lines to the new data points.
      drone_coordinates = []
      (drone_plotWidget, drone_graphics_layout, drone_line_handles) = plot_handles
      for (drone_index, drone_data) in enumerate(data):
        x = drone_lon_to_m(drone_data['longitude'])
        y = drone_lat_to_m(drone_data['latitude'])
        drone_plot_color_index = drone_plot_color_lookup_keys.searchsorted(drone_data['altitude_relative_m'])
        drone_plot_color_index = min(drone_plot_color_index, drone_plot_color_lookup.shape[0]-1)
        drone_line_handles[drone_index].setData(
            [x], [y],
            symbolSize=drone_plot_symbolSize if ('is_dummy_data' not in drone_data) or (not drone_data['is_dummy_data']) else 0,
            symbolBrush=pyqtgraph.mkColor(*drone_plot_color_lookup[drone_plot_color_index], 255),
            symbolPen=drone_plot_symbolPens[drone_index],
        )
        if ('is_dummy_data' not in drone_data) or (not drone_data['is_dummy_data']):
          drone_coordinates.append([x, y])
      # Update the plot range.
      if len(drone_coordinates) > 0:
        drone_coordinates = np.array(drone_coordinates)
        max_distance_m = np.amax(spatial.distance.cdist(drone_coordinates, drone_coordinates))
        plot_range = max(drone_plot_minRange_m, 2*max_distance_m)
        x_extremes = [np.amin(drone_coordinates[:,0]), np.amax(drone_coordinates[:,0])]
        y_extremes = [np.amin(drone_coordinates[:,1]), np.amax(drone_coordinates[:,1])]
        x_center = np.mean(drone_plotWidget.getAxis('bottom').range)
        y_center = np.mean(drone_plotWidget.getAxis('left').range)
        x_limits = x_center + np.array([-plot_range/2, plot_range/2])
        y_limits = y_center + np.array([-plot_range/2, plot_range/2])
        if x_extremes[0] < x_limits[0] + drone_plot_rangePad:
          x_limits[0] = (x_extremes[0] - drone_plot_rangePad)
          x_limits[1] = x_limits[0] + plot_range
        if x_extremes[1] > x_limits[1] - drone_plot_rangePad:
          x_limits[1] = (x_extremes[1] + drone_plot_rangePad)
          x_limits[0] = x_limits[1] - plot_range
        if y_extremes[0] < y_limits[0] + drone_plot_rangePad:
          y_limits[0] = (y_extremes[0] - drone_plot_rangePad)
          y_limits[1] = y_limits[0] + plot_range
        if y_extremes[1] > y_limits[1] - drone_plot_rangePad:
          y_limits[1] = (y_extremes[1] + drone_plot_rangePad)
          y_limits[0] = y_limits[1] - plot_range
        drone_plotWidget.setAspectLocked(False)
        drone_plotWidget.setXRange(*x_limits, padding=0)
        drone_plotWidget.setYRange(*y_limits, padding=0)
        drone_plotWidget.setAspectLocked(True)
      # Grab the plot as an image.
      img = drone_graphics_layout.grab().toImage()
      img = qimage_to_numpy(img)
      img = np.array(img[:,:,0:3])
      (_, _, rowspan, colspan) = layout_specs
      img = scale_image(img, target_width=composite_layout_column_width*colspan,
                             target_height=composite_layout_row_height*rowspan)
      # Update the subplot with the image.
      composite_img = update_subplot(composite_img, layout_specs, [img], subplot_label=subplot_label)
    return composite_img
  
  # Create the blank image to use as the background.
  composite_img_blank = np.zeros(shape=(output_video_height, output_video_width, 3), dtype=np.uint8)
  composite_img_dummy = composite_img_blank.copy()
  
  # Store dummy data for each subplot so it can be cleared when no device data is available.
  # Also store the widgets/plots for each audio visualization so they can be updated later.
  # Will use layout_specs as the key, in case multiple devices are in the same subplot.
  audio_grid_layouts = {}
  audio_plot_handles = {}
  dummy_datas = {}
  # Initialize pyqtgraph.
  app = QtWidgets.QApplication([])
  # Initialize the visualizations for each stream.
  for (device_friendlyName, layout_specs) in composite_layout.items():
    device_id = device_friendlyName_to_id(device_friendlyName)
    (row, col, rowspan, colspan) = layout_specs
    # If a widget has already been created for this subplot location, just use that one for this device too.
    if str(layout_specs) in dummy_datas:
      continue
    # Skip if no media information is stored for this device (e.g. a synthetic device such as drones)
    if device_id not in media_infos:
      continue
    # Load information about the stream.
    media_file_infos = media_infos[device_id]
    example_filepath = list(media_file_infos.keys())[0]
    (example_timestamps_s, example_data) = media_file_infos[example_filepath]
    # Create a layout and dummy data based on the stream type.
    if is_video(example_filepath) or is_image(example_filepath):
      if is_video(example_filepath):
        success, example_image = load_frame(example_data, 0,
                                            target_width=composite_layout_column_width*colspan,
                                            target_height=composite_layout_row_height*rowspan)
      elif is_image(example_filepath):
        example_image = load_image(example_filepath,
                                   target_width=composite_layout_column_width*colspan,
                                   target_height=composite_layout_row_height*rowspan)
      else:
        raise AssertionError('Thought it was a video or image, but apparently not')
      # Create a gray image the size of the real image that can be used to see the composite layout.
      blank_image = 100*np.ones_like(example_image)
      # Update the dummy composite image with the dummy image.
      update_subplot(composite_img_dummy, layout_specs, [example_image],
                     subplot_label=device_friendlyName,
                     subplot_label_color=drone_plot_colors[list(drone_datas.keys()).index(device_id)] if device_id in drone_datas else None)
      # Store a black image as dummy data.
      # Make it the full size of the subplot, rather than the size of the example image,
      #  since other data for this subplot may be a different size than this first example
      #  (for example, if a camera has both audio and video of different sizes/orientations).
      (start_row_index, end_row_index, start_col_index, end_col_index) = get_slice_indexes_for_subplot_update(layout_specs)
      subplot_width = end_col_index-start_col_index
      subplot_height = end_row_index-start_row_index
      dummy_datas[str(layout_specs)] = [np.zeros((subplot_height, subplot_width, 3), dtype=np.uint8)]
    elif is_audio(example_filepath):
      # Initialize the layout.
      # The top level will be a GraphicsLayout, since that seems easier to export to an image.
      # Then the main level will be a GridLayout to flexibly arrange the visualized data streams.
      graphics_layout = pyqtgraph.GraphicsLayoutWidget()
      grid_layout = QtWidgets.QGridLayout()
      graphics_layout.setLayout(grid_layout)
      # Create a plot for the audio data, that is set to the target size.
      audio_plotWidget = pyqtgraph.PlotWidget()
      grid_layout.addWidget(audio_plotWidget, *layout_specs, alignment=pyqtgraph.QtCore.Qt.AlignmentFlag.AlignCenter)
      graphics_layout.setGeometry(10, 10, composite_layout_column_width*colspan,
                                          composite_layout_row_height*rowspan)
      # Ensure the widget fills the width of the entire allocated region of subplots.
      grid_layout.setRowMinimumHeight(row, composite_layout_row_height*rowspan)
      audio_plotWidget.setMinimumWidth(composite_layout_column_width*colspan)
      # Generate random noise that can be used to preview the visualization layout.
      random_audio = 500*np.random.normal(size=(1+int(audio_plot_duration_s*audio_resample_rate_hz), audio_num_channels_toPlot))
      if audio_plot_waveform:
        # Plot the dummy data, and store handles to the lines so their lines can be updated later.
        # Currently assumes 2 channels of audio data.
        h_lines = []
        for channel_index in range(audio_num_channels_toPlot):
          h_lines.append(audio_plotWidget.plot(audio_timestamps_toPlot_s, random_audio[:,channel_index],
                                               pen=audio_waveform_plot_pens[channel_index]))
        h_lines.append(audio_plotWidget.plot([0, 0], [-500, 500], pen=pyqtgraph.mkPen([0, 150, 150], width=7)))
        # Store the line handles.
        audio_plot_handles[str(layout_specs)] = (audio_plotWidget, graphics_layout, h_lines)
        # Update the example composite image.
        update_subplot(composite_img_dummy, layout_specs, [random_audio],
                       subplot_label=None,
                       plot_handles=audio_plot_handles[str(layout_specs)])
        # Store dummy data.
        dummy_datas[str(layout_specs)] = [0*random_audio]
      elif audio_plot_spectrogram:
        # Assumes one channel for now
        # Create a random-noise spectrogram.
        spectrogram_f, spectrogram_t, spectrogram = \
          signal.spectrogram(random_audio[:,0], audio_resample_rate_hz,
                             window=signal.get_window('tukey', int(audio_spectrogram_window_s*audio_resample_rate_hz)),
                             scaling='density', # density or spectrum (default is density)
                             nperseg=None)
        # Use the formatting from the example spectrogram.
        (_, t_ticks, f_ticks, colorbar_levels) = example_data
        # Plot the spectrogram.
        h_heatmap = pyqtgraph.ImageItem(image=spectrogram.T, hoverable=False)
        audio_plotWidget.addItem(h_heatmap)
        audio_plotWidget.showAxis('bottom')
        audio_plotWidget.showAxis('left')
        audio_plotWidget.getAxis('left').setTicks([f_ticks])
        audio_plotWidget.getAxis('bottom').setTicks([t_ticks])
        audio_plotWidget.getAxis('bottom').setLabel('Time [s]')
        audio_plotWidget.getAxis('left').setLabel('Frequency [kHz]')
        # Force an update of the window size (double-check if this is needed?)
        graphics_layout.show()
        graphics_layout.hide()
        # h_plot.setAspectLocked(True)
        h_colorbar = audio_plotWidget.addColorBar(h_heatmap, colorMap=audio_spectrogram_colormap, interactive=False)
        # Create an exporter to get the plot as an image.
        audio_graphics_exporter = pyqtgraph.exporters.ImageExporter(audio_plotWidget.plotItem)
        audio_graphics_exporter.parameters()['width'] = composite_layout_column_width*colspan
        # Store the various handles to update later.
        audio_plot_handles[str(layout_specs)] = (audio_plotWidget, audio_graphics_exporter, h_heatmap, h_colorbar)
        # Update the plot now, to set formatting such as tick labels.
        update_subplot(composite_img_dummy, layout_specs, (spectrogram, t_ticks, f_ticks, colorbar_levels),
                       subplot_label=None,
                       plot_handles=audio_plot_handles[str(layout_specs)])
        # Store dummy data.
        dummy_datas[str(layout_specs)] = (0*spectrogram, t_ticks, f_ticks, colorbar_levels)
      # Store the overall plot handle.
      audio_grid_layouts[str(layout_specs)] = grid_layout
      # Show the window if desired.
      QtCore.QCoreApplication.processEvents()
      if show_visualization_window:
        graphics_layout.show()

  # Do the same as above but for drone data visualizations.
  drone_grid_layout = None
  drone_plot_handles = None
  num_drone_datas = len(drone_datas)
  if num_drone_datas > 0:
    # Find the layout for the drone plot.
    drone_data_layout_specs = composite_layout['Drone Positions']
    (row, col, rowspan, colspan) = drone_data_layout_specs
    # Initialize the layout if it has not been done already.
    # The top level will be a GraphicsLayout, since that seems easier to export to an image.
    # Then the main level will be a GridLayout to flexibly arrange the visualized data streams.
    drone_graphics_layout = pyqtgraph.GraphicsLayoutWidget()
    # drone_grid_layout = QtWidgets.QGridLayout()
    # drone_graphics_layout.setLayout(drone_grid_layout)
    # Create a plot for the data, that is set to the target size.
    drone_plotWidget = pyqtgraph.PlotItem()
    drone_graphics_layout.addItem(drone_plotWidget, *(0, 0, 1, 1))
                                # alignment=pyqtgraph.QtCore.Qt.AlignmentFlag.AlignCenter)
    drone_graphics_layout.setGeometry(10, 10, composite_layout_column_width*colspan,
                                      composite_layout_row_height*rowspan)
    # Set the plot bounds.
    (x_center, y_center) = drone_plot_reference_location_lonLat
    x_center = drone_lon_to_m(x_center)
    y_center = drone_lat_to_m(y_center)
    x_limits = x_center + np.array([-drone_plot_minRange_m/2, drone_plot_minRange_m/2])
    y_limits = y_center + np.array([-drone_plot_minRange_m/2, drone_plot_minRange_m/2])
    drone_plotWidget.setXRange(*x_limits, padding=0)
    drone_plotWidget.setYRange(*y_limits, padding=0)
    # Set the tick spacing and axis labels.
    drone_plotWidget.getAxis('left').setTickSpacing(**drone_plot_tickSpacing_m)
    drone_plotWidget.getAxis('bottom').setTickSpacing(**drone_plot_tickSpacing_m)
    drone_plotWidget.getAxis('left').setLabel('Y From Home [m]')
    drone_plotWidget.getAxis('bottom').setLabel('X From Home [m]')
    # Set the aspect ratio to be square and show the grid.
    drone_plotWidget.setAspectLocked(True)
    drone_plotWidget.showGrid(x=True, y=True, alpha=0.8)
    # Add a box around the plot.
    drone_plotWidget.showAxis('right')
    drone_plotWidget.showAxis('top')
    drone_plotWidget.getAxis('right').setTicks([])
    drone_plotWidget.getAxis('top').setTicks([])
    # Adjust the width of the grid and box.
    drone_plotWidget.getAxis('bottom').setPen(width=6)
    drone_plotWidget.getAxis('left').setPen(width=6)
    drone_plotWidget.getAxis('top').setPen(width=6)
    drone_plotWidget.getAxis('right').setPen(width=6)
    # Put the grid behind the plotted data.
    drone_plotWidget.getAxis('bottom').setZValue(-1000)
    drone_plotWidget.getAxis('left').setZValue(-1000) 
    # Generate dummy data for each drone.
    def get_example_drone_data():
      return {
        'latitude': (np.random.rand()-0.5)*0.0001 + (15.38146),
        'longitude': (np.random.rand()-0.5)*0.0001 + (-61.48562),
        'altitude_relative_m': (np.random.rand()-0.5)*10 + (20),
      }
    drone_dummy_data = [get_example_drone_data() for i in range(num_drone_datas)]
    # Plot the dummy data.
    h_lines = []
    for (drone_index, drone_data) in enumerate(drone_dummy_data):
      h_lines.append(
          drone_plotWidget.plot(x=[drone_data['longitude']], y=[drone_data['latitude']],
                                symbol='o', symbolSize=drone_plot_symbolSize,
                                symbolpen=drone_plot_symbolPens[drone_index]))
    # Add a colorbar.
    drone_altitude_colorbar = pyqtgraph.ColorBarItem(colorMap=drone_plot_colormap,
                                                     values=(np.min(drone_plot_color_lookup_keys), np.max(drone_plot_color_lookup_keys)),
                                                     width=12, # default 25
                                                     interactive=False)
    drone_altitude_colorbar.axis.setTickSpacing(**drone_colorbar_tickSpacing_m)
    drone_altitude_colorbar.axis.setLabel('Altitude [m]')
    drone_graphics_layout.addItem(drone_altitude_colorbar, *(0, 1, 1, 1))
    # Store the line handles.
    drone_plot_handles = (drone_plotWidget, drone_graphics_layout, h_lines)
    # Update the example composite image.
    update_subplot(composite_img_dummy, drone_data_layout_specs, drone_dummy_data,
                   subplot_label=None,
                   plot_handles=drone_plot_handles)
    # Store the dummy data.
    # Add a marker to indicate that it is dummy data.
    for (drone_index, dummy_data) in enumerate(drone_dummy_data):
      drone_dummy_data[drone_index]['is_dummy_data'] = True
    dummy_datas[str(drone_data_layout_specs)] = drone_dummy_data
    # Show the window if desired.
    QtCore.QCoreApplication.processEvents()
    if show_visualization_window:
      drone_graphics_layout.show()
  
  # Show the window if desired.
  if show_visualization_window or debug_composite_layout:
    cv2.imshow('Happy Birthday!', cv2.cvtColor(composite_img_dummy, cv2.COLOR_BGR2RGB))
    cv2.waitKey(1)
    if debug_composite_layout:
      cv2.waitKey(0)
      import sys
      sys.exit()


######################################################
# CREATE A VIDEO
######################################################

print()
print('Generating an output video with %d frames' % output_video_timestamps_s.shape[0])

# Will store some timing information for finding processing bottlenecks.
duration_s_updatePlots_total = 0
duration_s_updatePlots_audio = 0
duration_s_getIndex = 0
duration_s_readImages = 0
readImages_count = 0
readVideos_count = 0
duration_s_readVideos = 0
duration_s_audioParsing = 0
duration_s_exportFrame = 0
duration_s_writeFrame = 0

# Generate a frame for every desired timestamp.
composite_video_writer = None
if use_opencv_subplots:
  composite_img_current = composite_img_blank.copy()
last_status_time_s = 0
layouts_updated = {}
layouts_showing_dummyData = dict([(str(layout_specs), False) for layout_specs in composite_layout.values()])
layouts_prevState = dict([(str(layout_specs), None) for layout_specs in composite_layout.values()])
start_loop_time_s = time.time()
for (frame_index, current_time_s) in enumerate(output_video_timestamps_s):
  # Print periodic status updates.
  if time.time() - last_status_time_s > 10:
    print(' Processing frame %6d/%6d (%0.2f%%) for time %10d (%s)' %
          (frame_index+1, output_video_num_frames, 100*(frame_index+1)/output_video_num_frames,
           current_time_s, time_s_to_str(current_time_s, localtime_offset_s, localtime_offset_str)))
    last_status_time_s = time.time()
  
  # Mark that no subplot layouts have been updated.
  for (device_friendlyName, layout_specs) in composite_layout.items():
    layouts_updated[str(layout_specs)] = False
  
  # Loop through each specified device stream.
  # Note that multiple devices may be mapped to the same layout position;
  #  in that case the last device with data for this timestep will be used.
  for (device_friendlyName, layout_specs) in composite_layout.items():
    device_id = device_friendlyName_to_id(device_friendlyName)
    (row, col, rowspan, colspan) = layout_specs
    if device_id in media_infos:
      media_file_infos = media_infos[device_id]
    else:
      media_file_infos = {}
    # For each media file associated with this device, see if it has data for this timestep.
    # Note that the device may have multiple images that match this timestamp, but only the first will be used.
    for (filepath, (timestamps_s, data)) in media_file_infos.items():
      # Handle videos.
      if is_video(filepath):
        # Find the data index closest to the current time (if any).
        t0 = time.time()
        data_index = get_index_for_time_s(timestamps_s, current_time_s, timestamp_to_target_thresholds_s['video'])
        duration_s_getIndex += time.time() - t0
        if data_index is not None:
          # Only spend time loading data and updating the plot if it changed since last frame.
          if (filepath, data_index) == layouts_prevState[str(layout_specs)]:
            layouts_updated[str(layout_specs)] = True
            layouts_showing_dummyData[str(layout_specs)] = False
            break # don't check any more media for this device
          # Read the video frame at the desired index.
          t0 = time.time()
          success, img = load_frame(data, data_index,
                                    target_width=composite_layout_column_width*colspan,
                                    target_height=composite_layout_row_height*rowspan)
          
          if success:
            duration_s_readVideos += time.time() - t0
            readVideos_count += 1
            # Update the subplot with the video frame.
            t0 = time.time()
            if use_pyqtgraph_subplots:
              update_subplot(layout_widgets[str(layout_specs)], layout_specs, [img], label=device_friendlyName)
            elif use_opencv_subplots:
              img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
              update_subplot(composite_img_current, layout_specs, [img],
                             subplot_label=device_friendlyName,
                             subplot_label_color=drone_plot_colors[list(drone_datas.keys()).index(device_id)] if device_id in drone_datas else None)
            layouts_updated[str(layout_specs)] = True
            layouts_showing_dummyData[str(layout_specs)] = False
            layouts_prevState[str(layout_specs)] = (filepath, data_index)
            duration_s_updatePlots_total += time.time() - t0
            break # don't check any more media for this device
      # Handle photos.
      elif is_image(filepath):
        # Find the data index closest to the current time (if any).
        t0 = time.time()
        data_index = get_index_for_time_s(timestamps_s, current_time_s, timestamp_to_target_thresholds_s['image'])
        duration_s_getIndex += time.time() - t0
        if data_index is not None:
          # Only spend time loading data and updating the plot if it changed since last frame.
          if (filepath, data_index) == layouts_prevState[str(layout_specs)]:
            layouts_updated[str(layout_specs)] = True
            layouts_showing_dummyData[str(layout_specs)] = False
            break # don't check any more media for this device
          # Read the desired photo.
          t0 = time.time()
          img = load_image(filepath,
                           target_width=composite_layout_column_width*colspan,
                           target_height=composite_layout_row_height*rowspan)
          duration_s_readImages += time.time() - t0
          readImages_count += 1
          # Update the subplot with the photo.
          t0 = time.time()
          if use_pyqtgraph_subplots:
            update_subplot(layout_widgets[str(layout_specs)], layout_specs, [img], label=device_friendlyName)
          elif use_opencv_subplots:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            update_subplot(composite_img_current, layout_specs, [img],
                           subplot_label=device_friendlyName,
                           subplot_label_color=drone_plot_colors[list(drone_datas.keys()).index(device_id)] if device_id in drone_datas else None)
          layouts_updated[str(layout_specs)] = True
          layouts_showing_dummyData[str(layout_specs)] = False
          layouts_prevState[str(layout_specs)] = (filepath, data_index)
          duration_s_updatePlots_total += time.time() - t0
          break # don't check any more media for this device
      # Handle audio.
      elif is_audio(filepath):
        # Find the data index closest to the current time (if any).
        t0 = time.time()
        data_index = get_index_for_time_s(timestamps_s, current_time_s, timestamp_to_target_thresholds_s['audio'])
        duration_s_getIndex += time.time() - t0
        if data_index is not None:
          # Only spend time loading data and updating the plot if it changed since last frame.
          if (filepath, data_index) == layouts_prevState[str(layout_specs)]:
            layouts_updated[str(layout_specs)] = True
            layouts_showing_dummyData[str(layout_specs)] = False
            break # don't check any more media for this device
          t0 = time.time()
          # Get the start/end indexes of the data to plot.
          # Note that these may be negative or beyond the bounds of the data, indicating padding is needed.
          start_index = data_index - audio_plot_length_beforeCurrentTime
          end_index = data_index + audio_plot_length_afterCurrentTime + 1
          # Determine how much silence should be added to the data to fill the plot.
          data_t_length = data.shape[0] if audio_plot_waveform else data[0].shape[1]
          num_toPad_pre = 0 if start_index >= 0 else -start_index
          num_toPad_post = 0 if end_index <= data_t_length else end_index - data_t_length
          # Adjust the start/end indexes to be within the data bounds.
          start_index = max(0, start_index)
          end_index = min(data_t_length, end_index)
          # Get the data and pad it as needed.
          if audio_plot_waveform:
            audio_num_channels = data.shape[1]
            data_toPlot = data[start_index:end_index]
            data_toPlot = np.vstack([np.zeros((num_toPad_pre, audio_num_channels)),
                                     data_toPlot,
                                     np.zeros((num_toPad_post, audio_num_channels))])
            data_toPlot = [data_toPlot]
          if audio_plot_spectrogram:
            (spectrogram, t_ticks, f_ticks, colorbar_levels) = data
            data_toPlot = spectrogram[:, start_index:end_index]
            data_toPlot = np.hstack([np.zeros((spectrogram.shape[0], num_toPad_pre)),
                                     data_toPlot,
                                     np.zeros((spectrogram.shape[0], num_toPad_post))])
            data_toPlot = (data_toPlot, t_ticks, f_ticks, colorbar_levels)
          duration_s_audioParsing += time.time() - t0
          # Update the subplot with the waveform or spectrogram segment.
          t0 = time.time()
          if use_pyqtgraph_subplots:
            update_subplot(layout_widgets[str(layout_specs)], layout_specs, data_toPlot)
          elif use_opencv_subplots:
            update_subplot(composite_img_current, layout_specs, data_toPlot,
                           subplot_label=None,
                           plot_handles=audio_plot_handles[str(layout_specs)])
          layouts_updated[str(layout_specs)] = True
          layouts_showing_dummyData[str(layout_specs)] = False
          layouts_prevState[str(layout_specs)] = (filepath, data_index)
          duration_s_updatePlots_total += time.time() - t0
          duration_s_updatePlots_audio += time.time() - t0
          break # don't check any more media for this device
    # Check if this is a drone-positions layout, and if so update the plot.
    if device_id == 'Drone_Positions':
      drone_data_toPlot = dummy_datas[str(layout_specs)].copy()
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
            break # don't check any more media for this device
      # Only spend time updating the plot if it changed since last frame.
      if drone_data_toPlot == layouts_prevState[str(layout_specs)]:
        layouts_updated[str(layout_specs)] = True
        layouts_showing_dummyData[str(layout_specs)] = False
      else:
        t0 = time.time()
        update_subplot(composite_img_current, layout_specs, drone_data_toPlot,
                       subplot_label=None,
                       plot_handles=drone_plot_handles)
        layouts_updated[str(layout_specs)] = True
        layouts_showing_dummyData[str(layout_specs)] = False
        layouts_prevState[str(layout_specs)] = (drone_data_toPlot)
        duration_s_updatePlots_total += time.time() - t0
  
  # If a layout was not updated, show its dummy data.
  # But only spend time updating it if it isn't already showing dummy data.
  for (device_friendlyName, layout_specs) in composite_layout.items():
    if not layouts_updated[str(layout_specs)] and not layouts_showing_dummyData[str(layout_specs)]:
      device_id = device_friendlyName_to_id(device_friendlyName)
      t0 = time.time()
      if use_pyqtgraph_subplots:
        update_subplot(layout_widgets[str(layout_specs)], layout_specs, dummy_datas[str(layout_specs)])
      elif use_opencv_subplots:
        if is_audio(dummy_datas[str(layout_specs)][0]):
          update_subplot(composite_img_current, layout_specs, dummy_datas[str(layout_specs)],
                         subplot_label=None,
                         plot_handles=audio_plot_handles[str(layout_specs)])
          duration_s_updatePlots_audio += time.time() - t0
        else:
          update_subplot(composite_img_current, layout_specs, dummy_datas[str(layout_specs)],
                         subplot_label=None)
          duration_s_updatePlots_total += time.time() - t0
      layouts_showing_dummyData[str(layout_specs)] = True
      duration_s_updatePlots_total += time.time() - t0
      layouts_prevState[str(layout_specs)] = None
  
  # Refresh the figure with the updated subplots.
  if use_pyqtgraph_subplots or show_visualization_window:
    t0 = time.time()
    QtCore.QCoreApplication.processEvents()
    duration_s_updatePlots_total += time.time() - t0
  
  # Render the figure into a composite frame image.
  if use_pyqtgraph_subplots:
    t0 = time.time()
    exported_img = graphics_layout.grab().toImage()
    exported_img = qimage_to_numpy(exported_img)
    exported_img = np.array(exported_img[:,:,0:3])
    exported_img = scale_image(exported_img, target_width=output_video_width, target_height=output_video_height)
    duration_s_exportFrame += time.time() - t0
  elif use_opencv_subplots:
    exported_img = composite_img_current
  # Add a banner with the current timestamp.
  exported_img = add_timestamp_banner(exported_img, current_time_s)
  # Write the frame to the output video.
  if output_video_filepath is not None:
    t0 = time.time()
    # Create the video writer if this is the first frame, since we now know the frame dimensions.
    if composite_video_writer is None:
      composite_video_writer = cv2.VideoWriter(output_video_filepath,
                                               cv2.VideoWriter_fourcc(*'MJPG') if '.avi' in output_video_filepath.lower() else cv2.VideoWriter_fourcc(*'MP4V'),
                                               output_video_fps, [exported_img.shape[1], exported_img.shape[0]])
    composite_video_writer.write(exported_img)
    duration_s_writeFrame += time.time() - t0

# All done!
total_duration_s = time.time() - start_loop_time_s
print()
print('Generated composite video in %d seconds' % total_duration_s)
print()

# Release the output video.
if composite_video_writer is not None:
  composite_video_writer.release()

# Release video readers.
for (device_id, media_file_infos) in media_infos.items():
  for (filepath, (timestamps_s, data)) in media_file_infos.items():
    if isinstance(data, cv2.VideoCapture):
      data.release()

# Print timing information.
print()
print('Configuration:')
print('  Audio rate     : %d Hz' % audio_resample_rate_hz)
print('  Audio plot duration: [-%d %d] seconds' % (audio_plot_duration_beforeCurrentTime_s, audio_plot_duration_afterCurrentTime_s))
print('  Column width   : %d' % composite_layout_column_width)
print('  Output duration: %d' % output_video_duration_s)
print('  Output rate    : %d' % output_video_fps)
print('  Show visualization window: %s' % show_visualization_window)
print('Processing duration: ')
print('  Total duration: %0.3f seconds' % total_duration_s)
print('  Frame count   : %d' % output_video_timestamps_s.shape[0])
print('  Frame rate    : %0.1f frames per second' % (output_video_timestamps_s.shape[0]/total_duration_s))
print('  Speed factor  : %0.2f x real time' % (output_video_duration_s/total_duration_s))
print('Processing breakdown: ')
print('  UpdatePlots (total) : %6.2f%% (%0.3f seconds)' % (100 * duration_s_updatePlots_total / total_duration_s, duration_s_updatePlots_total))
print('  UpdatePlots (audio) : %6.2f%% (%0.3f seconds)' % (100 * duration_s_updatePlots_audio / total_duration_s, duration_s_updatePlots_audio))
print('  GetIndex            : %6.2f%% (%0.3f seconds)' % (100*duration_s_getIndex/total_duration_s, duration_s_getIndex))
print('  ReadImages          : %6.2f%% (%0.3f seconds) (%d calls)' % (100*duration_s_readImages/total_duration_s, duration_s_readImages, readImages_count))
print('  ReadVideos          : %6.2f%% (%0.3f seconds) (%d calls)' % (100*duration_s_readVideos/total_duration_s, duration_s_readVideos, readVideos_count))
print('  ParseAudio          : %6.2f%% (%0.3f seconds)' % (100*duration_s_audioParsing/total_duration_s, duration_s_audioParsing))
print('  ExportFrame         : %6.2f%% (%0.3f seconds)' % (100*duration_s_exportFrame/total_duration_s, duration_s_exportFrame))
print('  WriteFrame          : %6.2f%% (%0.3f seconds)' % (100*duration_s_writeFrame/total_duration_s, duration_s_writeFrame))
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
  print('  Compression completed in %0.3f seconds' % (time.time() - t0))
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
      audio_start_time_s += epoch_offsets_toAdd_s[device_id]
      (audio_rate, audio_data) = wavfile.read(filepath)
      audio_duration_s = (audio_data.shape[0]-1)/audio_rate
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
    print('  Audio track added in %0.3f seconds' % (time.time() - t0))
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
  app.exec()












