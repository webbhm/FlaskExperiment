'''
User object for device and database information
The object manages generating a device list and updating the default device values

Author: Howard Webb
Date: 10/19/2020
'''

from couchdb import Server

# Put your CouchDB url here
#url = 'http://webbhm:admin@localhost:5984'
#url = 'http://localhost:5984'
url = 'http://openagbloom.ddns.net/couch'
# this should not change
db_name = 'user'

class MarsFarmUser(object):
    def __init__(self, email=None):
        self._server = Server(url)
        self._db_name = db_name
        self._db = self._server[self._db_name]
        self._user = None
        self._device_list = None
        if email:
            self._user = self._db[email]
            self._device_list = [device["Device"]["Name"] for device in self._user["Devices"]]
        
    def validate(self, email):
        try:
            #self._user = self.getUser(email)
            self._user = self._db[email]
        except Exception as e:
            print(e)
            return False, 'User not found'
        try:
            self._device_list = [device["Device"]["Name"] for device in self._user["Devices"]]
            return True, self._device_list
        except:
            return True, []
            

    def getUser(self, email):
        # retreive user or create if not found
        # assumes id is the email
        payload = {"selector":{"Email":email}, "limit":1}
        print(payload)
        for row in self._db.find(payload):
            print(row)
        #if records:
        #    return records[0]
        #return []
        
    def createUser(self, record):
        #record["_id"] = email  # use email as id
        self._db.save(record)
        
    def saveUser(self):
        self._db.save(self._user)
        
    def setDefaultDevice(self, name):
        # Move the selected device info up a level
        # Only two attributes used here, add more for your record
        id = self._user.id
        # get index of selected device name
        index = self._device_list.index(name)
        # Update the default values
        self._user["Device"] = self._user["Devices"][index]["Device"]["Name"]
        self._user["Database"] = self._user["Devices"][index]["Device"]["Database"]
        self._user["S3"] = self._user["Devices"][index]["Device"]["S3"]
        self._user["S3_link"] = self._user["Devices"][index]["Device"]["S3_link"]

        # save back to database
        
        self._db.save(self._user)
        # refresh record for new version
        self._user = self._db[id]
        
    def getDeviceList(self):
        # use a slick list generator to get list of device names
        return self._device_list
    
    def getDevice(self):
        return self._user["Device"]
    
    def getDatabase(self):
        return self._user["Database"]
    
def test():
    email = "howard.webb@gmail.com"
    user = None
    try:
        user = MarsFarmUser(email)
    except:
        print("No user for Email")
    print("ID:", user._user.id)
    print("Revison:", user._user.rev)
    print("Default Device:", user.getDevice())
    print("Default Database:", user.getDatabase())
    
    # call this to get your selection list
    try:
        print("List:", user.getDeviceList())
    except:
        print("No device list for this user")
        
    # When the user picks a device name, update with this
    user.setDefaultDevice('Farm1')
    print("Device:", user._user["Device"])
    print("Database:", user._user["Database"])
    print("Database:", user._user["S3"])
    print("Database:", user._user["S3_link"])    
    print("Revision:", user._user.rev)
    
def test2():
    email = "ruddy@gmail.com"
    user = None
    try:
        user = MarsFarmUser()
        status, ret = user.validate(email)
        if not status:
            print(ret)
            return
    except:
        print("No user for Email")
    print("ID:", user._user.id)
    print("Revison:", user._user.rev)
    print("Default Device:", user.getDevice())
    print("Default Database:", user.getDatabase())
    
    # call this to get your selection list
    try:
        print("List:", user.getDeviceList())
    except:
        print("No device list for this user")
        
    # When the user picks a device name, update with this
    #user.setDefaultDevice('Farm1')
    print("Device:", user._user["Device"])
    print("Database:", user._user["Database"])
    print("Database:", user._user["S3"])
    print("Database:", user._user["S3_link"])    
    print("Revision:", user._user.rev)    

if __name__ == "__main__":
    test2()
    
