
#include "ecg_logging.h"

int ecg_log_setup()
{
  // Create a filename for the log.
  struct timeval tv;
  time_t t;
  struct tm *info;
  char buffer[64];
  gettimeofday(&tv, NULL);
  t = tv.tv_sec;
  info = localtime(&t);
  strftime(buffer, sizeof buffer, "%Y-%m-%d_%H-%M-%S", info);
  sprintf(ecg_log_filepath, "/data/ecg_testing/%s_ecg_log.csv", buffer);

  // Open the file.
  ecg_log_fout = fopen(ecg_log_filepath, "w");
  if(ecg_log_fout == NULL)
  {
      ECG_LOG("ecg_log_setup(): failed to open the ECG log file: %s\n", ecg_log_filepath);
      return -1;
  }
  ECG_LOG("ecg_log_setup(): opened an ECG log file: %s\n", ecg_log_filepath);

  // Write headers to the file.
  char headers[] = "Timestamp[ms],ECG,Leads-Off";
  fprintf(ecg_log_fout, "%s\n", headers);

  return 1;
}

void ecg_log_cleanup()
{
  // Close the log file.
  ECG_LOG("ecg_log_cleanup(): Closing the ECG log file.\n");
  fclose(ecg_log_fout);
}

void ecg_log_add_entry(long ecg_reading, int lod_reading)
{
  // Timestamp the entry.
  gettimeofday(&ecg_log_entry_time_timeval, NULL);
  ecg_log_entry_time_ms = ecg_log_entry_time_timeval.tv_sec * 1000LL
                            + ecg_log_entry_time_timeval.tv_usec / 1000;

  // Write the entry.
  fprintf(ecg_log_fout, "%lld,", ecg_log_entry_time_ms);
  fprintf(ecg_log_fout, "%ld,", ecg_reading);
  fprintf(ecg_log_fout, "%d,", lod_reading);
  fprintf(ecg_log_fout, "\n");
}