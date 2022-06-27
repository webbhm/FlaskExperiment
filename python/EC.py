'''
# Get elecrical conductivity (moisture probe) from ADC
# The analog moisture probe is hooked to pin1 of the analog to digital converter
# The ADC is running on the I2C bus
# Howard Webb
# 2019/08/16

 Out of water reads about 30000
 Just touching is about 28000 or lower
 The deeper it is submerged, the lower the value
 There is a good bit of drift when it is sitting
'''

import time
# Import the ADS1x15 module (analog to digital converter).
import Adafruit_ADS1x15

# Create an ADS1115 ADC (16-bit) instance.
adc = Adafruit_ADS1x15.ADS1115()

GAIN = 1

class EC(object):

   def __init__(self):
      self._pin = 1

   def getEC(self):
       return adc.read_adc(self._pin, gain=GAIN)

def test():
    ec = EC()
    for x in range(1, 100):
        print ec.getEC()
        time.sleep(0.5)
        
if __name__ == "__main__":
    test()
