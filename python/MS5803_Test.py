import ms5803py
import time

s = ms5803py.MS5803()

press, temp = s.read(pressure_osr=512)

print("Pressure: {:0.2f}, Temp: {:0.2f}".format(press, temp))

raw_temperature = s.read_raw_temperature(osr=4096)
for i in range(5):
    raw_pressure = s.read_raw_pressure(osr=256)
    press, temp = s.convert_raw_readings(raw_pressure, raw_temperature)
    print("Raw Pressure: {:0.2f}, Temp: {:0.2f}".format(press, temp))    
    