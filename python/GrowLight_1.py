'''
Exercise of the Hort-Light pannel
'''

import RPi.GPIO as GPIO
from time import sleep
from numpy import interp
import cv2

pin_R = 22
pin_B = 24
pin_G = 26
pin_W = 32 
state = False
# Values are dimming.  0 = Full power, 100 = off, going from max power up to 100

# Values of amplifier and LED board
A_OUT = 6      # Amps per channel of amplifier
R_MAX_A = 2.4  # max amps for red   2400mA
G_MAX_A = 0.6  # max amps for green  600mA
B_MAX_A = 1.2  # max amps for blue  1200mA
W_MAX_A = 1.8  # max amps for white 1800mA

R_MAX = 10 #88
G_MAX = 70
B_MAX = 35 #90
W_MAX = 20 #70

print("Max PWM", R_MAX, G_MAX, B_MAX, W_MAX)
OFF = 100

FREQUENCY = 100

SPEC_LOW = 380
SPEC_HIGH = 750


class GrowLight(object):

   def __init__(self, logger=None):

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)


        GPIO.setup(pin_R, GPIO.OUT)
        GPIO.setup(pin_G, GPIO.OUT)
        GPIO.setup(pin_B, GPIO.OUT)
        GPIO.setup(pin_W, GPIO.OUT)

        GPIO.output(pin_R, GPIO.LOW)
        GPIO.output(pin_G, GPIO.LOW)
        GPIO.output(pin_B, GPIO.LOW)
        GPIO.output(pin_W, GPIO.LOW)

        self.pwm_R = GPIO.PWM(pin_R, FREQUENCY)
        self.pwm_G = GPIO.PWM(pin_G, FREQUENCY)
        self.pwm_B = GPIO.PWM(pin_B, FREQUENCY)
        self.pwm_W = GPIO.PWM(pin_W, FREQUENCY)

        self.pwm_R.start(0)
        self.pwm_G.start(0)
        self.pwm_B.start(0)
        self.pwm_W.start(0)
        #print("off")
        self.set_lights(OFF, OFF, OFF, OFF)
    
   def set_lights(self, r, g, b, w=OFF):
        # change the duty cycle of the RGBW light
        #print("Set", r, g, b, w)
        # don't accept setting with numeric value lower than MAX
        
        self.pwm_R.ChangeDutyCycle(r)
        self.pwm_G.ChangeDutyCycle(g)
        self.pwm_B.ChangeDutyCycle(b)
        self.pwm_W.ChangeDutyCycle(w)
        
   def map_pannel(self, r, g, b, w=OFF):
        '''
        map rgb values to pannel range
        '''
        r1 = round(map(r, 0, 100, OFF, R_MAX), 1)
        g1 = round(map(g, 0, 100, OFF, G_MAX), 1)
        b1 = round(map(b, 0, 100, OFF, B_MAX), 1)
        w1 = round(map(w, 0, 100, OFF, W_MAX), 1)

        if r < R_MAX:
            r = R_MAX
        if g < G_MAX:
            g = G_MAX
        if b < B_MAX:
            b = B_MAX
        if w < W_MAX:
            w = W_MAX

        #print(r1, g1, b1, w1)
        
        return r1, g1, b1, w1
    
   def spectrum(self):
        # display the full spectrum
        for x in range(SPEC_LOW, SPEC_HIGH):
            # get spectrum as 0-1 values
            r, g, b = self.spectrumToRGB(x)
            #print("Spectrum", r, g, b)
            # map 0-100 to pwm value
            r1, g1, b1, w = self.map_pannel(r*100, g*100, b*100)
            # set the led            
            #print("Lights", r1, g1, b1)
            self.set_lights(r1, g1, b1)
            sleep(.1)
        self.set_lights(OFF, OFF, OFF)
        
   def spectrumToRGB(self, w):
        # for a spectrum value, return the RGB as 0-1 value
        if w >= 380 and w < 440:
            R = round(-(w - 440.) / (440. - 380.), 3)
            G = 0.0
            B = 1.0
        elif w >= 440 and w < 490:
            R = 0.0
            G = round((w - 440.) / (490. - 440.), 3)
            B = 1.0
        elif w >= 490 and w < 510:
            R = 0.0
            G = 1.0
            B = round(-(w - 510.) / (510. - 490.), 3)
        elif w >= 510 and w < 580:
            R = round((w - 510.) / (580. - 510.), 3)
            G = 1.0
            B = 0.0
        elif w >= 580 and w < 645:
            R = 1.0
            G = round(-(w - 645.) / (645. - 580.), 3)
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
        
   def end(self):
        # turn off all the leds
        self.set_lights(OFF, OFF, OFF, OFF)
        self.pwm_R.stop()
        self.pwm_G.stop()
        self.pwm_B.stop()
        self.pwm_W.stop()
        GPIO.cleanup()
        
   def kelvin(self):
        import KelvinRGB as k
        step_size = 100
        for i in range(0, 15000, step_size):
            r, g, b = k.convert_K_to_RGB(i)
            r, g, b, w = self.map_pannel(r, g, b)
            print(i, r, g, b)
            sleep(0.5)
            self.set_lights(r, g, b)
            
   def sun2(self, SUNRISE=True):
        import Sunset as s
        step_size = 1
        steps = 20
        # astronomical twilight
        print("Astronomical Twilight 1")
        for step in range(0, steps, step_size):
            r, g, b = s.astronomical_twilight1(step, steps)
            r, g, b, w = self.map_pannel(r, g, b)
            self.set_lights(r, g, b)
            sleep(0.25)

        print("Astronomical Twilight 2")
        for step in range(0, steps, step_size):
            r, g, b = s.astronomical_twilight2(step, steps)
            r, g, b, w = self.map_pannel(r, g, b)
            self.set_lights(r, g, b)
            sleep(0.25)

        # nautical twilight
        print("Nautical Twilight")
        for step in range(0, steps, step_size):
            r, g, b = s.nautical_twilight(step, steps)
            r, g, b, w = self.map_pannel(r, g, b)
            self.set_lights(r, g, b)
            sleep(0.25)

        print("Civil Twilight 1")
        for step in range(0, steps, step_size):
            r, g, b = s.civil_twilight1(step, steps)
            r, g, b, w = self.map_pannel(r, g, b)
            self.set_lights(r, g, b)
            sleep(0.25)

        print("Civil Twilight 2")
        for step in range(0, steps, step_size):
            r, g, b = s.civil_twilight2(step, steps)
            r, g, b, w = self.map_pannel(r, g, b)
            self.set_lights(r, g, b)
            sleep(0.25)

