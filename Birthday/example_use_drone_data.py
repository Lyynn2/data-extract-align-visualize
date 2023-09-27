
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

from helpers_various import *

##############################################################
# Configuration
##############################################################

# Specify the filepath for each drone's HDF5 file of metadata.
data_root_dir = '.'
drone_metadata_filepaths = OrderedDict([
  # Map from device ID to its HDF5 filepath.
  ('DSWP-DJI_MAVIC3-2', os.path.join(data_root_dir, 'DSWP-DJI_MAVIC3-2_metadata.hdf5')),
  ('CETI-DJI_MAVIC3-1', os.path.join(data_root_dir, 'CETI-DJI_MAVIC3-1_metadata.hdf5')),
  ])

############################################
# Load the drone data.
############################################
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
    original_timestamps_str = np.array(h5file[video_filename]['time']['original_timestamp_str'])
    
    # Load data about the drone's position.
    latitudes            = np.array(h5file[video_filename]['position']['latitude'])
    longitudes           = np.array(h5file[video_filename]['position']['longitude'])
    altitudes_relative_m = np.array(h5file[video_filename]['position']['altitude_relative_m'])
    #altitudes_absolute_m = np.array(h5file[video_filename]['position']['altitude_absolute_m'])
    
    # Load data about the drone's speed that was estimated from the GPS positions.
    speed_horizontal_m_s = np.array(h5file[video_filename]['speed']['estimated_speed_horizontal_fromGPS_m_s'])
    is_stationary_horizontal = np.array(h5file[video_filename]['speed']['estimated_isStationary_horizontal_fromGPS'])
    # Load data about the drone's speed that was estimated from altitude measurements.
    speed_vertical_m_s = np.array(h5file[video_filename]['speed']['estimated_speed_vertical_fromAltitude_m_s'])
    is_stationary_vertical = np.array(h5file[video_filename]['speed']['estimated_isStationary_vertical_fromAltitude'])
    
    # Note that there is 1 frame where the latitude was 0;
    #  presumably this is used to indicate a sensor error.
    # Mark any such frames as NaN for clarity.
    speed_horizontal_m_s[np.where((latitudes == 0) | (longitudes == 0))[0]] = np.nan
    is_stationary_horizontal[np.where((latitudes == 0) | (longitudes == 0))[0]] = np.nan
    speed_vertical_m_s[np.where((latitudes == 0) | (longitudes == 0))[0]] = np.nan
    is_stationary_vertical[np.where((latitudes == 0) | (longitudes == 0))[0]] = np.nan
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
    
    # Print a summary.
    print('    File %s: %4d frames | %5.1f s | %5.2f FPS | manual alignment offset %8.6f s' % (
            video_filename, timestamps_s.shape[0],
            (timestamps_s[-1] - timestamps_s[0]),
            (timestamps_s.shape[0]-1)/(timestamps_s[-1] - timestamps_s[0]),
             timestamps_s[0] - float(video_filename)/1000.0))

print()

###########################################################################
# Re-estimate speed using a different window duration if desired.
###########################################################################

speed_moving_average_window_duration_s = 2
stationary_speed_threshold_m_s = 0.001

for (device_id, drone_metadata_filepath) in drone_metadata_filepaths.items():
  # Open the HDF5 file.
  h5file = h5py.File(drone_metadata_filepath, 'r')
  # The top-level keys of the file are the corresponding video filenames.
  video_filenames = list(h5file.keys())
  
  for video_filename in video_filenames:
    # Load the global timestamps for each frame of the video.
    # Timestamps have been adjusted to be synchronized based on the current manual estimates.
    timestamps_s   = np.array(h5file[video_filename]['time']['aligned_timestamp_s'])
    timestamps_str = np.array(h5file[video_filename]['time']['aligned_timestamp_str'])
    
    # Load data about the drone's position.
    latitudes            = np.array(h5file[video_filename]['position']['latitude'])
    longitudes           = np.array(h5file[video_filename]['position']['longitude'])
    altitudes_relative_m = np.array(h5file[video_filename]['position']['altitude_relative_m'])
    #altitudes_absolute_m = np.array(h5file[video_filename]['position']['altitude_absolute_m'])
    
    # Estimate the horizontal and vertical speeds.
    (x_m, y_m) = gps_to_distance(longitudes, latitudes, units='m')
    z_m = altitudes_relative_m
    (_, x_m) = moving_average(timestamps_s, x_m, speed_moving_average_window_duration_s, 'centered')
    (_, y_m) = moving_average(timestamps_s, y_m, speed_moving_average_window_duration_s, 'centered')
    (_, z_m) = moving_average(timestamps_s, z_m, speed_moving_average_window_duration_s, 'centered')
    dx_m = np.diff(x_m)
    dy_m = np.diff(y_m)
    dz_m = np.diff(z_m)
    dt_s = np.diff(timestamps_s)
    speed_horizontal_m_s = np.sqrt(np.square(dx_m) + np.square(dy_m))/dt_s
    speed_horizontal_m_s = np.insert(speed_horizontal_m_s, 0, speed_horizontal_m_s[0])
    is_stationary_horizontal = speed_horizontal_m_s <= stationary_speed_threshold_m_s
    speed_vertical_m_s = np.sqrt(np.square(dz_m))/dt_s
    speed_vertical_m_s = np.insert(speed_vertical_m_s, 0, speed_vertical_m_s[0])
    is_stationary_vertical = speed_vertical_m_s <= stationary_speed_threshold_m_s
  
###########################################################################
# Helper methods for converting between epoch time and human-readable time.
###########################################################################

# Specify the time zone offset to get local time of this data collection day from UTC.
# These can be provided to the below helper functions.
localtime_offset_s = -4*3600
localtime_offset_str = '-0400'

# Do an example conversion.
example_epoch_time_s = timestamps_s[0]
example_timestamp_str = time_s_to_str(example_epoch_time_s,
                              timezone_offset_s=localtime_offset_s,
                              timezone_offset_str=localtime_offset_str)
restored_example_epoch_time_s = time_str_to_time_s(example_timestamp_str)
print('Example epoch time conversion: %f >> "%s" >> %f' % (example_epoch_time_s, example_timestamp_str, restored_example_epoch_time_s))
print()

############################################
# Happy analyzing!
############################################

