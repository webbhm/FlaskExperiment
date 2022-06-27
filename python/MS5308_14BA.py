# Distributed with a free-will license.
# Use it any way you want, profit or free, provided it fits in the licenses of its associated works.
# MS5803_05BA
# This code is designed to work with the MS5803_05BA_I2CS I2C Mini Module available from ControlEverything.com.
# https://www.controleverything.com/content/Temperature?sku=MS5803-05BA_I2CS#tabs-0-product_tabset-2

import smbus
import time

ADDR = 0x76
RESET_CMD = 0x1E
# PROM Reads
C1_CMD = 0xA2
C2_CMD = 0xA4
C3_CMD = 0xA6
C4_CMD = 0xA8
C5_CMD = 0xAA
C6_CMD = 0xAC
OSR_256 = 0x40   # 0x40(64)    Pressure conversion(OSR = 256) command
ADC_READ = 0x00 #  Read digital pressure
D2_OSR_256 = 0x50


# Get I2C bus
bus = smbus.SMBus(1)

# MS5803_05BA address, 0x76(118)
#       0x1E(30)    Reset command
bus.write_byte(ADDR, RESET_CMD)

time.sleep(0.5)

# Read 12 bytes of calibration data
# Read pressure sensitivity
data = bus.read_i2c_block_data(ADDR, C1_CMD, 2)
C1 = data[0] * 256 + data[1]
print("C1", C1, "Data:", data)

# Read pressure offset
data = bus.read_i2c_block_data(ADDR, C2_CMD, 2)
C2 = data[0] * 256 + data[1]
print("C2", C2, "Data:", data)


# Read temperature coefficient of pressure sensitivity
data = bus.read_i2c_block_data(ADDR, C3_CMD, 2)
C3 = data[0] * 256 + data[1]
print("C3", C3, "Data:", data)

# Read temperature coefficient of pressure offset
data = bus.read_i2c_block_data(ADDR, C4_CMD, 2)
C4 = data[0] * 256 + data[1]
print("C4", C4, "Data:", data)

# Read reference temperature
data = bus.read_i2c_block_data(ADDR, C5_CMD, 2)
C5 = data[0] * 256 + data[1]
print("C5", C5, "Data:", data)

# Read temperature coefficient of the temperature
data = bus.read_i2c_block_data(ADDR, C6_CMD, 2)
C6 = data[0] * 256 + data[1]
print("C6", C6, "Data:", data)

# MS5803_05BA address, 0x76(118)
#       0x40(64)    Pressure conversion(OSR = 256) command
bus.write_byte(ADDR, OSR_256)

time.sleep(0.5)

# Read digital pressure value
# Read data back from 0x00(0), 3 bytes
# D1 MSB2, D1 MSB1, D1 LSB
value = bus.read_i2c_block_data(ADDR, ADC_READ, 3)
print("Dig Pressure", value)
D1 = value[0] * 65536 + value[1] * 256 + value[2]
print("D1", D1, "Value:", value)

# MS5803_05BA address, 0x76(118)
#       0x50(64)    Temperature conversion(OSR = 256) command
bus.write_byte(ADDR, D2_OSR_256)

time.sleep(0.5)

# Read digital temperature value
# Read data back from 0x00(0), 3 bytes
# D2 MSB2, D2 MSB1, D2 LSB
value = bus.read_i2c_block_data(ADDR, ADC_READ, 3)
D2 = value[0] * 65536 + value[1] * 256 + value[2]
print("D2", D2, "Value", value)

dT = D2 - C5 * 256
TEMP = 2000 + dT * C6 / 8388608
OFF = C2 * 262144 + (C4 * dT) / 32
SENS = C1 * 131072 + (C3 * dT ) / 128
T2 = 0
OFF2 = 0
SENS2 = 0

if TEMP > 2000 :
    T2 = 0
    OFF2 = 0
    SENS2 = 0
elif TEMP < 2000 :
    T2 = 3 * (dT * dT) / 8589934592
    OFF2 = 3 * ((TEMP - 2000) * (TEMP - 2000)) / 8
    SENS2 = 7 * ((TEMP - 2000) * (TEMP - 2000)) / 8
    if TEMP < -1500 :
        SENS2 = SENS2 + 3 * ((TEMP + 1500) * (TEMP +1500))

TEMP = TEMP - T2
OFF = OFF - OFF2
SENS = SENS - SENS2
pressure = ((((D1 * SENS) / 2097152) - OFF) / 32768.0) / 100.0
cTemp = TEMP / 100.0
fTemp = cTemp * 1.8 + 32

# Output data to screen
print( "Pressure : %.2f mbar" %pressure)
print( "Temperature in Celsius : %.2f C" %cTemp)
print( "Temperature in Fahrenheit : %.2f F" %fTemp)