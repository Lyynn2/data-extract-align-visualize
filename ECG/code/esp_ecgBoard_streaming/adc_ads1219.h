
#ifndef ADC_ADS1219_H
#define ADC_ADS1219_H

#include "Arduino.h"
#include <Wire.h>
#include "gpio_pca9674.h"

#define CONFIG_REGISTER_ADDRESS 0x40
#define STATUS_REGISTER_ADDRESS 0x24

#define MUX_MASK 				0x1F
#define MUX_DIFF_0_1		0x00
#define MUX_DIFF_2_3		0x20
#define MUX_DIFF_1_2		0x40
#define MUX_SINGLE_0		0x60
#define MUX_SINGLE_1		0x80
#define MUX_SINGLE_2		0xA0
#define MUX_SINGLE_3		0xC0
#define MUX_SHORTED			0xE0

#define GAIN_MASK 			0xEF
#define GAIN_ONE				0x00
#define GAIN_FOUR				0x10

#define DATA_RATE_MASK		0xF3
#define DATA_RATE_20			0x00
#define DATA_RATE_90			0x04
#define DATA_RATE_330			0x08
#define DATA_RATE_1000		0x0c

#define MODE_MASK				  0xFD
#define MODE_SINGLE_SHOT	0x00
#define MODE_CONTINUOUS		0x02

#define VREF_MASK				0xFE
#define VREF_INTERNAL		0x00
#define VREF_EXTERNAL		0x01

#define ADC_CMD_RESET		0x06
#define ADC_CMD_START		0x08
#define ADC_CMD_POWERDOWN		0x02
#define ADC_CMD_RREG		0x10
#define ADC_CONFIG_RESET  0x00

class ADC_ADS1219
{
  protected:
	uint8_t i2c_address;

  public:
    // Constructor
    ADC_ADS1219(uint8_t in_i2c_address, int in_data_ready_pin = -1);

    // Methods
    void setup();
    void start();
    void resetConfig();
    long readSingleEnded(int channel);
    long readDifferential_0_1();
    long readDifferential_2_3();
    long readDifferential_1_2();
    long readShorted();
    void setGain(uint8_t gain);
    void setDataRate(int rate);
    void setConversionMode(uint8_t mode);
    void setVoltageReference(uint8_t vref);
    void powerDown();
    int readDataReady();

  private:
    uint8_t readRegister(uint8_t reg);
    void writeConfigRegister(uint8_t data);
    void setConfig();
    long readData();
    uint8_t config;
    uint8_t config_prev;
    int singleShot;
    int data_ready_pin;
};

#endif // ADC_ADS1219_H






