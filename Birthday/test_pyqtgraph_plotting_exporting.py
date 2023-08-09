
import pyqtgraph
from pyqtgraph.Qt import QtCore, QtGui, QtWidgets
from pyqtgraph.Qt.QtWidgets import QApplication, QWidget, QGridLayout, QLabel, QGraphicsView, QGraphicsScene
from pyqtgraph.Qt.QtGui import QPixmap, QImage
import pyqtgraph.exporters
import sys
import cv2
import numpy as np
import time
import random

def draw_text(img, text,
              font=cv2.FONT_HERSHEY_PLAIN,
              pos=(0, 0),
              font_scale=8,
              font_thickness=7,
              text_color=(255, 255, 255),
              text_color_bg=(100, 100, 100)
              ):
  pos = list(pos)
  x, y = pos
  text_size, _ = cv2.getTextSize(text, font, font_scale, font_thickness)
  text_w, text_h = text_size
  if y == -1:
    y = img.shape[0]-text_h
  if x == -1:
    x = img.shape[1]-text_w
  pos = [x, y]
  cv2.rectangle(img, pos, (x + text_w, y + text_h), text_color_bg, -1)
  cv2.putText(img, text, (x, y + text_h + font_scale - 1), font, font_scale, text_color, font_thickness)
  
  return text_size

def convertQImageToMat(qimg):
  img = qimg.convertToFormat(QtGui.QImage.Format.Format_RGB32)
  ptr = img.bits()
  ptr.setsize(img.sizeInBytes())
  arr = np.array(ptr).reshape(img.height(), img.width(), 4)  #  Copies the data
  return arr

def cv2_to_pixmap(cv_image):
  height, width, channel = cv_image.shape
  bytes_per_line = 3 * width
  q_image = QImage(cv_image.data, width, height, bytes_per_line, QImage.Format.Format_RGB888)
  return QPixmap.fromImage(q_image)

labels = []
def display_images(grid_layout, cv_images):
  global labels
  for row in range(2):
    for col in range(2):
      cv_image = cv_images[row * 2 + col]
      draw_text(cv_image, 'hello', pos=(0,-1))
      pixmap = cv2_to_pixmap(cv_image)
      label = QLabel()
      label.setPixmap(pixmap.scaledToWidth(300))
      grid_layout.addWidget(label, row, col)
      labels.append(label)

  return (grid_layout)

if __name__ == "__main__":
  # Replace these paths with the actual paths to your images
  image_paths = [
    'C:/Users/jdelp/Desktop/_whale_birthday_s3_data/DG-CANON_EOS_1DX_MARK_III-1/IMG_4844.1688814707000.JPG',
    'C:/Users/jdelp/Desktop/_whale_birthday_s3_data/DG-CANON_EOS_1DX_MARK_III-1/IMG_5013.1688816685000.JPG',
    'C:/Users/jdelp/Desktop/_whale_birthday_s3_data/DG-CANON_EOS_1DX_MARK_III-1/IMG_5350.1688816917000.JPG',
    'C:/Users/jdelp/Desktop/_whale_birthday_s3_data/DG-CANON_EOS_1DX_MARK_III-1/IMG_6550.1688831948000.JPG',
  ]

  app = QApplication(sys.argv)
  graphics_layout = pyqtgraph.GraphicsLayoutWidget(show=True)
  graphics_layout.setGeometry(10, 50, 100, 100)
  graphics_layout.show()
  grid_layout = QtWidgets.QGridLayout()
  grid_layout.setGeometry(QtCore.QRect(10, 50, 100, 100))
  graphics_layout.setLayout(grid_layout)
  
  # composite_widget.setGeometry(10, 50, composite_frame_width, composite_frame_height)
  # graphics_layout.show()
  vout = None
  cv_images = [cv2.cvtColor(cv2.imread(path), cv2.COLOR_RGB2BGR) for path in image_paths]
  exported_img = None
  for i in range(1):
    t0 = time.time()
    random.shuffle(cv_images)
    grid_layout = display_images(grid_layout, cv_images)
  
    QtCore.QCoreApplication.processEvents()
    # graphics_layout.show()
    # QtCore.QCoreApplication.processEvents()
    # sys.exit(app.exec())
    
    # exported_image = QPixmap.grabWindow(window.winId())
    
    # exporter = pyqtgraph.exporters.ImageExporter(graphics_layout.scene())
    # exported_img = exporter.export(toBytes=True)
    # exported_img = convertQImageToMat(exported_img)
    # exported_img = np.array(exported_img[:,:,0:3])

    exported_img = graphics_layout.grab().toImage()
    exported_img = convertQImageToMat(exported_img)
    exported_img = np.array(exported_img[:,:,0:3])
    
    # w, h = draw_text(img, "hello", pos=(0, 0))
    # print(img.shape)
    # if vout is None:
    #   vout = cv2.VideoWriter('filename.avi',
    #                          cv2.VideoWriter_fourcc(*'MJPG'),
    #                          5, [img.shape[1], img.shape[0]])
    # vout.write(img)
    print(time.time() - t0)
  # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
  # vout.release()
  cv2.imshow('yay', exported_img)
  cv2.waitKey(0)

