
#ifndef ECG_LOGGING_H
#define ECG_LOGGING_H

#include <time.h>
#include <sys/time.h>
#include <stdio.h>
#include "ecg_test.h" // for ECG_LOG

int ecg_log_setup();
void ecg_log_cleanup();
void ecg_log_add_entry(long ecg_reading, int lod_reading);

char ecg_log_filepath[100];
FILE *ecg_log_fout;
struct timeval ecg_log_entry_time_timeval;
long long ecg_log_entry_time_ms;

#endif // ECG_LOGGING_H




