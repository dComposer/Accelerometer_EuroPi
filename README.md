# Connecting an ADXL343 Accelerometer to a EuroPi module
 A simple script adapting [Shawn Hymel's ADXL343 I2C tutorial code](https://www.digikey.com/en/maker/projects/raspberry-pi-pico-rp2040-i2c-example-with-micropython-and-cc/47d0c922b79342779cdbd4b37b7eb7e2) for the [EuroPi](https://github.com/Allen-Synthesis/EuroPi) module.

## Voltage Outputs
Output | Value
--- | ---
CV1 | X
CV2 | Y
CV3 | Z
CV4 | 1-X
CV5 | 1-Y
CV6 | 1-Z

## Hex Addresses on the ADXL343
Refer to [Table 19 on Page 21 of the ADXL343's Datasheet](https://cdn-learn.adafruit.com/assets/assets/000/070/556/original/adxl343.pdf#page=21) for a complete description of what each hex address is referring to in the accelerometer_europi.py code.

## EuroPi I2C setup
For I2C, you only need to use 4 pins on the ADXL343: VIN, GND, SDA, and SCL. Connect these pins to the EuroPi (the I2C breakout header lists VIN as 3V3) and use this code to let the EuroPi read data from the [ADXL343 breakout board](https://www.digikey.com/en/products/detail/adafruit-industries-llc/4097/9951931): 
```python
i2c = machine.I2C(1, scl=machine.Pin(3), sda=machine.Pin(2), freq=400000)
```

## Demo
![ADXL343 to EuroPi Demo](accel_demo.gif)