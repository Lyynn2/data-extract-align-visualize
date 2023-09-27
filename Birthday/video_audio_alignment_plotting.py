
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

import os
import glob
import re
import time
from collections import OrderedDict

import numpy as np
from scipy import signal
from scipy.io import wavfile
from scipy import interpolate
from moviepy.editor import VideoFileClip, AudioFileClip, CompositeAudioClip
import proglog

import cv2
import decord
import pyqtgraph
from pyqtgraph.Qt import QtCore, QtGui, QtWidgets
from pyqtgraph.Qt.QtGui import QPixmap, QImage
import pyqtgraph.exporters

from helpers_various import *

######################################################
# CONFIGURATION
# Note that some of the below could be loaded
#  from metadata files in the future.
######################################################

# Specify the root data directory, which contains subfolders for each device
data_dir_root = 'path_to_data_root_folder'

audio_filepaths = OrderedDict([
  # ('DSWP-KASHMIR_MIXPRE6-1', os.path.join(data_dir_root, 'DSWP-KASHMIR_MIXPRE6-1', 'CETI23-279.1688830800000.WAV')),
  ('DSWP-KASHMIR_MIXPRE6-1', os.path.join(data_dir_root, 'DSWP-KASHMIR_MIXPRE6-1', 'CETI23-280.1688831582000.WAV')),
  ('Misc/Pagani', os.path.join(data_dir_root, 'Misc', 'Pagani.IMG_6821.1688831614043.mp4')),
  ('Misc/Baumgartner', os.path.join(data_dir_root, 'Misc', 'Baumgartner.1688831238560.mov')),
  ('Misc/Aluma', os.path.join(data_dir_root, 'Misc', 'Aluma.IMG_4693.1688831667112.mov')),
  ('JD-CANON_REBEL_T5I', os.path.join(data_dir_root, 'JD-CANON_REBEL_T5I', '20230708_115400_DelPreto_T5i_MVI_7972_epoch1688831300110.MOV')),
  # ('Misc/DelPreto', os.path.join(data_dir_root, 'Misc', '20230708_154207_2023-07-08_10-56-52 recording epoch1688845327000.m4a')),
])
hydrophone_index = 0

alignment_click_timestamps_s = [
  1688831683.178,
  1688831661.947,
  # 1688831463.917,
  ]

yranges = [{
  'DSWP-KASHMIR_MIXPRE6-1'     : [-400, 400],
  'Misc/Pagani'                : [-0.15, 0.15],
  'Misc/Baumgartner'           : [-0.07, 0.07],
  'Misc/Aluma'                 : [-0.11, 0.11],
},
  {
    'DSWP-KASHMIR_MIXPRE6-1'     : [-400, 400],
    'Misc/Pagani'                : [-0.15, 0.15],
    'Misc/Baumgartner'           : [-0.07, 0.07],
    'Misc/Aluma'                 : [-0.11, 0.11],
  }
]

# Specify offsets to add to timestamps extracted from filenames.
epoch_offsets_toAdd_s = {
  'CETI-DJI_MAVIC3-1'          : 0.79859,
  'DSWP-DJI_MAVIC3-2'          : 2.10833,
  'DG-CANON_EOS_1DX_MARK_III-1': 14603.81506,
  'JD-CANON_REBEL_T5I'         : 14.37973,
  'DSWP-CANON_EOS_70D-1'       : 14486.21306,
  'DSWP-KASHMIR_MIXPRE6-1'     : 32.7085, #32.701, #32.7160
  'Misc/Aluma'                 : -0.55946,
  'Misc/Baumgartner'           : 3.303, #2.940, #3.28,
  'Misc/Pagani'                : 0, # used as reference time
  'Misc/SalinoHugg'            : -0.13826,
  'Misc/DelPreto_Pixel5'       : 26.39846,
  'Misc/DelPreto_GoPro'        : 8.52572,
}

