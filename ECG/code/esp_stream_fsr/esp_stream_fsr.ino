////////////////////////
//
// Copyright (c) 2022 MIT CSAIL and Joseph DelPreto
//
// Permission is hereby granted, free of charge, to any person obtaining a copy
// of this software and associated documentation files (the "Software"), to deal
// in the Software without restriction, including without limitation the rights
// to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
// copies of the Software, and to permit persons to whom the Software is
// furnished to do so, subject to the following conditions:
//
// The above copyright notice and this permission notice shall be included in all
// copies or substantial portions of the Software.
//
// THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
// IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
// FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
// AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
// WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR
// IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
//
// See https://action-net.csail.mit.edu for more usage information.
// Created 2021-2022 for the MIT ActionNet project by Joseph DelPreto [https://josephdelpreto.com].
//
////////////////////////

#define SEND_RAW_ADC 1
#define SEND_WEIGHT_G 0

#define SEND_DEBUG_VALUES 0 // Whether to send known values instead of sensor readings.
                            // Can set this in SerialStreamer.py too to validate the data.

const int sensor_pins[] = {A0};
const int num_sensors = sizeof(sensor_pins)/sizeof(int);
const int poll_period_ms = 10;
const int baud_rate = 1000000;

//const float coefficients[] = {-34.416410, 399.877749, -1386.324462, 2122.079718, -1470.201359, 479.334415, 4.552456};
//const float coefficients[] = {-1949.588886, 13243.139465, -33011.884780, 37425.445088, -18921.242689, 3389.203504, 2.768159};
//const float coefficients[] = {8339.076153, -91715.885797, 428078.730459, -1103709.224302, 1713579.959523, -1636660.026717, 941007.491040, -303550.181292, 46852.889309, -2176.721159, 13.891007};
//const float coefficients[] = {101.886767, -593.699816, 1228.494027, -985.772478, 172.939088, 163.948741, 6.843702};
//const float coefficients[] = {-30.467544, 367.334293, -1286.201335, 1981.716805, -1383.710184, 461.584498, 4.622415};
const float coefficients[] = {-25.674057, 322.216413, -1120.630206, 1684.381111, -1116.269110, 352.785676, 18.982699};
const int num_coefficients = sizeof(coefficients)/sizeof(float);

void setup()
{
  Serial.begin(baud_rate);
  while(!Serial);
  Serial.println();

  for(int sensor_index = 0; sensor_index < num_sensors; sensor_index++)
    pinMode(sensor_pins[sensor_index], INPUT);
}

void loop()
{
  for(int sensor_index = 0; sensor_index < num_sensors; sensor_index++)
  {
    #if SEND_DEBUG_VALUES
    Serial.print(sensor_index);
    #else
    #if SEND_RAW_ADC
    Serial.print(analogRead(sensor_pins[sensor_index]));
    Serial.print(" ");
    #endif
    #if SEND_WEIGHT_G
    double reading_adc = analogRead(sensor_pins[sensor_index]);
    double reading_v = 3.3*reading_adc/4095.0;
    double weight_g = 0;
    for(int i = 0; i < num_coefficients; i++)
      weight_g += coefficients[i]*pow(reading_v, num_coefficients-(i+1));
//    Serial.print(reading_adc); Serial.print(" ");
//    Serial.print(reading_v); Serial.print(" ");
//    Serial.print(num_coefficients); Serial.print(" ");
    Serial.print(weight_g, 1);
    Serial.print(" ");
    #endif
    #endif
    if(sensor_index+1 < num_sensors)
      Serial.print(" ");
  }
  Serial.println();
  delay(poll_period_ms);
}
