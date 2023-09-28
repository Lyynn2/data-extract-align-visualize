
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
#
############

############
# A class to speed up video writing via threading.
# Will store the frames to write in a buffer, and then do the
#  actual writing in a separate thread.
# The main calling thread thus does not need to wait for the writing to finish.
############

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
    # Store the configuration.
    self.set_output_filepath(output_filepath, overwrite_existing_video)
    self.set_frame_size(frame_width, frame_height)
    self.set_frame_rate(frame_rate)
    self.set_max_buffered_frames(max_buffered_frames)
    self.set_copy_added_frames(copy_added_frames)
    # Initialize state.
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
  
  # Create a video writer.
  def _init_writer(self):
    # Verify that all configurations have been specified.
    video_extension = os.path.splitext(self._output_filepath)[-1].lower()
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
    # Create the video writer.
    self._video_writer = cv2.VideoWriter(self._output_filepath,
                                         cv2.VideoWriter_fourcc(*fourcc),
                                         self._frame_rate,
                                         (self._frame_width, self._frame_height))
  
  # Start the thread that will write frames as they become available.
  def _start_thread(self):
    # Initialize state.
    self._frame_buffer = [None]*self._max_buffered_frames
    self._next_frame_index_toWrite = 0
    self._next_frame_index_toAdd = 0
    self._active = True
    self._writing_thread = Thread(target=self._write_frames_thread_fn)
    self._writing_thread.start()
  
  # Wait for frames to be available, and then write them to the video.
  def _write_frames_thread_fn(self):
    while self._active:
      # Wait for a frame to write.
      while self._frame_buffer[self._next_frame_index_toWrite] is None and self._active:
        time.sleep(0.001)
      # End the loop if the thread has been stopped.
      if not self._active:
        break
      # Write the frame!
      self._video_writer.write(self._frame_buffer[self._next_frame_index_toWrite])
      # Mark this slot as available in the buffer, and advance the index pointer.
      self._frame_buffer[self._next_frame_index_toWrite] = None
      self._next_frame_index_toWrite = (self._next_frame_index_toWrite + 1) % self._max_buffered_frames
  
  # Add a frame to the buffer of frames to write.
  def add_frame(self, frame):
    # Create a video writer if this is the first frame.
    if self._video_writer is None:
      # Set the frame size based on the first frame if needed.
      if self._frame_width is None or self._frame_height is None:
        self.set_frame_size(frame_width=frame.shape[1], frame_height=frame.shape[0])
      # Create the video writer.
      self._init_writer()
    
    # Create and start a writing thread if this is the first frame.
    if self._writing_thread is None:
      self._start_thread()
    
    # Make a copy of the frame, so the caller can continue editing their array
    #  without affecting the one in our queue.
    # Do this now, so it subtracts from the time we may need to wait below
    #  in the case that the buffer is full.
    if self._copy_added_frames:
      frame_toAdd = frame.copy()
    else:
      frame_toAdd = frame
    # Wait for a spot to be available in the buffer.
    while self._frame_buffer[self._next_frame_index_toAdd] is not None:
      time.sleep(0.001)
    # Add the frame to the buffer, and advance the pointer for the next frame.
    self._frame_buffer[self._next_frame_index_toAdd] = frame_toAdd
    self._next_frame_index_toAdd = (self._next_frame_index_toAdd + 1) % self._max_buffered_frames
  
  # Check whether a frame at a given buffer index has been completely written.
  def frame_is_pending_write(self, buffer_index):
    # Check if the buffer has not been initialized.
    if self._video_writer is None:
      return False
    # Check if the index is out of bounds.
    if buffer_index >= len(self._frame_buffer):
      raise ValueError('Querying the status of buffered frame index %d but the buffer is only %d frames long.'
                       % (buffer_index, len(self._frame_buffer)))
    # Return the frame status.
    return self._frame_buffer[buffer_index] is not None
  
  # Release the writer, and flush any remaining frames that have not yet been written.
  def release(self, flush_buffer=True):
    if self._video_writer is None:
      return
    # Stop the thread, and wait for it to finish if it is currently writing a frame.
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

########################################################
# TESTING
########################################################
if __name__ == '__main__':
  import numpy as np
  
  width = 2440
  height = 2526
  fps = 30
  num_frames = 100
  
  # Some tests to try:
  #
  #  max_buffered_frames = 1, computation_delay_s = 0
  #    This shows the speed that would be achieved without any buffering/threading.
  #    All of the time will be spent writing, and basically none flushing,
  #     since each write call had to wait for it to finish.
  #  max_buffered_frames = num_frames, computation_delay_s = 0
  #    This shows the maximum runtime speed achieved by buffering/threading.
  #    The write calls will take very little time, and then the flushing
  #     will take a significant amount of time.  The write calls were
  #     essentially non-blocking, and then the flushing waits for the writes to finish.
  #     Note that the main writing delay in this case is copying the numpy array.
  #
  #  max_buffered_frames = 1, computation_delay_s = 1/50 or similar
  #    This shows how long it would take for a script to do some work (simulated by the delay)
  #     and then write the result to a video if there was no buffering/threading.
  #  max_buffered_frames = num_frames, computation_delay_s = 1/50 or similar
  #    This shows the advantage of buffering/threading.
  #    The same amount of 'processing work' will be done as in the previous test,
  #     but now the main script does not need to wait for the write to finish
  #     so the main loop rate will be close to the rate determined by the specified delay.
  #
  max_buffered_frames = num_frames
  computation_delay_s = 0
  
  # Generate random frames.
  frames = []
  start_time_s = time.time()
  for i in range(num_frames):
    frames.append(np.random.randint(low=0, high=255, size=(height, width, 3), dtype=np.uint8))
  
  # Create the video writer.
  video_writer = ThreadedVideoWriter(output_filepath='test_threaded_video_writer.mp4',
                                     frame_rate=fps,
                                     max_buffered_frames=max_buffered_frames,
                                     overwrite_existing_video=True,
                                     copy_added_frames=True)
  # Demonstrate the writing and measure the timing.
  start_time_s = time.time()
  write_duration_s = 0
  for (frame_index, frame) in enumerate(frames):
    # Simulate processing work by the main thread.
    if computation_delay_s > 0:
      time.sleep(computation_delay_s)
    # Add the frame to the writing buffer.
    start_writing_time_s = time.time()
    video_writer.add_frame(frame)
    write_duration_s += (time.time() - start_writing_time_s)
  main_loop_duration_s = time.time() - start_time_s
  # Flush any remaining frames, and release the writer.
  start_flushing_time_s = time.time()
  video_writer.release()
  flushing_duration_s = time.time() - start_flushing_time_s
  duration_s = (time.time() - start_time_s)
  
  # Print timing results.
  print('Timing results:')
  print('  Total    : %0.2fs --> %7.2f Hz' % (duration_s, num_frames/duration_s))
  print('  Main loop: %0.2fs --> %7.2f Hz' % (main_loop_duration_s, num_frames/main_loop_duration_s))
  print('  Writing  : %0.2fs --> %7.2f Hz' % (write_duration_s, num_frames/write_duration_s))
  print('  Flushing : %0.2fs --> %7.2f Hz' % (flushing_duration_s, num_frames/flushing_duration_s))
  print()
  
