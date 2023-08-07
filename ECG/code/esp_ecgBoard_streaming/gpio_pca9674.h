
#ifndef GPIO_PCA9674_H
#define GPIO_PCA9674_H

#include "Arduino.h"
#include <Wire.h>

const uint8_t i2c_address_expander = 0b0111001;
const int expander_channel_dataReady = 7; // The data-ready line of the ADC.
                                          //   7 for the new ECG board (v1.1), and
                                          //   3 for the old board (v0.9 and v1.0).
const int expander_channel_lod = 1;

void setup_gpioExpander();
int read_gpio_expander();
int parse_gpio_expander_dataReady(int data);
int parse_gpio_expander_lod(int data);



#endif // GPIO_PCA9674_H

