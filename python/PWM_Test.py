'''
Various exercises of an RGB led
'''

import RPi.GPIO as GPIO
from time import sleep
from numpy import interp

pin_R = 33
pin_B = 35
pin_G = 37
#pin_W = 22 
state = False
# Values are dimming.  0 = Full power, 100 = off, going from max power up to 100

OFF = 0

FREQUENCY = 100


# Spectrum range
SPEC_LOW = 380
SPEC_HIGH = 750

class PWM(object):

   def __init__(self, logger=None):

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)


        GPIO.setup(pin_R, GPIO.OUT)
        GPIO.setup(pin_G, GPIO.OUT)
        GPIO.setup(pin_B, GPIO.OUT)

        GPIO.output(pin_R, GPIO.LOW)
        GPIO.output(pin_G, GPIO.LOW)
        GPIO.output(pin_B, GPIO.LOW)

        self.pwm_R = GPIO.PWM(pin_R, FREQUENCY)
        self.pwm_G = GPIO.PWM(pin_G, FREQUENCY)
        self.pwm_B = GPIO.PWM(pin_B, FREQUENCY)

        self.pwm_R.start(0)
        self.pwm_G.start(0)
        self.pwm_B.start(0)
        #print("off")
        self.set_lights(OFF, OFF, OFF, OFF)
    
   def spectrum(self):
        # display the full spectrum
        for x in range(SPEC_LOW, SPEC_HIGH):
            # get spectrum as 0-1 values
            r, g, b = self.spectrumToRGB(x)
            # map 0-1 to pwm value
            #r1 = map(r, 0, 1, 0, 100)
            #g1 = map(g, 0, 1, 0, 100)
            #b1 = map(b, 0, 1, 0, 100)
            r1 = round(r*100, 1)
            g1 = round(g*100, 1)
            b1 = round(b*100, 1)
            print(r1, g1, b1)
            # set the led
            self.set_lights(r1, g1, b1)
            sleep(.1)
        self.set_lights(OFF, OFF, OFF)
        
   def spectrumToRGB(self, w):
        # for a spectrum value, return the RGB as 0-1 value
        if w >= 380 and w < 440:
            R = -(w - 440.) / (440. - 380.)
            G = 0.0
            B = 1.0
            print("Violet", R, G, B)
        elif w >= 440 and w < 490:
            R = 0.0
            G = (w - 440.) / (490. - 440.)
            B = 1.0
            print("Blue", R, G, B)
        elif w >= 490 and w < 510:
            R = 0.0
            G = 1.0
            B = -(w - 510.) / (510. - 490.)
            print("Green", R, G, B)
        elif w >= 510 and w < 580:
            R = (w - 510.) / (580. - 510.)
            G = 1.0
            B = 0.0
            print("Orange", R, G, B)
        elif w >= 580 and w < 645:
            R = 1.0
            G = -(w - 645.) / (645. - 580.)
            B = 0.0
            print("Red", R, G, B)
        elif w >= 645 and w <= 780:
            R = 1.0
            G = 0.0
            B = 0.0
            print("IR", R, G, B)
        else:
            R = 0.0
            G = 0.0
            B = 0.0

        return R, G, B

   def sun(self, RISE=True):
        R1 = 110
        R2 = 190
        R3 = 250
        
        G1 = 108
        G2 = 140
        G3 = 215
        
        B1 = 135
        B2 = 175
        B3 = 160

        MAX = 50
        
        MIN = 1
        MAX = 50
        INC = 1
        
        if RISE:
            print("Sunrise")
            for x in range(MIN, MAX, INC):
                w = R1 + x*(R2 - R1)/MAX
                r = round(map(w, 0, 256, 0, 100), 1)
                w = G1 + x*(G2 - G1)/MAX
                g = round(map(w, 0, 256, 0, 100), 1)
                w = B1 + x*(B2 - B1)/MAX
                b = round(map(w, 0, 256, 0, 100), 1)
                
                print(x, r, g, b)
                self.set_lights(r, g, b)
                sleep(0.5)
            print("Rise")    
            for x in range(MIN, MAX, INC):
                w = R2 + x*(R3 - R2)/MAX
                #print("R", x, w, R2, R3)
                b = round(map(w, 0, 256, 0, 100), 1)
                
                w = G2 + x*(G3 - G2)/MAX
                g = round(map(w, 0, 256, 0, 100), 1)
                
                w = B2 + x*(B3 - B2)/MAX
                b = round(map(w, 0, 256, 0, 100), 1)
                print(x, r, g, b)
                self.set_lights(r, g, b)            
                sleep(0.5)
        else:
            print("Sunset")
            for x in range(MAX, MIN, INC*-1):
                w = R2 + x*(R3 - R2)/MAX
                r = round(map(w, 0, 256, 0, 100), 1)
                
                w = G2 + x*(G3 - G2)/MAX
                g = round(map(w, 0, 256, 0, 100), 1)
                
                w = B2 + x*(B3 - B2)/MAX
                b = round(map(w, 0, 256, 0, 100), 1)
                
                self.set_lights(r, g, b)            
                sleep(0.5)
            print("Ending")    
            for x in range(MAX, MIN, INC*-1):
                w = R1 + x*(R2 - R1)/MAX
                r = round(map(w, 0, 256, 0, 100), 1)
                w = G1 + x*(G2 - G1)/MAX
                g = round(map(w, 0, 256, 0, 100), 1)
                w = B1 + x*(B2 - B1)/MAX
                b = round(map(w, 0, 256, 0, 100), 1)
                
                #print(r, g, b)
                self.set_lights(r, g, b)
                sleep(0.5)
        
            print("Done")
            
   def set_lights(self, r, g, b, w=OFF):
        # change the duty cycle of the RGBW light
        #print("Set", r, g, b)
        # don't accept setting with numeric value lower than MAX
        
        self.pwm_R.ChangeDutyCycle(r)
        self.pwm_G.ChangeDutyCycle(g)
        self.pwm_B.ChangeDutyCycle(b)
        
   def end(self):
        # turn off all the leds
        self.set_lights(OFF, OFF, OFF)
        self.pwm_R.stop()
        self.pwm_G.stop()
        self.pwm_B.stop()

        GPIO.cleanup()
        
        
   def kelvin(self):
        import KelvinRGB as K
        step_size = 100
        for i in range(0, 15000, step_size):
        #color = list(map(lambda div: div/255.0, convert_K_to_RGB(i))) + [1]
        #print(color)
            r, g, b = K.convert_K_to_RGB(i)
            r = round(map(r, 0, 256, 0, 100), 1)
            g = round(map(g, 0, 256, 0, 100), 1)
            b = round(map(b, 0, 256, 0, 100), 1)            
            print(i, r, g, b)
            self.set_lights(r, g, b)
            sleep(0.25)
            
   def kelvin_sunrise(self):
        import KelvinRGB as K
        start = 12000
        end = 5500
        step_size = -100
        step = 100/abs((start - end)/100)
        step_count = step
        for i in range(start, end, step_size):
        #color = list(map(lambda div: div/255.0, convert_K_to_RGB(i))) + [1]
        #print(color)
            r, g, b = K.convert_K_to_RGB(i)
            r = round(map(r, 0, 256, 0, 100), 1)
            # add factor for intensity
            ri = round((r/100) * (step_count), 1)
            g = round(map(g, 0, 256, 0, 100), 1)
            gi = round((g/100) * (step_count), 1)
            b = round(map(b, 0, 256, 0, 100), 1)
            bi = round((b/100) * (step_count), 1)
            #print(i, r, g, b)
            #self.set_lights(r, g, b)
            
            print(i, ri, gi, bi, step_count)            
            self.set_lights(ri, gi, bi)            
            step_count = step_count + step
            sleep(0.25)
            
    
   def sun2(self, SUNRISE=True):
        import Sunset as s
        step_size = 1
        steps = 20
        # astronomical twilight
        print("Astronomical Twilight 1")
        for step in range(0, steps, step_size):
            r, g, b = s.astronomical_twilight1(step, steps)
            #print(step, r, g, b)
            self.set_lights(r, g, b)
            sleep(0.25)
        print("Astronomical Twilight 2")
        for step in range(0, steps, step_size):
            r, g, b = s.astronomical_twilight2(step, steps)
            #print(step, r, g, b)
            self.set_lights(r, g, b)
            sleep(0.25)
        # nautical twilight
        print("Nautical Twilight")
        for step in range(0, steps, step_size):
            r, g, b = s.nautical_twilight(step, steps)
            #print(step, r, g, b)
            self.set_lights(r, g, b)
            sleep(0.25)
        print("Civil Twilight 1")
        for step in range(0, steps, step_size):
            r, g, b = s.civil_twilight1(step, steps)
            #print(step, r, g, b)
            self.set_lights(r, g, b)
            sleep(0.25)
        print("Civil Twilight 2")
        for step in range(0, steps, step_size):
            r, g, b = s.civil_twilight2(step, steps)
            #print(step, r, g, b)
            self.set_lights(r, g, b)
            sleep(0.25)
        
    