def map(value, R1_Low, R1_High, R2_Low, R2_High):
    # map one range of numbers to another range
    y = (value-R1_Low)/(R1_High-R1_Low)*(R2_High-R2_Low) + R2_Low
    #print(value, y, R1_Low, R1_High, R2_Low, R2_High)
    return y

def test():
    print("\nCycle LEDs")
    # cycle the leds
    gl = GrowLight()
    try:

        while True:
            print("Red")
            for r in range(0, OFF):
                r, g, b, w = gl.map_pannel(r, OFF, OFF)
                gl.set_lights(r, OFF, OFF)
                print("Cycle R", r)
                sleep(0.1)
            gl.set_lights(OFF, OFF, OFF)
            print("Green")
            for g in range(0, OFF):
                r, g, b, w = gl.map_pannel(OFF, g, OFF)
                gl.set_lights(OFF, g, OFF)
                print("Cycle G", g)
                sleep(0.1)
            gl.set_lights(OFF, OFF, OFF)
            print("Blue")
            for b in range(0, OFF):
                r, g, b, w = gl.map_pannel(OFF, OFF, b)
                gl.set_lights(OFF, OFF, b)                
                print("Cycle B", b)
                sleep(0.1)
            gl.set_lights(OFF, OFF, OFF)
            print("White")
            for w in range(0, OFF):
                r, g, b, w = gl.map_pannel(OFF, OFF, OFF, w)
                gl.set_lights(OFF, OFF, OFF, w)
                print("Cycle W", w)
                sleep(0.1)
            gl.set_lights(OFF, OFF, OFF, OFF)                
    except KeyboardInterrupt:
        pass
    
    gl.end()

def test2():
    print("\nMax Dimming")
    # max dimming
    gl = GrowLight()
    gl.set_lights(99, 99, 99, OFF)
    sleep(10)
    gl.set_lights(99, 99, 99, 99)
    '''
    for w in range(OFF, W_MAX, -1):
        r, g, b, w = gl.map_pannel(OFF, OFF, OFF, w)
        print("Cycle W", w)
        gl.set_lights(99, 99, 99, w)
        sleep(0.1)
    '''
    gl.set_lights(OFF, OFF, OFF, OFF)                
    
    gl.end()
    
