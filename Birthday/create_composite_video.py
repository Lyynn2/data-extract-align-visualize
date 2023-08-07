
import os
import glob
import re
import dateutil.parser
import time
from datetime import datetime
import numpy as np
from scipy.io import wavfile
from scipy import interpolate
import cv2
from collections import OrderedDict

import pyqtgraph
from pyqtgraph.Qt import QtCore, QtGui, QtWidgets
from pyqtgraph.Qt.QtGui import QPixmap, QImage

import inspect




def time_s_to_str(time_s):
  time_datetime = datetime.utcfromtimestamp(time_s - 4*3600) # TODO Avoid the hard-coded 4-hour shift?
  return time_datetime.strftime('%Y-%m-%d %H:%M:%S.%f -0400')

def time_str_to_time_s(time_str):
  time_datetime = dateutil.parser.parse(time_str)
  return time_datetime.timestamp()


######################################################
# CONFIGURATION
######################################################

data_dir_root = 'C:/Users/jdelp/Desktop/_whale_birthday_s3_data'

composite_layout = OrderedDict([ # each value is (row, column, rowspan, colspan)
  ('Mavic (CETI)'         , (0, 0, 2, 2)),
  ('Mavic (DSWP)'         , (0, 2, 2, 2)),
  ('Canon (DelPreto)'     , (2, 1, 1, 1)),
  ('Canon (Gruber)'       , (2, 0, 1, 1)),
  ('Phone (DelPreto)'     , (2, 1, 1, 1)),
  ('GoPro (DelPreto)'     , (2, 1, 1, 1)),
  ('Phone (Aluma)'        , (2, 3, 1, 1)),
  ('Canon (DSWP)'         , (2, 2, 1, 1)),
  ('Phone (Baumgartner)'  , (3, 0, 1, 1)),
  ('Phone (Pagani)'       , (3, 1, 1, 1)),
  ('Phone (SalinoHugg)'   , (3, 2, 1, 1)),
  ('Hydrophone (Mevorach)', (4, 0, 1, 4)),
  ])

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
}
epoch_offsets_toAdd_s = {
  'CETI-DJI_MAVIC3-1'          : 0,
  'DSWP-DJI_MAVIC3-2'          : 1.5, # 1.5 is estimated from images of the open mouth and baby flop near the boat (compared to the phones as ground truth)
  'DG-CANON_EOS_1DX_MARK_III-1': 4*3600 + 189 + 15, # 189+15 is estimated from images of the open mouth and baby flop near the boat (compared to the phones as ground truth)
  'JD-CANON_REBEL_T5I'         : 14, # 14 is estimated from images of the open mouth and baby flop near the boat (compared to the phones as ground truth)
  'DSWP-CANON_EOS_70D-1'       : 4*3600,
  'DSWP-KASHMIR_MIXPRE6-1'     : 0,
  'Misc/Aluma'                 : 0,
  'Misc/Baumgartner'           : 0,
  'Misc/Pagani'                : 0,
  'Misc/SalinoHugg'            : 0,
  'Misc/DelPreto_Pixel5'       : 0,
  'Misc/DelPreto_GoPro'        : 0,
}

# output_video_start_time_str = '2023-07-08 10:20:12 -0400' # start of ceti mavic
# output_video_start_time_str = '2023-07-08 11:40:12 -0400' # start of main event (ish)
output_video_start_time_str = '2023-07-08 11:35:00 -0400'
# output_video_start_time_str = '2023-07-08 11:50:45 -0400'
# output_video_start_time_str = '2023-07-08 11:53:45 -0400'
# output_video_start_time_str = '2023-07-08 10:51:34 -0400'
# output_video_start_time_str = '2023-07-08 10:53:40 -0400'
output_video_duration_s = 3000
output_video_fps = 10

composite_layout_column_width = 300
composite_layout_row_height = round(composite_layout_column_width/(1+7/9)) # Drone videos have an aspect ratio of 1.7777

