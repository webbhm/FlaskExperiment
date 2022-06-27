'''
Author: Howard Webb
Date: 12/20/2020
'''

import RPi.GPIO as GPIO
from time import sleep
from numpy import interp

# Assignments of Raspberry Pi pins to color chanels
# There is no significance to which pins were chosen
pin_R = 32 # Red
pin_B = 24 # Blue
pin_G = 26 # Green
pin_W = 22  # White
state = False

# Values are dimming.  0 = Full power, 100 = off, going from max power up to 100
OFF = 100


'''
Code used when trying to guess knob settings to amp readings
None of this is actually valid - knob goes 0-255, not 0-100 as assumed
# Values of amplifier and LED board
A_OUT = 6      # Amps per channel of amplifier
R_MAX_A = 2.4  # max amps for red   2400mA
G_MAX_A = 0.6  # max amps for green  600mA
B_MAX_A = 1.2  # max amps for blue  1200mA
W_MAX_A = 1.8  # max amps for white 1800mA

R_MAX = 100 - int((R_MAX_A/A_OUT)*100)  # max pwm range
G_MAX = 100 - int((G_MAX_A/A_OUT)*100)
B_MAX = 100 - int((B_MAX_A/A_OUT)*100)
W_MAX = 100 - int((W_MAX_A/A_OUT)*100)

print("Max PWM", R_MAX, G_MAX, B_MAX, W_MAX)
'''
# Maximum (minimum PWM) setting for LED safety
# Do not change at risk of burning out LEDs
R_MAX = 0
G_MAX = 50
B_MAX = 5
W_MAX = 0

# PWM frequency - 100 cycles/second
FREQUENCY = 100

# Range of the visible spectrum - used for one of the tests
SPEC_LOW = 380
SPEC_HIGH = 750


class GrowLight(object):
    ''' Representation of the grow light panel
    '''

    def __init__(self, logger=None):
        # standard setup of the GPIO pins
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)

        # Set up the pins for each chanel
        # Set pins for output
        GPIO.setup(pin_R, GPIO.OUT)
        GPIO.setup(pin_G, GPIO.OUT)
        GPIO.setup(pin_B, GPIO.OUT)
        GPIO.setup(pin_W, GPIO.OUT)
        # Pull the pins low
        GPIO.output(pin_R, GPIO.LOW)
        GPIO.output(pin_G, GPIO.LOW)
        GPIO.output(pin_B, GPIO.LOW)
        GPIO.output(pin_W, GPIO.LOW)
        # Set for PWM and ferquency for each chanel
        self.pwm_R = GPIO.PWM(pin_R, FREQUENCY)
        self.pwm_G = GPIO.PWM(pin_G, FREQUENCY)
        self.pwm_B = GPIO.PWM(pin_B, FREQUENCY)
        self.pwm_W = GPIO.PWM(pin_W, FREQUENCY)

        self.pwm_R.start(0)
        self.pwm_G.start(0)
        self.pwm_B.start(0)
        self.pwm_W.start(0)
        # Turn all lights off
        #print("off")
        self.set_lights(OFF, OFF, OFF, OFF)
    
            
    def set_lights(self, r, g, b, w=OFF):
        # change the duty cycle of the RGBW light
        #print("Set", r, g, b, w)
        # don't accept setting with numeric value lower than MAX
        if r < R_MAX:
            r = R_MAX
        if g < G_MAX:
            g = G_MAX
        if b < B_MAX:
            b = B_MAX
        if w < W_MAX:
            w = W_MAX
        self.pwm_R.ChangeDutyCycle(r)
        self.pwm_G.ChangeDutyCycle(g)
        self.pwm_B.ChangeDutyCycle(b)
        self.pwm_W.ChangeDutyCycle(w)    

        
    def end(self):
        # turn off all the leds
        self.set_lights(OFF, OFF, OFF, OFF)
        self.pwm_R.stop()
        self.pwm_G.stop()
        self.pwm_B.stop()
        self.pwm_W.stop()
        GPIO.cleanup()
        
    def turn_on(self):
        self.set_lights(50, OFF, 50)
    
    def turn_off():    
        self.end()        
    
