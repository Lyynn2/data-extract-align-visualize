
import cv2
import decord
from PIL import Image
import ffmpeg
import pysrt
import csv
from operator import itemgetter

import dateutil.parser
from datetime import datetime
import re
import os
import glob
import numpy as np

import pyqtgraph
from pyqtgraph.Qt.QtGui import QPixmap, QImage
from pyqtgraph.Qt import QtCore, QtGui, QtWidgets

############################################
# TIME
############################################

def time_s_to_str(time_s, timezone_offset_s=0, timezone_offset_str=''):
  # Get "UTC" time, which is actually local time because we will do the timezone offset first.
  time_datetime = datetime.utcfromtimestamp(time_s + timezone_offset_s)
  return time_datetime.strftime('%%Y-%%m-%%d %%H:%%M:%%S.%%f %s' % timezone_offset_str)

def time_str_to_time_s(time_str):
  time_datetime = dateutil.parser.parse(time_str)
  return time_datetime.timestamp()

############################################
# FILES AND TYPES
############################################

def get_file_extension(filepath):
  if not isinstance(filepath, str):
    return None
  file_extension = os.path.splitext(filepath)[-1]
  file_extension = file_extension.lower()
  return file_extension

def is_video(filepath_or_data):
  if filepath_or_data is None:
    return False
  if isinstance(filepath_or_data, cv2.VideoCapture):
    return True
  return get_file_extension(filepath_or_data) in ['.mp4', '.mov', '.avi', '.lrv', '.lrf'] or False

def is_image(filepath_or_data):
  if filepath_or_data is None:
    return False
  if isinstance(filepath_or_data, np.ndarray):
    return filepath_or_data.ndim == 3
  return get_file_extension(filepath_or_data) in ['.jpg', '.jpeg', '.png', '.bmp', '.tiff'] or False

def is_audio(filepath_or_data):
  if filepath_or_data is None:
    return False
  if isinstance(filepath_or_data, np.ndarray):
    return filepath_or_data.ndim == 2
  return get_file_extension(filepath_or_data) in ['.wav'] or False

def is_drone_data(filepath_or_data):
  if filepath_or_data is None:
    return False
  if isinstance(filepath_or_data, dict) and 'altitude_relative_m' in filepath_or_data:
    return True
  return get_file_extension(filepath_or_data) in ['.srt'] or False

def is_coda_annotations(filepath_or_data):
  if filepath_or_data is None:
    return False
  if isinstance(filepath_or_data, dict) and 'coda_start_times_s' in filepath_or_data:
    return True
  return get_file_extension(filepath_or_data) in ['.csv'] or False
  
############################################
# IMAGES / VIDEOS
############################################

# Load an image from file
def load_image(filepath, target_width=None, target_height=None, method='pil'):
  img = None
  if method.lower() == 'opencv':
    img = cv2.imread(filepath)
    if target_width is not None and target_height is not None:
      img = scale_image(img, target_width=target_width, target_height=target_height)
  elif method.lower() == 'pil':
    img = Image.open(filepath)
    if target_width is not None and target_height is not None:
      img.draft('RGB', (int(target_width*1.5), int(target_height*1.5)))
    img = np.asarray(img)
    if target_width is not None and target_height is not None:
      img = scale_image(img, target_width=target_width, target_height=target_height)
  return img

# Open a video file.
# target_width is only used for the 'decord' method
def get_video_reader(filepath, target_width=None, method='decord'):
  video_reader = None
  frame_rate = None
  num_frames = None
  if method.lower() == 'opencv':
    video_reader = cv2.VideoCapture(filepath)
    frame_rate = video_reader.get(cv2.CAP_PROP_FPS)
    num_frames = int(video_reader.get(cv2.CAP_PROP_FRAME_COUNT))
  elif method.lower() == 'decord':
    video_reader = decord.VideoReader(filepath)
    if target_width is not None:
      frame_shape = video_reader[0].asnumpy().shape
      target_height = int(frame_shape[0]/frame_shape[1]*target_width)
      video_reader = decord.VideoReader(filepath, width=target_width, height=target_height)
    frame_rate = video_reader.get_avg_fps()
    num_frames = len(video_reader)
  return (video_reader, frame_rate, num_frames)
  
