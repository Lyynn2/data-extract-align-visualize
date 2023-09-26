
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

import h5py
import numpy as np
import os
from collections import OrderedDict

from ThreadedVideoWriter import ThreadedVideoWriter

from helpers_synchronization import *
from helpers_various import *

##############################################################
# Specify the filepath for each drone's HDF5 file of metadata.
##############################################################
data_root_dir = 'C:/Users/jdelp/Desktop/_whale_birthday_s3_data'
drone_metadata_filepaths = OrderedDict([
  # Map from device ID to its HDF5 filepath.
  ('DSWP-DJI_MAVIC3-2', os.path.join(data_root_dir, 'DSWP-DJI_MAVIC3-2', 'DSWP-DJI_MAVIC3-2_metadata.hdf5')),
  ('CETI-DJI_MAVIC3-1', os.path.join(data_root_dir, 'CETI-DJI_MAVIC3-1', 'CETI-DJI_MAVIC3-1_metadata.hdf5')),
  ])

output_video_filepath = os.path.join(data_root_dir, 'drone_paths.mp4')

############################################
# Happy analyzing!
############################################

all_times_s = OrderedDict([(device_id, []) for device_id in drone_metadata_filepaths])
all_latitudes = OrderedDict([(device_id, []) for device_id in drone_metadata_filepaths])
all_longitudes = OrderedDict([(device_id, []) for device_id in drone_metadata_filepaths])
for (device_id, drone_metadata_filepath) in drone_metadata_filepaths.items():
  print()
  print('Loading data for device %s' % device_id)
  # Open the HDF5 file.
  h5file = h5py.File(drone_metadata_filepath, 'r')
  # The top-level keys of the file are the corresponding video filenames.
  video_filenames = list(h5file.keys())
  print('  See metadata for %d videos' % (len(video_filenames)))
  
  for video_filename in video_filenames:
    # Load the global timestamps for each frame of the video.
    # Timestamps have been adjusted to be synchronized based on the current manual estimates.
    timestamps_s   = np.array(h5file[video_filename]['time']['aligned_timestamp_s'])
    timestamps_str = np.array(h5file[video_filename]['time']['aligned_timestamp_str'])
    # The HDF5 file also has original timestamps recorded by the drone during filming.
    # These are not aligned using the manual offsets, and they may not account for time zone offsets.
    original_timestamps_s   = np.array(h5file[video_filename]['time']['original_timestamp_s'])
    original_timestamps_str   = np.array(h5file[video_filename]['time']['original_timestamp_str'])
    
    # Load data about the drone's position.
    altitudes_absolute_m = np.array(h5file[video_filename]['position']['altitude_absolute_m'])
    altitudes_relative_m = np.array(h5file[video_filename]['position']['altitude_relative_m'])
    latitudes            = np.array(h5file[video_filename]['position']['latitude'])
    longitudes           = np.array(h5file[video_filename]['position']['longitude'])
    # Note that there is 1 frame where the latitude was 0;
    #  presumably this is used to indicate a sensor error.
    latitudes[np.where(latitudes == 0)[0]] = np.nan
    longitudes[np.where(longitudes == 0)[0]] = np.nan
    
    # Load data about the camera settings.
    color_modes        = np.array(h5file[video_filename]['camera']['color_mode'])
    color_temperatures = np.array(h5file[video_filename]['camera']['color_temperature'])
    exposure_values    = np.array(h5file[video_filename]['camera']['exposure_value'])
    f_numbers          = np.array(h5file[video_filename]['camera']['f_number'])
    focal_lengths      = np.array(h5file[video_filename]['camera']['focal_length'])
    isos               = np.array(h5file[video_filename]['camera']['iso'])
    shutters           = np.array(h5file[video_filename]['camera']['shutter'])
    
    # Store the desired data.
    all_times_s[device_id].extend(timestamps_s)
    all_latitudes[device_id].extend(latitudes)
    all_longitudes[device_id].extend(longitudes)

all_times_s = OrderedDict([(device_id, np.array(x)) for (device_id, x) in all_times_s.items()])
all_latitudes = OrderedDict([(device_id, np.array(x)) for (device_id, x) in all_latitudes.items()])
all_longitudes = OrderedDict([(device_id, np.array(x)) for (device_id, x) in all_longitudes.items()])

timestamp_to_target_thresholds_s = ((1/30)*0.6, (1/30)*0.6)
drone_plot_colors_currentPosition = {
  'CETI-DJI_MAVIC3-1': (0.8, 0, 0),
  'DSWP-DJI_MAVIC3-2': (0, 0, 0.8),
  }
drone_plot_colors_pastTrace = {
  'CETI-DJI_MAVIC3-1': (0.9, 0.3, 0.3),
  'DSWP-DJI_MAVIC3-2': (0.3, 0.3, 0.9),
  }
marker_size_currentPosition = 100
marker_size_pastTrace = 10
linewidth_pastTrace = 1

drone_plot_reference_location_lonLat = [-61.373179, 15.306914]
min_latitude = min([np.nanmin(all_latitudes[device_id]) for device_id in all_latitudes])# + [drone_plot_reference_location_lonLat[1]])
max_latitude = max([np.nanmax(all_latitudes[device_id]) for device_id in all_latitudes])# + [drone_plot_reference_location_lonLat[1]])
min_longitude = min([np.nanmin(all_longitudes[device_id]) for device_id in all_longitudes] + [drone_plot_reference_location_lonLat[0]])
max_longitude = max([np.nanmax(all_longitudes[device_id]) for device_id in all_longitudes] + [drone_plot_reference_location_lonLat[0]])
padding_deg = 0.003


import matplotlib
import matplotlib.pyplot as plt
if output_video_filepath is not None:
  matplotlib.use("Agg")
