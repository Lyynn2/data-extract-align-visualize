
#include "PCA9674.h"

void setup_gpioExpander()
{
  // Note that all ports are inputs by default at power-on.
  // The below code should also set them all to inputs,
  //   but will also cause strong pullups to be briefly connected (during HIGH time of the acknowledgment pulse).
  //   To avoid this for now, the default state is leveraged and no commands are sent.
//  Wire.beginTransmission((i2c_address_expander << 1) & 0b00000000); // set last bit to 0 to indicate write mode
//  Wire.send(0b11111111); // set all to inputs (1 = weakly driven high)
//  Wire.endTransmission();
}


int read_gpio_expander()
{
  Wire.requestFrom((int)(i2c_address_expander), // set last bit to 1 to indicate read mode,(uint8_t)3);
                   1, // read a single byte
                   1 // stop the transmission when done
                   );
  int data = Wire.read();
//  Serial.println(data);
  return data;
}

int parse_gpio_expander_dataReady(int data)
{
  return (data >> expander_channel_dataReady) & 0b00000001;
}




