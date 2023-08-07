
import serial
from scipy import signal
from scipy import fftpack
import numpy as np
import matplotlib.pyplot as plt
import pickle
import h5py
import time
import os
script_dir = os.path.dirname(os.path.realpath(__file__))

from utils.numpy_scipy_utils import *
from utils.time_utils import *

###########################
###### CONFIGURATION ######
###########################

# Specify where data will be saved.
data_dir = os.path.join(script_dir, '..', 'data')
output_dir = os.path.join(data_dir, '2023-02-20 testing electrodes')#'%s testing ecg board esp' % get_time_str(format='%Y-%m-%d'))
hdf5_filename = '%s_test_ecgBoard4_2adhesive_wrist_tagPower.hdf5' % get_time_str(format='%Y-%m-%d_%H-%M-%S')
hdf5_filepath = os.path.join(output_dir, hdf5_filename)
os.makedirs(output_dir, exist_ok=True)

# Specify the ESP configuration.
esp_com_port = 'COM4'
esp_baud_rate = 1000000 # 1000000
esp_channel_names = ['ECG', 'LOD']#, ['ECG', 'LOD', 'Electrode 1', 'Electrode 2']
esp_num_channels = len(esp_channel_names)
adc_gain = 1 # set this in the Arduino code (just here for metadata)
# Given a line of data from the ESP, parse it into each channel in esp_data_columns.
# Will expect each line to have space-separated values,
#  and each entry may be '--' to indicate that the signal was not sampled that timestep.
def parse_esp_data_line(data_line):
  data = []
  if isinstance(data_line, bytes):
    try:
      data_line = data_line.decode('ascii')
    except UnicodeDecodeError:
      return (None, [None]*esp_num_channels)
  data_line_split = data_line.strip().split(' ')
  if len(data_line) == 0 or len(data_line_split) < (2+esp_num_channels): # add 2 for timestamp and checksum
    return (None, [None]*esp_num_channels)
  checksum = 0
  # Append the timestamp
  try:
    esp_time_us = data_line_split[0]
    checksum += int(esp_time_us)
    esp_time_s = float(esp_time_us)/1000000.0
  except ValueError:
    esp_time_s = None
    return (None, [None]*esp_num_channels)
  for channel_index in range(esp_num_channels):
    try:
      data_entry = int(data_line_split[channel_index+1])
      checksum += data_entry
      data.append(data_entry)
    except ValueError:
      data.append(None)
  esp_checksum = int(data_line_split[-1])
  valid_data = (checksum == esp_checksum)
  if not valid_data:
    print('WARNING: Invalid cheksum.  Line: [%s] > %d: %s, %d' % (data_line.strip(), esp_time_s, str(data), checksum))
    return (None, [None]*esp_num_channels)
  return (esp_time_s, data)

# Filtering options.
enable_60hz_notch_filter = False # NOTE: seems to be a bit weird after converting to faster multi-channel streaming, but probably won't use it anyway
esp_channels_to_filter = [0]
notch_N = 5
notch_frequencies_hz = [50, 70]

# Plotting/printing options.
fs_update_period_s = 10
channel_indexes_toPlot = [0, 1, 2] # corresponds to esp_data_columns
plot_duration_s = 10
plot_update_period_s = 0.2
plot_fft = False

############################
###### INITIALIZATION ######
############################

# Connect to the ESP serial.
print('Connecting to the ESP... ', end='')
esp_serial = serial.Serial(port=esp_com_port, baudrate=esp_baud_rate)
esp_serial.flushInput()
print('done')
# Read a burn line to become aligned with the data.
print('Reading a line of data from the ESP... ', end='')
while parse_esp_data_line(esp_serial.readline())[0] is None:
  time.sleep(0.05)
print('done')

# Estimate the ESP streaming rate.
print('Estimating the ESP streaming rates... ', end='')
esp_serial.flushInput()
count = 0
start_time_s = time.time()
esp_sampleTest_counts = [0] * esp_num_channels
while time.time() - start_time_s < 3:
  (time_s, data) = parse_esp_data_line(esp_serial.readline())
  if data is None:
    continue
  for channel_index in range(esp_num_channels):
    if data[channel_index] is not None:
      esp_sampleTest_counts[channel_index] += 1
esp_sampleTest_duration_s = time.time() - start_time_s
ecg_sampling_rates_hz = [round(esp_sampleTest_count/esp_sampleTest_duration_s) for esp_sampleTest_count in esp_sampleTest_counts]
print('done')
print('Estimated the following sampling rates:')
for (channel_index, channel_name) in enumerate(esp_channel_names):
  print('  %s: %7.2f Hz' % (channel_name, ecg_sampling_rates_hz[channel_index]))

# Initialize plotting lengths and logs based on the sampling rate.
plot_lengths = [round(plot_duration_s*ecg_sampling_rate_hz) for ecg_sampling_rate_hz in ecg_sampling_rates_hz]
plot_esp_times_s = [np.linspace(-plot_duration_s, 0, num=plot_length) for plot_length in plot_lengths]
plot_data = [np.zeros(plot_length) for plot_length in plot_lengths]
plot_data_filtered = [np.zeros(plot_length) for plot_length in plot_lengths]