# Load a specified frame from a video reader
def load_frame(video_reader, frame_index, target_width=None, target_height=None, method='decord'):
  success = False
  img = None
  if method.lower() == 'opencv':
    video_reader.set(cv2.CAP_PROP_POS_FRAMES, frame_index)
    success, img = video_reader.read()
    if success and (target_width is not None and target_height is not None):
      img = scale_image(img, target_width=target_width, target_height=target_height)
  elif method.lower() == 'decord':
    try:
      img = video_reader[frame_index].asnumpy()
      success = (img is not None)
    except:
      img = None
      success = False
    if success and (target_width is not None and target_height is not None):
      img = scale_image(img, target_width=target_width, target_height=target_height)
  return (success, img)
  
# Convert an OpenCV image to a PyQtGraph Pixmap.
def cv2_to_pixmap(cv_image):
  height, width, channel = cv_image.shape
  bytes_per_line = 3 * width
  q_image = QImage(cv_image.data, width, height, bytes_per_line, QImage.Format.Format_RGB888)
  return QPixmap.fromImage(q_image)

# Convert a PyQtGraph QImage to a numpy array.
def qimage_to_numpy(qimg):
  img = qimg.convertToFormat(QtGui.QImage.Format.Format_RGB32)
  ptr = img.bits()
  ptr.setsize(img.sizeInBytes())
  arr = np.array(ptr).reshape(img.height(), img.width(), 4)  #  Copies the data
  return arr

# Scale an image to fit within a target width and height.
# Will maintain the aspect ratio of the input image.
# The input can be a PyQtGraph QPixmap or a numpy array.
def scale_image(img, target_width, target_height):
  if isinstance(img, np.ndarray):
    img_width = img.shape[1]
    img_height = img.shape[0]
    if img_width == target_width and img_height == target_height:
      return img
    scale_factor_byWidth = target_width/img_width
    scale_factor_byHeight = target_height/img_height
    scale_factor = min(scale_factor_byWidth, scale_factor_byHeight)
    return cv2.resize(src=img, dsize=(0,0), fx=scale_factor, fy=scale_factor)
  if isinstance(img, QPixmap):
    return img.scaled(target_width, target_height,
                      aspectRatioMode=pyqtgraph.QtCore.Qt.AspectRatioMode.KeepAspectRatio)

# Draw text on an image, with a shaded background.
# If the y position is -1, will place the text at the bottom of the image.
# If the x position is -1, will place the text at the left of the image.
# If x or y is between 0 and 1, will place at that ratio of the width or height.
def draw_text_on_image(img, text, pos=(0, 0),
                       font_scale=8, text_width_ratio=None,
                       font_thickness=1, font=cv2.FONT_HERSHEY_DUPLEX,
                       text_color=None, text_bg_color=None, text_bg_outline_color=None,
                       preview_only=False,
                       ):
  # If desired, compute a font scale based on the target width ratio.
  if text_width_ratio is not None:
    target_text_w = text_width_ratio * img.shape[1]
    font_scale = 0
    text_w = 0
    while text_w < target_text_w:
      font_scale += 0.2
      (text_w, text_h), _ = cv2.getTextSize(text, font, font_scale, font_thickness)
    font_scale -= 0.2
  # Compute the text dimensions.
  (text_w, text_h), _ = cv2.getTextSize(text, font, font_scale, font_thickness)
  # Compute padding.
  text_bg_pad = round(text_w*0.03)
  text_bg_outline_width = round(text_w*0.02) if text_bg_outline_color is not None else 0
  # Place the text at the bottom and/or left if desired, and handle fractional placement if desired.
  pos = list(pos)
  x, y = pos
  if y == -1:
    y = round(img.shape[0] - text_h - text_bg_pad*2 - text_bg_outline_width*2)
  elif y > 0 and y < 1:
    y = round(img.shape[0]*y - text_h/2 - text_bg_pad - text_bg_outline_width)
  if x == -1:
    x = round(img.shape[1] - text_w - text_bg_pad*2 - text_bg_outline_width*2)
  elif x > 0 and x < 1:
    x = round(img.shape[1]*x - text_w/2 - text_bg_pad - text_bg_outline_width)
  if not preview_only:
    # Draw a border around the background if desired.
    if text_bg_outline_color is not None:
      cv2.rectangle(img, (x,y), (x + text_w + 2*text_bg_outline_width + 2*text_bg_pad,
                                 y + text_h + 2*text_bg_outline_width + 2*text_bg_pad),
                    text_bg_outline_color, -1)
      x += text_bg_outline_width
      y += text_bg_outline_width
    
    # Draw the background shading.
    text_bg_color = text_bg_color or (100, 100, 100)
    cv2.rectangle(img, (x,y), (x + text_w + 2*text_bg_pad, y + text_h + 2*text_bg_pad),
                  text_bg_color, -1)
    x += text_bg_pad
    y += text_bg_pad
    
    # Draw the text.
    text_color = text_color or (255, 255, 255)
    cv2.putText(img, text, (x, int(y + text_h + font_scale - 1)),
                font, font_scale, text_color, font_thickness)
  
  return (text_w, text_h)

