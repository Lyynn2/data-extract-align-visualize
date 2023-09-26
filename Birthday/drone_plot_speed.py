
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

import matplotlib
import matplotlib.pyplot as plt

from helpers_synchronization import *
from helpers_various import *

##############################################################
# Configuration
##############################################################

# Specify the filepath for each drone's HDF5 file of metadata.
data_root_dir = 'C:/Users/jdelp/Desktop/_whale_birthday_s3_data'
drone_metadata_filepaths = OrderedDict([
  # Map from device ID to its HDF5 filepath.
  ('DSWP-DJI_MAVIC3-2', os.path.join(data_root_dir, 'DSWP-DJI_MAVIC3-2', 'DSWP-DJI_MAVIC3-2_metadata.hdf5')),
  ('CETI-DJI_MAVIC3-1', os.path.join(data_root_dir, 'CETI-DJI_MAVIC3-1', 'CETI-DJI_MAVIC3-1_metadata.hdf5')),
  ])

# Define the GPS smoothing window for computing speed.
speed_moving_average_window_duration_s = 2
# Define the threshold for considering the drone stationary.
stationary_speed_threshold_m_s = 0.001

############################################
# Load the drone data.
############################################

# Will map from device ID to a list of lists.
#   So it will be indexed as all_times_s[device_id][file_index][timestep_index]
#   Each top-level list will have an entry for each drone video filepath.
#   Each of those lists will have an entry for each frame.
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
    all_times_s[device_id].append(np.array(timestamps_s))
    all_latitudes[device_id].append(np.array(latitudes))
    all_longitudes[device_id].append(np.array(longitudes))


############################################
# Process and plot the drone speed.
############################################
print()
for device_id in all_times_s:
  print('See device %s' % device_id)
  fig, axs = plt.subplots(nrows=2, ncols=1,
                         squeeze=False, # if False, always return 2D array of axes
                         sharex=True, sharey=False,
                         subplot_kw={'frame_on': True},
                         figsize=(4,6),
                         )
  # Compute the stationary and moving durations.
  stationary_durations_s = []
  moving_durations_s = []
  for file_index in range(len(all_times_s[device_id])):
    time_s = all_times_s[device_id][file_index]
    longitudes = all_longitudes[device_id][file_index]
    latitudes = all_latitudes[device_id][file_index]
    # Estimate the speed.
    (x_m, y_m) = gps_to_m(longitudes, latitudes)
    (_, x_m) = moving_average(time_s, x_m, speed_moving_average_window_duration_s, 'centered')
    (_, y_m) = moving_average(time_s, y_m, speed_moving_average_window_duration_s, 'centered')
    dx_m = np.diff(x_m)
    dy_m = np.diff(y_m)
    dt_s = np.diff(time_s)
    speed_m_s = np.sqrt(np.square(dx_m) + np.square(dy_m)) / dt_s
    speed_m_s = np.insert(speed_m_s, 0, speed_m_s[0])
    # Plot the speed for this file.
    axs[0][0].plot(time_s, speed_m_s, '-')
    axs[0][0].grid(True, color='lightgray')
    
    # Compute stationary durations.
    is_stationary = speed_m_s <= stationary_speed_threshold_m_s
    is_moving = speed_m_s > stationary_speed_threshold_m_s
    stationary_startEnd_times_s = np.vstack(
        [rising_edges(is_stationary, include_first_step_if_high=True),
         falling_edges(is_stationary, include_last_step_if_high=True)]).T
    stationary_durations_s.extend(np.diff(stationary_startEnd_times_s, axis=1)*np.mean(dt_s))
    # Compute moving durations.
    moving_startEnd_times_s = np.vstack(
        [rising_edges(is_moving, include_first_step_if_high=True),
         falling_edges(is_moving, include_last_step_if_high=True)]).T
    moving_durations_s.extend(np.diff(moving_startEnd_times_s, axis=1)*np.mean(dt_s))
    
    # Plot stationary periods.
    axs[1][0].plot(time_s, is_stationary, '-')
    axs[1][0].fill_between(x=time_s, y1=is_stationary, alpha=0.2)
    axs[1][0].grid(True, color='lightgray')
  
  # Print summaries for this device.
  print('  Average stationary duration [s]: %0.3f +- %0.3f' % (np.mean(stationary_durations_s),
                                                               np.std(stationary_durations_s)))
  print('  Average moving duration [s]    : %0.3f +- %0.3f' % (np.mean(moving_durations_s),
                                                               np.std(moving_durations_s)))
  # Format the plots.
  axs[0][0].set_title('%s: Speed' % device_id)
  axs[0][0].set_ylabel('Speed [m/s]')
  axs[1][0].set_title('%s: Is Stationary' % device_id)
  axs[1][0].set_xlabel('Epoch Timestamp [s]')

print()

# Show the plot windows.
plt.show()
