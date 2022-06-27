from couchdb import Server

# This is already in your user.py
def couch_access():
    url = 'http://openagbloom.ddns.net/couch'
    return Server(url)
    
'''
-------------------------------------------------------
Copy and paste the below functions into your user.py
'''

def getRecord(email):
    # Retreives the entire user record
    server = couch_access()
    db_name = "user"
    db = server[db_name]
    
    payload = {"selector":{"Email":email}, "limit":1}
    data = db.find(payload)
    
    if not data:
        return []
    # return first record of list, but should only be one
    return data[0]

def set_default_device(email, name):

    rec = getRecord(email)
    if not rec:
        return False

    server = couch_access()
    db_name = "user"
    db = server[db_name]

    # Move the selected device info up a level
    # Only two attributes used here, add more for your record
    id = rec['_id']
    # get index of selected device name
    print(rec['Devices'])
    dev_list = [dev['Device']['Name'] for dev in rec['Devices']]
    print(dev_list)
    index = dev_list.index(name)
    # Update the default values
    rec["Device"] = rec["Devices"][index]["Device"]["Name"]
    rec["Database"] = rec["Devices"][index]["Device"]["Database"]
    rec["S3"] = rec["Devices"][index]["Device"]["S3"]
    rec["S3_link"] = rec["Devices"][index]["Device"]["S3_link"]

    # save back to database
    db[id] = rec    
    return True

if __name__ == "__main__":
    status = set_default_device('howard.webb@gmail.com', 'Farm1')
    print(status)
