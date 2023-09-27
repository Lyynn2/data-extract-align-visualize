
############
#
# Copyright (c) 2023 Joseph DelPreto / MIT CSAIL and Project CETI
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
# [can add additional updates and authors as desired]
#
############

from scipy.io import wavfile
from scipy import interpolate
from scipy import signal
import pysrt
import csv
import numpy as np
from operator import itemgetter
import re
import glob
from collections import OrderedDict

from helpers_synchronization import *
from helpers_various import *


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
# Will adjust timestamps to synchronize devices.
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
  annotation_start_times_perAudioFile_s = OrderedDict()
  annotation_end_times_perAudioFile_s = OrderedDict()
  
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
      # Get the start time of the file from its filename,
      #  and add the specified offset for this device to synchronize devices.
      start_time_s = get_time_s_from_filename(audio_filepath)
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
    # Store the start/end times of annotations for each audio file.
    annotation_start_times_perAudioFile_s.setdefault(audio_file_keyword, 9e9)
    annotation_end_times_perAudioFile_s.setdefault(audio_file_keyword, 0)
    annotation_start_times_perAudioFile_s[audio_file_keyword] = min(click_times_s_forCoda[0], annotation_start_times_perAudioFile_s[audio_file_keyword])
    annotation_end_times_perAudioFile_s[audio_file_keyword] = max(click_times_s_forCoda[-1], annotation_end_times_perAudioFile_s[audio_file_keyword])
    
  return (coda_start_times_s, coda_end_times_s, click_icis_s, click_times_s, whale_indexes,
          annotation_start_times_perAudioFile_s, annotation_end_times_perAudioFile_s)

############################################
# MAIN DATA/TIMESTAMP EXTRACTION
############################################

# Get the start time of a file from its filename.
# This timestamp will not be aligned to synchronize with other devices.
def get_time_s_from_filename(filepath):
  filename = os.path.basename(filepath)
  start_time_ms = int(re.search('\d{13}', filename)[0])
  start_time_s = start_time_ms/1000.0
  return start_time_s
  