output_video_banner_height_fraction = 0.03
output_video_banner_bg_color = [100, 100, 100] # BGR
output_video_banner_text_color = [255, 255, 0] # BGR
output_video_banner_fontScale = None # will be determined later
output_video_banner_textSize = None # will be determined later

audio_resample_rate_hz = 9600 # original rate is 96000
audio_plot_duration_beforeCurrentTime_s = 5
audio_plot_duration_afterCurrentTime_s = 10
audio_plot_length_beforeCurrentTime = int(audio_resample_rate_hz * audio_plot_duration_beforeCurrentTime_s)
audio_plot_length_afterCurrentTime = int(audio_resample_rate_hz * audio_plot_duration_afterCurrentTime_s)
audio_plot_length = 1 + audio_plot_length_beforeCurrentTime + audio_plot_length_afterCurrentTime
audio_timestamps_toPlot_s = np.arange(start=0, stop=audio_plot_length)/audio_resample_rate_hz - audio_plot_duration_beforeCurrentTime_s
output_video_filepath = os.path.join(data_dir_root, 'composite_video_fps%d_duration%d_start%d_colWidth%d.mp4'
                                     % (output_video_fps, output_video_duration_s, 1000*time_str_to_time_s(output_video_start_time_str), composite_layout_column_width))

timestamp_to_target_thresholds_s = { # each entry is allowed time (before_current, after_current)
  'video': (1/output_video_fps*0.5, 1/output_video_fps*0.5),
  'audio': (1/output_video_fps*0.5, 1/output_video_fps*0.5),
  'image': (1, 1/output_video_fps),
}


######################################################
# HELPERS
######################################################

def get_extension(filepath):
  file_extension = os.path.splitext(filepath)[-1]
  file_extension = file_extension.lower()
  return file_extension

def is_video(filepath_or_data):
  if filepath_or_data is None:
    return False
  if isinstance(filepath_or_data, cv2.VideoCapture):
    return True
  return get_extension(filepath_or_data) in ['.mp4', '.mov', '.avi', '.lrv', '.lrf']

def is_image(filepath_or_data):
  if filepath_or_data is None:
    return False
  if isinstance(filepath_or_data, np.ndarray):
    return filepath_or_data.ndim == 3
  return get_extension(filepath_or_data) in ['.jpg', '.jpeg', '.png', '.bmp', '.tiff']

def is_audio(filepath_or_data):
  if filepath_or_data is None:
    return False
  if isinstance(filepath_or_data, np.ndarray):
    return filepath_or_data.ndim == 2
  return get_extension(filepath_or_data) in ['.wav']

def device_friendlyName_to_id(device_friendlyName_toFind):
  for (device_id, device_friendlyName) in device_friendlyNames.items():
    if device_friendlyName == device_friendlyName_toFind:
      return device_id


  
def get_index_for_time_s(timestamps_s, target_time_s, timestamp_to_target_thresholds_s):
  # print('======= get_index_for_time_s', target_time_s, time_s_to_str(target_time_s))
  # print('%f %f' % (timestamps_s[0], timestamps_s[1]))
  # print(timestamps_s.dtype)
  # print('  ', time_s_to_str(timestamps_s[0]), time_s_to_str(timestamps_s[1]))
  if timestamps_s.shape[0] == 1:
    best_index = 0
  else:
    next_index_pastTarget = timestamps_s.searchsorted(target_time_s)
    # print('  ', 'next_index_pastTarget', next_index_pastTarget)
    if next_index_pastTarget == timestamps_s.shape[0]:
      next_index_pastTarget -= 1
    index_candidates = np.array([next_index_pastTarget-1, next_index_pastTarget])
    dt_candidates = abs(timestamps_s[index_candidates] - target_time_s)
    # print('  ', 'dt_candidates', dt_candidates)
    if dt_candidates[0] < dt_candidates[1]:
      best_index = index_candidates[0]
    else:
      best_index = index_candidates[1]
    # print('  ', 'best_index', best_index)
  # Check if it is within the threshold region of the target time.
  if timestamps_s[best_index] < (target_time_s - timestamp_to_target_thresholds_s[0]):
    return None
  if timestamps_s[best_index] > (target_time_s + timestamp_to_target_thresholds_s[1]):
    return None
  # Return the best index.
  return best_index
  
  # # First approach used numpy.where, but this was slow on the large audio arrays.
  # dt = abs(timestamps_s - target_time_s)
  # best_dt = min(dt)
  # if best_dt > timestamp_to_target_threshold_s:
  #   return None
  # return np.where(dt > best_dt)[0][0]

