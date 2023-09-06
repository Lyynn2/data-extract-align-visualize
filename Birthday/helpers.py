
############
#
# Copyright (c) 2023 Joseph DelPreto and MIT CSAIL
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
#
############

import cv2
import decord
from PIL import Image
import ffmpeg
import pysrt
import csv

import numpy as np
import dateutil.parser
from datetime import datetime
from operator import itemgetter
import re
import os
import glob

try:
  import pyqtgraph
  from pyqtgraph.Qt.QtGui import QPixmap, QImage
  from pyqtgraph.Qt import QtCore, QtGui, QtWidgets
  have_pyqt = True
except:
  have_pyqt = False

############################################
# TIME
############################################

# Convert time as seconds since epoch to a human-readable string.
# timezone_offset_s is offset to add to time_s to convert from local time to UTC time.
# timezone_offset_str is the offset string in format HHMM, and may be negative.
# For example, for Eastern Daylight Time which is UTC-4:
#   timezone_offset_s = -14400
#   timezone_offset_str = '-0400'
def time_s_to_str(time_s, timezone_offset_s=0, timezone_offset_str=''):
  # Get "UTC" time, which is actually local time because we will do the timezone offset first.
  time_datetime = datetime.utcfromtimestamp(time_s + timezone_offset_s)
  # Format the string then add the local offset string.
  return time_datetime.strftime('%%Y-%%m-%%d %%H:%%M:%%S.%%f %s' % timezone_offset_str)

# Convert from a human-readable time string to time as seconds since epoch.
# The time string should include a timezone offset if applicable, for example '0400' for EDT.
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
  if isinstance(filepath_or_data, (cv2.VideoCapture, decord.VideoReader)):
    return True
  return get_file_extension(filepath_or_data) in ['.mp4', '.mov', '.avi', '.lrv', '.lrf'] or False

def is_image(filepath_or_data, enforce_dtype_uint8=True):
  if filepath_or_data is None:
    return False
  if isinstance(filepath_or_data, np.ndarray):
    if filepath_or_data.ndim != 3:
      return False
    if enforce_dtype_uint8 and (filepath_or_data.dtype != np.uint8):
      return False
    return True
  return get_file_extension(filepath_or_data) in ['.jpg', '.jpeg', '.png', '.bmp', '.tiff'] or False

def is_audio(filepath_or_data, max_num_channels=2):
  if filepath_or_data is None:
    return False
  if isinstance(filepath_or_data, np.ndarray):
    return filepath_or_data.squeeze().ndim <= max_num_channels
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

# Load an image from file.
# Optionally scale the image to a target size.
# Using the PIL method is fastest, since it can draft the downscaling during loading if it is a JPG.
# Will maintain the image's aspect ratio when scaling.
def load_image(filepath, target_width=None, target_height=None, method='pil'):
  img = None
  if method.lower() == 'opencv':
    img = cv2.imread(filepath)
    if target_width is not None and target_height is not None:
      img = scale_image(img, target_width=target_width, target_height=target_height)
  elif method.lower() == 'pil':
    img = Image.open(filepath)
    if target_width is not None and target_height is not None and get_file_extension(filepath) in ['jpg', 'jpeg']:
      img.draft('RGB', (int(target_width), int(target_height)))
      print('target:', (target_width, target_height), '  drafted:', img.size, os.path.basename(filepath))
    img = np.asarray(img)
    if target_width is not None and target_height is not None:
      img = scale_image(img, target_width=target_width, target_height=target_height)
  return img

# Open a video file.
# Using decord is fastest and most accurate for frame seeking.
# target_width and target_height are only used for the 'decord' method.
#  Will then scale the frames as they are loaded to the target size (maintaining aspect ratio).
def get_video_reader(filepath, target_width=None, target_height=None, method='decord'):
  video_reader = None
  frame_rate = None
  num_frames = None
  if method.lower() == 'opencv':
    video_reader = cv2.VideoCapture(filepath)
    frame_rate = video_reader.get(cv2.CAP_PROP_FPS)
    num_frames = int(video_reader.get(cv2.CAP_PROP_FRAME_COUNT))
  elif method.lower() == 'decord':
    video_reader = decord.VideoReader(filepath)
    if target_width is not None or target_height is not None:
      img = video_reader[0].asnumpy()
      img = scale_image(img, target_width, target_height)
      video_reader = decord.VideoReader(filepath, width=img.shape[1], height=img.shape[0])
    frame_rate = video_reader.get_avg_fps()
    num_frames = len(video_reader)
  return (video_reader, frame_rate, num_frames)
  