# Get video, audio, or image data with associated aligned timestamps.
# Will create a dictionary with following structure:
#   [device_id][filepath] = (timestamps_s, data)
#   If filepath points to a video:
#     timestamps_s is a numpy array of epoch timestamps for every frame
#     data is a video reader object
#   If filepath points to a wav file:
#     timestamps_s is a numpy array of epoch timestamps for every sample
#     if requesting waveforms, data is a [num_samples x num_channels] matrix of audio data
#     if requesting spectrograms, data is a tuple with (spectrogram, spectrogram_t, spectrogram_f).
#   If filepath points to an image:
#     timestamps_s is a single-element numpy array with the epoch timestamps of the image
#     data is the filepath again
# @param data_root_dir The path to the root of the data directory,
#   which contains subfolders for each requested device.
# @param device_ids A list of device IDs for which to extract data.
#   Each ID should match the name of a subfolder in data_root_dir, but
#   for Misc devices, the keyword after "Misc/" will be used to find matching files in the Misc directory.
# @param device_friendlyName If provided, will print this name instead of the device ID.
# @param audio_type can be 'spectrogram' or 'waveform'
# @param audio_spectrogram_target_window_s The target window size if using a spectrogram.
# @param audio_resample_rate_hz If provided, will resample audio to this target rate.
# @param start_time_cutoff_s and end_time_cutoff_s [seconds since epoch]
#   If provided, will ignore media files that start after the end time or that end before the start time.
# @param video_target_width, video_target_height
#   specify target resolutions for reading videos.
def get_timestamped_data_audioVideoImage(data_root_dir, device_ids, device_friendlyNames=None,
                                         audio_type='spectrogram', audio_resample_rate_hz=None, audio_spectrogram_target_window_s=None,
                                         video_target_width=None, video_target_height=None,
                                         start_time_cutoff_s=None, end_time_cutoff_s=None,
                                         suppress_printing=False):
  media_infos = OrderedDict()
  
  for (device_index, device_id) in enumerate(device_ids):
    # Find data files for this device.
    if 'Misc' in device_id:
      data_dir = os.path.join(data_root_dir, 'Misc')
      filename_keyword = device_id.split('/')[1]
      filepaths = glob.glob(os.path.join(data_dir, '*%s*' % filename_keyword))
    else:
      data_dir = os.path.join(data_root_dir, device_id)
      filepaths = glob.glob(os.path.join(data_dir, '*'))
    filepaths = [filepath for filepath in filepaths if not os.path.isdir(filepath)]
    filepaths = [filepath for filepath in filepaths if is_video(filepath) or is_image(filepath) or is_audio(filepath)]
    if len(filepaths) == 0:
      continue
    
    # Skip files that start after the specified end time.
    # Do this now, so the below loop can know how many files there are (for printing purposes and whatnot).
    filepaths_toKeep = []
    if end_time_cutoff_s is not None and 'coda_annotations' not in device_id:
      for (file_index, filepath) in enumerate(filepaths):
        # Get the start time in epoch time
        start_time_s = get_time_s_from_filename(filepath)
        start_time_s = adjust_start_time_s(start_time_s, device_id)
        if start_time_s <= end_time_cutoff_s:
          filepaths_toKeep.append(filepath)
    else:
      filepaths_toKeep = filepaths
    print('Extracting from %4d files for device [%s] (ignored %d files starting after the end time)'
          % (len(filepaths_toKeep),
             device_friendlyNames[device_index] if device_friendlyNames is not None else device_id,
             len(filepaths) - len(filepaths_toKeep)))
    filepaths = filepaths_toKeep
  
    # Loop through each file to extract its timestamps and data pointers.
    media_infos[device_id] = {}
    for (file_index, filepath) in enumerate(filepaths):
      # Get the start time in epoch time from the filename.
      # Will add manual offsets to synchronize devices.
      if 'coda_annotations' not in device_id:
        start_time_s = get_time_s_from_filename(filepath)
        start_time_s = adjust_start_time_s(start_time_s, device_id)
      else:
        start_time_s = None
      
      # Process the data/timestamps for each file.
      
      if is_video(filepath):
        (video_reader, frame_rate, num_frames) = get_video_reader(filepath,
                                                                  target_width=video_target_width,
                                                                  target_height=video_target_height)
        # For drones, extract frame timestamps from an SRT file if one exists.
        # Otherwise, generate timestamps assuming a constant frame rate.
        drone_data = get_drone_srt_data(filepath)
        if drone_data is not None:
          timestamps_s = drone_data['timestamp_s']
          # Adjust for time zone offset, since the filename epochs correct for it
          #  but the SRT data does not.  So this will get us to the filename reference frame,
          #  and allow the manually specified offsets to apply.
          if not drone_srt_timestamps_are_local_time[device_id]:
            timestamps_s = timestamps_s + localtime_offset_s
          # Apply the manually specified offsets.
          start_timestamp_s = adjust_start_time_s(timestamps_s[0], device_id)
          timestamps_s = timestamps_s + (start_timestamp_s - timestamps_s[0])
        else:
          frame_duration_s = 1/frame_rate
          timestamps_s = start_time_s + np.arange(start=0, stop=num_frames)*frame_duration_s
        media_infos[device_id][filepath] = (timestamps_s, video_reader)
      
      elif is_image(filepath):
        timestamps_s = np.array([start_time_s])
        media_infos[device_id][filepath] = (timestamps_s, filepath)
      
      elif is_audio(filepath):
        if not suppress_printing:
          if file_index > 0:
            print('\r', end='')
          print('    Loading file %2d/%2d %s' % (file_index+1, len(filepaths), ' '*15), end='')
        (audio_rate, audio_data) = wavfile.read(filepath)
        num_samples = audio_data.shape[0]
        timestamps_s = start_time_s + np.arange(start=0, stop=num_samples)/audio_rate
        # Only process/store it if it is not excluded by a specified end time.
        audio_start_time_s = timestamps_s[0]
        audio_end_time_s = timestamps_s[-1]
        if (start_time_cutoff_s is not None and audio_end_time_s < start_time_cutoff_s) \
            or (end_time_cutoff_s is not None and audio_start_time_s > end_time_cutoff_s):
          if file_index == len(filepaths)-1 and not suppress_printing:
            print()
          continue
        # Resample the data.
        if audio_resample_rate_hz != audio_rate:
          if not suppress_printing:
            print('\r', end='')
            print('    Resampling file %2d/%2d %s' % (file_index+1, len(filepaths), ' '*15), end='')
          fn_interpolate_audio = interpolate.interp1d(
              timestamps_s,  # x values
              audio_data,    # y values
              axis=0,        # axis of the data along which to interpolate
              kind='linear', # interpolation method, such as 'linear', 'zero', 'nearest', 'quadratic', 'cubic', etc.
              fill_value='extrapolate' # how to handle x values outside the original range
          )
          num_samples = int(num_samples * (audio_resample_rate_hz/audio_rate))
          timestamps_s_resampled = start_time_s + np.arange(start=0, stop=num_samples)/audio_resample_rate_hz
          audio_data_resampled = fn_interpolate_audio(timestamps_s_resampled)
          audio_data = audio_data_resampled
          timestamps_s = timestamps_s_resampled
        # Compute a spectrogram of the entire file.
        if audio_type == 'spectrogram':
          if not suppress_printing:
            print('\r', end='')
            print('    Computing spectrogram for file %2d/%2d     ' % (file_index+1, len(filepaths)), end='')
          spectrogram_f, spectrogram_t, spectrogram = \
            signal.spectrogram(audio_data[:,0], audio_resample_rate_hz,
                               window=signal.get_window('tukey', int(audio_spectrogram_target_window_s * audio_resample_rate_hz)),
                               scaling='density',  # density or spectrum (default is density)
                               nperseg=None)
          # Determine epoch timestamps of each entry in the spectrogram.
          timestamps_s = spectrogram_t + timestamps_s[0]
          # Save the spectrogram information.
          media_infos[device_id][filepath] = (timestamps_s, (spectrogram, spectrogram_t, spectrogram_f))
        elif audio_type == 'waveform':
          media_infos[device_id][filepath] = (timestamps_s, audio_data)
        if file_index == len(filepaths)-1 and not suppress_printing:
          print()
  
  # Remove devices that were not requested or that had no data.
  device_ids_to_remove = []
  for (device_id, data) in media_infos.items():
    if len(data) == 0:
      device_ids_to_remove.append(device_id)
  if len(device_ids_to_remove) > 0:
    for device_id in device_ids_to_remove:
      del media_infos[device_id]
  
  # Return the completed dictionary of timestamps and data.
  return media_infos