def cv2_to_pixmap(cv_image):
  height, width, channel = cv_image.shape
  bytes_per_line = 3 * width
  q_image = QImage(cv_image.data, width, height, bytes_per_line, QImage.Format.Format_RGB888)
  return QPixmap.fromImage(q_image)

def convertQImageToMat(qimg):
  img = qimg.convertToFormat(QtGui.QImage.Format.Format_RGB32)
  ptr = img.bits()
  ptr.setsize(img.sizeInBytes())
  arr = np.array(ptr).reshape(img.height(), img.width(), 4)  #  Copies the data
  return arr

def scale_image(img, target_width, target_height):
  if isinstance(img, np.ndarray):
    img_width = img.shape[1]
    img_height = img.shape[0]
    scale_factor_byWidth = target_width/img_width
    scale_factor_byHeight = target_height/img_height
    scale_factor = min(scale_factor_byWidth, scale_factor_byHeight)
    return cv2.resize(src=img, dsize=(0,0), fx=scale_factor, fy=scale_factor)
  if isinstance(img, QPixmap):
    return img.scaled(target_width, target_height,
                      aspectRatioMode=pyqtgraph.QtCore.Qt.AspectRatioMode.KeepAspectRatio)

def draw_text_on_image(img, text, pos=(0, 0),
                       font_scale=8, font_thickness=1, font=cv2.FONT_HERSHEY_PLAIN,
                       text_color=(255, 255, 255), text_bg_color=(100, 100, 100)
                      ):
  if font_scale < 1:
    target_text_w = font_scale * img.shape[1]
    font_scale = 0
    text_w = 0
    while text_w < target_text_w:
      font_scale += 1
      (text_w, text_h), _ = cv2.getTextSize(text, font, font_scale, font_thickness)
  pos = list(pos)
  x, y = pos
  (text_w, text_h), _ = cv2.getTextSize(text, font, font_scale, font_thickness)
  if y == -1:
    y = img.shape[0]-round(1.25*text_h)
  if x == -1:
    x = img.shape[1]-text_w
  pos = [x, y]
  cv2.rectangle(img, pos, (x + text_w, y + text_h), text_bg_color, -1)
  cv2.putText(img, text, (x, y + text_h + font_scale - 1), font, font_scale, text_color, font_thickness)
  
def add_timestamp_banner(img, timestamp_s):
  global output_video_banner_height_fraction, output_video_banner_bg_color, output_video_banner_fontScale, output_video_banner_textSize
  output_video_banner_height = int(output_video_banner_height_fraction*img.shape[0])
  img = cv2.copyMakeBorder(img, 0, output_video_banner_height, 0, 0,
                           cv2.BORDER_CONSTANT, value=output_video_banner_bg_color)
  timestamp_str = '%s (%0.3f)' % (time_s_to_str(timestamp_s), timestamp_s)
  
  fontFace = cv2.FONT_HERSHEY_SIMPLEX
  fontThickness = 2 if output_video_banner_height > 25 else 1
  if output_video_banner_fontScale is None:
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
    output_video_banner_textSize = cv2.getTextSize(timestamp_str, fontFace, output_video_banner_fontScale, fontThickness)[0]
  
  img = cv2.putText(img, timestamp_str,
                    [int(img.shape[1]/2 - output_video_banner_textSize[0]/2),
                     int(img.shape[0] - output_video_banner_height/2 + output_video_banner_textSize[1]/3)],
                    fontFace=fontFace, fontScale=output_video_banner_fontScale,
                    color=output_video_banner_text_color, thickness=fontThickness)
  return img


  
