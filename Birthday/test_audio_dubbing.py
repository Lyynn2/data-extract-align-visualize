
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
                              'composite_video_fps10_duration3000_start1688830500000_colWidth300.mp4'
                              # 'composite_video_fps10_duration10_start1688831625000_colWidth300.mp4'
                              )
output_video_filepath = '%s_withAudioPython%s' % os.path.splitext(video_filepath)
output_audio_filepath = '%s.m4a' % os.path.splitext(output_video_filepath)[0]
save_output_audio = True

volume_gain_factor = 50

# Get the video start time
video_filename = os.path.basename(video_filepath)
video_start_time_ms = int(re.search('\d{13}', video_filename)[0])
video_start_time_s = video_start_time_ms/1000.0

# Load the video
t0 = time.time()
video_clip = VideoFileClip(video_filepath, audio=False)
video_end_time_s = video_start_time_s + video_clip.duration
print('See video %s spanning times [%d, %d]' % (video_filename, video_start_time_s, video_end_time_s))

# Find audio files that overlap with the video.
print('Searching for audio files that overlap with the video')
audio_clips = []
for audio_filepath in glob.glob(os.path.join(audio_dir, '*.wav')):
  audio_filename = os.path.basename(audio_filepath)
  audio_start_time_ms = int(re.search('\d{13}', audio_filename)[0])
  audio_start_time_s = audio_start_time_ms/1000.0
  (audio_rate, audio_data) = wavfile.read(audio_filepath)
  audio_duration_s = (audio_data.shape[0]-1)/audio_rate
  audio_end_time_s = audio_start_time_s + audio_duration_s
  
  audio_clip = None
  # Compute how far into the audio clip the video clip starts.
  # Being negative would imply the audio starts inside video, so the audio start should not be clipped.
  audio_clip_start_offset_s = max(0.0, video_start_time_s - audio_start_time_s)
  # Compute the duration of the audio that would align it with the end of the video.
  # Being longer than the audio duration implies the audio ends inside the video, so the audio end should not be clipped.
  audio_clip_duration_s = min(audio_duration_s, video_end_time_s - audio_start_time_s)
  audio_clip_duration_s -= audio_clip_start_offset_s
  # Load the audio segment if it is valid (if the audio file overlaps with the video).
  if audio_clip_duration_s > 0:
    audio_clip = AudioFileClip(audio_filepath).subclip(t_start=audio_clip_start_offset_s,
                                                       t_end=audio_clip_start_offset_s+audio_clip_duration_s)
    
    # Compute the video time at which this audio clip should start.
    audio_clip_start_time_s = audio_start_time_s + audio_clip_start_offset_s
    audio_video_start_offset_s = audio_clip_start_time_s - video_start_time_s
    audio_clip = audio_clip.set_start(audio_video_start_offset_s)
    print('  Found %s spanning [%d, %d] > placed segment [%6.1f, %6.1f] at video time %5ds'
          % (audio_filename, audio_start_time_s, audio_end_time_s,
             audio_clip_start_offset_s, audio_clip_start_offset_s+audio_clip_duration_s,
             audio_video_start_offset_s))
    
    # Store the audio clip.
    audio_clips.append(audio_clip)
  
# Create the composite audio.
print('Adding %d audio clips to the video' % (len(audio_clips)))
composite_audio_clip = CompositeAudioClip(audio_clips)
composite_audio_clip = composite_audio_clip.volumex(volume_gain_factor)
video_clip = video_clip.set_audio(composite_audio_clip)
video_clip.write_videofile(output_video_filepath,
                           verbose=False,
                           logger=proglog.TqdmProgressBarLogger(print_messages=False),
                           # codec='libx264',
                           audio_codec='aac',
                           temp_audiofile=output_audio_filepath,
                           remove_temp=(not save_output_audio),
                           )


print()
print('Done!')
print()




