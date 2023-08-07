import pandas
import numpy as np
import matplotlib.pyplot as plt
import sys

filepath = 'data_ecg_%02d.csv' % int(sys.argv[1])
df = pandas.read_csv(filepath)
ecg = np.array(df['ECG'])[100:]
time_us = np.array(df['Timestamp [us]'])[100:]
time_s = time_us/1000000.0
dt_s = np.diff(time_s)

plt.plot(time_s[1:], dt_s)
plt.grid()
plt.show()