"""
SI7021 humidity and temperature sensor
Technical notes of commands and operation and from:
https://www.silabs.com/documents/public/data-sheets/Si7021-A20.pdf

 Author : Howard Webb
 Date   : 06/20/2018
 
"""


import time
from I2CUtil import *

# Device path
path = "/dev/i2c-1"
# Device I2C address
addr = 0x40
rh_no_hold = 0xF5      # Use and do own time hold
previous_temp = 0xE0   # Works but should not use

rh_hold = 0xE5         # Not used
temp_hold = 0XE3       # Not used
temp_no_hold = 0xF3    # Use but do own hold
temp_from_rh = 0xE0    # Not used
reset_cmd = 0xFE       # Available
write_reg_1 = 0xE6     # Not used
read_reg_1 = 0xE7      # Not used
# Heater control
write_heater_reg = 0x51 # Not doing callibration and fancy stuff at this time
read_heater_reg = 0x11  # ditto
# Unique ID for this chip
read_id_1_1 = 0xFA     # Available option
read_id_1_2 = 0x0F     # Available option
read_id_2_1 = 0xFC     # Available option
read_id_2_2 = 0xC9     # Available option
# Firmware revision
firm_rev_1_1 = 0x84
firm_rev_1_2 = 0x88


 
def calc_humidity(read):
   """Calculate relative humidity from sensor reading
        Args:
            read: the sensor value
        Returns:
            rh: calculated relative humidity
        Raises:
            None
   """
   rh = ((125.0*read)/65536.0)-6.0
   return rh

def calc_temp(read):
   """Calculate relative humidity from sensor reading
        Args:
            read: the sensor value
        Returns:
            tempC: calculated temperature in Centigrade
        Raises:
            None
   """
   tempC = ((175.72*read)/65536.0)-46.85
   return tempC

def get_tempC_prior():
    """Get the temperature from the prior humidity reading
        Args:
            None
        Returns:
            tempC: calculated temperature in Centigrade
        Raises:
            None
    """

    print "\nGet Temp - get previous"
    msgs = get_msg(path, addr, [previous_temp], 3)
    if msgs == None:
        return None
    else:
        value = bytesToWord(msgs[1].data[0],msgs[1].data[1])
        tempC = calc_temp(value) 
        return tempC

def get_humidity():
    """Get the humidity
        Args:
            None
        Returns:
            rh: calculated relative humidity
        Raises:
             None
    """
    print "\nGet Humidity - no hold split"
    msgs = msg_write(path, addr, [rh_no_hold])
    # need a pause here between sending the request and getting the data
    time.sleep(0.03)
    msgs = msg_read(path, addr, 3)
    if msgs == None:
        return None
    else:
        value = bytesToWord(msgs[0].data[0], msgs[0].data[1])
        rh = calc_humidity(value)
        return rh

def get_tempC():
    """Get the temperature (new reading)
        Args:
            None
        Returns:
            tempC: calculated temperature in Centigrade
        Raises:
            None
    """
#    print "\nGet Temp - no hold split"
    msgs = msg_write(path, addr, [temp_no_hold])
    # need a pause here between sending the request and getting the data
    time.sleep(0.03)
    msgs = msg_read(path, addr, 3)
    if msgs == None:
        return None
    else:
        value = bytesToWord(msgs[0].data[0], msgs[0].data[1])
        return calc_temp(value)


def get_rev():
    """Get the firmware revision number
        Args:
            None
        Returns:
            rev: coded revision number
        Raises:
            None
    """
    print "\nGet Revision"
    msgs = get_msg(path, addr, [firm_rev_1_1, firm_rev_1_2], 3)
    rev = msgs[1].data[0]
    if rev == 0xFF:
        print "version 1.0"
    elif rev == 0x20:
        print "version 2.0"
    else:
        print "Unknown"
    return rev        

def get_id1():
    """Print the first part of the chips unique id
        Args:
            None
        Returns:
            None
        Raises:
             None
    """
    print "\nGet ID 1"
    msgs = get_msg(path, addr, [read_id_1_1, read_id_1_2], 4)
    ret= msgs[1].data
    for data in ret:
        print "ID", hex(data)

def get_id2():
    """Print the second part of the chips unique id
        The device version is in SNA_3
        Args:
            None
        Returns:
            None
        Raises:
            None
    """
        
    print "\nGet ID 2"
    msgs = get_msg(path, addr, [read_id_2_1, read_id_2_2], 4)
    ret= msgs[1].data
    for data in ret:
        print "ID", hex(data)
    sna3 = msgs[1].data[0]
    if sna3 == 0x00:
        print "Device: Engineering Sample"
    elif sna3 == 0xFF:
        print "Device: Engineering Sample"        
    elif sna3 == 0x14:
        print "Device: SI7020"
    elif sna3 == 0x15:
        print "Device: SI7021"
    else:
        print "Unknown"

def reset():
    """Reset the device
        Args:
            None
        Returns:
            None
        Raises:
            None
    """
         
    print "\nReset"
    rev_1 = msg_write(path, addr, [reset_cmd])
    print "Reset: ", rev_1
    
def test():
    """Test the SI7021 functions
        Args:
            None
        Returns:
            None
        Raises:
            None
   """
 
    print "\nTest Humidity - split"
    rh = get_humidity()        
    if rh != None:
        print('Humidity : %.2f %%' % rh)
    else:
        print "Error getting Humidity"

    print "\nTest Temp - split"
    temp = get_tempC()
    if temp == None:
        print "Error getting Temp"
    else:        
        print('Temp C: %.2f C' % temp)        


    print "\nTest Temp - previous"
    temp = get_tempC_prior()
    if temp == None:
        print "Error getting Temp"
    else:        
        print('Temp C: %.2f C' % temp)

    reset()
    get_rev()
    get_id1()
    get_id2()

if __name__ == "__main__":
    test()
