
// Whether there is a direct GPIO connection to the data ready line,
//  or whether the GPIO expander is being used.
#define DATAREADY_iS_DIRECT 0

#include "adc_ads1219.h"
#include "gpio_pca9674.h"
#include <Wire.h>

//===========================
// CONFIGURATION
//===========================

// Specify debugging modes.
#define DEBUG_EXPANDER_RATE   0 // measure the data-ready polling rate via the expander
#define DEBUG_DRDY_HIGHS_LOWS 0 // count the high/low samples of data ready

// Activate data streaming and/or debug printouts as desired.
#define STREAM_DATA 1      // stream data for Python to read
#define STREAM_ECG_ONLY  0 // stream ECG only, e.g. for Arduino plotting
#define DEBUG_PRINT_RATE 0 // print rate and latest data, using downsampled rate
#define DEBUG_PRINT_DATA 0 // print latest data, at fastest rate
#define SERIAL_BAUD_RATE 1000000
const int convert_to_v = 0;

// Specify the ADC channels for each data stream.
const int adc_channel_ecg = 0; // 0
const int adc_channel_electrode1 = 2; // 2
const int adc_channel_electrode2 = 3; // 3

// Downsample the streams relative to the ADC rate.
const int downsampling_factor_ecg = 5;
const int downsampling_factor_electrode1 = -1; // -1 to not sample
const int downsampling_factor_electrode2 = -1; // -1 to not sample
const int downsampling_factor_lod = downsampling_factor_ecg; // -1 to not sample

// Pins and I2C.
const int led_pin = 13;
const uint8_t i2c_address_adc = 0b1000100;
#if DATAREADY_iS_DIRECT
const int data_ready_pin = 32;
#else
// See setup in gpio_pca9674.h
const int data_ready_pin = -1; // will indicate that it is not used
#endif

// ADC configuration.
uint8_t adc_gain_toSet = GAIN_ONE; // GAIN_ONE or GAIN_FOUR
uint8_t adc_mode_toSet = MODE_CONTINUOUS; // MODE_SINGLE_SHOT or MODE_CONTINUOUS

//===========================
// DECLARATIONS
//===========================

ADC_ADS1219 adc(i2c_address_adc, data_ready_pin);
float latest_reading_ecg = 0;
float latest_reading_electrode1 = 0;
float latest_reading_electrode2 = 0;
float latest_reading_lod = 0;
long num_readings = 0;
long num_readings_ecg = 0;
long num_readings_electrode1 = 0;
long num_readings_electrode2 = 0;
long num_readings_lod = 0;
float start_time_ms = 0;
float time_since_start_ms = 0;
int led_state = 0;

//===========================
// INITIALIZATION
//===========================
void setup()
{
  Serial.begin(SERIAL_BAUD_RATE);
  delay(1000);
  #if DEBUG_PRINT_RATE || DEBUG_PRINT_DATA
  Serial.println();
  Serial.println();
  Serial.println("Setting up!");
  #endif

  // Pins.
  #if DATAREADY_iS_DIRECT
  pinMode(data_ready_pin, INPUT_PULLUP);
  #endif
  pinMode(led_pin, OUTPUT);
  digitalWrite(led_pin, led_state);

  // ADC.
  adc.setup();
  adc.setVoltageReference(VREF_EXTERNAL);
  adc.setGain(adc_gain_toSet);
  adc.setDataRate(1000); // 20, 90, 330, 1000
  adc.setConversionMode(adc_mode_toSet);
  adc.start(); // start continuous conversion (or a single reading)

  // GPIO expander.
  if(downsampling_factor_lod > 0)
    setup_gpioExpander();
  else
  {
    #if !DATAREADY_iS_DIRECT
    setup_gpioExpander();
    #endif
  }
}

//===========================
// STREAM DATA
//===========================
int adc_reading_ecg = 0;
int acquired_any = 0;
int acquired_ecg = 0;
int acquired_electrode1 = 0;
int acquired_electrode2 = 0;
int acquired_lod = 0;

