'''
Remote control of several LED lights
'''

import RPi.GPIO as GPIO
from time import sleep

pins = {
   16 : {'name' : 'GPIO 26 - Red', 'state' : GPIO.LOW},
   23 : {'name' : 'GPIO 23 - Blue', 'state' : GPIO.LOW},
   24 : {'name' : 'GPIO 24 - Green', 'state' : GPIO.LOW},
   25 : {'name' : 'GPIO 25 - IR', 'state' : GPIO.LOW}   
   }

class LED(object):

    def __init__(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        # Set each pin as an output and make it low:
        for pin in pins:
           GPIO.setup(pin, GPIO.OUT)
           GPIO.output(pin, GPIO.LOW)
           
    def change(self, changePin, action):
       # Convert the pin from the URL into an integer:
       changePin = int(changePin)
       # Get the device name for the pin being changed:
       deviceName = pins[changePin]['name']
       # If the action part of the URL is "on," execute the code indented below:
       if action == "on":
          # Set the pin high:
          GPIO.output(changePin, GPIO.HIGH)
          # Save the status message to be passed into the template:
          message = "Turned " + deviceName + " on."
       if action == "off":
          GPIO.output(changePin, GPIO.LOW)
          message = "Turned " + deviceName + " off."

       # For each pin, read the pin state and store it in the pins dictionary:
       for pin in pins:
          pins[pin]['state'] = GPIO.input(pin)

       # Along with the pin dictionary, put the message into the template data dictionary:
       templateData = {
          'pins' : pins,
          'messages': {'message':message}
       }
       
       return templateData
    
    def setState(self):
        # For each pin, read the pin state and store it in the pins dictionary:
      for pin in pins:
          pins[pin]['state'] = GPIO.input(pin)
        # Put the pin dictionary into the template data dictionary:
      templateData = {
      'pins' : pins
      }
        
      return templateData        

def test():
    led = LED()
    led.change('23', 'on')
    led.change('24', 'on')
    sleep(3)
    led.change('23', 'off')
    led.change('24', 'off')
    

if __name__=="__main__":
    test()