# Specify the time zone offset to get local time of this data collection day from UTC.
# Note that in the future this could probably be determined automatically.
localtime_offset_s = -4*3600
localtime_offset_str = '-0400'

# Auto-alignment options
template_duration_beforeClickTime_s = 0.1
template_duration_afterClickTime_s = 0.9
search_duration_beforeClickTime_s = 300
search_duration_afterClickTime_s = 300
audio_channels_toSearch = [1]

# Plotting options.
audio_plot_original_data = False
audio_plot_filtered_data = True
audio_plot_duration_beforeCurrentTime_s = 10
audio_plot_duration_afterCurrentTime_s  = 10
audio_channels_toPlot = [0, 1]
audio_plot_pens = [
  pyqtgraph.mkPen([255,   0, 255], width=1), # channel 0
  pyqtgraph.mkPen([255, 255,   0], width=1), # channel 1
  ]
audio_plot_filtered_pens = [
  pyqtgraph.mkPen([255, 255, 255], width=1), # channel 0
  pyqtgraph.mkPen([  0, 255, 255], width=1), # channel 1
  ]
audio_plot_click_time_pen = pyqtgraph.mkPen([255, 0, 0], width=2,
                                            style=pyqtgraph.QtCore.Qt.PenStyle.DashLine)
plot_original_audio_data = False
corr_plot_pens = [
  pyqtgraph.mkPen([255, 255, 255], width=1), # channel 0
  pyqtgraph.mkPen([  0, 255, 255], width=1), # channel 1
]


######################################################
# HELPERS
######################################################

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


def filter_signal_highpass(data, cutoff, fs, order=5):
  nyq = 0.5 * fs
  normal_cutoff = cutoff / nyq
  b, a = signal.butter(order, normal_cutoff, btype='high', analog=False)
  return signal.filtfilt(b, a, data)

def filter_signal_lowpass(data, cutoff, fs, order=5):
  nyq = 0.5 * fs
  normal_cutoff = cutoff / nyq
  b, a = signal.butter(order, normal_cutoff, btype='low', analog=False)
  return signal.filtfilt(b, a, data)
  
######################################################
# PROCESSING
######################################################

def get_audio_timestamps_s(audio_filepath, audio_data, audio_rate, device_id, print_summary=False):
  filename = os.path.basename(audio_filepath)
  audio_start_time_ms = int(re.search('\d{13}', filename)[0])
  audio_start_time_s = audio_start_time_ms/1000.0
  audio_start_time_s += epoch_offsets_toAdd_s[device_id]
  num_samples = audio_data.shape[0]
  audio_duration_s = (num_samples-1)/audio_rate
  audio_end_time_s = audio_start_time_s + audio_duration_s
  audio_timestamps_s = audio_start_time_s + np.arange(start=0, stop=num_samples)/audio_rate
  if print_summary:
    print('See file %s:' % filename)
    print('  Start time: %s (%0.3f)' % (time_s_to_str(audio_start_time_s, localtime_offset_s, localtime_offset_str), audio_start_time_s))
    print('  End time  : %s (%0.3f)' % (time_s_to_str(audio_end_time_s, localtime_offset_s, localtime_offset_str), audio_end_time_s))
    print('  Duration  : %0.3f seconds' % audio_duration_s)
    print('  Rate      : %d Hz' % audio_rate)
    print('  Data shape:', audio_data.shape)
  return audio_timestamps_s

# Extract audio waveforms.
audio_rates = OrderedDict()
audio_datas = OrderedDict()
audio_timestamps_s = OrderedDict()
for (device_id, audio_filepath) in audio_filepaths.items():
  if is_audio(audio_filepath):
    (audio_rate, audio_data) = wavfile.read(audio_filepath)
  elif is_video(audio_filepath):
    video_clip = VideoFileClip(audio_filepath)
    audio_clip = video_clip.audio
    audio_rate = audio_clip.fps
    audio_data = audio_clip.to_soundarray(tt=None,
                                          fps=None,
                                          quantize=False,
                                          nbytes=2,
                                          buffersize=50000)
  else:
    raise AssertionError('Unknown file type for', audio_filepath)
  audio_rates[device_id] = audio_rate
  audio_datas[device_id] = audio_data
  audio_timestamps_s[device_id] = get_audio_timestamps_s(audio_filepath,
                                                         audio_data, audio_rate, device_id,
                                                         print_summary=True)