import tilemapbase
# tilemapbase.start_logging()
# Don't need if you have run before; DB file will already exist.
tilemapbase.init(create=True)
# Use open street map
t = tilemapbase.tiles.build_OSM()
# Get the map extent
extent = tilemapbase.Extent.from_lonlat(min_longitude - padding_deg, max_longitude + padding_deg,
                                        min_latitude - padding_deg, max_latitude + padding_deg)
# extent = extent.to_aspect(1.0)

# Create a scatter figure
fig, ax = plt.subplots(figsize=(8, 8), dpi=300)
ax.xaxis.set_visible(False)
ax.yaxis.set_visible(False)

# Show the map
plotter = tilemapbase.Plotter(extent, t, width=1200)
plotter.plot(ax, t)




# target_time_s = time_str_to_time_s('2023-07-08 11:54:34.72 -0400')
# index = get_index_for_time_s(all_times_s['DSWP-DJI_MAVIC3-2'], target_time_s, timestamp_to_target_thresholds_s)
# latitude = all_latitudes['DSWP-DJI_MAVIC3-2'][index]
# longitude = all_longitudes['DSWP-DJI_MAVIC3-2'][index]

output_video_timestep_s = 60
output_video_playback_duration_s = 30

min_time_s = min([np.nanmin(all_times_s[device_id]) for device_id in all_times_s])
max_time_s = min([np.nanmax(all_times_s[device_id]) for device_id in all_times_s])
output_video_duration_s = max_time_s - min_time_s
output_video_num_frames = np.ceil(output_video_duration_s/output_video_timestep_s)
output_video_timestamps_s = min_time_s + np.arange(start=0,
                                                   stop=output_video_num_frames)*output_video_timestep_s

output_video_fps = output_video_num_frames/output_video_playback_duration_s
print('output_video_num_frames', output_video_num_frames)
print('output_video_fps', output_video_fps)
frame_buffer_length = 200
# Create a video writer that will use threading to reduce overhead.
if output_video_filepath is not None:
  video_writer = ThreadedVideoWriter(
                              output_filepath=output_video_filepath,
                              frame_rate=output_video_fps, max_buffered_frames=frame_buffer_length,
                              copy_added_frames=True,
                              overwrite_existing_video=True)
else:
  video_writer = None

x, y = tilemapbase.project(*drone_plot_reference_location_lonLat)
ax.scatter(x,y, marker='.', color='black', s=200)
current_position_handles = dict([(device_id, None) for device_id in all_latitudes])
previous_position_xy = dict([(device_id, None) for device_id in all_latitudes])
previous_drone_off = dict([(device_id, True) for device_id in all_latitudes])
previous_print_time_s = time.time()
for (frame_index, output_video_timestamp_s) in enumerate(output_video_timestamps_s):
  if time.time() - previous_print_time_s > 5:
    print(' Processing frame %4d/%4d (%5.1f%%)' % (frame_index, output_video_num_frames, 100*frame_index/output_video_num_frames))
    previous_print_time_s = time.time()
  for device_id in all_latitudes:
    index = get_index_for_time_s(all_times_s[device_id], output_video_timestamp_s, timestamp_to_target_thresholds_s)
    if index is not None:
      current_position = [all_longitudes[device_id][index], all_latitudes[device_id][index]]
    else:
      current_position = [0, 0]
    x, y = tilemapbase.project(*current_position)
    ax.scatter(x,y, marker='.', color=[drone_plot_colors_pastTrace[device_id]], s=marker_size_pastTrace)
    if current_position_handles[device_id] is None:
      current_position_handles[device_id] = ax.scatter(x,y, marker='.', color=[drone_plot_colors_currentPosition[device_id]], s=marker_size_currentPosition)
    else:
      current_position_handles[device_id].set_offsets(np.c_[x, y])
    if index is not None:
      if previous_position_xy[device_id] is not None:
        ax.plot([previous_position_xy[device_id][0], x], [previous_position_xy[device_id][1], y],
                '-' if not previous_drone_off[device_id] else '--',
                color=drone_plot_colors_pastTrace[device_id],
                linewidth=linewidth_pastTrace)
      previous_position_xy[device_id] = [x,y]
      previous_drone_off[device_id] = False
    else:
      previous_drone_off[device_id] = True
    ax.set_title(time_s_to_str(output_video_timestamp_s,
                              timezone_offset_s=localtime_offset_s,
                              timezone_offset_str=localtime_offset_str))
  fig.canvas.draw_idle()
  # plt.show(block=False)
  # cv2.waitKey(1)
  
  if video_writer is not None:
    frame_img = np.frombuffer(fig.canvas.tostring_rgb(), dtype=np.uint8)
    frame_img = frame_img.reshape(fig.canvas.get_width_height()[::-1] + (3,))
    
    frame_img = frame_img[int(frame_img.shape[0]*0.33):int(frame_img.shape[0]*0.65),
                          int(frame_img.shape[1]*0.11):int(frame_img.shape[1]*0.915)]
    
    video_writer.add_frame(cv2.cvtColor(frame_img, cv2.COLOR_BGR2RGB))
    cv2.imshow('frame', cv2.cvtColor(frame_img, cv2.COLOR_BGR2RGB))
    cv2.waitKey(1)
    
    # fig.canvas.draw_idle()
    # import cv2
    # cv2.waitKey(3000)
    # x, y = tilemapbase.project(all_longitudes['DSWP-DJI_MAVIC3-2'][0], all_latitudes['DSWP-DJI_MAVIC3-2'][0])
    # h.set_offsets(np.c_[x, y])
    # fig.canvas.draw_idle()
    # cv2.waitKey(3000)

video_writer.release()
print()
