
# import threading
import numpy as np
import time

print_results = False
results_filepath = 'ecg_circuit_filters_gains.csv'

gain_target = 88
gain_tolerance = 10

q_target = 1.5
q_tolerance = 1

fc_target = 50
fc_tolerance = 25

# def good_r10r6(R10, R6):
#   return R10/R6 >= 10
#
# def good_c4c5(C4, C5):
#   return C4/C5 >= 4

R6 = 100e3
# R6 = 24.9e3

available_resistors = [
  100e3,
  15e3,
  150e3,
  402e3,
  510e3,
  1.5e6,
  1e6,
  15e6,
  20e6,
  4.02e6,
  8.2e6,
  30e6,
  50e6,
  5.1e6,
  300e3,
  200e3,
  2e6,
  2.49e6,
  10e6,
  649e3,
  # 100,
  10e3,
  182e3,
  249e3,
  348e3,
  100e6,
  24.9e3,
  40.2e3,
  ]
available_capacitors = [
  2.2e-6,
  4.7e-6,
  10e-6,
  1e-6,
  0.1e-6,
  1000e-12,
  6800e-12,
  5600e-12,
  6.2e-9,
  ]
available_resistors = [float(r) for r in sorted(list(set(available_resistors)))]
available_capacitors = [float(c) for c in sorted(list(set(available_capacitors)))]

def compute_fc(R10, R9, R7, R8, C5, C4):
  return 1/(2*np.pi)/np.sqrt(R10*C5*R9*C4)

def compute_gain(R10, R9, R7, R8, C5, C4):
  return 1 + (R7/R8)

def compute_q(R10, R9, R7, R8, C5, C4):
  numerator = np.sqrt(R10*C5*R9*C4)
  denominator = R10*C4 + R9*C4 + R10*C5*(1-compute_gain(R10=R10, R9=R9, R7=R7, R8=R8, C5=C5, C4=C4))
  if denominator == 0:
    return None
  return numerator/denominator

################################################################
################################################################

if results_filepath is not None:
  results_fout = open(results_filepath, 'w')
  results_fout.write('R10 [k],R9 [k],R7 [k],R8 [k],C5 [n],C4 [n],Fc [Hz],Gain,Q,C4/C5')
else:
  results_fout = None
  
print()
print('Target gain: %s +/- %g' % (gain_target, gain_tolerance))
print('Target Q   : %s +/- %g' % (q_target, q_tolerance))
print('Target Fc  : %s +/- %g' % (fc_target, fc_tolerance))
print()
if print_results:
  print('             resistors in kOhm, capacitors in nF                     ')
  print(' R10      R9    R7     R8    |    C5      C4     |    Fc      Gain     Q       R10/R6  C4/C5   ')
  print('-----------------------------------------------------------------------------------------------')
total_N = len(available_resistors)**4 * len(available_capacitors)**2
N = 0
N_good = 0
# threads = []
msgs = []
last_print_time_s = time.time()
# def compute_for_r10(R10, printer):
for R10 in available_resistors:
  # global N, last_print_time_s
  for R9 in available_resistors:
    for R7 in available_resistors:
      for R8 in available_resistors:
        for C5 in available_capacitors:
          for C4 in available_capacitors:
            N += 1
            if time.time() - last_print_time_s > 1 and True:#(N % 500 == 0) and printer:
              print('\r', end='')
              print('%6d/%d (%0.1f%%) -> %d selected options' % (N, total_N, 100*N/total_N, N_good), end='')
              last_print_time_s = time.time()
            fc = compute_fc(R10=R10, R9=R9, R7=R7, R8=R8, C5=C5, C4=C4)
            gain = compute_gain(R10=R10, R9=R9, R7=R7, R8=R8, C5=C5, C4=C4)
            q = compute_q(R10=R10, R9=R9, R7=R7, R8=R8, C5=C5, C4=C4)
            if fc_target is not None:
              good_fc = abs(fc - fc_target) <= fc_tolerance
            else:
              good_fc = True
            if gain_target is not None:
              good_gain = abs(gain - gain_target) <= gain_tolerance
            else:
              good_gain = True
            if q_target is not None:
              good_q = abs(q - q_target) <= q_tolerance if q is not None else False
            else:
              good_q = q is not None
            if good_fc and good_gain and good_q:
              N_good += 1
              if print_results:
                msgs.append('%6d %6d %6d %6d  | %7.3f %7.3f   |   %6.2f   %5.2f   %5.3f    %4.1f   %4.1f' %
                      (R10/1000, R9/1000, R7/1000, R8/1000, C5*1000000000, C4*1000000000, fc, gain, q, R10/R6, C4/C5))
                print('\r', end='')
                print(msgs[-1])
              if results_fout is not None:
                results_fout.write('\n%g,%g,%g,%g,%g,%g,%g,%g,%g,%g' %
                                   (R10/1000, R9/1000, R7/1000, R8/1000, C5*1000000000, C4*1000000000,
                                    fc, gain, q, C4/C5))

if results_fout is not None:
  results_fout.close()
  
# for R10 in available_resistors:
#   threads.append(threading.Thread(target=compute_for_r10, args=(R10, R10==available_resistors[0])))
# for thread in threads:
#   thread.start()
# for thread in threads:
#   thread.join()
# print('\r', end='')
# for msg in msgs:
#   print(msg)
# print('\r                                                                            ')
print()