app = QtWidgets.QApplication([])


# # Search for alignment.
# template_audio_rate = None
# template_waveform = None
# for (alignment_click_index, alignment_click_timestamp_s) in enumerate(alignment_click_timestamps_s):
#   print('Auto-aligning using click index %d at %0.3f seconds' % (alignment_click_index, alignment_click_timestamp_s))
#   graphics_layout = pyqtgraph.GraphicsLayoutWidget()
#   plot_handles = []
#   for channel_index in audio_channels_toSearch:
#     print(' Channel %d' % channel_index)
#     for (device_index, device_id) in enumerate(audio_datas.keys()):
#       if device_index > len(plot_handles)-1:
#         plot_handles.append(graphics_layout.addPlot(row=device_index, col=0, title=device_id))
#       timestamps_s = audio_timestamps_s[device_id]
#       audio_rate = audio_rates[device_id]
#       audio_data = audio_datas[device_id][:,channel_index]
#       audio_data_filtered = audio_data.copy()
#       audio_data_filtered = filter_signal_highpass(audio_data_filtered, 2e3, audio_rate)
#       audio_data_filtered = filter_signal_lowpass(audio_data_filtered, 9e3, audio_rate)
#       if device_index == 0:
#         click_index = get_index_for_time_s(timestamps_s, alignment_click_timestamp_s, np.array([0.5, 0.5])/audio_rate)
#         template_length_beforeClickTime_s = int(template_duration_beforeClickTime_s*audio_rate)
#         template_length_afterClickTime_s = int(template_duration_afterClickTime_s*audio_rate)
#         start_index = click_index - template_length_beforeClickTime_s
#         end_index = click_index + template_length_afterClickTime_s + 1
#         template_audio_rate = audio_rate
#         template_waveform = audio_data_filtered[start_index:(end_index+1)]
#         plot_handles[device_index].plot(x=timestamps_s[start_index:(end_index+1)],
#                                         y=template_waveform,
#                                         pen=corr_plot_pens[channel_index])
#       else:
#         print('  Device [%s]' % (device_id))
#         # Resample to match the template waveform.
#         fn_interpolate_audio = interpolate.interp1d(
#             timestamps_s,  # x values
#             audio_data_filtered,    # y values
#             axis=0,        # axis of the data along which to interpolate
#             kind='linear', # interpolation method, such as 'linear', 'zero', 'nearest', 'quadratic', 'cubic', etc.
#             fill_value='extrapolate' # how to handle x values outside the original range
#         )
#         num_samples = audio_data_filtered.shape[0]
#         num_samples_resampled = int(num_samples * (template_audio_rate/audio_rate))
#         timestamps_s = timestamps_s[0] + np.arange(start=0, stop=num_samples_resampled)/template_audio_rate
#         audio_data_filtered = fn_interpolate_audio(timestamps_s)
#         audio_rate = template_audio_rate
#         num_samples = audio_data_filtered.shape[0]
#         # Extract the segment to search.
#         click_index = get_index_for_time_s(timestamps_s, alignment_click_timestamp_s, np.array([0.5, 0.5])/audio_rate)
#         search_length_beforeClickTime_s = int(search_duration_beforeClickTime_s*audio_rate)
#         search_length_afterClickTime_s = int(search_duration_afterClickTime_s*audio_rate)
#         start_index = max(0, click_index - search_length_beforeClickTime_s)
#         end_index = min(num_samples_resampled, click_index + search_length_afterClickTime_s + 1)
#         search_waveform = audio_data_filtered[start_index:(end_index+1)]
#         # Shift the template over the search segment and compute distance scores.
#         lags = signal.correlation_lags(len(search_waveform), len(template_waveform), mode='valid')
#         lags_s = lags/template_audio_rate
#         offsets_s = ((click_index-start_index) - lags - template_length_beforeClickTime_s)/template_audio_rate
#         t0 = time.time()
#         scores = signal.correlate(np.abs(search_waveform), np.abs(template_waveform),
#                                   mode='valid',
#                                   method='fft')
#         # scores = []
#         # for (lag_index, lag) in enumerate(lags):
#         #   if lag_index % 96000 == 0:
#         #     print(' computing lag %d/%d' % (lag_index, len(lags)))
#         #   test_waveform = search_waveform[lag:(lag+len(template_waveform))]
#         #   scores.append(np.linalg.norm(test_waveform - template_waveform))
#         print('time to compute:', time.time()-t0)
#         best_lag_index = np.where(scores == np.amax(scores))[0]
#         print('   Best lag(s)    : ', lags_s[best_lag_index])
#         print('   Best offsets(s): ', offsets_s[best_lag_index])
#         # plot_handles[device_index].plot(x=timestamps_s[start_index:(end_index+1)],
#         #                                 y=search_waveform,
#         #                                 pen=corr_plot_pens[channel_index])
#         plot_handles[device_index].plot(x=offsets_s,
#                                         y=scores,
#                                         pen=corr_plot_pens[channel_index])
#
# graphics_layout.show()
# app.exec()

