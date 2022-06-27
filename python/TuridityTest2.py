"""
Test of the Turbidity meter using an ADC
# The Turbidity sensor mapped from 0 to 1023 (0 - 5 volts)
# ADC maps values -32768 to 32767, GND is 0 (-5 - 5 v)
# Voltage conversion is volts = (reading / 32767) * 5
# This may need some calibration adjustment


"""
import time

# Import the ADS1x15 module.
import ADS1115
from math import exp

# Create an ADS1115 ADC (16-bit) instance.
adc = ADS1115.ADS1115()
file_name = '/home/pi/data/tb_2018-07012-CC2.txt'
f = open(file_name, 'w+')
hdr = 'Raw_Value\tNTU\n'
print( hdr)
f.write(hdr) 
# Choose a gain of 1 for reading voltages from 0 to 4.09V.
# Or pick a different gain to change the range of voltages that are read:
#  - 2/3 = +/-6.144V
#  -   1 = +/-4.096V
#  -   2 = +/-2.048V
#  -   4 = +/-1.024V
#  -   8 = +/-0.512V
#  -  16 = +/-0.256V
# See table 3 in the ADS1015/ADS1115 datasheet for more info on gain.
#GAIN = 1
GAIN = 1
# Main loop.
for x in range(0, 25):
    value = adc.read_adc(0, gain=GAIN)
    volts = (value/32767.0) * 4.4773                                                                                                                                                                                                                                                                    
#    print('Volts: {0}'.format(volts))
    # Turbidity
    # y = -1120.4xsq + 5742,3x - 4352.9
    A = (-1120.4 * (volts * volts))
    B = (5742.3 * volts)    
    C = 4352.9
    tb = A + B - C
#    print('NTU: {0:>2}'.format(tb))
    st = '{0}\t{1}\n'.format(value, tb)
    print( st)
    f.write(st)    
    time.sleep(0.5)

    
#    print('Channel 0: {0}'.format(value))


    # Sleep for half a second.
    time.sleep(0.5)
f.close()    
# Stop continuous conversion.  After this point you can't get data from get_last_result!
adc.stop_adc()
