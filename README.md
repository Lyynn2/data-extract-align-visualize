
# Examples of Extracting Timestamped Data

`example_get_audio_with_timestamps.py` 
- Will load audio data as a raw waveform or as a spectrogram
- Will load aligned timestamps for each audio sample.

`example_get_coda_annotations.py`
- Will load coda annotations from the biology and/or Haifa teams.
- Will provide click times, ICIs, whale indexes, etc. for each coda.
- Timestamps will be adjusted based on alignment offsets.
- **Link to coda annotations files:** [https://drive.google.com/drive/folders/1o6aclfZT1td0Xjm15IKLw7Pj57yaxBNU?usp=sharing](https://drive.google.com/drive/folders/1o6aclfZT1td0Xjm15IKLw7Pj57yaxBNU?usp=sharing)
  - Download the folders from the above link and place them in your root data directory alongside other folders downloaded from AWS.
  - For example, another folder within that root data directory is probably `DSWP-KASHMIR_MIXPRE6-1`
  - `_coda_annotations_biology` and `_coda_annotations_haifa` will be considered the device IDs for now.

`example_use_drone_data.py`
- Will load extracted metadata from HDF5 files.
- Includes GPS positions, altitude, estimated speed, and camera settings for each video frame.
- Includes aligned timestamps for each video frame.
- **Link to drone data files:** [https://drive.google.com/drive/folders/1VRa-VetmZ5YfDLSZ_6jQgG1d_zl_QoxG?usp=drive_link](https://drive.google.com/drive/folders/1VRa-VetmZ5YfDLSZ_6jQgG1d_zl_QoxG?usp=drive_link)
  - Download the two HDF5 files from the `Data and Code` folder. 

# Visualizing Data
`create_composite_video.py` **will create a video with synchronized visualizations from any desired combination of devices.**
  - The dictionary `composite_layout` defines which device streams should be visualized and how they should be arranged on the video.
  - The variables `output_video_start_time_str` and `output_video_duration_s` define the span of the video.


`drone_plot_gps.py` will create an animation of the drones' GPS paths.

 `drone_ploy_speed.py` will plot horizontal drone speed and stationary periods as estimated from the GPS positions.


# Notable Helpers

## Timestamps and Device Alignment

- To get an aligned start time of a file, you can call `adjust_start_time_s(get_time_s_from_filename(filepath), device_id)`
  - `helpers_data_extraction.py > get_time_s_from_filename()` will extract the start time of a file from the 13-digit epoch timestamp in the filename.  This timestamp is from the device clock (not aligned to other devices).
  - `helpers_synchronization.py > adjust_start_time_s()` will adjust a device-based start time to synchronize it with other devices.  Will look up the appropriate offset to add based on the device and the original start time.


- The dictionary `helpers_synchronization.py > epoch_offsets_toAdd_s` defines the manual synchronization offsets.  There may be a single offset per device, or a variable offset per device that changes throughout the expedition.  
  - These were manually defined by finding key frames throughout the data (typically frames when a blow just barely begins).  
  - The hydrophone offset was determined using two codas in file 280 that were also audible in videos.  The file `video_audio_alignment_plotting.py` will plot the waveforms at these codas to visualize the alignment.


- `helpers_various.py > time_s_to_str()` and `time_str_to_time_s()` convert between epoch time (seconds since January 1, 1970) and a human-readable timestamp string.  Note that `time_s_to_str` requires information about the local time zone; for the birthday data `timezone_offset_s = -14400` and `timezone_offset_str = '-0400'`.

## Extracting Timestamped Data
- `helpers_data_extraction.py` provides methods for getting video frames, images, audio waveforms, audio spectrograms, drone flight/camera data, and coda annotations with associated aligned timestamps: 
  - `get_timestamped_data_audioVideoImage()`
  - `get_timestamped_data_codas()` 
  - `get_timestamped_data_drones()` (but note that the HDF5 files mentioned above are recommended, since they include both aligned and original timestamps as well as other formatted fields)

## Subclasses

- `ImagePlot` is a custom plotting class to speed up plotting for video generation.  It builds plot images directly instead of using a plotting library, so it is fast for basic functions and does not require a dedicated export/render step to fetch an image of the plot.
- `ThreadedVideoWriter` is a video writer wrapper to speed up video writing.  It maintains a rolling buffer of frames to write and then performs the actual write in a dedicated thread, so your main code can continue working on synthesizing the next frame while the previous frame is being written.

# Installation

The code has so far been run with Python version `3.9.9`. Versions of notable packages that the code has currently been tested with are listed below:

**Image/Video**
- `pip install decord==0.6.0` for quickly loading video frames
- `pip install Pillow==9.1.0` for quickly loading images
- `pip install moviepy==1.0.3` for adding aligned audio to generated composite videos
- `pip install proglog==0.1.10` for controlling log outputs when adding audio to generated composite videos
- `pip install ffmpeg-python==0.2.0` and maybe `pip install ffmpegcv==0.3.7` for compressing output videos
- `pip install opencv-python==4.8.0.76` for drawing text and shapes on images

**Plotting**
- `pip install distinctipy==1.2.2` for generating unique plot colors
- `pip install matplotlib==3.5.1` for plotting drone data
- `pip install tilemapbase==0.4.7` for plotting maps with drone GPS data
- `pip install pyqtgraph==0.12.4` for plotting video/audio alignment graphs. May also be relevant: `pip install PyQt6==6.3.0`, `pip install PyQt6-Qt6==6.3.0`, `pip install PyQt6-sip==13.3.1`, `pip install PyOpenGL==3.1.6`

**Data/Math**
- `pip install numpy==1.23.5`
- `pip install h5py==3.1.0` and maybe `pip install h5py-cache==1.0` for storing/loading extracted drone data
- `pip install pandas==1.3.5` for downloading data from AWS
- `pip install scipy==1.9.1` for loading/processing audio files
- `pip install python-dateutil==2.8.2` for parsing timestamp strings
- `pip install pysrt==1.1.2` for extracting drone data from SRT files

**All of the above**
```
  pip install decord==0.6.0
  pip install Pillow==9.1.0
  pip install moviepy==1.0.3
  pip install proglog==0.1.10
  pip install ffmpeg-python==0.2.0
  pip install ffmpegcv==0.3.7
  pip install opencv-python==4.8.0.76
  pip install distinctipy==1.2.2
  pip install matplotlib==3.5.1
  pip install tilemapbase==0.4.7
  pip install pyqtgraph==0.12.4
  #pip install PyQt6==6.3.0
  #pip install PyQt6-Qt6==6.3.0
  #pip install PyQt6-sip==13.3.1
  #pip install PyOpenGL==3.1.6
  pip install numpy==1.23.5
  pip install h5py==3.1.0
  pip install h5py-cache==1.0
  pip install pandas==1.3.5
  pip install scipy==1.9.1
  pip install python-dateutil==2.8.2
  pip install pysrt==1.1.2
```