if enable_60hz_notch_filter:
  # # Create a 60 Hz notch IIR filter.
  # notch_frequency_hz = 60.0  # Frequency to be removed from signal (Hz)
  # notch_quality_factor = 1.0  # Quality factor
  # b_notch, a_notch = signal.iirnotch(notch_frequency_hz, notch_quality_factor, ecg_sampling_rate_hz)
  # Create a 60 Hz notch butterworth filter.
  b_notches = []
  a_notches = []
  for channel_index in range(esp_num_channels):
    if channel_index in esp_channels_to_filter:
      b_notch, a_notch = signal.butter(notch_N, notch_frequencies_hz, btype='bandstop',
                                       analog=False, output='ba', fs=ecg_sampling_rates_hz[channel_index])
      b_notches.append(b_notch)
      a_notches.append(a_notch)
    else:
      b_notches.append(None)
      a_notches.append(None)
  # # Plot the filter
  # freq, h = signal.freqz(b_notch, a_notch, fs = ecg_sampling_rate_hz)
  # plt.figure('filter')
  # plt.plot( freq, 20*np.log10(abs(h)))
  # plt.grid(True, color='lightgray')
  # plt.show()

# Prepare a plot.
figure_size = None#(8,6)
plt.ioff()
num_plot_rows = esp_num_channels
num_plot_cols = 2 if plot_fft else 1
fig, axs = plt.subplots(nrows=num_plot_rows, ncols=num_plot_cols,
                        squeeze=False, # if False, always return 2D array of axes
                        sharex=True, #sharey=True,
                        subplot_kw={'frame_on': True},
                        figsize=figure_size
                        )
