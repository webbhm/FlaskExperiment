'''
Create demo data for testing
'''

from couchdb import Server
import os

usr = 'webbhm'
pwd = 'admin'

def test():
    try:
        server = Server('http://localhos:5984')
        for db in server:
            print db
    except:
        print "failed"

def test2():
    cmd = 'curl -X GET http://localhost:5984'
    print os.system(cmd)
    
    
    
if __name__=="__main__":
    test2()
