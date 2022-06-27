from couchdb import Server

def main():
    url = 'http://webbhm:admin@localhost:5984'
    db_name = 'python-test'
    server = Server(url)
    db = createDB(server, db_name)
    if db == None:
        print "No Database"
        return
    createRecords(db)
    query(db)
    deleteDB(server, db_name)
    print "Done"

def query(db):
    mango = {'selector': {'type': 'Person'},
              'fields': ['name']}
    for row in db.find(mango):                          
        print(row['name'])                               

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
    
