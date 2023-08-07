
import serial
from scipy import signal
from scipy import fftpack
import numpy as np
import matplotlib.pyplot as plt
import time
import os
import h5py

from utils.numpy_utils import *
from utils.time_utils import *

output_dir = os.path.join('data')
# hdf5_filename = '%s_ra-UnderRightPec-hold_la-UnderLeftPec-hold_rl-RightAbs-adhesive.hdf5' % get_time_str()
hdf5_filename = '%s_ad8232-eval_p4_belowPecs-adhesive-swapRL_gain1_groundRsometimes.hdf5' % get_time_str()
hdf5_filepath = os.path.join(output_dir, hdf5_filename)
os.makedirs(output_dir, exist_ok=True)

esp_com_port = 'COM29'
esp_baud_rate = 500000
adc_gain = 1 # set this in the Arduino code (just here for metadata)
enable_60hz_notch_filter = False

esp_serial = serial.Serial(port=esp_com_port, baudrate=esp_baud_rate)
esp_serial.flushInput()
count = 0
start_time_s = time.time()
for i in range(1000):
  esp_serial.readline()
ecg_sampling_rate_hz = round(1000/(time.time() - start_time_s))

plot_duration_s = 10
plot_fft = False
plot_length = round(plot_duration_s*ecg_sampling_rate_hz)
ecg_time_s = np.linspace(-plot_duration_s, 0, num=plot_length)
# sample_size = [1]
# ecg_log = np.zeros((plot_length, *sample_size))
ecg_log = np.zeros(plot_length)

# # Create a 60 Hz notch IIR filter.
# notch_frequency_hz = 60.0  # Frequency to be removed from signal (Hz)
# notch_quality_factor = 1.0  # Quality factor
# b_notch, a_notch = signal.iirnotch(notch_frequency_hz, notch_quality_factor, ecg_sampling_rate_hz)
# Create a 60 Hz notch butterworth filter.
notch_N = 10
notch_frequencies_hz = [55, 65]
b_notch, a_notch = signal.butter(notch_N, notch_frequencies_hz, btype='bandstop',
                                 analog=False, output='ba', fs=ecg_sampling_rate_hz)
# # Plot the filter
# freq, h = signal.freqz(b_notch, a_notch, fs = ecg_sampling_rate_hz)
# plt.figure('filter')
# plt.plot( freq, 20*np.log10(abs(h)))
# plt.grid(True, color='lightgray')
# plt.show()

# Prepare a plot.
figure_size = (5.5, 3.5)
plt.ioff()
fig, axs = plt.subplots(nrows=2 if plot_fft else 1, ncols=1,
                        squeeze=False, # if False, always return 2D array of axes
                        # sharex=True, sharey=True,
                        subplot_kw={'frame_on': True},
                        figsize=figure_size
                        )
ax = axs[0][0]
if enable_60hz_notch_filter:
  ax.plot(ecg_time_s, ecg_log, '-', linewidth=2)
  ax.plot(ecg_time_s, ecg_log, '-', linewidth=1)
else:
  ax.plot(ecg_time_s, ecg_log, '-')
ax.grid(True, color='lightgray')
if plot_fft:
  ax_fft = axs[1][0]
  ax_fft.plot(np.linspace(0.0, ecg_sampling_rate_hz/2, plot_length//2), np.zeros(plot_length//2))
  ax_fft.grid(True, color='lightgray')
plt.suptitle(hdf5_filename)
fig.show()


ecg_data = []
ecg_data_filtered = []
time_s = []
plot_update_period_s = 1
last_plot_update_time_s = time.time()
fs_update_period_s = 10
last_fs_update_time_s = time.time()
plotting_start_time_s = time.time()
try:
  while True:
    # Acquire and timestamp a new sample.
    ecg_sample = float(esp_serial.readline().strip())
    time_s.append(time.time())
    ecg_data.append(ecg_sample)
    # Prepare the data for plotting.
    new_data = np.atleast_1d(ecg_sample) # np.atleast_1d(1)
    new_time_s = np.atleast_1d(time.time())
    new_time_s = new_time_s - plotting_start_time_s
    ecg_time_s = add_to_rolling_array(ecg_time_s, new_time_s)
    ecg_log = add_to_rolling_array(ecg_log, new_data)
    # Apply a 60 Hz notch filter if desired.
    if enable_60hz_notch_filter:
      ecg_log_filtered = signal.filtfilt(b_notch, a_notch, ecg_log)
    else:
      ecg_log_filtered = ecg_log
    ecg_data_filtered.append(ecg_log_filtered[-1])
    # Update the ECG sampling rate estimate.
    if time.time() - last_fs_update_time_s >= fs_update_period_s:
      print(ecg_sampling_rate_hz)
      ecg_sampling_rate_hz = len(ecg_data)/(time.time() - plotting_start_time_s)
      if enable_60hz_notch_filter:
        b_notch, a_notch = signal.butter(notch_N, notch_frequencies_hz, btype='bandstop',
                                         analog=False, output='ba', fs=ecg_sampling_rate_hz)
      last_fs_update_time_s = time.time()
    # Update the plot
    if time.time() - last_plot_update_time_s >= plot_update_period_s:
      # Plot ECG data
      ax.get_lines()[0].set_xdata(ecg_time_s)
      ax.get_lines()[0].set_ydata(ecg_log)
      if enable_60hz_notch_filter:
        ax.get_lines()[1].set_xdata(ecg_time_s)
        ax.get_lines()[1].set_ydata(ecg_log_filtered)
      ax.relim()
      ax.autoscale_view(scalex=True, scaley=True)
      # Plot FFT
      if plot_fft:
        N = plot_length
        T = 1.0 / ecg_sampling_rate_hz
        yf = fftpack.fft(ecg_log_filtered - np.mean(ecg_log_filtered))
        xf = np.linspace(0.0, ecg_sampling_rate_hz/2, N//2)
        ax_fft.get_lines()[0].set_xdata(xf)
        ax_fft.get_lines()[0].set_ydata(2.0/N * np.abs(yf[:N//2]))
        ax_fft.relim()
        ax_fft.autoscale_view(scalex=True, scaley=True)
      # Update the figure
      fig.canvas.draw()
      fig.canvas.flush_events()
      last_plot_update_time_s = time.time()
except KeyboardInterrupt:
  print()
  print('Quitting!')

metadata = {}
metadata['adc_gain'] = adc_gain
metadata['esp_baud_rate'] = esp_baud_rate
metadata['ecg_sampling_rate_hz'] = ecg_sampling_rate_hz
metadata['enable_60hz_notch_filter'] = enable_60hz_notch_filter
metadata['notch_N'] = notch_N
metadata['notch_frequencies_hz'] = notch_frequencies_hz
metadata['plot_duration_s'] = plot_duration_s

ecg_data = np.array(ecg_data)
ecg_data_filtered = np.array(ecg_data_filtered)
time_s = np.array(time_s)
time_str = [get_time_str(t, format='%Y-%m-%d %H:%M:%S.%f') for t in time_s]
hout = h5py.File(hdf5_filepath, 'w')
hout.create_dataset('ecg_data', data=ecg_data)
hout.create_dataset('ecg_data_filtered', data=ecg_data_filtered)
hout.create_dataset('time_s', data=time_s)
hout.create_dataset('time_str', dtype='S26', data=time_str)
hout.attrs.update(metadata)
hout.close()

print()
print('Close the plot to exit')
plt.show()
print()








