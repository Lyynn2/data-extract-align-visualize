
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

from helpers import *

######################################################
# CONFIGURATION
# Note that some of the below could be loaded
#  from metadata files in the future.
######################################################

# Specify the root data directory, which contains subfolders for each device
data_dir_root = 'C:/Users/jdelp/Desktop/_whale_birthday_s3_data'

audio_filepaths = OrderedDict([
  ('DSWP-KASHMIR_MIXPRE6-1', os.path.join(data_dir_root, 'DSWP-KASHMIR_MIXPRE6-1', 'CETI23-280.1688831582000.WAV')),
  ('Misc/Pagani', os.path.join(data_dir_root, 'Misc', 'Pagani.IMG_6821.1688831614043.mp4')),
])
hydrophone_index = 0

alignment_click_timestamps_s = [
  # 1688831657.840,
  1688831683.178,
  ]

# Specify offsets to add to timestamps extracted from filenames.
epoch_offsets_toAdd_s = {
  'CETI-DJI_MAVIC3-1'          : 0.47,
  'DSWP-DJI_MAVIC3-2'          : 2.17,
  'DG-CANON_EOS_1DX_MARK_III-1': 4*3600 + 204,
  'JD-CANON_REBEL_T5I'         : 14.28,
  'DSWP-CANON_EOS_70D-1'       : 4*3600,
  'DSWP-KASHMIR_MIXPRE6-1'     : 32.7160,
  'Misc/Aluma'                 : 0,
  'Misc/Baumgartner'           : 0,
  'Misc/Pagani'                : 0,
  'Misc/SalinoHugg'            : 0,
  'Misc/DelPreto_Pixel5'       : 0,
  'Misc/DelPreto_GoPro'        : 0,
}

# Specify the time zone offset to get local time of this data collection day from UTC.
# Note that in the future this could probably be determined automatically.
localtime_offset_s = -4*3600
localtime_offset_str = '-0400'

# Plotting options.
audio_plot_original_data = False
audio_plot_filtered_data = True
audio_plot_duration_beforeCurrentTime_s = 10
audio_plot_duration_afterCurrentTime_s  = 10
audio_plot_pen = pyqtgraph.mkPen([255, 0, 255], width=1)
audio_plot_filtered_pen = pyqtgraph.mkPen([255, 255, 255], width=1)
audio_plot_click_time_pen = pyqtgraph.mkPen([255, 0, 0], width=2)
plot_original_audio_data = False


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

# Plot all waveforms.
app = QtWidgets.QApplication([])
for alignment_click_timestamp_s in alignment_click_timestamps_s:
  graphics_layout = pyqtgraph.GraphicsLayoutWidget()
  plot_handles = []
  for (device_index, device_id) in enumerate(audio_datas.keys()):
    timestamps_s = audio_timestamps_s[device_id]
    audio_rate = audio_rates[device_id]
    audio_data = audio_datas[device_id][:,1]
    audio_data_filtered = audio_data.copy()
    audio_data_filtered = filter_signal_highpass(audio_data_filtered, 2e3, audio_rate)
    audio_data_filtered = filter_signal_lowpass(audio_data_filtered, 9e3, audio_rate)
    click_index = get_index_for_time_s(timestamps_s, alignment_click_timestamp_s, np.array([0.5, 0.5])/audio_rate)
    audio_plot_length_beforeCurrentTime_s = int(audio_plot_duration_beforeCurrentTime_s*audio_rate)
    audio_plot_length_afterCurrentTime_s = int(audio_plot_duration_afterCurrentTime_s*audio_rate)
    start_index = click_index - audio_plot_length_beforeCurrentTime_s
    end_index = click_index + audio_plot_length_afterCurrentTime_s
    plot_handles.append(graphics_layout.addPlot(row=device_index, col=0, title=device_id))
    if audio_plot_original_data:
      plot_handles[-1].plot(x=timestamps_s[start_index:end_index]-alignment_click_timestamp_s,
                            y=audio_data[start_index:end_index],
                            pen=audio_plot_pen)
    if audio_plot_filtered_data:
      plot_handles[-1].plot(x=timestamps_s[start_index:end_index]-alignment_click_timestamp_s,
                            y=audio_data_filtered[start_index:end_index],
                            pen=audio_plot_filtered_pen)
    if device_index == 0:
      plot_handles[-1].setYRange(-425, 425)
    else:
      plot_handles[-1].setYRange(-0.12, 0.12)
    plot_handles[-1].plot(np.array([0, 0])*alignment_click_timestamp_s,
                          max(plot_handles[-1].getAxis('left').range)*np.array([-1, 1]),
                          pen=audio_plot_click_time_pen)
    if device_index > 0:
      plot_handles[-1].setXLink(plot_handles[0])
  graphics_layout.show()
  app.exec()





