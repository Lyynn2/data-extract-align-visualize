
import numpy as np
import csv
import distinctipy
import os
import time
from operator import itemgetter
from collections import OrderedDict

import pyqtgraph
from pyqtgraph.Qt import QtCore, QtGui, QtWidgets
from pyqtgraph.Qt.QtGui import QPixmap, QImage

plot_icis = True

data_dir_root = 'C:/Users/jdelp/Desktop/_whale_birthday_s3_data'
annotation_dir = os.path.join(data_dir_root, '_coda_annotations')
annotation_filepath = os.path.join(annotation_dir, 'CETI23-280-manual-Shane.csv')

csv_rows = []
with open(annotation_filepath, 'r') as annotations_file:
  csv_reader = csv.reader(annotations_file)
  csv_rows = list(csv_reader)
headers = csv_rows[0]
audio_file_keyword_columnIndex = [i for (i, h) in enumerate(headers) if 'recording' in h.lower()][0]
whale_columnIndex = [i for (i, h) in enumerate(headers) if 'whale' in h.lower()][0]
tfs_columnIndex = [i for (i, h) in enumerate(headers) if 'tfs' in h.lower()][0]
ici_columnIndexes = [i for (i, h) in enumerate(headers) if 'ici' in h.lower()]
print('audio_file_keyword_columnIndex', audio_file_keyword_columnIndex)
print('whale_columnIndex', whale_columnIndex)
print('tfs_columnIndex', tfs_columnIndex)
print('ici_columnIndexes', ici_columnIndexes)

# Get unique colors for each whale index.
whale_indexes_all = [int(coda_row[whale_columnIndex]) for coda_row in csv_rows[1:]]
unique_whale_indexes = list(OrderedDict(zip(whale_indexes_all, whale_indexes_all)).keys())
whale_colors = [distinctipy.get_rgb256(c) for c in distinctipy.get_colors(len(unique_whale_indexes))]
whale_pens = [pyqtgraph.mkPen(whale_color, width=5) for whale_color in whale_colors]

app = QtWidgets.QApplication([])
codas_graphics_layout = pyqtgraph.GraphicsLayoutWidget()
codas_plotWidget = pyqtgraph.PlotItem()
codas_graphics_layout.addItem(codas_plotWidget, *(0, 0, 1, 1))
codas_graphics_layout.setGeometry(50, 50, 1000, 1000/2.5)
codas_yrange = [0, 600]
codas_currentTime_handle = codas_plotWidget.plot(x=[5, 5], y=codas_yrange, pen=pyqtgraph.mkPen([200, 200, 200], width=7))
for coda_row in csv_rows[1:]:
  coda_start_time_s = float(coda_row[tfs_columnIndex])
  click_icis_s = [float(ici) for ici in itemgetter(*ici_columnIndexes)(coda_row)]
  click_icis_s = [ici for ici in click_icis_s if ici > 0]
  coda_click_times_s = np.cumsum([0.0] + click_icis_s)
  click_times_s = coda_start_time_s + coda_click_times_s
  whale_index = int(coda_row[whale_columnIndex])
  whale_pen = whale_pens[unique_whale_indexes.index(whale_index)]
  whale_color = whale_colors[unique_whale_indexes.index(whale_index)]
  if plot_icis:
    if len(click_icis_s) > 0:
      click_icis_s = click_icis_s + [click_icis_s[-1]]
    click_icis_s = np.array(click_icis_s)
    symbols = ['d' if whale_index >= 20 else 'o']*len(click_times_s)
    symbols[-1] = 't' if whale_index >= 20 else 's'
    codas_plotWidget.plot(x=click_times_s, y=click_icis_s*1000,
                          symbol=symbols,
                          symbolSize=8, pen=whale_pen,
                          symbolBrush=whale_color)
  else:
    codas_plotWidget.plot(x=click_times_s, y=coda_click_times_s*1000,
                          symbol='d' if whale_index >= 20 else 'o',
                          symbolSize=8, pen=whale_pen,
                          symbolBrush=whale_color)

codas_plotWidget.showGrid(x=True, y=True, alpha=1)

codas_graphics_layout.show()
t0 = time.time()
n = 0
for t in np.arange(start=10, stop=50, step=0.1):
  codas_currentTime_handle.setData((t+5)*np.array([1, 1]), codas_yrange)
  codas_plotWidget.setXRange(t, t+15)
  # codas_plotWidget.setYRange(*codas_yrange)
  QtCore.QCoreApplication.processEvents()
  n+=1
print(n/(time.time() - t0))
  
app.exec()