def gbe():
    print("\nGBE Settings")
    # Convert GBE values for knob controller to amplifier pwm values    
    MAX_RANGE = 1000
    KNOB_A = 5
    
    
    GBE_R_HI = 172
    GBE_G_HI = 105
    GBE_B_HI = 130
    
    GBE_R_MAX = 172
    GBE_G_MAX = 170
    GBE_B_MAX = 190
    
    FACTOR = 1000
    
    # Convert GBE values for knob controller to amplifier pwm values
    # (value / range) * (knob amps / amp) * percent to int
    r = 100 - int((GBE_R_HI/FACTOR)*(KNOB_A/A_OUT)*100)
    g = 100 - int((GBE_G_HI/FACTOR)*(KNOB_A/A_OUT)*100)
    b = 100 - int((GBE_B_HI/FACTOR)*(KNOB_A/A_OUT)*100)
    w = OFF
    print("Growing Beyond Earth")
    print(r, g, b)
    gl = GrowLight()
    gl.set_lights(r, g, b)
    sleep(20)
    print("Done")
    gl.end()

def amp_read(color):
    gl = GrowLight()
    x = 100
    r = 100
    g = 100
    b = 100
    w = 100
    # open a frame to catch keys
    frame = cv2.imread("/home/pi/Pictures/2020-07-20_1439.jpg")
    cv2.imshow("Frame", frame)
    
    while True:
        key = cv2.waitKey(1)
        if key != -1:
            print("Key", key)
        if key == ord("u"):  # up key
            x += 5
            if x > 100:
                x = 100
            print(color, x)
                
        if key == ord("d"):
            x -= 5
            if x < 0:
                x = 0
            print(color, x)
                
        if key == ord("q"):
            gl.set_lights(OFF, OFF, OFF)
            break
        
        if color == 'R':
            r = x
        elif color == 'G':
            g = x
        elif color == 'B':
            b = x
        elif color == 'W':
            w = x
        gl.set_lights(r, g, b, w)
        
def amp2():
    gl = GrowLight()
    r = 0
    g = OFF
    b = OFF
    w = OFF
    gl.set_lights(r, g, b, w)
    sleep(6)
    r = 0
    g = 55
    b = 0
    w = 0
    gl.set_lights(r, g, b, w)
    sleep(6)
    gl.set_lights(OFF, OFF, OFF, OFF)
        

def test3():
    print("\nRainbow")
    # Run rainbow spectrum from Violet to Red
    gl = GrowLight()
    gl.spectrum()
    gl.end()
    
def test4(W=False):
    # Amp testing to find minimum value (max A)
    print("\nAmp Test")
    #r = 86
    #g = 92
    #b = 90
    r = 70
    g = 97
    b = 90
    w = 70    
    if W == False:
        w = 100

    
    print(r, g, b, w)
    gl = GrowLight()
    gl.set_lights(r, g, b, w)
    sleep(30)
    print("Done")
    gl.end()

def test5():
    # Amp testing to find minimum value (max A)
    print("\nKelvin")
    gl = GrowLight()
    gl.kelvin()
    print("Done")
    gl.end()

def test6():
    # Sunset
    print("\nSunset")
    gl = GrowLight()
    gl.sun2()
    print("Done")
    gl.end()
    
def test7():
    print("\nCycle Colors")
    r = 70
    g = 97
    b = 90
    w = 70

    pl = GrowLight()
    for x in range(0, 15):
        print("Red")
        pl.set_lights(r, OFF, OFF, OFF)
        sleep(0.5)
        print("Green")
        pl.set_lights(OFF, g, OFF, OFF)
        sleep(0.5)
        print("Blue")
        pl.set_lights(OFF, OFF, b, OFF)
        sleep(0.5)
        print("White")
        pl.set_lights(OFF, OFF, OFF, w)
        sleep(0.5)
        print("Full")
        pl.set_lights(r, g, b, OFF)
        sleep(1)
    pl.end()
    
def white():
    # White
    print("\nWhite")
    gl = GrowLight()
    gl.set_lights(OFF, OFF, OFF, W_MAX)
    sleep(30)
    print("Done")
    gl.end()
        

if __name__ == "__main__":
    #test()  # cycle all lights
    test2() # max dimming
    #test3() # spectrum
    #test4(True)  # MAX
    #test4()  # MAX    
    #test5() # kelvin
    #test6() # sunset
    #gbe()    
    #white()
    #test4(True)
    #test7()
    #amp_read("R")
    #amp2()
