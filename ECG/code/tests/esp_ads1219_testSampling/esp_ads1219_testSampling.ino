
#include "ADS1219.h"
#include <Wire.h>

const int debug_readings = 0;
const int debug_rate = 1;
const int lod_downsampling_factor = 10;
const int iao_downsampling_factor =  3;

const int ecg_channel = 0;
const int lod_channel = 1;
const int iao_channel = 2;
const int data_ready_pin = 14;
const uint8_t i2c_address = 0b1000000;
adsGain_t adc_gain_toSet = ONE; // ONE or FOUR
adsMode_t adc_mode_toSet = debug_rate ? CONTINUOUS : SINGLE_SHOT; // SINGLE_SHOT or CONTINUOUS

ADS1219 adc(data_ready_pin, i2c_address);

float latest_reading_ecg = 0;
float latest_reading_lod = 0;
float latest_reading_iao = 0;
long num_ecg_readings = 0;
float start_time_ms = 0;
float time_since_start_ms = 0;
int led_state = 0;

void setup()
{
  Serial.begin(500000);
  delay(1000);
  Serial.println();
  Serial.println();
  Serial.println("Setting up!");

  pinMode(data_ready_pin, INPUT_PULLUP);
  pinMode(13, OUTPUT);
  digitalWrite(13, led_state);

  adc.begin();
  Wire.setClock(400000);
  adc.setVoltageReference(REF_EXTERNAL);
  adc.setGain(adc_gain_toSet);
  adc.setDataRate(1000); // 20, 90, 330, 1000
  adc.setConversionMode(adc_mode_toSet);
  if(adc_mode_toSet == CONTINUOUS)
    start_continuous_conversion();
}

void loop()
{
  if(start_time_ms == 0)
    start_time_ms = millis();

  latest_reading_ecg = adc.readSingleEnded(ecg_channel)*3.3/pow(2,23);
  if(num_ecg_readings % lod_downsampling_factor == 0)
    latest_reading_lod = adc.readSingleEnded(lod_channel)*3.3/pow(2,23);
  if(num_ecg_readings % iao_downsampling_factor == 0)
    latest_reading_iao = adc.readSingleEnded(iao_channel)*3.3/pow(2,23);
  time_since_start_ms = millis() - start_time_ms;
  num_ecg_readings++;

  if(debug_readings)
  {
    Serial.println();
    Serial.print("Single ended results: ");
    Serial.print(latest_reading_ecg, 5); Serial.print(" ECG | ");
    Serial.print(latest_reading_lod, 5); Serial.print(" LOD | ");
    Serial.print(latest_reading_iao, 5); Serial.print(" IAO");
    Serial.println();
    delay(500);
  }
  else if(debug_rate)
  {
    if(num_ecg_readings % 100 == 0)
    {
      digitalWrite(13, led_state); led_state = !led_state;
      Serial.print("Fs: ");
      Serial.print(1000.0*(float)num_ecg_readings/(float)time_since_start_ms);
      Serial.print(" (");
      Serial.print(num_ecg_readings); Serial.print(" readings in ");
      Serial.print(time_since_start_ms/1000.0, 3); Serial.print(" s");
      Serial.print(")");
      Serial.print(" Latest: ");
      Serial.print(latest_reading_ecg, 5); Serial.print(" ECG | ");
      Serial.print(latest_reading_lod, 5); Serial.print(" LOD | ");
      Serial.print(latest_reading_iao, 5); Serial.print(" IAO");
      Serial.println();
    }
  }

}

void start_continuous_conversion()
{
  Wire.beginTransmission(i2c_address);
  #if ARDUINO >= 100
  Wire.write(0x08);
  #else
  Wire.send(0x08);
  #endif
  Wire.endTransmission();
}