######################################################
# LOADING / TIMESTAMPING
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

print()
print('Extracting timestamps for every frame/photo')
media_infos = {}
for (device_id, device_friendlyName) in device_friendlyNames.items():
  media_infos[device_id] = {}
  if 'Misc' in device_id:
    data_dir = os.path.join(data_dir_root, 'Misc')
    filename_keyword = device_id.split('/')[1]
    filepaths = glob.glob(os.path.join(data_dir, '*%s*' % filename_keyword))
  else:
    data_dir = os.path.join(data_dir_root, device_id)
    filepaths = glob.glob(os.path.join(data_dir, '*'))
  print(' See %4d files for device [%s]' % (len(filepaths), device_friendlyName))
  for filepath in filepaths:
    if os.path.isdir(filepath):
      continue
    # Get the start time in epoch time
    filename = os.path.basename(filepath)
    start_time_ms = int(re.search('\d{13}', filename)[0])
    start_time_s = start_time_ms/1000.0
    start_time_s += epoch_offsets_toAdd_s[device_id]
    if is_video(filepath):
      video_reader = cv2.VideoCapture(filepath)
      frame_duration_s = 1/video_reader.get(cv2.CAP_PROP_FPS)
      num_frames = int(video_reader.get(cv2.CAP_PROP_FRAME_COUNT))
      timestamps_s = start_time_s + np.arange(start=0, stop=num_frames)*frame_duration_s
      media_infos[device_id][filepath] = (timestamps_s, video_reader)
    elif is_image(filepath):
      timestamps_s = np.array([start_time_s])
      media_infos[device_id][filepath] = (timestamps_s, filepath)
    elif is_audio(filepath):
      (audio_rate, audio_data) = wavfile.read(filepath)
      # Resample the data.
      num_samples = audio_data.shape[0]
      timestamps_s = start_time_s + np.arange(start=0, stop=num_samples)/audio_rate
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
      media_infos[device_id][filepath] = (timestamps_s_resampled, audio_data_resampled)
      # media_infos[device_id][filepath] = (timestamps_s, np.random.rand(timestamps_s.shape[0], 2))



######################################################
# CREATE A VIDEO
######################################################

# Convert the starting time to epoch time.
output_video_start_time_s = time_str_to_time_s(output_video_start_time_str)
# output_video_start_time_datetime = dateutil.parser.parse(output_video_start_time_str)
# output_video_start_time_s = output_video_start_time_datetime.timestamp()

# Generate timestamps for the output video frames.
output_video_num_frames = output_video_duration_s * output_video_fps
output_video_frame_duration_s = 1/output_video_fps
output_video_timestamps_s = output_video_start_time_s \
                            + np.arange(start=0, stop=output_video_num_frames)*output_video_frame_duration_s

# Create the plotting layout.
# The top level will be a GraphicsLayout, since that seems easier to export to an image.
# Then the main level will be a GridLayout to flexibly arrange the visualized data streams.

def update_layout_widget(layout_widget, layout_specs, data, label=None):
  if is_image(data):
    data = scale_image(data, target_width=composite_layout_column_width*layout_specs[3], # column width times colspan
                             target_height=composite_layout_row_height*layout_specs[2])  # row height times rowspan
    if label is not None:
      draw_text_on_image(data, label, pos=(0,-1), font_scale=1)
    pixmap = cv2_to_pixmap(data)
    # pixmap = scale_image(pixmap, target_width=composite_layout_column_width*layout_specs[3], # column width times colspan
    #                              target_height=composite_layout_row_height*layout_specs[2])  # row height times rowspan
    layout_widget.setPixmap(pixmap)
  elif is_audio(data):
    layout_widget[0].setData(audio_timestamps_toPlot_s, data[:,0])
    layout_widget[1].setData(audio_timestamps_toPlot_s, data[:,1])
    if np.amax(data) < 50:
      layout_widget[2].setData([0, 0], np.amax(data)*np.array([-50, 50]))
      audio_plotWidget.setYRange(-50, 50)
    else:
      layout_widget[2].setData([0, 0], np.amax(data)*np.array([-1, 1]))
      audio_plotWidget.enableAutoRange(enable=0.9)
    
