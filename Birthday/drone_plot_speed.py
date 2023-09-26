
import h5py
import numpy as np
import os
from collections import OrderedDict

from ThreadedVideoWriter import ThreadedVideoWriter

from helpers_synchronization import *
from helpers_various import *

##############################################################
# Specify the filepath for each drone's HDF5 file of metadata.
##############################################################
data_root_dir = 'C:/Users/jdelp/Desktop/_whale_birthday_s3_data'
drone_metadata_filepaths = OrderedDict([
  # Map from device ID to its HDF5 filepath.
  ('DSWP-DJI_MAVIC3-2', os.path.join(data_root_dir, 'DSWP-DJI_MAVIC3-2', 'DSWP-DJI_MAVIC3-2_metadata.hdf5')),
  ('CETI-DJI_MAVIC3-1', os.path.join(data_root_dir, 'CETI-DJI_MAVIC3-1', 'CETI-DJI_MAVIC3-1_metadata.hdf5')),
  ])

output_video_filepath = os.path.join(data_root_dir, 'drone_paths.mp4')

############################################
# Happy analyzing!
############################################

all_times_s = OrderedDict([(device_id, []) for device_id in drone_metadata_filepaths])
all_latitudes = OrderedDict([(device_id, []) for device_id in drone_metadata_filepaths])
all_longitudes = OrderedDict([(device_id, []) for device_id in drone_metadata_filepaths])
for (device_id, drone_metadata_filepath) in drone_metadata_filepaths.items():
  print()
  print('Loading data for device %s' % device_id)
  # Open the HDF5 file.
  h5file = h5py.File(drone_metadata_filepath, 'r')
  # The top-level keys of the file are the corresponding video filenames.
  video_filenames = list(h5file.keys())
  print('  See metadata for %d videos' % (len(video_filenames)))
  
  for video_filename in video_filenames:
    # Load the global timestamps for each frame of the video.
    # Timestamps have been adjusted to be synchronized based on the current manual estimates.
    timestamps_s   = np.array(h5file[video_filename]['time']['aligned_timestamp_s'])
    timestamps_str = np.array(h5file[video_filename]['time']['aligned_timestamp_str'])
    # The HDF5 file also has original timestamps recorded by the drone during filming.
    # These are not aligned using the manual offsets, and they may not account for time zone offsets.
    original_timestamps_s   = np.array(h5file[video_filename]['time']['original_timestamp_s'])
    original_timestamps_str   = np.array(h5file[video_filename]['time']['original_timestamp_str'])
    
    # Load data about the drone's position.
    altitudes_absolute_m = np.array(h5file[video_filename]['position']['altitude_absolute_m'])
    altitudes_relative_m = np.array(h5file[video_filename]['position']['altitude_relative_m'])
    latitudes            = np.array(h5file[video_filename]['position']['latitude'])
    longitudes           = np.array(h5file[video_filename]['position']['longitude'])
    # Note that there is 1 frame where the latitude was 0;
    #  presumably this is used to indicate a sensor error.
    latitudes[np.where(latitudes == 0)[0]] = np.nan
    longitudes[np.where(longitudes == 0)[0]] = np.nan
    
    # Load data about the camera settings.
    color_modes        = np.array(h5file[video_filename]['camera']['color_mode'])
    color_temperatures = np.array(h5file[video_filename]['camera']['color_temperature'])
    exposure_values    = np.array(h5file[video_filename]['camera']['exposure_value'])
    f_numbers          = np.array(h5file[video_filename]['camera']['f_number'])
    focal_lengths      = np.array(h5file[video_filename]['camera']['focal_length'])
    isos               = np.array(h5file[video_filename]['camera']['iso'])
    shutters           = np.array(h5file[video_filename]['camera']['shutter'])
    
    # Store the desired data.
    all_times_s[device_id].append(np.array(timestamps_s))
    all_latitudes[device_id].append(np.array(latitudes))
    all_longitudes[device_id].append(np.array(longitudes))

drone_plot_reference_location_lonLat = [-61.373179, 15.306914] # will plot meters from this location (the Mango house)
conversion_factor_lat_to_km = (111.32) # From simplified Haversine formula: https://stackoverflow.com/a/39540339
conversion_factor_lon_to_km = (40075 * np.cos(np.radians(drone_plot_reference_location_lonLat[1])) / 360) # From simplified Haversine formula: https://stackoverflow.com/a/39540339
drone_lat_to_km = lambda lat:  (lat - drone_plot_reference_location_lonLat[1])*conversion_factor_lat_to_km
drone_lon_to_km = lambda lon:  (lon - drone_plot_reference_location_lonLat[0])*conversion_factor_lon_to_km

import matplotlib
import matplotlib.pyplot as plt

def moving_average(time_s, x, window_duration_s, centering):
  Fs = 1/np.mean(np.diff(time_s))
  window_length = min(len(x), round(window_duration_s*Fs))
  window = np.ones((window_length,))
  moving_average = np.convolve(x, window, 'valid')/len(window)
  if centering == 'leading':
    return (time_s[0:(time_s.shape[0] - len(window) + 1)], moving_average)
  elif centering == 'trailing':
    return (time_s[len(window)-1:], moving_average)
  elif centering == 'centered':
    start_index = round((len(window)-1)/2)
    end_index = start_index + moving_average.shape[0]
    return (time_s[start_index:end_index], moving_average)