# Load a specified frame from a video reader.
# The video reader should be an OpenCV VideoCapture or Decord VideoReader object.
# Will return None if there was an issue fetching the frame.
def load_frame(video_reader, frame_index, target_width=None, target_height=None):
  img = None
  if isinstance(video_reader, cv2.VideoCapture):
    video_reader.set(cv2.CAP_PROP_POS_FRAMES, frame_index)
    success, img = video_reader.read()
    if success and (target_width is not None and target_height is not None):
      img = scale_image(img, target_width=target_width, target_height=target_height)
  elif isinstance(video_reader, decord.VideoReader):
    try:
      img = video_reader[frame_index].asnumpy()
      success = (img is not None)
    except:
      img = None
      success = False
    if success and (target_width is not None and target_height is not None):
      img = scale_image(img, target_width=target_width, target_height=target_height)
  return img
  
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
# If maintaining the image's aspect ratio (which is the default),
#   Will scale to the largest size that fits within the target size.
# If the image size already meets the target criteria,
#   will return the original image (this call will not incur any delays beyond the size check).
# The input can be a numpy array or a PyQtGraph QPixmap object.
# Will also measure the total time spent in this method, for profiling purposes.
import time
duration_s_scaleImage = 0
def get_duration_s_scaleImage():
  global duration_s_scaleImage
  return duration_s_scaleImage
def scale_image(img, target_width, target_height, maintain_aspect_ratio=True):
  global duration_s_scaleImage
  t0 = time.time()
  # Scale a numpy array.
  if isinstance(img, np.ndarray):
    img_width = img.shape[1]
    img_height = img.shape[0]
    # Determine an appropriate scale factor by considering both dimensions.
    scale_factor_byWidth = target_width/img_width if target_width is not None else None
    scale_factor_byHeight = target_height/img_height if target_height is not None else None
    # If maintaining the aspect ratio, use the same factor for both dimensions.
    if maintain_aspect_ratio:
      scale_factor = 1
      if scale_factor_byWidth is not None and scale_factor_byHeight is not None:
        scale_factor = min(scale_factor_byWidth, scale_factor_byHeight)
      elif scale_factor_byWidth is not None:
        scale_factor = scale_factor_byWidth
      elif scale_factor_byHeight is not None:
        scale_factor = scale_factor_byHeight
      if scale_factor != 1:
        res = cv2.resize(src=img, dsize=(0,0), fx=scale_factor, fy=scale_factor)
      else:
        # Do nothing if the image size is already as desired.
        res = img
      duration_s_scaleImage += time.time() - t0
      return res
    else:
      # If not maintaining the aspect ratio, scale each dimension by its computed factor.
      if scale_factor_byWidth != 1 or scale_factor_byHeight != 1:
        res = cv2.resize(src=img, dsize=(0,0), fx=scale_factor_byWidth, fy=scale_factor_byHeight)
      else:
        # Do nothing if the image size is already as desired.
        res = img
      duration_s_scaleImage += time.time() - t0
      return res
  # Scale a QPixmap object.
  if isinstance(img, QPixmap):
    if maintain_aspect_ratio:
      res = img.scaled(target_width, target_height,
                       aspectRatioMode=pyqtgraph.QtCore.Qt.AspectRatioMode.KeepAspectRatio)
      duration_s_scaleImage += time.time() - t0
      return res
    else:
      res = img.scaled(target_width, target_height,
                       aspectRatioMode=pyqtgraph.QtCore.Qt.AspectRatioMode.IgnoreAspectRatio)
      duration_s_scaleImage += time.time() - t0
      return res

# Draw text on an image, with a shaded background.
# pos is the target (x, y) position of the upper-left corner of the text, except:
#   If y is -1, will place the text at the bottom of the image.
#   If x is -1, will place the text at the right of the image.
#   If x and/or y is between 0 and 1, will center the text at that ratio of the width and/or height.
# If text_width_ratio is not None, will compute a font scale such that the text width is that fraction of the image width.
#   font_scale will be ignored if text_width_ratio is not None.
# If preview_only is True, will compute the text size but will not edit the image.
# The input image and any color arguments should be in BGR format, scaled out of 255.
import time
duration_s_drawText = 0
def get_duration_s_drawText():
  global duration_s_drawText
  return duration_s_drawText
