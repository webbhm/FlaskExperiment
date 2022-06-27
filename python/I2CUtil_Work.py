"""
 Wrapper of commonly used I2C message functions from periphery

 Author : Howard Webb
 Date   : 06/20/2018
 
"""

from periphery import I2C as pI2C
from LogUtil import get_logger

class I2C(object):

   def __init__(self, addr):
      self._path = "/dev/i2c-1"
      self._addr = addr
      self._i2c = pI2C(self._path)
      self._logger = get_logger('I2C')

   def __exit__(self, exc_type, exc_value, traceback):
      self._i2c.close()

   def get_msg(self, cmds, size):
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
       msgs = [self._i2c.Message(cmds), self._i2c.Message(bytearray([0x00 for x in range(size)]), read=True)]
       try:
           self._i2c.transfer(self._addr, msgs)
           ret = msgs[1].data
   #        for data in ret:
   #            print "Data:", hex(data)
           return msgs
       except Exception as e:
           print e
           return None


   def msg_write(self, cmds):
       """Write to sensor
           Args:
               cmds: commands to send
           Returns:
               msb: data from sent message
           Raises:
               None
      """
   #    print "Msg Write"
   #    for cmd in cmds:
   #        print hex(cmd)
       msgs = [self._i2c.Message(cmds)]
       try:
           self._i2c.transfer(self._addr, msgs)
   #        msb = msgs[0].data[0]
   #        print "MSB", hex(msb)
           return msgs

       except Exception as e:
           print e
           return None

   def msg_read(self, size):
       """Read existing data
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
       msgs = [self._i2c.Message(bytearray([0x00 for x in range(size)]), read=True)]
       try:
           self._i2c.transfer(self._addr, msgs)
           msb = msgs[0].data[0]
           lsb = msgs[0].data[1]
           checksum = msgs[0].data[2]
   #        print "MSB", msb, "LSB:", lsb, "Checksum:", checksum
           return msgs 

       except Exception as e:
           print e
           return None
'''
    def writeRaw8(self, value):
        """Write an 8-bit value on the bus (without register)."""
        value = value & 0xFF
        pass
'''
    def write8(self, register, value):
        """Write an 8-bit value to the specified register."""
        value = value & 0xFF
        self._i2c.msg_write([register], [value])
        self._logger.debug("Wrote 0x%02X to register 0x%02X",
                     value, register)
'''
    def write16(self, register, value):
        """Write a 16-bit value to the specified register."""
        value = value & 0xFFFF
        self._i2c.msg_write([register], value)
        self._logger.debug("Wrote 0x%04X to register pair 0x%02X, 0x%02X",
                     value, register, register+1)

    def writeList(self, register, data):
        """Write bytes to the specified register."""
        self._bus.write_i2c_block_data(self._address, register, data)
        self._logger.debug("Wrote to register 0x%02X: %s",
                     register, data)
'''
    def readList(self, register, length):
        """Read a length number of bytes from the specified register.  Results
        will be returned as a bytearray."""
        results = self._i2c.msg_read([register], length)
        self._logger.debug("Read the following from register 0x%02X: %s",
                     register, results)
        return results

    def readRaw8(self):
        """Read an 8-bit value on the bus (without register)."""
        msgs = self._i2c.msg_read(1)[0].[0] & 0xFF
#        result = self._bus.read_byte(self._address) & 0xFF
        self._logger.debug("Read 0x%02X",
                    result)
        return result

    def readU8(self, register):
        """Read an unsigned byte from the specified register."""
        result = self._bus.read_byte_data(self._address, register) & 0xFF
        self._logger.debug("Read 0x%02X from register 0x%02X",
                     result, register)
        return result

    def readS8(self, register):
        """Read a signed byte from the specified register."""
        result = self.readU8(register)
        if result > 127:
            result -= 256
        return result

    def readU16(self, register, little_endian=True):
        """Read an unsigned 16-bit value from the specified register, with the
        specified endianness (default little endian, or least significant byte
        first)."""
        result = self._bus.read_word_data(self._address,register) & 0xFFFF
        self._logger.debug("Read 0x%04X from register pair 0x%02X, 0x%02X",
                           result, register, register+1)
        # Swap bytes if using big endian because read_word_data assumes little
        # endian on ARM (little endian) systems.
        if not little_endian:
            result = ((result << 8) & 0xFF00) + (result >> 8)
        return result

    def readS16(self, register, little_endian=True):
        """Read a signed 16-bit value from the specified register, with the
        specified endianness (default little endian, or least significant byte
        first)."""
        result = self.readU16(register, little_endian)
        if result > 32767:
            result -= 65536
        return result

    def readU16LE(self, register):
        """Read an unsigned 16-bit value from the specified register, in little
        endian byte order."""
        return self.readU16(register, little_endian=True)

    def readU16BE(self, register):
        """Read an unsigned 16-bit value from the specified register, in big
        endian byte order."""
        return self.readU16(register, little_endian=False)

    def readS16LE(self, register):
        """Read a signed 16-bit value from the specified register, in little
        endian byte order."""
        return self.readS16(register, little_endian=True)

    def readS16BE(self, register):
        """Read a signed 16-bit value from the specified register, in big
        endian byte order."""
        return self.readS16(register, little_endian=False)         

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


