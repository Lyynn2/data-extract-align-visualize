
import os
import time
import dateutil.parser
from PIL import Image
import cv2
import decord
import numpy as np

dir = 'C:/Users/jdelp/Desktop/_whale_birthday_s3_data/CETI-DJI_MAVIC3-1'
filepath = os.path.join(dir, '1688826012514.LRF')

N = 100
target_width = 600
target_height = 600

use_opencv = False
use_decord = True
use_decord_batch = False

if use_opencv:
  video_reader = cv2.VideoCapture(filepath)
  print('fps:', video_reader.get(cv2.CAP_PROP_FPS))
  print('num frames:', video_reader.get(cv2.CAP_PROP_FRAME_COUNT))
if use_decord or use_decord_batch:
  video_reader = decord.VideoReader(filepath, width=1280//2, height=720//2)
  print('fps:', video_reader.get_avg_fps())
  print('num frames:', len(video_reader))

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


t0 = time.time()
if use_decord_batch:
  frame_loading_batch_size = N//4
  frame_indexes_loaded = []
  loaded_frames = None
for n in range(N):
  if use_opencv:
    video_reader.set(cv2.CAP_PROP_POS_FRAMES, n) # should this be data_index-1? A bit unclear from documentation/examples
    success, img = video_reader.read()
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) # OpenCV uses BGR, but PyQtGraph uses RGB
    img = scale_image(img, target_width=target_width, target_height=target_height)
  
  if use_decord:
    img = video_reader[n].asnumpy()
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) # OpenCV uses BGR, but PyQtGraph uses RGB
    # img = scale_image(img, target_width=target_width, target_height=target_height)
  
  if use_decord_batch:
    if n not in frame_indexes_loaded:
      frame_indexes_loaded = np.arange(start=n, stop=n+frame_loading_batch_size)
      loaded_frames = video_reader.get_batch(frame_indexes_loaded).asnumpy()
    img = loaded_frames[frame_indexes_loaded.searchsorted(n, side='left'), :]
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) # OpenCV uses BGR, but PyQtGraph uses RGB
    img = scale_image(img, target_width=target_width, target_height=target_height)
  
duration_s = time.time() - t0
print()
print('duration: %0.3f s' % (duration_s))
print('duration per loop: %0.4f s' % (duration_s/N))
print('loop rate: %0.3f Hz' % (N/duration_s))
print()

# cv2.imshow('test', img)
# cv2.waitKey(0)
