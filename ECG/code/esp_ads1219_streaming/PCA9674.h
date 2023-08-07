
#ifndef PCA9674_H
#define PCA9674_H

#include "Arduino.h"
#include <Wire.h>

const uint8_t i2c_address_expander = 0b0111001;
const int expander_channel_dataReady = 3;

void setup_gpioExpander();
int read_gpio_expander();
int parse_gpio_expander_dataReady(int data);



#endif // PCA9674_H

