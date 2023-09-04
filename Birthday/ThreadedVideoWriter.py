
import cv2
from threading import Thread
import os
import time

class ThreadedVideoWriter:
  
  #########################################
  # Initialization
  #########################################
  def __init__(self, output_filepath,
               frame_width=None, frame_height=None, frame_rate=None,
               max_buffered_frames=10, overwrite_existing_video=False,
               copy_added_frames=True):
    self.set_output_filepath(output_filepath, overwrite_existing_video)
    self.set_frame_size(frame_width, frame_height)
    self.set_frame_rate(frame_rate)
    self.set_max_buffered_frames(max_buffered_frames)
    self.set_copy_added_frames(copy_added_frames)
    self._frame_buffer = []
    self._next_frame_index_toWrite = 0
    self._next_frame_index_toAdd = 0
    self._video_writer = None
    self._writing_thread = None
    self._active = False
    
  def set_max_buffered_frames(self, max_buffered_frames):
    self._max_buffered_frames = max_buffered_frames
    
  def set_frame_size(self, frame_width, frame_height):
    self._frame_width = frame_width
    self._frame_height = frame_height
    
  def set_frame_rate(self, frame_rate):
    self._frame_rate = frame_rate
    
  def set_copy_added_frames(self, copy_added_frames):
    self._copy_added_frames = copy_added_frames
    
  def set_output_filepath(self, output_filepath, overwrite_existing_video=False):
    if not overwrite_existing_video:
      if os.path.exists(output_filepath):
        raise AssertionError('Desired output video already exists: [%s]' % output_filepath)
    self._output_filepath = output_filepath
  
  #########################################
  # Write a video!
  #########################################
  
  def _init_writer(self):
    #print('Creating video writer!')
    video_extension =  os.path.splitext(self._output_filepath)[-1].lower()
    if '.mp4' == video_extension:
      fourcc = 'MP4V'
    elif '.avi' == video_extension:
      fourcc = 'MJPG'
    else:
      raise ValueError('Unknown video extension: [%s]' % video_extension)
    if self._output_filepath is None:
      raise ValueError('No output video filepath has been specified.')
    if self._frame_rate is None:
      raise ValueError('No output video frame rate has been specified.')
    if self._frame_width is None or self._frame_height is None:
      raise ValueError('The output video frame size has not been fully specified.')
    self._video_writer = cv2.VideoWriter(self._output_filepath,
                                         cv2.VideoWriter_fourcc(*fourcc),
                                         self._frame_rate,
                                         (self._frame_width, self._frame_height))
  
  def _start_thread(self):
    #print('Creating thread!')
    self._frame_buffer = [None]*self._max_buffered_frames
    self._next_frame_index_toWrite = 0
    self._next_frame_index_toAdd = 0
    self._active = True
    self._writing_thread = Thread(target=self._write_frames_thread_fn)
    self._writing_thread.start()
    
  def add_frame(self, frame):
    # Create a video writer if this is the first frame.
    if self._video_writer is None:
      if self._frame_width is None or self._frame_height is None:
        self.set_frame_size(frame_width=frame.shape[1], frame_height=frame.shape[0])
      self._init_writer()
    
    # Create and start a writing thread if this is the first frame.
    if self._writing_thread is None:
      self._start_thread()
    
    # t00 = time.time()
    # Make a copy of the frame, so the caller can continue editing their array
    #  without affecting the one in our queue.
    # Do this now, so it subtracts from the time we may need to wait below
    #  in the case that the buffer is full.
    if self._copy_added_frames:
      # frame_toAdd = np.empty_like(frame)
      # np.copyto(frame_toAdd, frame)
      frame_toAdd = frame.copy()
    else:
      frame_toAdd = frame
    # Wait for a spot to be available.
    #print('addframe waiting on', self._next_frame_index_toAdd)
    # t01 = time.time()
    while self._frame_buffer[self._next_frame_index_toAdd] is not None:
      time.sleep(0.001)
    # print('addframe Waited %0.2f ms on frame %d' % ((time.time() - t00)*1000, self._next_frame_index_toAdd))
    # Add the frame to the buffer!
    #print('Adding frame to index  %3d' % self._next_frame_index_toAdd)
    # t02 = time.time()
    self._frame_buffer[self._next_frame_index_toAdd] = frame_toAdd
    # t03 = time.time()
    self._next_frame_index_toAdd = (self._next_frame_index_toAdd + 1) % self._max_buffered_frames
    # t04 = time.time()
    # d = t04 - t00
    # d1 = t01 - t00
    # d2 = t02 - t01
    # d3 = t03 - t02
    # d4 = t04 - t03
    # print('%0.4f | %5.2f%% %5.2f%% %5.2f%% %5.2f%%' % (d, 100*d1/d, 100*d2/d, 100*d3/d, 100*d3/d))
    
  def _write_frames_thread_fn(self):
    while self._active:
      # Wait for a frame to write.
      #print('writeframe Waiting on frame', self._next_frame_index_toWrite)
      t00 = time.time()
      while self._frame_buffer[self._next_frame_index_toWrite] is None and self._active:
        time.sleep(0.001)
      # if time.time() - t00 > 0.01:
      #print('writeframe Waited %0.2f ms on frame %d' % ((time.time() - t00)*1000, self._next_frame_index_toWrite))
      if not self._active:
        break
      # Write the frame!
      # print('Writing frame at index %3d' % self._next_frame_index_toWrite)
      self._video_writer.write(self._frame_buffer[self._next_frame_index_toWrite])
      #print('Done writing frame at index %d' % self._next_frame_index_toWrite)
      self._frame_buffer[self._next_frame_index_toWrite] = None
      self._next_frame_index_toWrite = (self._next_frame_index_toWrite + 1) % self._max_buffered_frames
  
  def release(self, flush_buffer=True):
    print('Releasing')
    if self._video_writer is None:
      return
    # Stop the thread.
    self._active = False
    self._writing_thread.join()
    # Flush the buffer.
    if flush_buffer:
      while self._frame_buffer[self._next_frame_index_toWrite] is not None:
        self._video_writer.write(self._frame_buffer[self._next_frame_index_toWrite])
        self._frame_buffer[self._next_frame_index_toWrite] = None
        self._next_frame_index_toWrite = (self._next_frame_index_toWrite + 1) % self._max_buffered_frames
    # Release the video writer.
    self._video_writer.release()
    # Clear up some state.
    self._video_writer = None
    self._writing_thread = None