def map(value, R1_Low, R1_High, R2_Low, R2_High):
    # map one range of numbers to another range
    y = (value-R1_Low)/(R1_High-R1_Low)*(R2_High-R2_Low) + R2_Low
    return y

def test():
    # cycle the leds
    gl = PWM()
    try:

        while True:
            print("Red")
            for r in range(0, 100):
                gl.set_lights(r, OFF, OFF)
                print("Cycle R", r)
                sleep(0.1)
            gl.set_lights(OFF, OFF, OFF)
            print("Green")
            for g in range(0, 100):
                gl.set_lights(OFF, g, OFF)
                print("Cycle G", g)
                sleep(0.1)
            gl.set_lights(OFF, OFF, OFF)
            print("Blue")
            for b in range(0, 100):
                gl.set_lights(OFF, OFF, b)                
                print("Cycle B", b)
                sleep(0.1)
            gl.set_lights(OFF, OFF, OFF)
    except KeyboardInterrupt:
        pass
    
    gl.end()
    
def test1():
    # Check minimum dimming
    print("Check dimming")
    gl = PWM()
    gl.set_lights(1, 1, 1)
    sleep(10)
    gl.set_lights(100, 100, 100)
    sleep(10)
    
    gl.end()
    print("Done")

def test3():
    # Run rainbow spectrum from Violet to Red
    gl = PWM()
    gl.spectrum()
    gl.end()
    