# Get drone metadata with associated timestamps, including GPS and camera settings.
# Will create a dictionary with following structure:
#   [device_id][filepath] = (timestamps_s, data) where
#    timestamps_s is a numpy array of epoch timestamps for every frame and
#    data is a dictionary returned by get_drone_srt_data()
# @param data_root_dir The path to the root of the data directory,
#   which contains subfolders for each requested device.
# @param device_ids A list of device IDs for which to extract data.
#   Each ID should match the name of a subfolder in data_root_dir, but
#   for Misc devices, the keyword after "Misc/" will be used to find matching files in the Misc directory.
# @param device_friendlyName If provided, will print this name instead of the device ID.
# @param end_time_cutoff_s [seconds since epoch]
#   If provided, will ignore media files that start after the end time or that end before the start time.
def get_timestamped_data_drones(data_root_dir, device_ids, device_friendlyNames=None,
                                end_time_cutoff_s=None,
                                suppress_printing=False):
  drone_datas = OrderedDict()
  
  for (device_index, device_id) in enumerate(device_ids):
    # Find data files for this device.
    if 'Misc' in device_id:
      data_dir = os.path.join(data_root_dir, 'Misc')
      filename_keyword = device_id.split('/')[1]
      filepaths = glob.glob(os.path.join(data_dir, '*%s*' % filename_keyword))
    else:
      data_dir = os.path.join(data_root_dir, device_id)
      filepaths = glob.glob(os.path.join(data_dir, '*'))
    filepaths = [filepath for filepath in filepaths if not os.path.isdir(filepath)]
    filepaths = [filepath for filepath in filepaths if is_drone_data(filepath)]
    if len(filepaths) == 0:
      continue
    
    # Skip files that start after the specified end time.
    # Do this now, so the below loop can know how many files there are (for printing purposes and whatnot).
    filepaths_toKeep = []
    if end_time_cutoff_s is not None and 'coda_annotations' not in device_id:
      for (file_index, filepath) in enumerate(filepaths):
        # Get the start time in epoch time.
        # Will add manual offsets to synchronize devices.
        start_time_s = get_time_s_from_filename(filepath)
        start_time_s = adjust_start_time_s(start_time_s, device_id)
        if start_time_s <= end_time_cutoff_s:
          filepaths_toKeep.append(filepath)
    else:
      filepaths_toKeep = filepaths
    print('Extracting from %4d files for device [%s] (ignored %d files starting after the end time)'
          % (len(filepaths_toKeep),
             device_friendlyNames[device_index] if device_friendlyNames is not None else device_id,
             len(filepaths) - len(filepaths_toKeep)))
    filepaths = filepaths_toKeep
  
    # Loop through each file to extract its timestamps and data pointers.
    for (file_index, filepath) in enumerate(filepaths):
      # Process the data/timestamps for each file.
      if is_drone_data(filepath):
        drone_data = get_drone_srt_data(filepath)
        if drone_data is not None:
          timestamps_s = drone_data['timestamp_s']
          # Adjust for time zone offset, since the filename epochs correct for it
          #  but the SRT data does not.  So this will get us to the filename reference frame,
          #  and allow the manually specified offsets to apply.
          if not drone_srt_timestamps_are_local_time[device_id]:
            timestamps_s = timestamps_s + localtime_offset_s
          # Apply the manually specified offsets.
          start_timestamp_s = adjust_start_time_s(timestamps_s[0], device_id)
          timestamps_s = timestamps_s + (start_timestamp_s - timestamps_s[0])
          # Store the extracted timestamps and data.
          drone_data['original_timestamp_s'] = drone_data['timestamp_s'].copy()
          drone_data['original_timestamp_str'] = drone_data['timestamp_str'].copy()
          drone_data['aligned_timestamp_s'] = timestamps_s
          drone_data['aligned_timestamp_str'] = [time_s_to_str(timestamp_s, localtime_offset_s, localtime_offset_str) for timestamp_s in timestamps_s]
          del drone_data['timestamp_s']
          del drone_data['timestamp_str']
          drone_datas.setdefault(device_id, {})
          drone_datas[device_id][filepath] = (timestamps_s, drone_data)
  
  # Return the completed dictionary of timestamps and data.
  return drone_datas

