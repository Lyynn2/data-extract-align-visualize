
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

from collections import OrderedDict
from helpers_data_extraction import *

import h5py
import os

############################################
# CONFIGURATION
############################################

# The path to the root of the data directory,
#   which contains subfolders for each requested device.
data_root_dir = 'C:/Users/jdelp/Desktop/_whale_birthday_s3_data'

# A start and end time if desired.
# If specified, will ignore wav files outside this range.
# The example range below essentially selects file 280.
end_time_cutoff_s = None #time_str_to_time_s('2023-07-08 11:56:34.72 -0400')

# The device IDs from which to extract data.
device_ids = [
  'CETI-DJI_MAVIC3-1',
  'DSWP-DJI_MAVIC3-2',
  ]

############################################
# EXTRACT DATA
############################################

# Will create a dictionary with following structure:
#   [device_id][filepath] = (timestamps_s, data) where
#    timestamps_s is a numpy array of epoch timestamps for every frame and
#    data is a dictionary returned by helpers.get_drone_srt_data()
drone_datas = OrderedDict()

print()
print('Getting timestamps and data for every drone frame')
for device_id in device_ids:
  # Extract the timestamped data for this device.
  drone_data = get_timestamped_data_drones(data_root_dir, [device_id],
                                           device_friendlyNames=None,
                                           end_time_cutoff_s=end_time_cutoff_s,
                                           suppress_printing=False)
  
  # Perform any additional processing on the data if desired,
  #  then store it in the appropriate dictionary.
  if device_id in drone_data:
    drone_datas[device_id] = {}
    for (filepath, (timestamps_s, data)) in drone_data[device_id].items():
      drone_datas[device_id][filepath] = (timestamps_s, data)
  
############################################
# SAMPLE USAGE
############################################

print()
print('='*50)
print()

for device_id in drone_datas:
  print('See device id: %s' % device_id)
  for (filepath, (timestamps_s, data)) in drone_datas[device_id].items():
    print('  See data for file   : %s' % filepath)
    print('    Start time of file: %0.3f s | %s' % (timestamps_s[0], time_s_to_str(timestamps_s[0], localtime_offset_s, localtime_offset_str)))
    print('    End time of file  : %0.3f s | %s' % (timestamps_s[-1], time_s_to_str(timestamps_s[-1], localtime_offset_s, localtime_offset_str)))
    print('    Data keys         : %s' % (str(list(data.keys()))))

############################################
# SAVE HDF5 FILES
############################################

print()
print('='*50)
print()
print('Saving drone data to HDF5 files')
for device_id in drone_datas:
  print('See device id: %s' % device_id)
  h5file = h5py.File(os.path.join(data_root_dir, device_id, '%s_metadata.hdf5' % device_id), 'w')
  for (filepath, (timestamps_s, data)) in drone_datas[device_id].items():
    file_group = h5file.create_group(os.path.splitext(os.path.basename(filepath))[0])
    time_group = file_group.create_group('time')
    position_group = file_group.create_group('position')
    camera_group = file_group.create_group('camera')
    for key in data:
      if key in ['original_timestamp_s', 'original_timestamp_str', 'aligned_timestamp_s', 'aligned_timestamp_str']:
        time_group.create_dataset(key, data=data[key])
      elif key in ['latitude', 'longitude', 'altitude_absolute_m', 'altitude_relative_m']:
        position_group.create_dataset(key, data=data[key])
      elif key in ['color_mode', 'color_temperature', 'exposure_value', 'f_number',
                   'focal_length', 'iso', 'shutter']:
        camera_group.create_dataset(key, data=data[key])
      else:
        file_group.create_dataset(key, data=data[key])
  h5file.close()

print()
print('Done!')
print()