def draw_text_on_image(img_bgr, text, pos=(0, 0),
                       font_scale=8, text_width_ratio=None,
                       font_thickness=1, font=cv2.FONT_HERSHEY_DUPLEX,
                       text_color_bgr=None,
                       text_bg_color_bgr=None, text_bg_outline_color_bgr=None, text_bg_pad_width_ratio=0.03,
                       preview_only=False,
                       ):
  global duration_s_drawText
  t0 = time.time()
  # If desired, compute a font scale based on the target width ratio.
  if text_width_ratio is not None:
    if len(text) > 0:
      target_text_w = text_width_ratio * img_bgr.shape[1]
      font_scale = 0
      text_w = 0
      while text_w < target_text_w:
        font_scale += 0.2
        (text_w, text_h), _ = cv2.getTextSize(text, font, font_scale, font_thickness)
      font_scale -= 0.2
    else:
      font_scale = 1
  # Compute the text dimensions.
  (text_w, text_h), _ = cv2.getTextSize(text, font, font_scale, font_thickness)
  # Compute padding.
  text_bg_pad = round(text_w*text_bg_pad_width_ratio)
  text_bg_outline_width = round(text_w*0.02) if text_bg_outline_color_bgr is not None else 0
  # Compute the text position.
  # Place the text at the bottom and/or right if desired, and handle fractional placement if desired.
  x, y = pos
  if y == -1:
    y = round(img_bgr.shape[0] - text_h - text_bg_pad*2 - text_bg_outline_width*2)
  elif y > 0 and y < 1:
    y = round(img_bgr.shape[0]*y - text_h/2 - text_bg_pad - text_bg_outline_width)
  if x == -1:
    x = round(img_bgr.shape[1] - text_w - text_bg_pad*2 - text_bg_outline_width*2)
  elif x > 0 and x < 1:
    x = round(img_bgr.shape[1]*x - text_w/2 - text_bg_pad - text_bg_outline_width)
  # Add text to the image if desired.
  if not preview_only:
    # Draw a border around the background if desired.
    if text_bg_outline_color_bgr is not None:
      cv2.rectangle(img_bgr, (x,y), (x + text_w + 2*text_bg_outline_width + 2*text_bg_pad,
                                 y + text_h + 2*text_bg_outline_width + 2*text_bg_pad),
                    text_bg_outline_color_bgr, -1)
      x += text_bg_outline_width
      y += text_bg_outline_width
    
    # Draw the background shading.
    text_bg_color_bgr = text_bg_color_bgr or (100, 100, 100)
    cv2.rectangle(img_bgr, (x,y), (x + text_w + 2*text_bg_pad, y + text_h + 2*text_bg_pad),
                  text_bg_color_bgr, -1)
    x += text_bg_pad
    y += text_bg_pad
    
    # Draw the text.
    if text_color_bgr is None:
      text_color_bgr = (255, 255, 255)
    cv2.putText(img_bgr, text, (x, int(y + text_h + font_scale - 1)),
                font, font_scale, tuple(text_color_bgr), font_thickness)
  
  duration_s_drawText += time.time() - t0
  return (text_w, text_h, font_scale, (x, y))

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

# Extract data from a drone SRT file associated with the given video file.
# Assumes the SRT file is in the same directory and has the same base name as the video file.
# Return a dictionary with timestamps, GPS, altitude, and image settings for each frame.
def get_drone_srt_data(video_filepath):
  # Open the SRT file if it exists.
  srt_filepath = '%s.srt' % (os.path.splitext(video_filepath)[0])
  if not os.path.exists(srt_filepath):
    return None
  srt = pysrt.open(srt_filepath)
  num_frames = len(srt)
  
  # Initialize arrays for the data.
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
  
  # Parse the data for each frame.
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

# Parse coda annotations from a CSV file.
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
  
  # Get the data for each annotated coda.
  for coda_row in csv_rows[1:]: # row 0 is the header row
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

  
  
############################################
# Various
############################################

# Get the next multiple of a number above a specified target.
# For example, the next multiple of 5 above 23 would be 25.
def next_multiple(value, multiple_of):
  if int(value/multiple_of) == value/multiple_of:
    return value
  return (np.floor(value/multiple_of) + 1)*multiple_of

# Get the previous multiple of a number below a specified target.
# For example, the previous multiple of 5 below 23 would be 20.
def previous_multiple(value, multiple_of):
  if int(value/multiple_of) == value/multiple_of:
    return value
  return np.floor(value/multiple_of)*multiple_of



