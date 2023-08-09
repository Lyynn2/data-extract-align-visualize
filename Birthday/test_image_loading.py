
import os
import time
import dateutil.parser
from PIL import Image
import cv2
import numpy as np

dir = 'P:/Media/Pictures/2023/2023-07 Dominica/_BOAT_2023-07-08/David'
#dir = 'path_to_david_photos_folder'
# fp = os.path.join(dir, 'IMG_4790.1688812736000.jpg') # his first photo
fp = os.path.join(dir, 'IMG_6558.1688831949000.jpg') # his last photo


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


N = 20
target_width = 600
target_height = 600
t0 = time.time()
for n in range(N):
  # img = cv2.imread(fp)
  # img = scale_image(img, target_width=target_width, target_height=target_height)
  img = Image.open(fp)
  # img.draft('RGB', (target_width, target_height))
  img = np.asarray(img)

duration_s = time.time() - t0
print()
print('duration: %0.3f s' % (duration_s))
print('duration per loop: %0.3f s' % (duration_s/N))
print('loop rate: %0.3f Hz' % (N/duration_s))
print()

cv2.imshow('test', img)
cv2.waitKey(0)
