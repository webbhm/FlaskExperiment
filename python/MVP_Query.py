'''
Simple program for testing the MVP_DEMO_DATA database
Author: Howard Webb
Date: 2018-09-03

'''
import couchdb
from datetime import datetime
import json

def getServer(url):
    ''' Simple wrapper to get a server object
        Args:
            url: location of the CouchDB instance
        Return:
            server object
        Raises:
            None
    '''                
    return couchdb.Server(url)

def getDatabase(db_name, server):
    ''' Tests if the database exists and opens it
        Args:
            db_name: name of the database to open
            server: server object containing the databases
        Return:
            database object
        Raises:
            None
    '''                
    if db_name in server:
        return server[db_name]
    else:
        print db_name, "Not Found in Server"
        return None

def getViewResults(db, view, start, end, level):
    ''' Test the Trial view
        Args:
            db: Database object
            view: Name of the view to use
            start: Key array defining the start parameters
            end: Key array defining the end parameters
            level: Grouping level
        Return:
            Non
        Raises:
            None
    '''                
    print "In Results", view, start, end
    result = db.view(view, startkey=start, endkey=end, group=True, group_level=level)
    for item in result:
        tm = ''
        if level == 2:
            tm = 'Week:'
            KEY = 1
        elif level == 3:
            KEY = 2
            tm = 'Day: '
            
        print tm, item.key[KEY], item.key[0], 'Min', item.value['min'], 'Max', item.value['max'], 'Avg', item.value['sum']/item.value['count']

def MangoQuery(db):
    ''' Test query of the Trial View
        Args:
            db: Database object
        Return:
            None
        Raises:
            None
    '''                
    # Pass the current date/time so get anything less than this
    ts = str('{:%Y-%m-%d %H:%M:%S}'.format(datetime.utcnow()))    
#    mango =     print db.find(mango)
    for row in db.find(mango):
        print row["start_date.timestamp"], row["subject.attribute.value"]

    # Pull the first 25 records
    mango = '{"limit":25}'
    print mango
    print db.find(mango)
    for row in db.find(mango):
        print row["start_date.timestamp"], row["subject.attribute.value"]

def MangoQ(db, query):
    print db.find(query)
    for row in db.find(query):
        print row
    
def test():
    ''' Test query of the Trial View
        Args:
            None
        Return:
            None
        Raises:
            None
    '''            
  
    url = 'http://localhost:5984'
    db_name = 'mvp_demo_data'
    usr = 'webbhm'
    pwd = 'admin'

    server = getServer(url)
    # Need to give credentials, not just login to the database
    server.resource.credentials = (usr, pwd)    
    db = getDatabase(db_name, server)

    view = '_design/trial_d3ca243b-2740-4557-87f9-c07be9d929ad_view/_view/trial_view'
    start = ['Temperature',0, 0]
    end = ['Temperature', {}, {}]
    # Pull the weekly averages
    level = 2
    getViewResults(db, view, start, end, level)
    # Pull the daily averages
    level = 3
    getViewResults(db, view, start, end, level)



if __name__ == "__main__":
    test()
    