def rising_edges(x, threshold=0.5, include_first_step_if_high=False, include_last_step_if_low=False):
  if not isinstance(x, np.ndarray):
    x = np.array(x)
  # Copied from https://stackoverflow.com/a/50365462
  edges = list(np.flatnonzero((x[:-1] < threshold) & (x[1:] > threshold))+1)
  if x[0] > threshold and include_first_step_if_high:
    edges = [0] + edges
  if x[-1] < threshold and include_last_step_if_low:
    edges = edges + [len(x)-1]
  return np.array(edges)
def falling_edges(x, threshold=0.5, include_first_step_if_low=False, include_last_step_if_high=False):
  if not isinstance(x, np.ndarray):
    x = np.array(x)
  edges = list(np.flatnonzero((x[:-1] > threshold) & (x[1:] < threshold))+1)
  if x[0] < threshold and include_first_step_if_low:
    edges = [0] + edges
  if x[-1] > threshold and include_last_step_if_high:
    edges = edges + [len(x)-1]
  return np.array(edges)
  
print()
moving_average_window_duration_s = 1
for device_id in all_times_s:
  # fig_speed = plt.figure()
  # fig_stationary = plt.figure()
  fig, axs = plt.subplots(nrows=2, ncols=1,
                         squeeze=False, # if False, always return 2D array of axes
                         sharex=True, sharey=False,
                         subplot_kw={'frame_on': True},
                         figsize=(4,6),
                         )
  print('See device %s' % device_id)
  stationary_durations_s = []
  moving_durations_s = []
  for file_index in range(len(all_times_s[device_id])):
    #print('Computing speed for device %s file %02d' % (device_id, file_index))
    time_s = all_times_s[device_id][file_index]
    latitudes = all_latitudes[device_id][file_index]
    longitudes = all_longitudes[device_id][file_index]
    x_m = [drone_lon_to_km(x)*1000.0 for x in longitudes]
    y_m = [drone_lat_to_km(x)*1000.0 for x in latitudes]
    # plt.plot(time_s, x_m, '.-')
    # (time_s_x, x_m) = moving_average(time_s, x_m, moving_average_window_duration_s, 'centered')
    # plt.plot(time_s_x, x_m, '.-')
    (_, x_m) = moving_average(time_s, x_m, moving_average_window_duration_s, 'centered')
    (time_s, y_m) = moving_average(time_s, y_m, moving_average_window_duration_s, 'centered')
    # (time_s_y, y_m) = moving_average(time_s, y_m, moving_average_window_duration_s, 'leading')
    dx_m = np.diff(x_m)
    dy_m = np.diff(y_m)
    dt_s = np.diff(time_s)
    speed_m_s = np.sqrt(np.square(dx_m) + np.square(dy_m))
    # plt.figure(fig_speed)
    axs[0][0].plot(time_s[1:], speed_m_s, '-')
    axs[0][0].grid(True, color='lightgray')
    
    is_stationary = speed_m_s == 0
    is_moving = speed_m_s > 0
    stationary_startEnd_times_s = np.vstack(
        [rising_edges(is_stationary, include_first_step_if_high=True),
         falling_edges(is_stationary, include_last_step_if_high=True)]).T
    stationary_durations_s.extend(np.diff(stationary_startEnd_times_s, axis=1)*np.mean(dt_s))
    
    moving_startEnd_times_s = np.vstack(
        [rising_edges(is_moving, include_first_step_if_high=True),
         falling_edges(is_moving, include_last_step_if_high=True)]).T
    moving_durations_s.extend(np.diff(moving_startEnd_times_s, axis=1)*np.mean(dt_s))
    
    # plt.figure(fig_stationary)
    axs[1][0].plot(time_s[1:], is_stationary, '-')
    axs[1][0].fill_between(x= time_s[1:],
                           y1= is_stationary,
                           alpha= 0.2)
    axs[1][0].grid(True, color='lightgray')
  
  print('  Average stationary duration [s]: %0.3f +- %0.3f' % (np.mean(stationary_durations_s),
                                                               np.std(stationary_durations_s)))
  print('  Average moving duration [s]    : %0.3f +- %0.3f' % (np.mean(moving_durations_s),
                                                               np.std(moving_durations_s)))
  # fig, axs = plt.subplots(nrows=1, ncols=2,
  #                        squeeze=False, # if False, always return 2D array of axes
  #                        sharex=False, sharey=True,
  #                        subplot_kw={'frame_on': True},
  #                        figsize=(4,6),
  #                        )
  # axs[0][0].hist(stationary_durations_s)
  # axs[0][1].hist(moving_durations_s)
  # axs[0][0].set_title('Stationary Durations')
  # axs[0][1].set_title('Moving Durations')
  # plt.figure(fig_stationary)
  axs[1][0].set_title('%s: Is Stationary' % device_id)
  axs[1][0].set_xlabel('Epoch Timestamp [s]')
  # plt.figure(fig_speed)
  axs[0][0].set_title('%s: Speed' % device_id)
  # axs[0][0].set_xlabel('Epoch Timestamp [s]')
  axs[0][0].set_ylabel('Speed [m/s]')
  
plt.show()

print()