if __name__ == '__main__':
  import numpy as np
  
  width = 2440
  height = 2526
  framerate = 30
  num_frames = 100
  
  #print('Generating random frames', end='')
  frames = []
  t0 = time.time()
  for i in range(num_frames):
    frames.append(np.random.randint(low=0, high=255, size=(height, width, 3), dtype=np.uint8))
    # frames[-1] = np.ascontiguousarray(frames[-1])
  #print('  %6.2f Hz' % (num_frames/(time.time() - t0)))
  
  video_writer = ThreadedVideoWriter(output_filepath='P:/MIT/Lab/Whales/Birthday/fps_test_opencv_threaded.mp4',
                                     frame_rate=30, max_buffered_frames=100,
                                     overwrite_existing_video=True,
                                     copy_added_frames=True)
  t0 = time.time()
  write_duration_s = 0
  for (frame_index, frame) in enumerate(frames):
    #print('Main loop adding frame %d' % frame_index)
    # time.sleep(1/30)
    t00 = time.time()
    video_writer.add_frame(frame)
    write_duration_s += (time.time() - t00)
  t00 = time.time()
  video_writer.release()
  flushing_duration_s = time.time() - t00
  duration_s = (time.time() - t0)
  print('total   : %0.2fs --> %7.2f Hz' % (duration_s, num_frames/duration_s))
  print('writing : %0.2fs --> %7.2f Hz' % (write_duration_s, num_frames/write_duration_s))
  print('flushing: %0.2fs --> %7.2f Hz' % (flushing_duration_s, num_frames/flushing_duration_s))
  