# pyqtgraph.setConfigOption('background', 'w')
# pyqtgraph.setConfigOption('foreground', 'k')

layout_widgets = {} # use layout specs as the key, so if multiple devices are in the same subplot we can know that we alreayd initialized a widget for that location
dummy_datas = {}
app = QtWidgets.QApplication([])
graphics_layout = pyqtgraph.GraphicsLayoutWidget()
grid_layout = QtWidgets.QGridLayout()
graphics_layout.setLayout(grid_layout)
# Initialize the visualizations for each stream.
for (device_friendlyName, layout_specs) in composite_layout.items():
  device_id = device_friendlyName_to_id(device_friendlyName)
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
      success, example_image = example_data.read()
    elif is_image(example_filepath):
      example_image = cv2.imread(example_filepath)
    else:
      raise AssertionError('Thought it was a video or image, but apparently not')
    blank_image = 100*np.ones_like(example_image) # scale it so it will be gray
    image_labelWidget = QtWidgets.QLabel()
    grid_layout.addWidget(image_labelWidget, *layout_specs, alignment=pyqtgraph.QtCore.Qt.AlignmentFlag.AlignCenter)
    grid_layout.setRowMinimumHeight(layout_specs[0], composite_layout_row_height)
    update_layout_widget(image_labelWidget, layout_specs, blank_image)
    layout_widgets[str(layout_specs)] = image_labelWidget
    dummy_datas[str(layout_specs)] = 0*blank_image
  elif is_audio(example_filepath):
    audio_plotWidget = pyqtgraph.PlotWidget()
    grid_layout.addWidget(audio_plotWidget, *layout_specs, alignment=pyqtgraph.QtCore.Qt.AlignmentFlag.AlignCenter)
    grid_layout.setRowMinimumHeight(layout_specs[0], composite_layout_row_height)
    random_audio = np.random.rand(audio_plot_length, 2)
    audio_plotWidget.setMinimumWidth(composite_layout_column_width*layout_specs[3])
    h_lines = []
    h_lines.append(audio_plotWidget.plot(audio_timestamps_toPlot_s, random_audio[:,0], pen=pyqtgraph.mkPen([255, 255, 255], width=5)))
    h_lines.append(audio_plotWidget.plot(audio_timestamps_toPlot_s, random_audio[:,1], pen=pyqtgraph.mkPen([255, 0, 255], width=2)))
    h_lines.append(audio_plotWidget.plot([0, 0], [-500, 500], pen=pyqtgraph.mkPen([0, 150, 150], width=7)))
    # audio_plotWidget.setYRange(-2000, 2000)
    # update_layout_widget(audio_plotWidget, layout_specs, random_audio)
    layout_widgets[str(layout_specs)] = h_lines
    dummy_datas[str(layout_specs)] = random_audio
QtCore.QCoreApplication.processEvents()
graphics_layout.setWindowTitle('Happy Birthday!')
graphics_layout.show()
# app.exec()

