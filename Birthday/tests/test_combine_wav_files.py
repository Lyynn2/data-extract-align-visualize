
import os
import glob
import numpy as np
from scipy.io import wavfile
import re

data_dir_root = 'C:/Users/jdelp/Desktop/_whale_birthday_s3_data'
wav_file_dir = os.path.join(data_dir_root, 'DSWP-KASHMIR_MIXPRE6-1')

epoch_offset_toAdd_s = 0
audio_rate = 96000
audio_num_channels = 2
audio_bitdepth_bytes = 2

wav_filepaths = sorted(glob.glob(os.path.join(wav_file_dir, '*.wav')))

combined_wavs = []
combined_start_timestamp_s = None
previous_end_time_s = None
import pydub
mp3_filepaths = []
for wav_filepath in wav_filepaths:
  print('Loading file', os.path.basename(wav_filepath), end='')
  # Get the start time in epoch time.
  filename = os.path.basename(wav_filepath)
  start_time_ms = int(re.search('\d{13}', filename)[0])
  start_time_s = start_time_ms/1000.0
  start_time_s += epoch_offset_toAdd_s
  # # Get the audio data.
  # (audio_rate_forFile, audio_data) = wavfile.read(wav_filepath)
  # assert(audio_rate == audio_rate_forFile)
  # assert(audio_num_channels == audio_data.shape[1])
  # num_samples = audio_data.shape[0]

  # mp3_output_filepath =  wav_filepath.lower().replace('.wav', '.mp3')
  # print('Writing data to', mp3_output_filepath)
  # song = pydub.AudioSegment(audio_data.tobytes(), frame_rate=audio_rate,
  #                           sample_width=audio_bitdepth_bytes, channels=audio_num_channels)
  # song.export(mp3_output_filepath, format="mp3", bitrate="320k")

  # # Get timestamps for each sample.
  # timestamps_s = start_time_s + np.arange(start=0, stop=num_samples)/audio_rate
  # Initialize the combined information if needed.
  if len(combined_wavs) == 0:
    # combined_wavs.append(audio_data)
    # combined_start_timestamp_s = timestamps_s[0]
    mp3_filepaths.append(wav_filepath.lower().replace('.wav', '.mp3'))
  else:
    # # Measure the gap between this file and the previous file.
    # pad_duration_s = timestamps_s[0] - previous_end_time_s
    # if pad_duration_s < 0:
    #   raise AssertionError('The wav files are overlapping!')
    # # Determine the number of samples needed to fill the gap.
    # #   Note that if they were spaced by 1/audio_rate, no padding is needed (hence the -1 below).
    # num_pad_samples = round((pad_duration_s*audio_rate) - 1)
    # pad_start_time_s = previous_end_time_s + 1/audio_rate
    # pad_timestamps_s = pad_start_time_s + np.arange(start=0, stop=num_pad_samples)/audio_rate
    # pad_data = np.zeros((num_pad_samples, audio_num_channels))
    # print(' | padded %5.1fs | gap from previous to pad: %0.1f us | gap from pad to current: %0.1f us'
    #       % (pad_duration_s, 1e6 * (timestamps_s[0] - pad_timestamps_s[-1]), 1e6 * (pad_timestamps_s[0] - previous_end_time_s)),
    #       end='')
    # # Combine the data.
    # combined_wavs.append(pad_data)
    # combined_wavs.append(audio_data)
    # # combined_wav = np.vstack([combined_wav,
    # #                           np.zeros((num_pad_samples, audio_num_channels)),
    # #                           audio_data])
    #
    # # wavfile.write( wav_filepath.lower().replace('.wav', '_pad.wav'), audio_rate, pad_data)
    #
    # # mp3_output_filepath =  wav_filepath.lower().replace('.wav', '_pad.mp3')
    # # print('Writing data to', mp3_output_filepath)
    # # song = pydub.AudioSegment(pad_data.tobytes(), frame_rate=audio_rate,
    # #                           sample_width=audio_bitdepth_bytes, channels=audio_num_channels)
    # # song.export(mp3_output_filepath, format="mp3", bitrate="320k")

    mp3_filepaths.append(wav_filepath.lower().replace('.wav', '_pad.mp3'))
    mp3_filepaths.append(wav_filepath.lower().replace('.wav', '.mp3'))
    
  # previous_end_time_s = timestamps_s[-1]
  # print()
print()

# # Concatenate the data.
# # Doing this once at the end is faster than doing it in the loop since it only creates one new array.
# print('Concatenating all data')
# combined_wav = np.vstack(combined_wavs)
# # print('max', np.amax(combined_wav))
# # print('min', np.amin(combined_wav))
# # print('nan', np.sum(np.isnan(combined_wav), axis=0))


# # Save the combined wav file.
# combined_wav_filepath = os.path.join(wav_file_dir, 'combined_audio_%d.wav' % (combined_start_timestamp_s*1000))
# print('Writing combined data to', combined_wav_filepath)
# wavfile.write(combined_wav_filepath, int(audio_rate/2), combined_wav[0::2, :])

# import pydub
# combined_output_filepath = os.path.join(wav_file_dir, 'combined_audio_%d_part01.mp3' % (combined_start_timestamp_s*1000))
# print('Writing combined data to', combined_output_filepath)
# song = pydub.AudioSegment(combined_wav[0:int(combined_wav.shape[0]/4),:].tobytes(), frame_rate=audio_rate,
#                           sample_width=audio_bitdepth_bytes, channels=audio_num_channels)
# song.export(combined_output_filepath, format="mp3", bitrate="320k")

print('Done!')
print()


combined_audioSegment = None
for (i, mp3_filepath) in enumerate(mp3_filepaths):
  print(i, len(mp3_filepaths))
  if combined_audioSegment is None:
    combined_audioSegment = pydub.AudioSegment.from_file(mp3_filepath, format='mp3')
  else:
    combined_audioSegment += pydub.AudioSegment.from_file(mp3_filepath, format='mp3')
file_handle = combined_audioSegment.export(os.path.join(data_dir_root, '_pydub_combined.mp3'), format="mp3")