from couchdb import Server
from datetime import datetime

def main():
    url = 'http://webbhm:admin@localhost:5984'
    db_name = 'mvp_dummy_data'
    server = Server(url)
    db = server[db_name]
    query(db)
    print "Done"

def query(db):
    ts = str('{:%Y-%m-%d %H:%M:%S}'.format(datetime.utcnow()))    
    mango = {'selector': {'start_date.timestamp':{'$lt':ts},'activity_type':{'$eq':'Environment_Observation'}, 'subject.attribute.name':'temperature'},
              'fields': ['subject.attribute.name', 'subject.attribute.value'],
              'limit':10}
    for row in db.find(mango):                          
        print(row)                               

def createDB(server, db_name):
    db = None    
    try:
        db = Server[db_name]
    except Exception:
        print "failure finding ", db_name
        print Exception
        db = server.create(db_name)
        print "Created ", db_name
    return db

def createRecords(db):
    db['johndoe'] = dict(type='Person', name='John Doe')
    db['maryjane'] = dict(type='Person', name='Mary Jane')
    db['gotham'] = dict(type='City', name='Gotham City')    

def deleteDB(server, db_name):
    print "Deleting ", db_name
    del server[db_name]

if __name__ == "__main__":
    main()
    