# Plot all waveforms.
for (alignment_click_index, alignment_click_timestamp_s) in enumerate(alignment_click_timestamps_s):
  graphics_layout = pyqtgraph.GraphicsLayoutWidget()
  plot_handles = []
  for (device_index, device_id) in enumerate(audio_datas.keys()):
    timestamps_s = audio_timestamps_s[device_id]
    audio_rate = audio_rates[device_id]
    click_index = get_index_for_time_s(timestamps_s, alignment_click_timestamp_s, np.array([0.5, 0.5])/audio_rate)
    if click_index is None:
      continue
    audio_plot_length_beforeCurrentTime_s = int(audio_plot_duration_beforeCurrentTime_s*audio_rate)
    audio_plot_length_afterCurrentTime_s = int(audio_plot_duration_afterCurrentTime_s*audio_rate)
    start_index = click_index - audio_plot_length_beforeCurrentTime_s
    end_index = click_index + audio_plot_length_afterCurrentTime_s
    plot_handles.append(graphics_layout.addPlot(row=device_index, col=0, title=device_id))
    for channel_index in audio_channels_toPlot:
      audio_data = audio_datas[device_id][:,channel_index]
      audio_data_filtered = audio_data.copy()
      audio_data_filtered = filter_signal_highpass(audio_data_filtered, 2e3, audio_rate)
      audio_data_filtered = filter_signal_lowpass(audio_data_filtered, 9e3, audio_rate)
      if audio_plot_original_data:
        plot_handles[-1].plot(x=timestamps_s[start_index:end_index]-alignment_click_timestamp_s,
                              y=audio_data[start_index:end_index],
                              pen=audio_plot_pens[channel_index])
      if audio_plot_filtered_data:
        plot_handles[-1].plot(x=timestamps_s[start_index:end_index]-alignment_click_timestamp_s,
                              y=audio_data_filtered[start_index:end_index],
                              pen=audio_plot_filtered_pens[channel_index])
      # plot_handles[-1].enableAutoRange(enable=0.9) # allow automatic scaling that shows 90% of the data
      if device_id in yranges[alignment_click_index]:
        plot_handles[-1].setYRange(*yranges[alignment_click_index][device_id])
    plot_handles[-1].plot(np.array([0, 0])*alignment_click_timestamp_s,
                          max(plot_handles[-1].getAxis('left').range)*np.array([-1, 1]),
                          pen=audio_plot_click_time_pen)
    if device_index > 0:
      plot_handles[-1].setXLink(plot_handles[0])
  graphics_layout.show()
  app.exec()





