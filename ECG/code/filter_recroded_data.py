

import h5py
import numpy as np
from scipy import signal
from scipy import fftpack
import matplotlib.pyplot as plt
import time
import os
script_dir = os.path.dirname(os.path.realpath(__file__))

from utils.numpy_utils import *
from utils.time_utils import *

data_dir = os.path.join(script_dir, '..', 'data')
# log_filepath = os.path.join(data_dir, '2022-07-24 testing ecg board esp', '2022-07-24_15-39-12_test_ecgBoard_esp_adhesivesBack_ecg-lod.hdf5')
log_filepath = os.path.join(data_dir, '2022-07-23 testing ecg board esp', '2022-07-23_21-36-53_test_ecgBoard_esp_adhesives_ecg-lod.hdf5')

notch_N = 5
notch_frequencies_hz = [50, 70]
band_N = 2
band_frequencies_hz = [3, 30]

# Load the data.
log = h5py.File(log_filepath, 'r')
ecg_time_s = np.squeeze(np.array(log['ecg']['esp_time_s']))
ecg_time_s = ecg_time_s - min(ecg_time_s)
ecg_data = np.squeeze(np.array(log['ecg']['data']))
ecg_Fs = (ecg_data.shape[0]-1)/(max(ecg_time_s) - min(ecg_time_s))

# Filter the data.
ecg_data_filtered = ecg_data
if notch_N is not None:
  b_notch, a_notch = signal.butter(notch_N, notch_frequencies_hz, btype='bandstop',
                                   analog=False, output='ba', fs=ecg_Fs)
  ecg_data_filtered = signal.filtfilt(b_notch, a_notch, ecg_data_filtered)
if band_N is not None:
  b_band, a_band = signal.butter(band_N, band_frequencies_hz, btype='bandpass',
                                   analog=False, output='ba', fs=ecg_Fs)
  ecg_data_filtered = signal.filtfilt(b_band, a_band, ecg_data_filtered)

# Plot the data.
fig, axs = plt.subplots(nrows=1, ncols=1,
                        squeeze=False, # if False, always return 2D array of axes
                        sharex=True, #sharey=True,
                        subplot_kw={'frame_on': True},
                        figsize=(10,6)
                        )
ax = axs[0][0]
# plt.plot(ecg_time_s, ecg_data, '-')
plt.plot(ecg_time_s, ecg_data_filtered, '-')
ax.grid(True, color='lightgray')
ax.set_title('ECG Filtered: Notch %s Hz | Bandpass %s Hz' % (notch_frequencies_hz, band_frequencies_hz))
# ax.set_xlim([14,26])
ax.set_xlim([9,20.5])
# ax.set_ylim([-350000,450000])
plt.show(block=True)

log.close()












