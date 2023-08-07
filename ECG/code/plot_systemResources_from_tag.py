
import pandas
import numpy as np
import matplotlib.pyplot as plt
import os
import sys
from pathlib import Path
import time

######################
# CONFIGURATION
######################
# data_dir = 'path_to_folder_with_csv_files_copied_from_pi'
# data_dir = 'P:/MIT/Lab/Whales/ECG/data/2023-04-14 debugging audio images etc/test 02 builtImage allSensors long3hours/ecg'
# data_dir = 'P:/MIT/Lab/Whales/ECG/data/2023-04-14 debugging audio images etc/test 07 builtImage allSensors flacAudio'
# data_dir = 'P:/MIT/Lab/Whales/ECG/data/2023-04-14 debugging audio images etc/test 08 builtImage allSensors flacAudio'
# data_dir = 'P:/MIT/Lab/Whales/ECG/data/2023-04-14 debugging audio images etc/test 09 builtImage localBuild allSensors flacAudio/ecg'
# data_dir = 'P:/MIT/Lab/Whales/ECG/data/2023-04-14 debugging audio images etc/test 10 builtImage localBuild allSensors flacAudio assignAudioWriteCPU/ecg'

# data_dir = os.path.join('P:/MIT/Lab/Whales/ECG/data/2023-04-20 debugging ecg sampling rates/',
#             'archived_2023-04-20_test08')
# data_dir = os.path.join('P:/MIT/Lab/Whales/ECG/data/2023-04-21 debugging ecg sampling rates - own I2C bus/',
#             'archived_2023-04-21_test01')
# data_dir = os.path.join('P:/MIT/Lab/Whales/ECG/data/2023-04-24 debugging ecg sampling rate/',
#             'test_13')
# data_dir = os.path.join('P:/MIT/Lab/Whales/ECG/data/2023-04-24 debugging ecg rates - different images',
#             'test_00_newImage_allSensors_rawAudio')
#             # 'test_01_defaultOS_allSensors_rawAudio')
#             # 'test_02_defaultOS_allSensors_rawAudio')
# data_dir = os.path.join('P:/MIT/Lab/Whales/ECG/data/2023-04-25 debugging ecg rates cpus',
#                         'test00 allSensors rawAudio fixPriority')
# data_dir = os.path.join('P:/MIT/Lab/Whales/ECG/data/2023-04-26 debugging ecg rates cpus',
#                         'test00 allSensors rawAudio fixedPriorities isolatedCPUs')
# data_dir = os.path.join('P:/MIT/Lab/Whales/ECG/data/2023-04-26 debugging ecg rates cpus',
#                         # 'test00 allSensors rawAudio fixedPriorities isolatedCPUs')
#                         # 'test01 allSensors rawAudio fixedPriorities isolatedCPUs builtImage')
#                         # 'test02 allSensors rawAudio fixedPriorities isolatedCPUs builtImage')
#                         'test03 allSensors rawAudio fixedPriorities isolatedCPUs builtImage addSwap')
# data_dir = os.path.join('P:/MIT/Lab/Whales/ECG/data/', '2023-05-05 testing updated flac')
# data_dir = os.path.join('P:/MIT/Lab/Whales/ECG/data/', '2023-05-11 testing ecg interrupt',
#                         # 'test 00 polling')
#                         # 'test 01 interrupt')
#                         # 'test 02 interrupt read sleep')
#                         # 'test 03 interrupt sleep read')
#                         # 'test 04 interrupt')
#                         # 'test 05 interrupt scope')
#                         # 'test 06 direct poll maybe not')
#                         # 'test 07 direct poll')
#                         # 'test 08 sigalarm')
#                         # 'test 09 direct poll')
#                         # 'test 10 interrupt flag')
#                         # 'test 11 expander poll')
#                         # 'test 12 direct poll')
#                         # 'test 13 interrupt')
#                         # 'test 14 timer')
#                         # 'test 15 direct poll - adjust cpus')
#                         # 'test 16 new image')
#                         'test 17 new image')
# data_dir = os.path.join('P:/MIT/Lab/Whales/ECG/data/', '2023-05-17 ecg suction cup electrodes',
#                         # 'test 00 1left 1right Gright')
#                         # 'test 01 1left 1right Gright none-hold-strap-strapHold')
#                         # 'test 02 1left 1right Gright strap none-unplugLaptop-hold')
#                         # 'test 03 1left 1right Gright benchPwr none-hold-none')
#                         # 'test 04 1left 1right Gright benchPwr gndOff-on-off-on still-move-still')
#                         # 'test 05 2right Gleft benchPwr')
#                         # 'test 06 2right Gleft benchPwr hold-none')
#                         # 'test 07 1left 1right Gright swappedWiresSameCups benchPwr none-hold-none')
#                         # 'test 08 2right 1left benchPwr gndBotR-gndTopR-gndLeft-gndLeftSwapRights')
#                         # 'test 09 2left 1right benchPwr gndTopL-gndBotL-gndR-gndRSwapLefts-hold-gndTopL-swapOthers')
#                         # 'test 10 2right 1left benchPwr gndTopR-gndBotR-gndL-gndLSwapRights-hold-gndTopR-swapOthers')
#                         # 'test 13 2right 1left swapLtopR benchPwr gndTopR-gndBotR-gndL-gndLSwapRights-hold-gndTopR-swapOthers')
#                         'test 14 2left 1right benchPwr gndTopL-gndBotL-gndR-gndRSwapLefts-hold-gndTopL-swapOthers')
# data_dir = os.path.join('P:/MIT/Lab/Whales/ECG/data/', '2023-05-22 testing ecg board disconnection',
#                         # 'test 00 updated edge checking')
#                         # 'test 01 comment new edge checking')
#                         # 'test 02 zero checking with ecg board')
#                         # 'test 03 zero checking no ecg board')
#                         # 'test 04 zero checking time checking no-yes ecg board')
#                         # 'test 05 zero checking time checking yes-no-yes-no-yes ecg board')
#                         # 'test 06 with ecg board')
#                         'test 07 with ecg board larger buffer')
data_dir = os.path.join('P:/MIT/Lab/Whales/ECG/data/2023-06-21 testing v2-2 tags',
                        '01_tagA_gain44-cutoff38_cups_gndSoloLeft')

