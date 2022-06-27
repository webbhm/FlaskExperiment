import RPi.GPIO as GPIO
import time
print "Loading smtplib"
import smtplib

ON=1
OFF=0

switchPin=17

class Vole(object):

    def __init__(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(switchPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def getState(self, pin):
        '''Get the current state of the pin'''
        state=GPIO.input(pin)
        return state

    def checkTrap(self,test=False):
        if self.getState(switchPin):
            if test:
                print "Trap is closed - got the bugger!!!"
            self.phoneHome(test)
        else:            
            if test:
                print "Trap is open - have patience"

    def phoneHome(self,test=False):
        FROM='hmwebb.development@gmail.com'
        TO='3146818893@txt.att.net'
        pwd='deVel0pp'
        if test:
            print "Sending Messagage"
            print "Connecting to Server"
        server=smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        if test:
            print "Passed Security"
            print "Login"
        server.login(FROM, pwd)
        msg="Got it"
        if test:
            print "Sending message"
        server.sendmail(FROM, TO, msg)
        server.quit()
        

    def test(self):
        print "Test"
        while True:
            
            print "State ", self.getState(switchPin)

if __name__=="__main__":
    v=Vole()
    v.checkTrap(True)        
    
