
import pysrt
import os
import glob

import pyqtgraph
from pyqtgraph.Qt import QtCore, QtGui, QtWidgets
from pyqtgraph.Qt.QtGui import QPixmap, QImage

from helpers import *

# data_dir = 'C:/Users/jdelp/Desktop/_whale_birthday_s3_data/CETI-DJI_MAVIC3-1'
data_dir = 'C:/Users/jdelp/Desktop/_whale_birthday_s3_data/DSWP-DJI_MAVIC3-2'
# fp = os.path.join(data_dir, '1688829190202.SRT')
filepaths = glob.glob(os.path.join(data_dir, '*.srt'))

timezone_offset_str = '-0400'

for fp in filepaths:
  srt = pysrt.open(fp)
  
  times_s = np.nan*np.ones(shape=(len(srt),))
  for (frame_index, srt_frame) in enumerate(srt):
    text_lines = srt_frame.text_without_tags.split('\n')
    timestamp_str = '%s %s' % (text_lines[1], timezone_offset_str)
    times_s[frame_index] = time_str_to_time_s(timestamp_str)
    data_line = text_lines[2]
    data_line = data_line.replace(' ', '')
    iso = float(data_line.split('[iso:')[1].split(']')[0].strip())
    shutter = [float(x.strip()) for x in data_line.split('[shutter:')[1].split(']')[0].split('/')]
    f_number = float(data_line.split('[fnum:')[1].split(']')[0].strip())
    exposure_value = float(data_line.split('[ev:')[1].split(']')[0].strip())
    color_temperature = float(data_line.split('[ct:')[1].split(']')[0].strip())
    focal_length = float(data_line.split('[focal_len:')[1].split(']')[0].strip())
    color_mode = data_line.split('[color_md:')[1].split(']')[0].strip()
    latitude = float(data_line.split('[latitude:')[1].split(']')[0].strip())
    longitude = float(data_line.split('[longitude:')[1].split(']')[0].strip())
    altitude_relative_m = float(data_line.split('[rel_alt:')[1].split('abs_alt')[0].strip())
    altitude_absolute_m = float(data_line.split('abs_alt:')[1].split(']')[0].strip())
    
    if frame_index == 0 and fp == filepaths[0]:
      print('Sample data from first frame of first file:')
      print('  timestamp_str', timestamp_str)
      print('  timestamp_s', time_str_to_time_s(timestamp_str))
      print('  timestamp_str', time_s_to_str(time_str_to_time_s(timestamp_str), timezone_offset_s=-4*3600, timezone_offset_str='-0400'))
      print('  iso', iso)
      print('  shutter', shutter)
      print('  f_number', f_number)
      print('  exposure_value', exposure_value)
      print('  color_temperature', color_temperature)
      print('  focal_length', focal_length)
      print('  color_mode', color_mode)
      print('  latitude', latitude)
      print('  longitude', longitude)
      print('  altitude_relative_m', altitude_relative_m)
      print('  altitude_absolute_m', altitude_absolute_m)
      print()
  
  # Print the maximum inter-frame time jump.
  print('Max time jump for %s: %5.1f ms' % (os.path.basename(fp), 1000*np.max(np.diff(times_s))))

print()
print()
print(dir(srt[0]))
print('--------------------------')
print('duration', srt[0].duration)
print('--------------------------')
print('end', srt[0].end)
print('--------------------------')
print('index', srt[0].index)
print('--------------------------')
print('position', srt[0].position)
print('--------------------------')
print('shift', srt[0].shift)
print('--------------------------')
print('split_timestamps', srt[0].split_timestamps)
print('--------------------------')
print('start', srt[0].start)
print('--------------------------')
print('text', srt[0].text)
print('--------------------------')
print('text_without_tags', srt[0].text_without_tags)
print('--------------------------')
print()
print()

start_time_s = times_s[0]
(video_reader, frame_rate, num_frames) = get_video_reader(fp.replace('.SRT', '.LRF'))
assert(num_frames == times_s.shape[0])
frame_duration_s = 1/frame_rate

times_s_constantRate = np.squeeze(start_time_s + np.arange(start=0, stop=num_frames)*frame_duration_s)
times_s = np.squeeze(times_s)

app = QtWidgets.QApplication([])
pyqtgraph.setConfigOption('background', 'w')
pyqtgraph.setConfigOption('foreground', 'k')
win = pyqtgraph.GraphicsWindow()
plt = win.addPlot()
plt.plot(times_s, pen=pyqtgraph.mkPen([0, 0, 0], width=2))
plt.plot(times_s_constantRate, pen=pyqtgraph.mkPen([255, 50, 50], width=2))
plt.showGrid(x=True, y=True)

print()
print()
print('Offset at start: %0.3fs' % (times_s[0] - times_s_constantRate[0]))
print('Offset at end  : %0.3fs' % (times_s[-1] - times_s_constantRate[-1]))
print('Max offset     : %0.3fs' % (np.amax(times_s - times_s_constantRate)))
print()
print()
app.exec()