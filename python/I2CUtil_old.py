"""
 Wrapper of commonly used I2C message functions from periphery

 Author : Howard Webb
 Date   : 06/20/2018
 
"""

from periphery import I2C

def bytesToWord(high, low):
   """Convert two byte buffers into a single word value
       shift the first byte into the work high position
       then add the low byte
        Args:
            high: byte to move to high position of word
            low: byte to place in low position of word
        Returns:
            word: the final value
        Raises:
            None
   """   
   word = (high << 8) + low
   return word


def get_msg(path, addr, cmds, size):
    """Send and receive multiple messages
        Should return the welcome message

        Args:
            path: location of device file
            addr: address of the I2C Device
            cmds: array of commands to send
            size: size of byte array to return data in
        Returns:
            msgs: array of messages
        Raises:
            None
    """
#    print "Get Msg1"
#    for cmd in cmds:
#        print "Cmd: ", hex(cmd)
#    print "Buffer:", size        
    i2c = I2C(path)
    msgs = [I2C.Message(cmds), I2C.Message(bytearray([0x00 for x in range(size)]), read=True)]
    try:
        i2c.transfer(addr, msgs)
        ret = msgs[1].data
#        for data in ret:
#            print "Data:", hex(data)
        i2c.close()
        return msgs

    except Exception as e:
        print e
        return None

def msg_write(path, addr, cmds):
    """Send a message
        Args:
            path: location of device file
            addr: address of the I2C Device
            cmds: commands to send
        Returns:
            msb: data from sent message
        Raises:
            None
   """
#    print "Msg Write"
#    for cmd in cmds:
#        print hex(cmd)
    i2c = I2C(path)
    msgs = [I2C.Message(cmds)]
    try:
        i2c.transfer(addr, msgs)
#        msb = msgs[0].data[0]
#        print "MSB", hex(msb)
        i2c.close()
        return msgs

    except Exception as e:
        print e
        return None    
 
def msg_read(path, addr, size):
    """Read memory
        Args:
            path: location of device file
            addr: address of the I2C Device
            size: size of byte array for receiving data
        Returns:
            msgs: should be only one message returned
        Raises:
            None
   """
        
#    print "Msg Read", size
    i2c = I2C(path)
    msgs = [I2C.Message(bytearray([0x00 for x in range(size)]), read=True)]
    try:
        i2c.transfer(addr, msgs)
        msb = msgs[0].data[0]
        lsb = msgs[0].data[1]
        checksum = msgs[0].data[2]
#        print "MSB", msb, "LSB:", lsb, "Checksum:", checksum
        i2c.close()
        return msgs 

    except Exception as e:
        print e
        return None    

