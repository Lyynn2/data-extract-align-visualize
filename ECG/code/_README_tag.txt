
===============
SETUP
===============

* Get a tag running branch v2_2_refactor

In `launcher.h` on the tag
-------------------------------
* Check that ECG is enabled via the line `#define ENABLE_ECG 1`
* The other components may or not be enabled, whatever you prefer.

Python packages on your local computer
--------------------------------------
Required packages include:
  pip install pandas
  pip install numpy
  pip install matplotlib


===============
RUNNING
===============

* Run the app for as long as desired.
* I usually use the following commands:

cd ~/whale-tag-embedded/packages/ceti-tag-data-capture
(find src/ -name "*.o" -type f -delete); (rm bin/cetiTagApp); make
(cd bin; sudo ./cetiTagApp)

* To run the app for a predetermined length of time then quit, I use the following:

((sleep 20 && echo "quit" > ipc/cetiCommand) &) && (echo "" > ipc/cetiCommand) && (cd bin; sudo ./cetiTagApp; cd ..)

* The "20" in the above command specifies that it will run for 20 seconds.

=====================
OFFLINE DATA VIEWING
=====================

* Copy the ECG CSV file(s) from /data on the tag to your local computer

In `plot_ecg_data_from_tag.py`:
-------------------------------
* Update the data directory (the variable `data_dir`) to the folder where you put the CSV file.
* Run `plot_ecg_data_from_tag.py`
* It will plot the most recent CSV file in the specified data folder.