def map(value, R1_Low, R1_High, R2_Low, R2_High):
    # map one range of numbers to another range
    # Used for RGB to PWM conversion (0-255, 100-0)
    # Used for Specturm to RGB (0-1, 0-255)
    y = (value-R1_Low)/(R1_High-R1_Low)*(R2_High-R2_Low) + R2_Low
    return y

def spectrum():
    # display the full spectrum
    print("Spectrum")
    gl = GrowLight()
    for x in range(SPEC_LOW, SPEC_HIGH):
        # get spectrum as 0-1 values
        r, g, b = spectrumToRGB(x)
        # map 0-1 to pwm value
        r1 = round(map(r, 0, 1, OFF, R_MAX), 1)
        g1 = round(map(g, 0, 1, OFF, G_MAX), 1)
        b1 = round(map(b, 0, 1, OFF, B_MAX), 1)
        print(r1, g1, b1)
        # set the led
        gl.set_lights(r1, g1, b1)
        sleep(.1)
    gl.end()
     
def spectrumToRGB(w):
    # for a spectrum value, return the RGB as 0-1 value
    # taken from noah.org/wiki/Wavelength_to_RGB_in_Python
    # Other formulas are available with better calculations, but this was good for playing
    if w >= 380 and w < 440:
        R = -(w - 440.) / (440. - 380.)
        G = 0.0
        B = 1.0
    elif w >= 440 and w < 490:
        R = 0.0
        G = (w - 440.) / (490. - 440.)
        B = 1.0
    elif w >= 490 and w < 510:
        R = 0.0
        G = 1.0
        B = -(w - 510.) / (510. - 490.)
    elif w >= 510 and w < 580:
        R = (w - 510.) / (580. - 510.)
        G = 1.0
        B = 0.0
    elif w >= 580 and w < 645:
        R = 1.0
        G = -(w - 645.) / (645. - 580.)
        B = 0.0
    elif w >= 645 and w <= 780:
        R = 1.0
        G = 0.0
        B = 0.0
    else:
        R = 0.0
        G = 0.0
        B = 0.0
    return R, G, B

def kelvin():
    # Color range of kelvin scale
    import KelvinRGB as k
    gl = GrowLight()
    step_size = 100
    for i in range(0, 15000, step_size):
        r, g, b = k.convert_K_to_RGB(i)
        r1 = round(map(r, 0, 256, OFF, R_MAX), 1)
        g1 = round(map(g, 0, 256, OFF, G_MAX), 1)
        b1 = round(map(b, 0, 256, OFF, B_MAX), 1)
        print(i, r1, g1, b1)
        sleep(0.5)
        gl.set_lights(r1, g1, b1)
    gl.end()
            
def sun(SUNRISE=True):
    import Sunset as s
    print("Sunrise")
    gl = GrowLight()
    step_size = 1
    steps = 20
    # astronomical twilight
    print("Astronomical Twilight 1")
    for step in range(0, steps, step_size):
        r, g, b = s.astronomical_twilight1(step, steps)
        r = round(map(r, 0, 256, OFF, R_MAX), 1)
        g = round(map(g, 0, 256, OFF, G_MAX), 1)
        b = round(map(b, 0, 256, OFF, B_MAX), 1)
        gl.set_lights(r, g, b)
        sleep(0.25)
        
    print("Astronomical Twilight 2")
    for step in range(0, steps, step_size):
        r, g, b = s.astronomical_twilight2(step, steps)
        r = round(map(r, 0, 256, OFF, R_MAX), 1)
        g = round(map(g, 0, 256, OFF, G_MAX), 1)
        b = round(map(b, 0, 256, OFF, B_MAX), 1)
        gl.set_lights(r, g, b)
        sleep(0.25)

    # nautical twilight
    print("Nautical Twilight")
    for step in range(0, steps, step_size):
        r, g, b = s.nautical_twilight(step, steps)
        r = round(map(r, 0, 256, OFF, R_MAX), 1)
        g = round(map(g, 0, 256, OFF, G_MAX), 1)
        b = round(map(b, 0, 256, OFF, B_MAX), 1)
        gl.set_lights(r, g, b)
        sleep(0.25)
        
    print("Civil Twilight 1")
    for step in range(0, steps, step_size):
        r, g, b = s.civil_twilight1(step, steps)
        r = round(map(r, 0, 256, OFF, R_MAX), 1)
        g = round(map(g, 0, 256, OFF, G_MAX), 1)
        b = round(map(b, 0, 256, OFF, B_MAX), 1)
        gl.set_lights(r, g, b)
        sleep(0.25)

    print("Civil Twilight 2")
    for step in range(0, steps, step_size):
        r, g, b = s.civil_twilight2(step, steps)
        r = round(map(r, 0, 256, OFF, R_MAX), 1)
        g = round(map(g, 0, 256, OFF, G_MAX), 1)
        b = round(map(b, 0, 256, OFF, B_MAX), 1)
        gl.set_lights(r, g, b)
        sleep(0.25)
    gl.end()
        
