import machine
import utime
import ustruct
import sys
from europi import *

###############################################################################
# Constants

# I2C address
ADXL343_ADDR = 0x53

# Registers
REG_DEVID = 0x00
REG_POWER_CTL = 0x2D
REG_DATAX0 = 0x32

# Other constants
DEVID = 0xE5
SENSITIVITY_2G = 1.0 / 256  # (g/LSB)
EARTH_GRAVITY = 9.80665  # Earth's gravity in [m/s^2]

###############################################################################
# Settings

# Initialize I2C with pins
i2c = machine.I2C(1, scl=machine.Pin(3), sda=machine.Pin(2), freq=400000)

###############################################################################
# Functions


def reg_write(i2c, addr, reg, data):
    """
    Write bytes to the specified register.
    """

    # Construct message
    msg = bytearray()
    msg.append(data)

    # Write out message to register
    i2c.writeto_mem(addr, reg, msg)


def reg_read(i2c, addr, reg, nbytes=1):
    """
    Read byte(s) from specified register. If nbytes > 1, read from consecutive
    registers.
    """

    # Check to make sure caller is asking for 1 or more bytes
    if nbytes < 1:
        return bytearray()

    # Request data from specified register(s) over I2C
    data = i2c.readfrom_mem(addr, reg, nbytes)

    return data


# Range converter
# Will return a integer
def convert(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min


###############################################################################
# Main

# Read device ID to make sure that we can communicate with the ADXL343
data = reg_read(i2c, ADXL343_ADDR, REG_DEVID)
if data != bytearray((DEVID,)):
    print("ERROR: Could not communicate with ADXL343")
    sys.exit()

# Read Power Control register
data = reg_read(i2c, ADXL343_ADDR, REG_POWER_CTL)
print(data)

# Tell ADXL343 to start taking measurements by setting Measure bit to high
data = int.from_bytes(data, "big") | (1 << 3)
reg_write(i2c, ADXL343_ADDR, REG_POWER_CTL, data)

# Test: read Power Control register back to make sure Measure bit was set
data = reg_read(i2c, ADXL343_ADDR, REG_POWER_CTL)
print(data)

# Wait before taking measurements
# utime.sleep(2.0)

# Run forever
while True:

    # Read X, Y, and Z values from registers (16 bits each)
    data = reg_read(i2c, ADXL343_ADDR, REG_DATAX0, 6)

    # Convert 2 bytes (little-endian) into 16-bit integer (signed)
    acc_x = ustruct.unpack_from("<h", data, 0)[0]
    acc_y = ustruct.unpack_from("<h", data, 2)[0]
    acc_z = ustruct.unpack_from("<h", data, 4)[0]

    acc_x = convert(acc_x, -512, 512, 0, 1000) / 100
    acc_y = convert(acc_y, -512, 512, 0, 1000) / 100
    acc_z = convert(acc_z, -512, 512, 0, 1000) / 100

    if acc_x < 0:
        acc_x = 0

    if acc_y < 0:
        acc_y = 0

    if acc_z < 0:
        acc_z = 0

    print(f"{acc_x} | {acc_y} | {acc_z}")

    # Print results
    oled.fill(0)

    oled.centre_text(f"X: {acc_x:.2f}\nY: {acc_y:.2f}\nZ: {acc_z:.2f}")

    # Send X/Y/Z voltage data out the EuroPi's CV outputs
    cv1.voltage(acc_x)
    cv2.voltage(acc_y)
    cv3.voltage(acc_z)
    cv4.voltage(10 - acc_x)
    cv5.voltage(10 - acc_y)
    cv6.voltage(10 - acc_z)

    oled.show()
    utime.sleep_ms(10)
