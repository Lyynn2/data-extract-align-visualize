
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

from collections import OrderedDict
from helpers_data_extraction import *

############################################
# CONFIGURATION
############################################

# The path to the root of the data directory,
#   which contains subfolders for each requested device.
data_root_dir = 'C:/Users/jdelp/Desktop/_whale_birthday_s3_data'

# A start and end time if desired.
# If specified, will ignore wav files outside this range.
# The example range below essentially selects file 280.
start_time_cutoff_s = time_str_to_time_s('2023-07-08 11:53:34.72 -0400')
end_time_cutoff_s = start_time_cutoff_s + 184

# Whether to extract raw audio data, or a spectrogram.
audio_data_type = 'waveform' # 'waveform' or 'spectrogram'

# A rate to which the audio data should be resampled, if desired.
audio_resample_rate_hz = 96000

# The target window size if requesting a spectrogram.
# Note that the achieved window may be a bit different.
#  The achieved window size can be computed as the difference between times in the returned spectrogram_t vector.
audio_spectrogram_target_window_s = 0.03
audio_spectrogram_window_s = None # will be set to the achieved window size
# The desired frequency range if requesting a spectrogram.
audio_spectrogram_frequency_range = [0e3, min(40e3, audio_resample_rate_hz//2)]

# The device IDs from which to extract data.
device_ids = ['DSWP-KASHMIR_MIXPRE6-1']

############################################
# EXTRACT DATA
############################################

# Will create a dictionary with the following structure:
#   [device_id][wav_filepath] = (timestamps_s, data) where
#     timestamps_s is a numpy array of epoch timestamps for every sample
#     If requesting waveforms, data is an [num_samples x num_channels] matrix of audio data
#     If requesting spectrograms, data is a tuple with (spectrogram, spectrogram_t, spectrogram_f).
audio_datas = OrderedDict()

print()
print('Getting timestamps and data for every audio sample')
for device_id in device_ids:
  # Extract the timestamped data for this device.
  media_info = get_timestamped_data_audioVideoImage(
                data_root_dir, [device_id], device_friendlyNames=None,
                audio_type=audio_data_type, audio_resample_rate_hz=audio_resample_rate_hz,
                audio_spectrogram_target_window_s=audio_spectrogram_target_window_s,
                start_time_cutoff_s=start_time_cutoff_s, end_time_cutoff_s=end_time_cutoff_s,
                suppress_printing=False)
    
  # Perform any additional processing on the data if desired,
  #  then store it in the appropriate dictionary.
  if device_id in media_info:
    audio_datas[device_id] = {}
    for (filepath, (timestamps_s, data)) in media_info[device_id].items():
      if audio_data_type == 'spectrogram':
        # Get the computed spectrogram of the entire file.
        (spectrogram, spectrogram_t, spectrogram_f) = data
        # Determine epoch timestamps of each entry in the spectrogram.
        timestamps_s = spectrogram_t + timestamps_s[0]
        # Truncate to the desired frequency range.
        min_f_index = spectrogram_f.searchsorted(audio_spectrogram_frequency_range[0])
        max_f_index = spectrogram_f.searchsorted(audio_spectrogram_frequency_range[-1])
        spectrogram_f = spectrogram_f[min_f_index:(max_f_index+1)]
        spectrogram = spectrogram[min_f_index:max_f_index, :]
        # Compute the achieved window size.
        audio_spectrogram_window_s = np.round(np.mean(np.diff(spectrogram_t)), 6)
        # Save the information
        audio_datas[device_id][filepath] = (timestamps_s, (spectrogram, spectrogram_t, spectrogram_f))
      else:
        audio_datas[device_id][filepath] = (timestamps_s, data)
  
############################################
# SAMPLE USAGE
############################################

print()
print('='*50)
print()

for device_id in audio_datas:
  print('See device id: %s' % device_id)
  for (filepath, (timestamps_s, data)) in audio_datas[device_id].items():
    print('  See data for file   : %s' % filepath)
    print('    Start time of file: %0.3f s | %s' % (timestamps_s[0], time_s_to_str(timestamps_s[0], localtime_offset_s, localtime_offset_str)))
    print('    End time of file  : %0.3f s | %s' % (timestamps_s[-1], time_s_to_str(timestamps_s[-1], localtime_offset_s, localtime_offset_str)))
    if audio_data_type == 'waveform':
      print('    Number of samples : %d' % (len(timestamps_s)))
      print('    Number of channels: %d' % (data.shape[1]))
      print('    Duration          : %0.3f s' % (timestamps_s[-1] - timestamps_s[0]))
      print('    Sampling rate     : %0.2f Hz' % ((data.shape[0]-1)/(timestamps_s[-1] - timestamps_s[0])))
      print('    Size of data      : %s' % (str(data.shape)))
    if audio_data_type == 'spectrogram':
      (spectrogram, spectrogram_t, spectrogram_f) = data
      print('    Spectrogram window size    : %g s' % (audio_spectrogram_window_s))
      print('    Number of time windows     : %s' % (spectrogram.shape[1]))
      print('    Number of frequency bins   : %s' % (spectrogram.shape[0]))
      print('    Size of spectrogram matrix : %s' % (str(spectrogram.shape)))
      print('    Size of spectrogram t array: %s' % (spectrogram_t.shape))
      print('    Size of spectrogram f array: %s' % (spectrogram_f.shape))
