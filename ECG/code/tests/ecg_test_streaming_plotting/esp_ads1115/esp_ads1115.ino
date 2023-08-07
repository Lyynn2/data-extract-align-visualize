

#include <Wire.h>
#include "Adafruit_ADS1X15.h"

// Define the ECG pins.
#define ADC_CHANNEL_ECG 0
#define ECG_PIN_LO_NEG A2
#define ECG_PIN_LO_POS A1
int16_t ecg_reading = 0;
float ecg_v = 0;
int ecg_leadOff_pos = 0;
int ecg_leadOff_neg = 0;

// Note that the Adafruit_ADS1X15 Arduino library should be installed (with dependencies).
Adafruit_ADS1115 adc;
// Set the ADC address, as set by the ADDR pin wiring:
//    GND: 0x48
//    VDD: 0x49
//    SDA: 0x4A
//    SCL: 0x4B
#define ADC_ADDRESS 0x48
// Set the ADC gain, selecting from the following options:
//    GAIN_TWOTHIRDS: 2/3x gain   max 6.144V  1 bit = 187.5    uV (default)
//    GAIN_ONE:         1x gain   max 4.096V  1 bit = 125.0    uV
//    GAIN_TWO:         2x gain   max 2.048V  1 bit =  62.5    uV
//    GAIN_FOUR:        4x gain   max 1.024V  1 bit =  31.25   uV
//    GAIN_EIGHT:       8x gain   max 0.512V  1 bit =  15.625  uV
//    GAIN_SIXTEEN:    16x gain   max 0.256V  1 bit =   7.8125 uV
adsGain_t adc_gain_code = GAIN_ONE;
float adc_gain = 1; // will be set during setup()
uint16_t adc_max_reading = pow(2, 15);
#define adc_reading_to_v(reading) ((reading)*(4.096/(adc_gain))/((float)adc_max_reading))
// Set the ADC sampling rate, selecting from the following options:
//    RATE_ADS1115_8SPS, RATE_ADS1115_16SPS, RATE_ADS1115_32SPS, RATE_ADS1115_64SPS
//    RATE_ADS1115_128SPS (default), RATE_ADS1115_250SPS, RATE_ADS1115_475SPS, RATE_ADS1115_860SPS
uint16_t adc_rate = RATE_ADS1115_860SPS; // sets speed of one reading (so if reading N channels, effective rate is rate/N)
// Specify which ADC channels are being used.
//int adc_channels[] = {0,1,2,3};
//const int num_adc_channels = sizeof(adc_channels)/sizeof(int);
//int16_t adc_readings[num_adc_channels] = {0};
//unsigned long reading_start_time_ms = 0;
//unsigned long reading_count = 0;

//=================================================
// SETUP
//=================================================
void setup()
{
  delay(500);

  // Start Serial.
  Serial.begin(500000);

  // Set up the ADC.
  adc.begin(ADC_ADDRESS);  // Initialize ads1115 at the specified address
  adc.setGain(adc_gain_code);
  adc.setDataRate(adc_rate);
//  Wire.setClock(100000);
  switch(adc_gain_code)
  {
    case GAIN_TWOTHIRDS: adc_gain = 0.66667; break;
    case GAIN_ONE: adc_gain = 1; break;
    case GAIN_TWO: adc_gain = 2; break;
    case GAIN_FOUR: adc_gain = 4; break;
    case GAIN_EIGHT: adc_gain = 8; break;
    case GAIN_SIXTEEN: adc_gain = 16; break;
  }

  // Set up the ECG.
  pinMode(ECG_PIN_LO_NEG, INPUT);
  pinMode(ECG_PIN_LO_POS, INPUT);

//  // Extra state.
//  reading_start_time_ms = millis();
}

//=================================================
// MAIN LOOP
//=================================================
void loop()
{
//  for(int channel_index = 0; channel_index < num_adc_channels; channel_index++)
//  {
//    adc_readings[channel_index] = adc.readADC_SingleEnded(adc_channels[channel_index]);
//    Serial.print(adc_readings[channel_index]);
//    Serial.print(" = "); Serial.print(adc_reading_to_v(adc_readings[channel_index])); Serial.print(" V");
//    Serial.print(" | ");
//  }
//  reading_count++;
//  Serial.print(1000*((float)reading_count)/(float)(millis() - reading_start_time_ms));
//  Serial.println(" Hz");
////  delay(500);

  ecg_reading = adc.readADC_SingleEnded(ADC_CHANNEL_ECG);
  ecg_v = adc_reading_to_v(ecg_reading);
  ecg_leadOff_neg = digitalRead(ECG_PIN_LO_NEG);
  ecg_leadOff_pos = digitalRead(ECG_PIN_LO_POS);
  Serial.println(ecg_v);
}
//int16_t readADC_Differential_0_1();
//int16_t readADC_Differential_0_3();
//int16_t readADC_Differential_1_3();
//int16_t readADC_Differential_2_3();












