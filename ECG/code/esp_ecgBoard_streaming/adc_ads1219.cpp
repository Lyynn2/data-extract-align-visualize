
#include "Arduino.h"
#include <Wire.h>
#include "adc_ads1219.h"

// ========================================================
// ==================== INITIALIZATION ====================
// ========================================================
ADC_ADS1219::ADC_ADS1219(uint8_t in_i2c_address, int in_data_ready_pin /* = -1 */)
{
  data_ready_pin = in_data_ready_pin;
  i2c_address = in_i2c_address;
  config = 0x00;
  config_prev = 0x00;
  singleShot = 1;
}

void ADC_ADS1219::setup()
{
  // Make sure power is settled.
  delayMicroseconds(500);
  // Start the I2C bus.
  Wire.begin();
  delayMicroseconds(500);
  Wire.setClock(400000);
  delayMicroseconds(500);
  // Send a reset command.
  Wire.beginTransmission(i2c_address);
  Wire.write(ADC_CMD_RESET);
  Wire.endTransmission();
  // Reset the configuration just to be sure, and to initialize our previous config state.
  resetConfig();
}

void ADC_ADS1219::start()
{
  Wire.beginTransmission(i2c_address);
  Wire.write(ADC_CMD_START);
  Wire.endTransmission();
}

void ADC_ADS1219::powerDown()
{
  Wire.beginTransmission(i2c_address);
  Wire.write(ADC_CMD_POWERDOWN);
  Wire.endTransmission();
}

// ========================================================
// ==================== MODES/SETTINGS ====================
// ========================================================

void ADC_ADS1219::setGain(uint8_t gain)
{
  config &= GAIN_MASK;
  config |= gain;
  setConfig();
}

void ADC_ADS1219::setDataRate(int rate)
{
	config &= DATA_RATE_MASK;
	switch (rate)
	{
    case (20):
      config |= DATA_RATE_20;
      break;
    case (90):
      config |= DATA_RATE_90;
      break;
    case (330):
      config |= DATA_RATE_330;
      break;
    case (1000):
      config |= DATA_RATE_1000;
      break;
	default:
	  break;
  }
  setConfig();
}

void ADC_ADS1219::setConversionMode(uint8_t mode)
{
  config &= MODE_MASK;
  config |= mode;
  setConfig();
  if(mode == MODE_CONTINUOUS)
	  singleShot = 0;
  else
	  singleShot = 1;
}

void ADC_ADS1219::setVoltageReference(uint8_t vref)
{
  config &= VREF_MASK;
  config |= vref;
  setConfig();
}

// ========================================================
// =================== CONFIG/REGISTERS ===================
// ========================================================
uint8_t ADC_ADS1219::readRegister(uint8_t reg)
{
  Wire.beginTransmission(i2c_address);
  Wire.write(reg);
  Wire.endTransmission();
  Wire.requestFrom((uint8_t)i2c_address, (uint8_t)1);
  return Wire.read();
}

void ADC_ADS1219::writeConfigRegister(uint8_t data)
{
  Wire.beginTransmission(i2c_address);
  Wire.write(CONFIG_REGISTER_ADDRESS);
  Wire.write(data);
  Wire.endTransmission();
}

void ADC_ADS1219::setConfig()
{
  if(config != config_prev)
  {
    writeConfigRegister(config);
    config_prev = config;
  }
}

void ADC_ADS1219::resetConfig()
{
  config = ADC_CONFIG_RESET;
  config_prev = config;
	writeConfigRegister(config);
}

// ========================================================
// ======================= READ DATA ======================
// ========================================================

// Read, parse, and return data.
// Assumes config is already set for the desired channel.
long ADC_ADS1219::readData()
{
  // Start conversion if needed (if not continuous mode).
  if(singleShot)
  {
    start();
  }
  // Wait for the data to be ready.
//  unsigned long t0, t1;
//  t0 = micros();
//  while(readDataReady()==0);
//  t1 = micros();
//  Serial.println((int)(t1 - t0));
//  t0 = micros();
  while(readDataReady()==1);
//  t1 = micros();
//  Serial.println((int)(t1 - t0));
  // Read the data!
  Wire.beginTransmission(i2c_address);
  Wire.write(ADC_CMD_RREG);
  Wire.endTransmission();
  Wire.requestFrom((uint8_t)i2c_address, (uint8_t)3);
  // Parse the data bytes.
  long data32 = Wire.read();
  data32 <<= 8;
  data32 |= Wire.read();
  data32 <<= 8;
  data32 |= Wire.read();
  return (data32 << 8) >> 8;
}

long ADC_ADS1219::readSingleEnded(int channel)
{
  // Update the configuration for the desired channel.
	config &= MUX_MASK;
	switch (channel)
	{
    case (0):
      config |= MUX_SINGLE_0;
      break;
    case (1):
      config |= MUX_SINGLE_1;
      break;
    case (2):
      config |= MUX_SINGLE_2;
      break;
    case (3):
      config |= MUX_SINGLE_3;
      break;
	default:
	  break;
  }
  setConfig();
  // Read the data.
  return readData();
}

long ADC_ADS1219::readDifferential_0_1()
{
  // Update the configuration for the desired channel.
  config &= MUX_MASK;
  config |= MUX_DIFF_0_1;
  setConfig();
  // Read the data.
  return readData();
}

long ADC_ADS1219::readDifferential_2_3()
{
  // Update the configuration for the desired channel.
  config &= MUX_MASK;
  config |= MUX_DIFF_2_3;
  setConfig();
  // Read the data.
  return readData();
}

long ADC_ADS1219::readDifferential_1_2()
{
  // Update the configuration for the desired channel.
  config &= MUX_MASK;
  config |= MUX_DIFF_1_2;
  setConfig();
  // Read the data.
  return readData();
}

long ADC_ADS1219::readShorted()
{
  // Update the configuration for the desired channel.
  config &= MUX_MASK;
  config |= MUX_SHORTED;
  setConfig();
  // Read the data.
  return readData();
}

// ========================================================
// ======================= HELPERS ========================
// ========================================================

// Read the data ready bit, either via a direct connection or via the GPIO expander.
int ADC_ADS1219::readDataReady()
{
  if(data_ready_pin >= 0)
    return digitalRead(data_ready_pin);
  else
    return parse_gpio_expander_dataReady(read_gpio_expander());
}