# Get coda annotations and associated timestamps.
# Will create a dictionary combining data from all coda annotations.
#   All lists are the same length, with each entry describing the coda at that index.
#   The dictionary keys are as follows:
#     coda_start_times_s: each entry is a coda start time
#     coda_end_times_s  : each entry is a coda end time
#     click_icis_s  : each entry is a list of ICIs for that coda
#     click_times_s  : each entry is a list of click times for clicks in that coda
#     click_times_s  : each entry is a whale index; indexes over 20 indicate uncertain annotations (see Shane's readme for more information)
# @param data_root_dir The path to the root of the data directory,
#   which contains subfolders for each requested device.
# @param device_ids A list of device IDs for which to extract data.
#   Should be 'coda_annotations_biology' or 'coda_annotations_haifa'
#   If None, will include both annotation sources.
# @param device_friendlyName If provided, will print this name instead of the device ID.
def get_timestamped_data_codas(data_root_dir, device_ids=None, device_friendlyNames=None,
                               suppress_printing=False):
  
  codas_data = dict([(source, {'coda_start_times_s': [],
                               'coda_end_times_s': [],
                               'click_icis_s': [],
                               'click_times_s': [],
                               'whale_indexes': [],
                               }) for source in ['biology', 'haifa']])
  codas_files_start_times_s = dict([(source, []) for source in ['biology', 'haifa']])
  codas_files_end_times_s = dict([(source, []) for source in ['biology', 'haifa']])
  if device_ids is None:
    device_ids = ['coda_annotations_biology', 'coda_annotations_haifa']
  
  for (device_index, device_id) in enumerate(device_ids):
    # Find data files for this device.
    if 'Misc' in device_id:
      data_dir = os.path.join(data_root_dir, 'Misc')
      filename_keyword = device_id.split('/')[1]
      filepaths = glob.glob(os.path.join(data_dir, '*%s*' % filename_keyword))
    else:
      data_dir = os.path.join(data_root_dir, device_id)
      filepaths = glob.glob(os.path.join(data_dir, '*'))
    filepaths = [filepath for filepath in filepaths if not os.path.isdir(filepath)]
    filepaths = [filepath for filepath in filepaths if is_coda_annotations(filepath)]
    if len(filepaths) == 0:
      continue
    
    # Skip files that start after the composite video ends.
    # Do this now, so the below loop can know how many files there are (for printing purposes and whatnot).
    print('Extracting from %4d files for device [%s]' % (len(filepaths), device_friendlyNames[device_index] if device_friendlyNames is not None else device_id,))
  
    # Loop through each file to extract its timestamps and data pointers.
    for (file_index, filepath) in enumerate(filepaths):
      if is_coda_annotations(filepath):
        # Get coda annotations and timestamps for this CSV file.
        (coda_start_times_s, coda_end_times_s, click_icis_s, click_times_s, whale_indexes,
         annotation_start_times_perAudioFile_s, annotation_end_times_perAudioFile_s) = \
          get_coda_annotations(filepath, data_root_dir, adjust_start_time_s)
        if '_coda_annotations_biology' in data_dir.lower():
          source = 'biology'
        elif '_coda_annotations_haifa' in data_dir.lower():
          source = 'haifa'
        else:
          raise AssertionError('Unknown coda annotations source for [%s]' % filepath)
        codas_data[source]['coda_start_times_s'].extend(coda_start_times_s)
        codas_data[source]['coda_end_times_s'].extend(coda_end_times_s)
        codas_data[source]['click_icis_s'].extend(click_icis_s)
        codas_data[source]['click_times_s'].extend(click_times_s)
        codas_data[source]['whale_indexes'].extend(whale_indexes)
        if len(click_times_s) > 0:
          codas_files_start_times_s[source].extend(list(annotation_start_times_perAudioFile_s.values()))
          codas_files_end_times_s[source].extend(list(annotation_end_times_perAudioFile_s.values()))
  
  # Remove sources that were not requested or that had no data.
  sources_to_remove = []
  for (source, data) in codas_data.items():
    if len(data['coda_start_times_s']) == 0 and len(codas_files_start_times_s[source]) == 0:
      sources_to_remove.append(source)
  if len(sources_to_remove) > 0:
    for source in sources_to_remove:
      del codas_data[source]
      del codas_files_start_times_s[source]
      del codas_files_end_times_s[source]
      
  # Return the completed set of coda annotations.
  return (codas_data, codas_files_start_times_s, codas_files_end_times_s)
      