def test():
    # cycle the leds
    print("Cycle LED")
    gl = GrowLight()
    
    # cycle Red
    for r in range(R_MAX, OFF):
        gl.set_lights(r, OFF, OFF)
        print("Cycle R", r)
        sleep(0.1)
    gl.set_lights(OFF, OFF, OFF)
    
    # cycle Green
    for g in range(G_MAX, OFF):
        gl.set_lights(OFF, g, OFF)
        print("Cycle G", g)
        sleep(0.1)
    gl.set_lights(OFF, OFF, OFF)

    #Cycle Blue
    for b in range(B_MAX, OFF):
        gl.set_lights(OFF, OFF, b)                
        print("Cycle B", b)
        sleep(0.1)
    gl.set_lights(OFF, OFF, OFF)

    # cycle white
    for w in range(W_MAX, OFF):
        gl.set_lights(OFF, OFF, OFF, w)
        print("Cycle W", w)
        sleep(0.1)
    gl.set_lights(OFF, OFF, OFF, OFF)                
    gl.end()

def test2():
    # Test how low the lights will dim
    print("Test Dimming")
    gl = GrowLight()

    # Try max dimming
    gl.set_lights(99.9, 99.9, 99.9, OFF)
    sleep(5)
    
    # cycle from bright to dim
    for w in range(OFF, W_MAX, -1):
        gl.set_lights(99.9, 99.9, 99.9, w)
        print("Cycle W", w)
        sleep(0.1)
    gl.end()
    
def test3():
    # Test settings used for the on test
    print("Test 3", "OFF, OFF, 50")
    gl = GrowLight()
    gl.set_lights(OFF, OFF, 50)
    sleep(20)
    gl.end()
    
def gbe():
    # There are bad assumption here, and this is not valid
    # Convert GBE values for knob controller to amplifier pwm values    
    MAX_RANGE = 1000
    KNOB_A = 5
    
    GBE_R_HI = 172
    GBE_G_HI = 105
    GBE_B_HI = 130
    
    GBE_R_MAX = 172
    GBE_G_MAX = 170
    GBE_B_MAX = 190
    
    # Convert GBE values for knob controller to amplifier pwm values
    # (value / range) * (knob amps / amp) * percent to int
    r = 100 - int((GBE_R_HI/1000)*(KNOB_A/A_OUT)*100)
    g = 100 - int((GBE_G_HI/1000)*(KNOB_A/A_OUT)*100)
    b = 100 - int((GBE_B_HI/1000)*(KNOB_A/A_OUT)*100)
    w = OFF
    print("Growing Beyond Earth")
    print(r, g, b)
    gl = GrowLight()
    gl.set_lights(r, g, b)
    sleep(20)
    print("Done")
    gl.end()

def turn_on():
    gl = GrowLight()
    gl.set_lights(OFF, OFF, 50)
    sleep(20)
    
def turn_off():    
    gl = GrowLight()
    gl.set_lights(OFF, OFF, OFF)
    gl.end()

            
def switch_test():
    gl = GrowLight()
    gl.turn_on()
    print("On")
    sleep(10)
    gl.turn_off()
    print("Off")
    


if __name__ == "__main__":
    #test()
    #test2()
    #spectrum()
    #kelvin()
    #sun()
    #switch_test()
    turn_on()
    #test3()
