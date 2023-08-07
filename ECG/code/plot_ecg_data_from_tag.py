
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
#             'test_01_defaultOS_allSensors_rawAudio')
#             # 'test_02_defaultOS_allSensors_rawAudio')
# data_dir = os.path.join('P:/MIT/Lab/Whales/ECG/data/2023-04-25 debugging ecg rates cpus',
#             'test00 allSensors rawAudio fixPriority')
# data_dir = os.path.join('P:/MIT/Lab/Whales/ECG/data/2023-04-26 debugging ecg rates cpus',
#                         # 'test00 allSensors rawAudio fixedPriorities isolatedCPUs')
#                         # 'test01 allSensors rawAudio fixedPriorities isolatedCPUs builtImage')
#                         # 'test02 allSensors rawAudio fixedPriorities isolatedCPUs builtImage')
#                         'test03 allSensors rawAudio fixedPriorities isolatedCPUs builtImage addSwap', 'copy_01')
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
                        # '01_tagA_gain44-cutoff38_cups_gndSoloLeft')
                        # '02_tagA_gain44-cutoff38_cups_gndSoloLeft')
                        # '03_tagA_gain44-cutoff38_cups_gndSoloLeft_holdMetal')
                        # '04_tagA_gain44-cutoff38_cups_gndSoloLeft_battery')
                        # '05_tagA_gain44-cutoff38_cups_gndSoloLeft_battery_holdGnd')
                        # '06_tagB_cups_gndSoloLeft')
                        # '07_tag5_gain11-cutoff100_cups_gndSoloLeft')
                        # '08_tag5_gain11-cutoff100_cups_gndSoloLeft_holdGnd-no-yes')
                        # '09_tag5_gain22-cutoff100_cups_gndSoloLeft_holdGnd-no-yes')
                        '10_tag5_gain44-cutoff38_cups_gndSoloLeft_holdGnd-no-yes')

######################
# READ DATA
######################

# Use the most recent CSV file in the data directory (according to date modified).
filepaths = sorted(Path(data_dir).glob('*ecg*.csv'), key=os.path.getmtime)
filepath = filepaths[-1]

df = pandas.read_csv(filepath)
ecg = np.array(df['ECG'])[100:]
try:
  leadsOff = np.array(df['Leads-Off'])[100:]
except:
  leadsOff_p = np.array(df['Leads-Off-P'])[100:]
  leadsOff_n = np.array(df['Leads-Off-N'])[100:]
  leadsOff = leadsOff_p + leadsOff_n
time_us = np.array(df['Timestamp [us]'])[100:]
time_s = time_us/1000000.0
dt_s = np.diff(time_s)

######################
# PLOT DATA STATS
######################
print()
duration_s = max(time_s)-min(time_s)
stats_str = '\n'
stats_str += 'Duration: %0.2f seconds (%02d:%02d:%05.2f)' % \
              (duration_s, int(duration_s/3600), int((duration_s % 3600)/60), duration_s % 60)
stats_str += '\n'
stats_str += '\nSampling rate:'
stats_str += '\n  Mean   : %6.1f Hz' % np.nanmean(1/dt_s)
stats_str += '\n  Median : %6.1f Hz' % np.nanmedian(1/dt_s)
stats_str += '\n  Std Dev: %6.1f Hz' % np.nanstd(1/dt_s)
stats_str += '\n  Min    : %6.1f Hz' % np.nanmin(1/dt_s)
stats_str += '\n  Max    : %6.1f Hz' % np.nanmax(1/dt_s)
stats_str += '\n  NaN    : %5.1f%% (%d)' % (100*np.sum(np.isnan(dt_s))/dt_s.shape[0], np.sum(np.isnan(dt_s)))
stats_str += '\n'
stats_str += '\nLeads-off:'
stats_str += '\n  Leads Off: %5.1f%%' % (100*np.nansum(leadsOff)/leadsOff.shape[0])
stats_str += '\n  Leads On : %5.1f%%' % (100 - 100*np.nansum(leadsOff)/leadsOff.shape[0])
stats_str += '\n  NaN      : %5.1f%% (%d)' % (100*np.sum(np.isnan(leadsOff))/leadsOff.shape[0], np.sum(np.isnan(leadsOff)))
stats_str += '\n'
stats_str += '\nECG:'
stats_str += '\n  Mean   : %6.1f' % np.nanmean(ecg)
stats_str += '\n  Median : %6.1f' % np.nanmedian(ecg)
stats_str += '\n  Std Dev: %6.1f' % np.nanstd(ecg)
stats_str += '\n  Min    : %6.1f' % np.nanmin(ecg)
stats_str += '\n  Max    : %6.1f' % np.nanmax(ecg)
stats_str += '\n  NaN    : %5.1f%% (%d)' % (100*np.sum(np.isnan(ecg))/ecg.shape[0], np.sum(np.isnan(ecg)))
stats_str += '\n'
print(stats_str)
if not os.path.exists('%s_stats.txt' % os.path.splitext(filepath)[0]):
  fout = open('%s_stats.txt' % os.path.splitext(filepath)[0], 'w')
  fout.write(stats_str)
  fout.close()
  
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

# Plot the ECG signal.
ax = axs[0][0]
ax.plot(time_s-time_s[0], ecg)
ax.grid()
ax.set_ylabel('ADC Value')
ax.set_title('ECG')
ax.set_ylim(np.array([0, 8e6]) + np.array([-0.05, 0.05])*8e6)

# Plot the leads-off signal.
ax = axs[1][0]
ax.plot(time_s-time_s[0], leadsOff)
# ax.set_ylim([-0.1, 1.1])
ax.grid()
ax.set_ylabel('[Binary]')
ax.set_title('Leads Off')

# Plot the instantaneous sampling rate (ideally around 1 kHz).
ax = axs[2][0]
ax.plot(time_s[0:-1]-time_s[0], 1/dt_s)
ax.set_title('Instantaneous Sampling Rate')
ax.grid()
ax.set_ylim([-1, ax.get_ylim()[-1]])
ax.set_ylabel('Hz')
ax.set_xlabel('Time [s]')

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
# plt.xlim([270, 330])
plt.xlim(np.mean(plt.xlim()) + [-10, 10])
plt.draw()
keyboardClick=False
while keyboardClick != True:
  keyboardClick=plt.waitforbuttonpress()
# Save the plot if an image with that filename doesn't already exist.
if not os.path.exists('%s_zoomIn.png' % os.path.splitext(filepath)[0]):
  plt.savefig('%s_zoomIn.png' % os.path.splitext(filepath)[0], dpi=300)
  plt.savefig('%s_zoomIn.pdf' % os.path.splitext(filepath)[0])





