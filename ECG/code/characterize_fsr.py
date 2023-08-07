
import numpy as np
import pandas as pd
from scipy import interpolate # for the resampling example
import h5py
from matplotlib import pyplot as plt

# With delryn:
# data_filepath = 'P:/MIT/Lab/Wearativity/data/tests/2022-09-14_fsr_scale/2022-09-14_19-58-25_fsr-weight-tests/2022-09-14_19-58-33_streamLog_fsr-weight-tests.hdf5'
data_filepath = 'P:/MIT/Lab/Wearativity/data/tests/2022-09-14_fsr_scale/2022-09-14_20-36-36_fsr-weight-tests/2022-09-14_20-36-43_streamLog_fsr-weight-tests.hdf5'
# With pen:
# data_filepath = 'P:/MIT/Lab/Wearativity/data/tests/2022-09-14_fsr_scale/2022-09-14_21-10-03_fsr-weight-tests/2022-09-14_21-10-11_streamLog_fsr-weight-tests.hdf5'
# data_filepath = 'P:/MIT/Lab/Wearativity/data/tests/2022-09-14_fsr_scale/2022-09-14_21-25-23_fsr-weight-tests/2022-09-14_21-25-31_streamLog_fsr-weight-tests.hdf5'
smooth_window_s = 0.25
fsr_fit_degree = 6

# Load the data.
h5py_file = h5py.File(data_filepath, 'r')
scale_time_s = np.squeeze(h5py_file['tactile-calibration-scale']['weight_g']['time_s'][:,:])
scale_weight_g = np.squeeze(h5py_file['tactile-calibration-scale']['weight_g']['data'][:,:])
fsr_time_s = np.squeeze(h5py_file['fsr-sensor']['serial_data']['time_s'][:,:])
fsr_adc = np.squeeze(h5py_file['fsr-sensor']['serial_data']['data'][:,:])
h5py_file.close()

# Smooth the signals.
def movmean(x, window_length):
  return pd.Series(x).rolling(window_length, min_periods=0, center=False).mean().to_numpy()
def movmedian(x, window_length):
  return pd.Series(x).rolling(window_length, min_periods=0, center=False).median().to_numpy()
Ts = (fsr_time_s[-1] - fsr_time_s[0])/(len(fsr_time_s)-1)
smooth_length = np.round(smooth_window_s/Ts).astype(int)
fsr_adc = movmedian(fsr_adc, window_length=smooth_length)
Ts = (scale_time_s[-1] - scale_time_s[0])/(len(scale_time_s)-1)
smooth_length = np.round(smooth_window_s/Ts).astype(int)
scale_weight_g = movmedian(scale_weight_g, window_length=smooth_length)

# Resample the FSR to match the scale timestamps.
#  Note that the FSR streamed at about 200 Hz while the scale streamed at about 5 Hz.
fn_interpolate = interpolate.interp1d(
    fsr_time_s, # x values
    fsr_adc,    # y values
    axis=0,              # axis of the data along which to interpolate
    kind='linear',       # interpolation method, such as 'linear', 'zero', 'nearest', 'quadratic', 'cubic', etc.
    fill_value='extrapolate' # how to handle x values outside the original range
)
time_s = scale_time_s
fsr_adc = fn_interpolate(time_s)
fsr_v = fsr_adc*3.3/4095
indexes = np.where((fsr_v > 0) & (scale_weight_g > 0))[0]
time_s = time_s[indexes]
fsr_v = fsr_v[indexes]
scale_weight_g = scale_weight_g[indexes]

# Fit!
coefficients = np.polyfit(fsr_v, scale_weight_g, deg=fsr_fit_degree)
fit_scale_weight_g = np.zeros_like(fsr_v)
for (i, c) in enumerate(coefficients):
  fit_scale_weight_g = fit_scale_weight_g + coefficients[i]*(fsr_v**(len(coefficients)-(i+1)))
print('Coefficients: {%s}' % ', '.join(['%f' % x for x in coefficients]))
print('Coefficients: {%s}' % '\t'.join(['%f' % x for x in coefficients]))
errors_g = np.abs(scale_weight_g - fit_scale_weight_g)
errors_g = errors_g[np.where(scale_weight_g > 0)[0]]
errors_pcnt = 100*errors_g/scale_weight_g[np.where(scale_weight_g > 0)[0]]
print('Average error: %0.1f grams | %0.1f%%' % (np.mean(errors_g), np.mean(errors_pcnt)))
# coefficients = np.polyfit(fsr_v, np.log(scale_weight_g), deg=1)
# a = np.exp(coefficients[1])
# b = coefficients[0]
# fit_scale_weight_g = np.zeros_like(fsr_v)
# for (i, c) in enumerate(coefficients):
#   fit_scale_weight_g = a*np.exp(b**fsr_v)
# print('Coefficients: {%s}' % ', '.join(['%f' % x for x in coefficients]))
# print('Coefficients: {%s}' % '\t'.join(['%f' % x for x in coefficients]))
# errors_g = np.abs(scale_weight_g - fit_scale_weight_g)
# errors_g = errors_g[np.where(scale_weight_g > 0)[0]]
# errors_pcnt = 100*errors_g/scale_weight_g[np.where(scale_weight_g > 0)[0]]
# print('Average error: %0.1f grams | %0.1f%%' % (np.mean(errors_g), np.mean(errors_pcnt)))

# Plot.
# plt.plot(time_s-time_s[0], fsr_adc, '.-')
plt.plot(fsr_v, scale_weight_g, '.')
plt.plot(fsr_v, fit_scale_weight_g, '.')
plt.grid(True, color='lightgray')
plt.title('Weight vs FSR Reading')
plt.ylabel('Weight [g]')
plt.xlabel('FSR Voltage [V]')
# plt.show()

plt.figure()
plt.plot(time_s-time_s[0], scale_weight_g, 'k.-', label='Scale')
plt.plot(time_s-time_s[0], fit_scale_weight_g, 'b.-', label='FSR')
plt.grid(True, color='lightgray')
plt.title('Weight Over Time')
plt.ylabel('Weight [g]')
plt.xlabel('Time Since Start [s]')
plt.legend()
plt.show()

