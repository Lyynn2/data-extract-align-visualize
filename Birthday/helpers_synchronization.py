
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

import numpy as np
from collections import OrderedDict

######################################################
# MANUAL SYNCHRONIZATION CONFIGURATION
######################################################

# Specify the time zone offset to get local time of this data collection day from UTC.
# Note that in the future this could probably be determined automatically.
localtime_offset_s = -4*3600
localtime_offset_str = '-0400'
# Specify whether drone timestamps in SRT files are in local or UTC time.
drone_srt_timestamps_are_local_time = {
  'CETI-DJI_MAVIC3-1'          : False,
  'DSWP-DJI_MAVIC3-2'          : True,
}

# Specify offsets to add to timestamps extracted from filenames.
# For each device, can specify:
#  A single number, which will be added to all timestamps for that device.
#  An ordered dictionary where each entry is (started-before-this-device-time, offset).
#   A started-before-this-device-time of -1 indicates timestamps after the previous cutoff.
#   For example, if the dictionary is [(5, 100), (8, 101), (-1, 102)] then device timestamps
#    within [0, 5] will have 100s added to them, timestamps within (5, 8] will
#    have 101 seconds added to them, and timestamps > 8 will have 102s added to them.
epoch_offsets_toAdd_s = {
  'CETI-DJI_MAVIC3-1'          : OrderedDict([(1688829599.0, 0.79859),
                                              (1688833020.0, 0.79859),
                                              (1688836800.0, 0.79859),
                                              (1688838240.0, 0.79859),
                                              (1688839260.0, 0.434701),
                                              (-1,           0.434701)]),
  'DSWP-DJI_MAVIC3-2'          : OrderedDict([(1688829599.0, 6.097219),
                                              (1688833020.0, 2.10833),
                                              (1688836800.0, 6.297219),
                                              (1688838240.0, 6.499997),
                                              (1688839260.0, 6.499997),
                                              (-1,           2.299997)]),
  'DG-CANON_EOS_1DX_MARK_III-1': 14603.81506,
  'JD-CANON_REBEL_T5I'         : OrderedDict([(1688831658, 14.37973),
                                              (-1,         15.244)]),
  'DSWP-CANON_EOS_70D-1'       : 14486.21306,
  'DSWP-KASHMIR_MIXPRE6-1'     : 32.7085,
  'Misc/Aluma'                 : -0.55946,
  'Misc/Baumgartner'           : 3.303,
  'Misc/Pagani'                : 0, # used as reference time
  'Misc/SalinoHugg'            : -0.13826,
  'Misc/DelPreto_Pixel5'       : 26.39846,
  'Misc/DelPreto_GoPro'        : 8.52572,
}

######################################################
# HELPER FUNCTIONS
######################################################

# Add the desired epoch offset for a given device at a given start time.
def adjust_start_time_s(media_start_time_s, device_id):
  if isinstance(epoch_offsets_toAdd_s[device_id], dict):
    cutoff_times = list(epoch_offsets_toAdd_s[device_id].keys())
    epoch_offsets_toAdd_s_forDevice = list(epoch_offsets_toAdd_s[device_id].values())
    if cutoff_times[-1] == -1:
      cutoff_times[-1] = 9e9
    cutoff_index = np.searchsorted(cutoff_times, media_start_time_s)
    return media_start_time_s + epoch_offsets_toAdd_s_forDevice[cutoff_index]
  else:
    return media_start_time_s + epoch_offsets_toAdd_s[device_id]
  
# Find a timestamp from a device that most closely matches a target timestamp.
# Will return the index of that matched timestamp within the device's array of timestamps.
# If there is no such timestamp within a specified threshold of the target, returns None.
def get_index_for_time_s(timestamps_s, target_time_s, timestamp_to_target_thresholds_s):
  if timestamps_s.shape[0] == 1:
    # If there is only one timestamp, consider that the best one.
    best_index = 0
  else:
    # Find the index where the target timestamp would be inserted without changing the sort order.
    # This is much faster than using something like numpy.where(), since it can assume the input is sorted.
    next_index_pastTarget = timestamps_s.searchsorted(target_time_s)
    # If it returned the length of the array, decrement it to make it a valid index.
    if next_index_pastTarget == timestamps_s.shape[0]:
      next_index_pastTarget -= 1
    # If it returned the first element, use that as the best index.
    if next_index_pastTarget == 0:
      best_index = 0
    else:
      # We have placed the target between two device timestamps.
      # Now see which one of those two is closer to the target.
      index_candidates = np.array([next_index_pastTarget-1, next_index_pastTarget])
      dt_candidates = np.abs(timestamps_s[index_candidates] - target_time_s)
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