######################
# READ DATA
######################

# Use the most recent CSV file in the data directory (according to date modified).
filepaths = sorted(Path(data_dir).glob('*systemMonitor*.csv'), key=os.path.getmtime)
filepath = filepaths[-1]

df = pandas.read_csv(filepath)
ram_free_percent = np.array(df['RAM Free [%]'])[1:]
swap_free_percent = np.array(df['Swap Free [%]'])[1:]
cpus_percent = [np.array(df['CPU %d [%%]' % cpu_index])[1:] for cpu_index in range(4)]
time_us = np.array(df['Timestamp [us]'])[1:]
time_s = time_us/1000000.0
dt_s = np.diff(time_s)

######################
# PLOT DATA
######################

plt.ion()

# Create a figure with subplots.
fig, axs = plt.subplots(nrows=3, ncols=1,
                        squeeze=False, # if False, always return 2D array of axes
                        sharex=True, #sharey=True,
                        subplot_kw={'frame_on': True},
                        )
plt.get_current_fig_manager().window.showMaximized()
plt.suptitle(os.path.join(*str(filepath).split(os.sep)[-3:]))

# Plot the memory usage.
ax = axs[0][0]
ax.plot(time_s-time_s[0], 100-ram_free_percent)
ax.plot(time_s-time_s[0], 100-swap_free_percent)
ax.set_ylim([-5, 105])
ax.grid()
ax.set_ylabel('Percent Used')
ax.legend(['RAM', 'Swap'])
ax.set_title('Memory Usage')

# # Plot the CPU usage.
# ax = axs[1][0]
# for cpu_index in range(len(cpus_percent)):
#   ax.plot(time_s-time_s[0], cpus_percent[cpu_index])
# ax.set_ylim([-5, 105])
# ax.grid()
# ax.set_ylabel('Percent Used')
# ax.legend(['CPU %d' % cpu_index for cpu_index in range(len(cpus_percent))])
# ax.set_title('CPU Usage')

# Plot the CPU usage.
ax = axs[1][0]
for cpu_index in [2,3]:
  ax.plot(time_s-time_s[0], cpus_percent[cpu_index])
ax.set_ylim([-5, 105])
ax.grid()
ax.set_ylabel('Percent Used')
ax.legend(['CPU 2 (ECG)', 'CPU 3 (Audio)'])
ax.set_title('CPU Usage: Audio and ECG Acquisition Threads')

ax = axs[2][0]
for cpu_index in [0,1]:
  ax.plot(time_s-time_s[0], cpus_percent[cpu_index])
ax.set_ylim([-5, 105])
ax.grid()
ax.set_ylabel('Percent Used')
ax.legend(['CPU %d' % cpu_index for cpu_index in [0,1]])
ax.set_title('CPU Usage: Other Cores')

ax.set_xlabel('Time Since Start [s]')

# Show the plot!
plt.draw()
keyboardClick=False
while keyboardClick != True:
  keyboardClick=plt.waitforbuttonpress()
# Save the plot if an image with that filename doesn't already exist.
plt.draw()
if not os.path.exists('%s.png' % os.path.splitext(filepath)[0]):
  plt.savefig('%s.png' % os.path.splitext(filepath)[0], dpi=300)
  plt.savefig('%s.pdf' % os.path.splitext(filepath)[0])

# Zoom in!
plt.xlim(np.mean(plt.xlim()) + [-150, 150])
plt.draw()
keyboardClick=False
while keyboardClick != True:
  keyboardClick=plt.waitforbuttonpress()
# Save the plot if an image with that filename doesn't already exist.
if not os.path.exists('%s_zoomIn.png' % os.path.splitext(filepath)[0]):
  plt.savefig('%s_zoomIn.png' % os.path.splitext(filepath)[0], dpi=300)
  plt.savefig('%s_zoomIn.pdf' % os.path.splitext(filepath)[0])