# Compress a video to the target bitrate.
# The target bitrate in bits per second will include both video and audio.
def compress_video(input_filepath, output_filepath, target_total_bitrate_b_s):
  # Reference: https://en.wikipedia.org/wiki/Bit_rate#Encoding_bit_rate
  min_audio_bitrate = 32000
  max_audio_bitrate = 256000
  
  # Open a probe to the input video.
  probe = ffmpeg.probe(input_filepath)
  
  # Check if ausio will be included.
  audio_streams = [s for s in probe['streams'] if s['codec_type'] == 'audio']
  if len(audio_streams) > 0:
    audio_bitrate = sum(float(audio_stream['bit_rate']) for audio_stream in audio_streams)
    
    if 10 * audio_bitrate > target_total_bitrate_b_s:
      audio_bitrate = target_total_bitrate_b_s / 10
    if audio_bitrate < min_audio_bitrate < target_total_bitrate_b_s:
      audio_bitrate = min_audio_bitrate
    elif audio_bitrate > max_audio_bitrate:
      audio_bitrate = max_audio_bitrate
    
    video_bitrate = target_total_bitrate_b_s - audio_bitrate
  else:
    audio_bitrate = None
    video_bitrate = target_total_bitrate_b_s
  
  # Compress!
  i = ffmpeg.input(input_filepath)
  # Pass 1
  ffmpeg_args = {
    'c:v': 'libx264',
    'b:v': video_bitrate,
    'pass': 1,
    'f': 'mp4',
    'loglevel':'error',
    'log': False,
  }
  ffmpeg.output(i, os.devnull,
                **ffmpeg_args
                ).overwrite_output().run()
  # Pass 2
  ffmpeg_args = {
    'c:v': 'libx264',
    'b:v': video_bitrate,
    'pass': 2,
    'c:a': 'aac',
    'loglevel': 'error',
    'log': False,
  }
  if len(audio_streams) > 0:
    ffmpeg_args['b:a'] = audio_bitrate
  ffmpeg.output(i, output_filepath,
                **ffmpeg_args
                ).overwrite_output().run()

############################################
# DRONE DATA
############################################

def get_drone_data(video_filepath, timezone_offset_str=''):
  srt_filepath = '%s.srt' % (os.path.splitext(video_filepath)[0])
  if not os.path.exists(srt_filepath):
    return None
  srt = pysrt.open(srt_filepath)
  num_frames = len(srt)
  drone_data = {
    'timestamp_str': ['']*num_frames,
    'timestamp_s': np.nan*np.ones(shape=(num_frames,)),
    'iso': np.nan*np.ones(shape=(num_frames,)),
    'shutter': np.nan*np.ones(shape=(num_frames, 2)),
    'f_number': np.nan*np.ones(shape=(num_frames,)),
    'exposure_value': np.nan*np.ones(shape=(num_frames,)),
    'color_temperature': np.nan*np.ones(shape=(num_frames,)),
    'focal_length': np.nan*np.ones(shape=(num_frames,)),
    'color_mode': ['']*num_frames,
    'latitude': np.nan*np.ones(shape=(num_frames,)),
    'longitude': np.nan*np.ones(shape=(num_frames,)),
    'altitude_relative_m': np.nan*np.ones(shape=(num_frames,)),
    'altitude_absolute_m': np.nan*np.ones(shape=(num_frames,)),
  }
  
  for (frame_index, srt_frame) in enumerate(srt):
    text_lines = srt_frame.text_without_tags.split('\n')
    drone_data['timestamp_str'][frame_index] = text_lines[1]
    drone_data['timestamp_s'][frame_index] = time_str_to_time_s(text_lines[1])
    data_line = text_lines[2]
    data_line = data_line.replace(' ', '')
    drone_data['iso'][frame_index] = float(data_line.split('[iso:')[1].split(']')[0].strip())
    drone_data['shutter'][frame_index] = [float(x.strip()) for x in data_line.split('[shutter:')[1].split(']')[0].split('/')]
    drone_data['f_number'][frame_index] = float(data_line.split('[fnum:')[1].split(']')[0].strip())
    drone_data['exposure_value'][frame_index] = float(data_line.split('[ev:')[1].split(']')[0].strip())
    drone_data['color_temperature'][frame_index] = float(data_line.split('[ct:')[1].split(']')[0].strip())
    drone_data['focal_length'][frame_index] = float(data_line.split('[focal_len:')[1].split(']')[0].strip())
    drone_data['color_mode'][frame_index] = data_line.split('[color_md:')[1].split(']')[0].strip()
    drone_data['latitude'][frame_index] = float(data_line.split('[latitude:')[1].split(']')[0].strip())
    drone_data['longitude'][frame_index] = float(data_line.split('[longitude:')[1].split(']')[0].strip())
    drone_data['altitude_relative_m'][frame_index] = float(data_line.split('[rel_alt:')[1].split('abs_alt')[0].strip())
    drone_data['altitude_absolute_m'][frame_index] = float(data_line.split('abs_alt:')[1].split(']')[0].strip())
  
  return drone_data