figManager = plt.get_current_fig_manager()
figManager.window.showMaximized()
# Plot dummy data to initialize the plots.
for row in range(num_plot_rows):
  ax = axs[row][0]
  if enable_60hz_notch_filter and row in esp_channels_to_filter:
    ax.plot(plot_esp_times_s[row], plot_data[row], '-', linewidth=2)
    ax.plot(plot_esp_times_s[row], plot_data[row], '-', linewidth=1)
  else:
    ax.plot(plot_esp_times_s[row], plot_data[row], '-')
  ax.grid(True, color='lightgray')
  ax.set_title(esp_channel_names[row])
  # Plot dummy data for the FFT axes
  if plot_fft:
    ax_fft = axs[row][1]
    ax_fft.plot(np.linspace(0.0, ecg_sampling_rates_hz[row]/2, plot_lengths[row]//2), np.zeros(plot_lengths[row]//2))
    ax_fft.grid(True, color='lightgray')
plt.suptitle(hdf5_filename)
fig.show()


#########################
###### STREAM DATA ######
#########################

data = [[] for i in range(esp_num_channels)]
data_filtered = [[] for i in range(esp_num_channels)]
esp_times_s = [[] for i in range(esp_num_channels)]
times_s = [[] for i in range(esp_num_channels)]
last_plot_update_time_s = time.time()
last_fs_update_time_s = time.time()
plotting_start_esp_times_s = [None for i in range(esp_num_channels)]
print('Starting to stream!')
try:
  while True:
    # Acquire and timestamp a new sample.
    (esp_time_s, new_data) = parse_esp_data_line(esp_serial.readline())
    time_s = time.time()
    if esp_time_s is None:
      print('WARNING: Got an invalid line of data')
      esp_serial.flushInput()
      for i in range(10):
        esp_serial.readline()
      continue
    for channel_index in range(esp_num_channels):
      if new_data[channel_index] is None:
        continue
        
      # Store the new data.
      esp_times_s[channel_index].append(esp_time_s)
      times_s[channel_index].append(time_s)
      data[channel_index].append(new_data[channel_index])
      if plotting_start_esp_times_s[channel_index] is None:
        plotting_start_esp_times_s[channel_index] = esp_time_s
      
      # Add the new sample and timestamp to the rolling buffers that will be plotted.
      plot_esp_times_s[channel_index] = add_to_rolling_array(
                                         plot_esp_times_s[channel_index],
                                         np.atleast_1d(esp_time_s) - plotting_start_esp_times_s[channel_index])
      plot_data[channel_index] = add_to_rolling_array(
                                         plot_data[channel_index],
                                         np.atleast_1d(new_data[channel_index]))
      # Apply a 60 Hz notch filter if desired.
      if enable_60hz_notch_filter and (channel_index in esp_channels_to_filter) \
          and (times_s[channel_index][-1] - min(times_s[channel_index]) > plot_duration_s + 1):
        plot_data_filtered[channel_index] = signal.filtfilt(b_notches[channel_index], a_notches[channel_index], plot_data[channel_index])
        data_filtered[channel_index].append(plot_data_filtered[channel_index][-1])
    
    # Update the ECG sampling rate estimate.
    if time.time() - last_fs_update_time_s >= fs_update_period_s:
      for channel_index in range(esp_num_channels):
        ecg_sampling_rates_hz[channel_index] = len(data[channel_index])/(esp_times_s[channel_index][-1] - esp_times_s[channel_index][0])
        if enable_60hz_notch_filter:
          b_notches = []
          a_notches = []
          for channel_index in range(esp_num_channels):
            if channel_index in esp_channels_to_filter:
              b_notch, a_notch = signal.butter(notch_N, notch_frequencies_hz, btype='bandstop',
                                               analog=False, output='ba', fs=ecg_sampling_rates_hz[channel_index])
              b_notches.append(b_notch)
              a_notches.append(a_notch)
            else:
              b_notches.append(None)
              a_notches.append(None)
        last_fs_update_time_s = time.time()
      print('Updated sampling rates: %s' % ' '.join(['%7.2f' % r for r in ecg_sampling_rates_hz]))
    
    # Update the plots.
    if time.time() - last_plot_update_time_s >= plot_update_period_s:
      for channel_index in range(esp_num_channels):
        # Plot main data.
        ax = axs[channel_index][0]
        ax.get_lines()[0].set_xdata(plot_esp_times_s[channel_index])
        ax.get_lines()[0].set_ydata(plot_data[channel_index])
        if enable_60hz_notch_filter and channel_index in esp_channels_to_filter:
          ax.get_lines()[1].set_xdata(plot_esp_times_s[channel_index])
          ax.get_lines()[1].set_ydata(plot_data_filtered[channel_index])
        ax.relim()
        ax.autoscale_view(scalex=True, scaley=True)
        # Plot FFT.
        if plot_fft:
          ax_fft = axs[channel_index][1]
          N = plot_lengths[channel_index]
          T = 1.0 / ecg_sampling_rates_hz[channel_index]
          yf = fftpack.fft(plot_data_filtered - np.mean(plot_data_filtered))
          xf = np.linspace(0.0, ecg_sampling_rates_hz[channel_index]/2, N//2)
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

#######################
###### SAVE DATA ######
#######################

# Compile metadata about the configuration.
metadata = {}
metadata['adc_gain'] = adc_gain
metadata['esp_baud_rate'] = esp_baud_rate
metadata['ecg_sampling_rates_hz'] = ecg_sampling_rates_hz
metadata['enable_60hz_notch_filter'] = enable_60hz_notch_filter
metadata['esp_channels_to_filter'] = esp_channels_to_filter
metadata['notch_N'] = notch_N
metadata['notch_frequencies_hz'] = notch_frequencies_hz
metadata['esp_channel_names'] = esp_channel_names
metadata['plot_duration_s'] = plot_duration_s

# Convert timestamps to readable strings.
times_str = [[get_time_str(t, format='%Y-%m-%d %H:%M:%S.%f') for t in time_s] for time_s in times_s]
# Save the data from each channel.
hout = h5py.File(hdf5_filepath, 'w')
for (channel_index, channel_name) in enumerate(esp_channel_names):
  group = hout.create_group(channel_name.replace(' ', '_').lower())
  group.create_dataset('data', data=np.array(data[channel_index]))
  if enable_60hz_notch_filter and channel_index in esp_channels_to_filter:
    group.create_dataset('data_filtered', data=np.array(data_filtered[channel_index]))
  group.create_dataset('esp_time_s', data=np.array(esp_times_s[channel_index]))
  group.create_dataset('time_s', data=np.array(times_s[channel_index]))
  group.create_dataset('time_str', dtype='S26', data=times_str[channel_index])
hout.attrs.update(metadata)
hout.close()

esp_serial.close()

print()
print('Close the plot to exit')
pickle.dump(fig, open(hdf5_filepath.replace('.hdf5', '.fig.pickle'), 'wb'))
plt.savefig(hdf5_filepath.replace('.hdf5', '.png'), dpi=300)
plt.savefig(hdf5_filepath.replace('.hdf5', '.pdf'))
plt.show()

fig, axs = plt.subplots(nrows=num_plot_rows, ncols=num_plot_cols,
                        squeeze=False, # if False, always return 2D array of axes
                        sharex=True, #sharey=True,
                        subplot_kw={'frame_on': True},
                        figsize=figure_size
                        )
figManager = plt.get_current_fig_manager()
figManager.window.showMaximized()
for channel_index in range(esp_num_channels):
  ax = axs[channel_index][0]
  ax.plot(np.array(esp_times_s[channel_index]) - esp_times_s[channel_index][0],
          data[channel_index], '-', linewidth=2)
  ax.grid(True, color='lightgray')
  ax.set_title(esp_channel_names[channel_index])
plt.suptitle(hdf5_filename)
plt.show(block=False)
time.sleep(1)
pickle.dump(fig, open(hdf5_filepath.replace('.hdf5', '_all.fig.pickle'), 'wb'))
plt.savefig(hdf5_filepath.replace('.hdf5', '_all.png'), dpi=300)
plt.savefig(hdf5_filepath.replace('.hdf5', '_all.pdf'))
plt.show()

print()








