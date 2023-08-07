
===============
SETUP
===============

Python packages
-------------------------------
Required packages include:
  pip install pyserial
  pip install numpy
  pip install matplotlib
  pip install h5py
  pip install scipy

In `stream_log_plot_ecg_via_microcontroller.py`
-------------------------------
* Update the data directory in the line `data_dir = os.path.join(script_dir, '..', 'data')`
* Update the COM port in the line `esp_com_port = 'COM4''`
* If using an Arduino, may need to decrease the baud rate if it can't keep up with 1000000; this would be at the line `esp_baud_rate = 1000000`

In `esp_ecgBoard_streaming.ino`
-------------------------------
* Update the baud rate if it was edited in the Python script; this would be at the line `#define SERIAL_BAUD_RATE 1000000`

In `gpio_pca9674.h`
-------------------------------
* Update the data ready channel at the line `const int expander_channel_dataReady = 7;` according to which ECG board version you're using (see comments at that line for more information).


===============
RUNNING
===============

* Connect the ECG board I2C to the ESP/Arduino, using the 3V pin for power
* Load the ESP/Arduino code onto the controller
* Run `stream_log_plot_ecg_via_microcontroller.py`
* Ctrl+C when done; the script should then save the plot and let you interact with it


=====================
OFFLINE DATA VIEWING
=====================

* The HDF5 files can be explored using HDFView: https://www.softpedia.com/get/Others/Miscellaneous/HDFView.shtml
* The HDF5 files can also be processed via the h5py Python library (or similar libraries for other languages/programs)
* The plots can be viewed as images or PDFs
* The plots in the .fig.pickle format can also be reopened via Python as an interactive plot if desired