############################################
# CODA ANNOTATIONS
############################################

def get_coda_annotations(annotation_filepath, data_root_dir, adjust_start_time_s_fn):
  # Read the CSV data.
  annotations_file = open(annotation_filepath, 'r')
  csv_reader = csv.reader(annotations_file)
  csv_rows = list(csv_reader)
  annotations_file.close()
  # Get the header indexes for particular columns of data.
  headers = csv_rows[0]
  audio_file_keyword_columnIndex = [i for (i, h) in enumerate(headers) if 'recording' in h.lower()][0]
  whale_columnIndex = [i for (i, h) in enumerate(headers) if 'whale' in h.lower()][0]
  tfs_columnIndex = [i for (i, h) in enumerate(headers) if 'tfs' in h.lower()][0]
  ici_columnIndexes = [i for (i, h) in enumerate(headers) if 'ici' in h.lower()]
  # Create a list of data for each desired field.
  coda_start_times_s = []
  coda_end_times_s = []
  click_icis_s = []
  click_times_s = []
  whale_indexes = []
  audio_file_start_times_s = {}
  for coda_row in csv_rows[1:]:
    # Get the start time of the file in this row.
    audio_file_keyword = coda_row[audio_file_keyword_columnIndex]
    if audio_file_keyword not in audio_file_start_times_s:
      # Find the wav file that the CSV references.
      filepaths = glob.glob(os.path.join(data_root_dir, '*/%s*.wav' % audio_file_keyword), recursive=True)
      if len(filepaths) == 0:
        raise AssertionError('Could not find an audio file for coda annotations with keyword [%s]' % audio_file_keyword)
      if len(filepaths) > 1:
        raise AssertionError('Found too many audio files for coda annotations with keyword [%s]' % audio_file_keyword)
      audio_filepath = filepaths[0]
      # Get the device ID as the name of its parent folder.
      device_id = os.path.split(os.path.dirname(audio_filepath))[-1]
      # Get the start time of the file from its filename and the specified offset for this device.
      filename = os.path.basename(audio_filepath)
      start_time_ms = int(re.search('\d{13}', filename)[0])
      start_time_s = start_time_ms/1000.0
      start_time_s = adjust_start_time_s_fn(start_time_s, device_id)
      # Store the result to reduce overhead next coda row.
      audio_file_start_times_s[audio_file_keyword] = start_time_s
    audio_file_start_time_s = audio_file_start_times_s[audio_file_keyword]
    # Get click timing information.
    coda_start_time_s = audio_file_start_time_s + float(coda_row[tfs_columnIndex])
    click_icis_s_forCoda = [float(ici) for ici in itemgetter(*ici_columnIndexes)(coda_row)]
    click_icis_s_forCoda = [ici for ici in click_icis_s_forCoda if ici > 0]
    click_times_s_forCoda = coda_start_time_s + np.cumsum([0.0] + click_icis_s_forCoda)
    # Get the whale index number.
    whale_index = int(coda_row[whale_columnIndex])
    # Store the information in each field array.
    coda_start_times_s.append(coda_start_time_s)
    coda_end_times_s.append(coda_start_time_s + sum(click_icis_s_forCoda))
    click_times_s.append(click_times_s_forCoda)
    click_icis_s.append(click_icis_s_forCoda)
    whale_indexes.append(whale_index)
    
  return (coda_start_times_s, coda_end_times_s, click_icis_s, click_times_s, whale_indexes)

  
  