# Generate a frame for every desired timestamp.
print()
print('Generating output video with %d frames' % output_video_timestamps_s.shape[0])
composite_video_writer = None
last_status_time_s = 0
duration_s_pyqt = 0
duration_s_getIndex = 0
duration_s_readImages = 0
readImages_count = 0
duration_s_readVideos = 0
layouts_updated = {}
layouts_showing_dummyData = dict([(str(layout_specs), False) for layout_specs in composite_layout.values()])
start_loop_time_s = time.time()
for (frame_index, current_time_s) in enumerate(output_video_timestamps_s):
  if time.time() - last_status_time_s > 5:
    print(' Processing frame %6d/%6d (%0.2f%%) for time %10d (%s)' %
          (frame_index+1, output_video_num_frames, 100*(frame_index+1)/output_video_num_frames,
           current_time_s, time_s_to_str(current_time_s)))
    last_status_time_s = time.time()
  
  # # Clear all subplots by showing dummy data.
  # t0 = time.time()
  # for (device_friendlyName, layout_specs) in composite_layout.items():
  #   device_id = device_friendlyName_to_id(device_friendlyName)
  #   update_layout_widget(layout_widgets[str(layout_specs)], layout_specs, dummy_datas[str(layout_specs)])
  # duration_s_pyqt += time.time() - t0
  # Mark that no layouts have been updated.
  for (device_friendlyName, layout_specs) in composite_layout.items():
    layouts_updated[str(layout_specs)] = False
  
  # Loop through each specified stream.
  # Note that multiple devices may be mapped to the same layout position;
  #  in that case the last device with data for this timestep will be used.
  for (device_friendlyName, layout_specs) in composite_layout.items():
    device_id = device_friendlyName_to_id(device_friendlyName)
    media_file_infos = media_infos[device_id]
    # For each media file associated with this device, see if it has data for this timestep.
    # Note that there may be multiple images that match this timestamp, but only the first will be used.
    for (filepath, (timestamps_s, data)) in media_file_infos.items():
      # print(device_id, os.path.basename(filepath), timestamps_s.shape, timestamps_s[0], timestamps_s[-1])
      if is_video(filepath):
        t0 = time.time()
        data_index = get_index_for_time_s(timestamps_s, current_time_s, timestamp_to_target_thresholds_s['video'])
        duration_s_getIndex += time.time() - t0
        if data_index is not None:
          # print('DATA INDEX', os.path.basename(filepath), data_index)
          t0 = time.time()
          data.set(cv2.CAP_PROP_POS_FRAMES, data_index) # should this be data_index-1? A bit unclear from documentation/examples
          success, img = data.read()
          if success:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            duration_s_readVideos += time.time() - t0
            # Update the subplot with the video frame.
            t0 = time.time()
            update_layout_widget(layout_widgets[str(layout_specs)], layout_specs, img, label=device_friendlyName)
            layouts_updated[str(layout_specs)] = True
            layouts_showing_dummyData[str(layout_specs)] = False
            duration_s_pyqt += time.time() - t0
            break # don't check any more media for this device
          
      elif is_image(filepath):
        t0 = time.time()
        data_index = get_index_for_time_s(timestamps_s, current_time_s, timestamp_to_target_thresholds_s['image'])
        duration_s_getIndex += time.time() - t0
        if data_index is not None:
          # print('FOUND DATA INDEX', device_id, os.path.basename(filepath), data_index)
          t0 = time.time()
          img = cv2.imread(filepath)
          img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
          duration_s_readImages += time.time() - t0
          readImages_count += 1
          # Update the subplot with the video image.
          t0 = time.time()
          update_layout_widget(layout_widgets[str(layout_specs)], layout_specs, img, label=device_friendlyName)
          layouts_updated[str(layout_specs)] = True
          layouts_showing_dummyData[str(layout_specs)] = False
          duration_s_pyqt += time.time() - t0
          break # don't check any more media for this device
          
      elif is_audio(filepath):
        t0 = time.time()
        data_index = get_index_for_time_s(timestamps_s, current_time_s, timestamp_to_target_thresholds_s['audio'])
        duration_s_getIndex += time.time() - t0
        if data_index is not None:
          # print('FOUND DATA INDEX', os.path.basename(filepath), data_index)
          # Get the audio rate and number of channels.
          audio_sps = round((timestamps_s.shape[0]-1)/(timestamps_s[-1] - timestamps_s[0])) # NOTE: using first/last indexes is much faster than using max/min
          audio_num_channels = data.shape[1]
          # # Get the start/end times of the plot.
          # start_time_s = current_time_s - audio_plot_duration_beforeCurrentTime_s
          # end_time_s = current_time_s + audio_plot_duration_afterCurrentTime_s
          # num_samples = (end_time_s - start_time_s)*audio_sps
          # timestamps_s_toPlot = np.arange(start=0, stop=num_samples)/audio_sps
          # Get the start/end indexes of the data to plot.
          # Note that these may be negative or beyond the bounds of the data.
          start_index = data_index - audio_plot_length_beforeCurrentTime
          end_index = data_index + audio_plot_length_afterCurrentTime + 1
          num_toPad_pre = 0 if start_index >= 0 else -start_index
          start_index = max(0, start_index)
          num_toPad_post = 0 if end_index <= data.shape[0] else end_index - data.shape[0]
          end_index = min(data.shape[0], end_index)
          # Get the data and pad it as needed.
          data_toPlot = data[start_index:end_index]
          data_toPlot = np.vstack([0*np.ones((num_toPad_pre, audio_num_channels)),
                                   data_toPlot,
                                   0*np.ones((num_toPad_post, audio_num_channels))])
          # Update the subplot with the waveform segment.
          t0 = time.time()
          update_layout_widget(layout_widgets[str(layout_specs)], layout_specs, data_toPlot)
          layouts_updated[str(layout_specs)] = True
          layouts_showing_dummyData[str(layout_specs)] = False
          duration_s_pyqt += time.time() - t0
          break # don't check any more media for this device
  
  # If a layout was not updated, show its dummy data.
  for (device_friendlyName, layout_specs) in composite_layout.items():
    if not layouts_updated[str(layout_specs)] and not layouts_showing_dummyData[str(layout_specs)]:
      t0 = time.time()
      device_id = device_friendlyName_to_id(device_friendlyName)
      update_layout_widget(layout_widgets[str(layout_specs)], layout_specs, dummy_datas[str(layout_specs)])
      layouts_showing_dummyData[str(layout_specs)] = True
      duration_s_pyqt += time.time() - t0
  
  # Refresh the figure with the updated subplots.
  t0 = time.time()
  QtCore.QCoreApplication.processEvents()
  duration_s_pyqt += time.time() - t0
  
  # Save the image to a composite frame.
  img = graphics_layout.grab().toImage()
  img = convertQImageToMat(img)
  img = np.array(img[:,:,0:3])
  img = add_timestamp_banner(img, current_time_s)
  if output_video_filepath is not None:
    # Create the video writer if this is the first frame, since we now know the frame dimensions.
    if composite_video_writer is None:
      composite_video_writer = cv2.VideoWriter(output_video_filepath,
                                               cv2.VideoWriter_fourcc(*'MJPG') if '.avi' in output_video_filepath.lower() else cv2.VideoWriter_fourcc(*'MP4V'),
                                               output_video_fps, [img.shape[1], img.shape[0]])
    composite_video_writer.write(img)

composite_video_writer.release()
total_duration_s = time.time() - start_loop_time_s
print('total_duration_s',total_duration_s)
print('duration_s_pyqt',duration_s_pyqt)
print('duration_s_getIndex',duration_s_getIndex)
print('duration_s_readImages',duration_s_readImages)
print('duration_s_readVideos',duration_s_readVideos)
print('pyqt percent:', 100*duration_s_pyqt/total_duration_s)
print('getIndex percent:', 100*duration_s_getIndex/total_duration_s)
print('readImages percent:', 100*duration_s_readImages/total_duration_s)
print('readVideos percent:', 100*duration_s_readVideos/total_duration_s)
print('readImages count:', readImages_count)

app.exec()


# Release video readers.
for (device_id, media_file_infos) in media_infos.items():
  for (filepath, (timestamps_s, data)) in media_file_infos.items():
    if isinstance(data, cv2.VideoCapture):
      data.release()