#if DEBUG_EXPANDER_RATE
long expander_count = 0;
#endif
#if DEBUG_DRDY_HIGHS_LOWS
int counts_high[100] = {0};
int counts_low[100] = {0};
int count_index = 0;
#endif

void loop()
{
  // Record the start time.
  if(start_time_ms == 0)
    start_time_ms = millis();

  // --------------------------------
  #if DEBUG_DRDY_HIGHS_LOWS

  while(adc.readDataReady()==1) counts_high[count_index]++;

  long start_time_us = micros();
  Wire.beginTransmission(i2c_address_adc);
  Wire.write(0x10);
  Wire.endTransmission();
  Wire.requestFrom((uint8_t)i2c_address_adc,(uint8_t)3);
  Wire.read();
  Wire.read();
  Wire.read();
  long end_time_us = micros();

  while(adc.readDataReady()==0) counts_low[count_index]++;
  count_index++;
  if(count_index == 100)
  {
     Serial.println();
     for(int i = 0; i < count_index; i++)
     {
       Serial.print(counts_high[i]);
       Serial.print("\t");
       Serial.print(counts_low[i]);
       Serial.println();
       counts_high[i] = 0;
       counts_low[i] = 0;
     }
     Serial.println((int)(end_time_us - start_time_us));
     count_index = 0;
  }
  return;
  #endif // DEBUG_DRDY_HIGHS_LOWS
  // --------------------------------

  // --------------------------------
  #if DEBUG_EXPANDER_RATE
  int data = read_gpio_expander();
  expander_count++;
  if(expander_count % 10000 == 0)
  {
    Serial.print(data); Serial.print("  ");
    Serial.println(1000.0*(float)expander_count/(float)(millis() - start_time_ms));
  }
  return;
  #endif // DEBUG_EXPANDER_RATE
  // --------------------------------

  // Get the latest ECG data from the ADC.
  // Do this regardless of the downsampling rate, since we will use
  //  this read to set the base loop rate.
  adc_reading_ecg = adc.readSingleEnded(adc_channel_ecg); //*3.3/pow(2,23);
  acquired_any = 0;
  acquired_ecg = 0;
  if((num_readings % downsampling_factor_ecg == 0) && (downsampling_factor_ecg > 0))
  {
    latest_reading_ecg = adc_reading_ecg;
    num_readings_ecg++;
    acquired_ecg = 1;
    acquired_any = 1;
  }
  // Get the latest downsampled electrode data from the ADC.
  acquired_electrode1 = 0;
  acquired_electrode2 = 0;
  acquired_lod = 0;
  if((num_readings % downsampling_factor_electrode1 == 0) && (downsampling_factor_electrode1 > 0))
  {
    latest_reading_electrode1 = adc.readSingleEnded(adc_channel_electrode1); //*3.3/pow(2,23);
    num_readings_electrode1++;
    acquired_electrode1 = 1;
    acquired_any = 1;
  }
  if((num_readings % downsampling_factor_electrode2 == 0) && (downsampling_factor_electrode2 > 0))
  {
    latest_reading_electrode2 = adc.readSingleEnded(adc_channel_electrode2); //*3.3/pow(2,23);
    num_readings_electrode2++;
    acquired_electrode2 = 1;
    acquired_any = 1;
  }
  if((num_readings % downsampling_factor_lod == 0) && (downsampling_factor_lod > 0))
  {
    latest_reading_lod = parse_gpio_expander_lod(read_gpio_expander());
    num_readings_lod++;
    acquired_lod = 1;
    acquired_any = 1;
  }
  // Increment the loop counter.
  num_readings++;
  time_since_start_ms = millis() - start_time_ms;

  // Indicate the ECG sampling rate using the LED.
  if(acquired_ecg)
    digitalWrite(led_pin, led_state); led_state = !led_state;

  // Convert ADC readings to volts if desired.
  if(convert_to_v)
  {
    if(acquired_ecg)
      latest_reading_ecg = latest_reading_ecg*3.3/pow(2,23);
    if(acquired_electrode1)
      latest_reading_electrode1 = latest_reading_electrode1*3.3/pow(2,23);
    if(acquired_electrode2)
      latest_reading_electrode2 = latest_reading_electrode2*3.3/pow(2,23);
  }

  // Stream data if desired.
  // Will be space-separated values, and will replace values with '--' if not sampled this timestep.
  #if STREAM_DATA
  if(acquired_any)
  {
    long long checksum = 0;
    long long timestamp_us = micros();
    Serial.print(timestamp_us);
    Serial.print(" ");
    checksum += timestamp_us;
    // Stream the main ECG reading.
    if(acquired_ecg)
    {
      Serial.print(latest_reading_ecg, convert_to_v ? 10 : 0);
      Serial.print(" ");
      checksum += (long long)(latest_reading_ecg);
    }
    else if(downsampling_factor_ecg > 0)
        Serial.print("-- ");
    // Stream the electrode1 value or '--', or nothing if not streaming it.
    if(acquired_electrode1)
    {
      Serial.print(latest_reading_electrode1, convert_to_v ? 10 : 0);
      Serial.print(" ");
      checksum += (long long)latest_reading_electrode1;
    }
    else if(downsampling_factor_electrode1 > 0)
      Serial.print("-- ");
    // Stream the electrode2 value or '--', or nothing if not streaming it.
    if(acquired_electrode2)
    {
      Serial.print(latest_reading_electrode2, convert_to_v ? 10 : 0);
      Serial.print(" ");
      checksum += (long long)latest_reading_electrode2;
    }
    else if(downsampling_factor_electrode1 > 0)
      Serial.print("-- ");
    // Stream the LOD value or '--', or nothing if not streaming it.
    if(acquired_lod)
    {
      Serial.print(latest_reading_lod, 0);
      Serial.print(" ");
      checksum += (long long)latest_reading_lod;
    }
    else if(downsampling_factor_lod > 0)
      Serial.print("-- ");
    Serial.print(checksum);
    Serial.println();
  }
  #endif

  // Stream only ECG data if desired.
  #if STREAM_ECG_ONLY
  if(acquired_ecg)
  {
    Serial.println(latest_reading_ecg, convert_to_v ? 10 : 0);
  }
  #endif

  // Debug printouts if desired.
  #if DEBUG_PRINT_DATA
  Serial.print("Single ended results (ECG | E1 | E2): ");
  Serial.print(" "); Serial.print(acquired_ecg ? latest_reading_ecg : -1, convert_to_v ? 3 : 0);
  Serial.print(" "); Serial.print(acquired_electrode1 ? latest_reading_electrode1 : -1, convert_to_v ? 3 : 0);
  Serial.print(" "); Serial.print(acquired_electrode2 ? latest_reading_electrode2 : -1, convert_to_v ? 3 : 0);
  Serial.println();
  #endif
  #if DEBUG_PRINT_RATE
  if(num_readings % 100 == 0)
  {
    Serial.print("ECG E1 E2 LOD | ");
    Serial.print("Fs:");
    Serial.print(" "); Serial.print(1000.0*(float)num_readings_ecg/(float)time_since_start_ms, 2);
    Serial.print(" "); Serial.print(1000.0*(float)num_readings_electrode1/(float)time_since_start_ms, 2);
    Serial.print(" "); Serial.print(1000.0*(float)num_readings_electrode2/(float)time_since_start_ms, 2);
    Serial.print(" "); Serial.print(1000.0*(float)num_readings_lod/(float)time_since_start_ms, 2);
    // Serial.print(" (");
    // Serial.print(num_readings_ecg); Serial.print(" readings in ");
    // Serial.print(time_since_start_ms/1000.0, 3); Serial.print(" s");
    // Serial.print(")");
    Serial.print(" Latest:");
    Serial.print(" "); Serial.print(latest_reading_ecg, convert_to_v ? 3 : 0);
    Serial.print(" "); Serial.print(latest_reading_electrode1, convert_to_v ? 3 : 0);
    Serial.print(" "); Serial.print(latest_reading_electrode2, convert_to_v ? 3 : 0);
    Serial.print(" "); Serial.print(latest_reading_lod, 0);
    Serial.println();
  }
  #endif
}

//===========================
// HELPERS
//===========================

