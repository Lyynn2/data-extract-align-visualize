
#include <stdio.h>
#include <unistd.h> // for usleep()

#include "ecg_test.h"
#include "ecg_gpio_expander.h"
#include "ecg_adc.h"
#include "ecg_logging.h"

#include <sys/time.h> // for gettimeofday

// -------------------------------
// Helpers
// -------------------------------
long long get_time_ms()
{
  long long time_ms;
  struct timeval te;
  gettimeofday(&te, NULL);
  time_ms = te.tv_sec * 1000LL + te.tv_usec / 1000;
  return time_ms;
}

// -------------------------------
// Main loop
// -------------------------------
int main()
{
  // Set up the output log file.
  ecg_log_setup();

  // Set up the GPIO expander.
  //   The ADC code will use it to poll the data-ready output,
  //   and this main loop will use it to read the ECG leads-off detection output.
  ecg_gpio_expander_setup();

  // Set up and configure the ADC.
  ecg_adc_setup();
  ecg_adc_set_voltage_reference(ECG_ADC_VREF_EXTERNAL); // ECG_ADC_VREF_EXTERNAL or ECG_ADC_VREF_INTERNAL
  ecg_adc_set_gain(ECG_ADC_GAIN_ONE); // ECG_ADC_GAIN_ONE or ECG_ADC_GAIN_FOUR
  ecg_adc_set_data_rate(1000); // 20, 90, 330, or 1000
  ecg_adc_set_conversion_mode(ECG_ADC_MODE_CONTINUOUS); // ECG_ADC_MODE_CONTINUOUS or ECG_ADC_MODE_SINGLE_SHOT
  // Start continuous conversion (or a single reading).
  ecg_adc_start();

  // Poll the ADC and the leads-off detection output, and monitor the sampling rate.
  long ecg_reading = 0;
  int lod_reading  = 0;
  long duration_ms = 120000;
  long sample_count = 0;
  ECG_LOG("Starting to log data! Will end after %0.1f s or via Ctrl-C\n", (float)duration_ms/1000.0);
  long long start_time_ms = get_time_ms();
  long long end_time_ms = get_time_ms();
  while(end_time_ms - start_time_ms < duration_ms)
  {
    lod_reading = ecg_gpio_expander_read_lod();
    ecg_reading = ecg_adc_read_singleEnded(ECG_ADC_CHANNEL_ECG);
    ecg_log_add_entry(ecg_reading, lod_reading);
//    ECG_LOG("ADC Reading! %ld\n", ecg_reading);
//    ECG_LOG("ADC Reading! %6.3f ", 3.3*(float)ecg_reading/(float)(1 << 23));
//    ECG_LOG("\tLOD Reading! %1d\n", lod_reading);
    end_time_ms = get_time_ms();
    sample_count++;
  }

  // Print the duration and sampling rate.
  duration_ms = end_time_ms - start_time_ms;
  ECG_LOG("\nDone!\n");
  ECG_LOG("\n");
  ECG_LOG("Samples : %d\n", sample_count);
  ECG_LOG("Duration: %ld ms\n", duration_ms);
  ECG_LOG("Rate    : %0.2f Hz\n", 1000.0*(float)sample_count/(float)duration_ms);
  ECG_LOG("\n");

  // Clean up.
  ecg_log_cleanup();
  ecg_adc_cleanup();
  ecg_gpio_expander_cleanup();

  return 0;
}