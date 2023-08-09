


from moviepy.editor import VideoFileClip, AudioFileClip, CompositeAudioClip
import proglog
from scipy.io import wavfile
import os
import glob
import re
import time

data_dir_root = 'C:/Users/jdelp/Desktop/_whale_birthday_s3_data'
audio_dir = os.path.join(data_dir_root, 'DSWP-KASHMIR_MIXPRE6-1')

video_filepath = os.path.join(data_dir_root,
                              # 'composite_video_fps10_duration10_start1688831625000_colWidth300_withAudio.mp4'
                              # 'composite_video_fps10_duration3000_start1688830500000_colWidth300_new_withAudio-gain40_compressed.mp4'
                              'composite_video_fps10_duration10_start1688831625000_colWidth300.mp4'
                              )
# output_video_filepath = '%s_compressedPython%s' % os.path.splitext(video_filepath)
output_video_filepath = os.path.join(data_dir_root,
                                     # 'composite_video_fps10_duration10_start1688831625000_colWidth300_withAudio.mp4'
                                     # 'composite_video_fps10_duration3000_start1688830500000_colWidth300_new_withAudio-gain40_compressed.mp4'
                                     'composite_video_fps10_duration10_start1688831625000_colWidth300_compressed0-50MBs.mp4'
                                     )

target_total_rate_MB_s = 0.5


import os, ffmpeg
def compress_video(video_full_path, output_file_name, target_total_bitrate):
  # Reference: https://en.wikipedia.org/wiki/Bit_rate#Encoding_bit_rate
  min_audio_bitrate = 32000
  max_audio_bitrate = 256000
  
  # Open a probe to the input video.
  probe = ffmpeg.probe(video_full_path)
  
  # Check if ausio will be included.
  audio_streams = [s for s in probe['streams'] if s['codec_type'] == 'audio']
  if len(audio_streams) > 0:
    audio_bitrate = sum(float(audio_stream['bit_rate']) for audio_stream in audio_streams)

    if 10 * audio_bitrate > target_total_bitrate:
      audio_bitrate = target_total_bitrate / 10
    if audio_bitrate < min_audio_bitrate < target_total_bitrate:
      audio_bitrate = min_audio_bitrate
    elif audio_bitrate > max_audio_bitrate:
      audio_bitrate = max_audio_bitrate
    
    video_bitrate = target_total_bitrate - audio_bitrate
  else:
    audio_bitrate = None
    video_bitrate = target_total_bitrate
  
  # Compress!
  i = ffmpeg.input(video_full_path)
  # Pass 1
  ffmpeg_args = {
    'c:v': 'libx264', 
    'b:v': video_bitrate, 
    'pass': 1, 
    'f': 'mp4', 
    'loglevel':'quiet',
  }
  ffmpeg.output(i, os.devnull,
                **ffmpeg_args
                ).overwrite_output().run()
  # Pass 2
  ffmpeg_args = {
    'c:v': 'libx264',
    'b:v': video_bitrate,
    'pass': 2,
    'c:a': 'aac',
    'loglevel': 'quiet',
  }
  if len(audio_streams) > 0:
    ffmpeg_args['b:a'] = audio_bitrate
  ffmpeg.output(i, output_file_name,
                **ffmpeg_args
                ).overwrite_output().run()




compress_video(video_filepath, output_video_filepath, target_total_rate_MB_s*1024*1024*8)