def test2():    
    # Run rainbow spectrum from Violet to Red
    gl = PWM()
    gl.sun()
    gl.sun(False)
    gl.end()
    
def test4():    
    # Run rainbow spectrum from Violet to Red
    print("Kelvin")
    gl = PWM()
    gl.kelvin()
    gl.end()
    print("Done")

def test5():    
    import Sunset
    print("Sunrise")
    gl = PWM()
    gl.sun2()
    gl.end()
    print("Done")

    
def test6():

   print("Dim")
   sc_r = 21
   sc_g = 40
   sc_b = 82

   so_r = round(map(253, 0, 255, 0, 100), 1)
   so_g = round(map(94, 0, 255, 0, 100), 1)
   so_b = round(map(83, 0, 255, 0, 100), 1)
   
   r = so_r
   g = so_g
   b = so_b
   gl = PWM()
   
   for x in range(0, 50):
       r = r -1
       if r < 0:
           r = 0
       g = g -1
       if g < 0:
           g = 0
       b = b -1
       if b < 0:
           b = 0
       gl.set_lights(r, g, b)
       print(x, r, g, b)
       sleep(0.5)
   gl.end()
   print("Done")
   
def test7():
    # Cycle colors in increasing brightness
    gl = PWM()
    s = 0.05
    for x in range(0, 101):
        print(x)
        gl.set_lights(x, OFF, OFF)
        sleep(s)
        gl.set_lights(OFF, x, OFF)
        sleep(s)
        gl.set_lights(OFF, OFF, x)
        sleep(s)

    gl.end()        
        
def test9():
    # Increase white
    gl = PWM()
    gl.kelvin_sunrise()
    gl.end()
    
    
           
    

if __name__ == "__main__":
    #test()  # cycle all lights
    #test1() # check dimming
    #test2() # Sunrise
    #test3() # spectrum
    #test4() # kelvin
    #test5() # sunset
    #test6() # dimming
    test7() # increase cycle
    #test8() # incease white
    #test9() # Kelvin_Sunset

