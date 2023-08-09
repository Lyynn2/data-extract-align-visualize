
import dateutil.parser
from datetime import datetime
import os
import numpy as np
import cv2
from PIL import Image
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
  file_extension = os.path.splitext(filepath)[-1]
  file_extension = file_extension.lower()
  return file_extension

def is_video(filepath_or_data):
  if filepath_or_data is None:
    return False
  if isinstance(filepath_or_data, cv2.VideoCapture):
    return True
  return get_file_extension(filepath_or_data) in ['.mp4', '.mov', '.avi', '.lrv', '.lrf']

def is_image(filepath_or_data):
  if filepath_or_data is None:
    return False
  if isinstance(filepath_or_data, np.ndarray):
    return filepath_or_data.ndim == 3
  return get_file_extension(filepath_or_data) in ['.jpg', '.jpeg', '.png', '.bmp', '.tiff']

def is_audio(filepath_or_data):
  if filepath_or_data is None:
    return False
  if isinstance(filepath_or_data, np.ndarray):
    return filepath_or_data.ndim == 2
  return get_file_extension(filepath_or_data) in ['.wav']

############################################
# IMAGES
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
def draw_text_on_image(img, text, pos=(0, 0),
                       font_scale=8, text_width_ratio=None,
                       font_thickness=1, font=cv2.FONT_HERSHEY_DUPLEX,
                       text_color=(255, 255, 255), text_bg_color=(100, 100, 100)
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
  # Place the text at the bottom and/or left if desired.
  pos = list(pos)
  x, y = pos
  if y == -1:
    y = img.shape[0]-round(1.25*text_h)
  if x == -1:
    x = img.shape[1]-text_w
  pos = [x, y]
  # Draw the background shading.
  cv2.rectangle(img, pos, (x + text_w, y + text_h), text_bg_color, -1)
  # Draw the text.
  cv2.putText(img, text, (x, int(y + text_h + font_scale - 1)),
              font, font_scale, text_color, font_thickness)



