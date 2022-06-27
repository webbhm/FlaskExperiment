from couchdb import Server

def getServer(name, port, user, pwd):
    ''' Return a server object '''
    return Server("https://%s:%s@%s:%s/" % (user, pwd, name, port))
    

def createDB(server, db_name):
    ''' Create a database if it does not exist '''
    db = None    
    try:
        db = Server[db_name]
    except Exception:
        print("{}: {}".format("Failure finding", db_name))
        print(Exception)
        db = server.create(db_name)
        print("{}: {}".format("Created", db_name))

    return db

def createRecords(db):
    ''' Create records in a database '''
    db['johndoe'] = dict(type='Person', name='John Doe')
    db['maryjane'] = dict(type='Person', name='Mary Jane')
    db['gotham'] = dict(type='City', name='Gotham City')

def query(db):
    ''' Run a mango query '''
    mango = {'selector': {'type': 'Person'},
              'fields': ['name']}
    for row in db.find(mango):                          
        print(row['name'])                               

def createUsers(server):
    ''' Create users with roles '''
    server.add_user('ThingOne', 'one', ['farmer'])
    server.add_user('ThingTwo', 'two', ['grower'])
    server.add_user('ThingThree', 'three', ['helper'])

def createRep(server):
    ''' Create replication user - for MVP users '''
    server.add_user('Rep', 'copy', ['grower'])

def insertSecurity(db):
    db.resource.put('_security', {"admins":{"roles":["farmer"]}, "members":{"roles":["grower", "helper"]}})

def buildDatabase(server, db_name):
    ''' create a database and add security document '''
    db = createDB(server, db_name)
    if db == None:
        print("No Database")
        return
    else:
        insertSecurity(db)
        return db

def makeReadOnly(db):
    '''Add a design document with a "validation function" '''
    doc = {"validate_doc_update":"function(newDoc, oldDoc, userCtx){if(userCtx.roles.indexOf('helper') !== -1){throw({forbidden:'Read Only Database!'});}}"}
    db["_design/read_only_helper"]=doc

def getUser(user, pwd):
    '''Query user database for info'''
    

def test():
    db_name = 'Test'
    print("Test read only - admin")
    usr = 'webb'
    pwd = 'admin'
    s = Server()
    s.resource.credentials = (usr, pwd)    
    db = s[db_name]
    db['TestDoc_admin'] = dict(foo='foo', bar='bar')

    db_name = 'Test'
    print("Test read only - helper")
    usr = 'webb'
    pwd = 'admin'
    s = Server()
    s.resource.credentials = (usr, pwd)    
    db = s[db_name]
    db['TestDoc_admin'] = dict(foo='foo', bar='bar')
   
    
    print("Test grower")
    usr = 'ThingTwo'
    pwd = 'Two'
    s = Server()
    s.resource.credentials = (usr, pwd)
    db = s[db_name]    
    db['TestDoc_2'] = dict(foo='foo', bar='bar')
    
    print("Test farmer")
    usr = 'ThingOne'
    pwd = 'One'
    s = Server()
    s.resource.credentials = (usr, pwd)
    db = s[db_name]
    db['TestDoc_1'] = dict(foo='foo', bar='bar')

def setup(name, port, db_name, user, pwd):
    server = getServer(name, port, user, pwd)
    db = buildDatabase(server, db_name)
    createUsers(server)
    print("Make Read Only")
    makeReadOnly(db)

def testSecurity(name, port, db_name, user, pwd):
    server = getServer(name, port, user, pwd)
    db = server[db_name]
    try:
        createRecords(db)
    except:
        "Failure creating records"
    print("Query")
    query(db)

def tearDown(name, port, db_name, user, pwd):
    server = getServer(name, port, user, pwd)
    del server[db_name]

def delete(db):
    doc = db['johndoe']
    db.delete(doc)
    doc = db['maryjane']
    db.delete(doc)
    doc = db['gotham']
    db.delete(doc)

def testUser(name, port, db_name, user, pwd):
    server = getServer(name, port, user, pwd)
    db = server[db_name]
    try:
        createRecords(db)
        print("Records Added")
    except:
        print("Failure creating records")
    print("Query")
    query(db)
    print("Delete Records")
    try:
        delete(db)
        print("Deleted Records")
    except:
        print("No Records to Delete")

def test2():
#    url = 'http://webbhm:admin@localhost:5984'
    name = 'fop4.urbanspacefarms.com'
    port = '6984'
    user = 'admin'
    pwd = 'cxsslecnpayzfich'     
    db_name = 'security_test'    
    print("Setting up new database")
#    setup(name, port, db_name, user, pwd)


    user = 'ThingOne'
    pwd = 'one'
    print("{} {} {}".format("Test with user", user, pwd, " Should succeed"))
    testUser(name, port, db_name, user, pwd)
    user = 'ThingTwo'
    pwd = 'two'
    print("{} {} {}".format("Test with user", user, pwd, " Should succeed"))
    testUser(name, port, db_name, user, pwd)
    user = 'ThingThree'
    pwd = 'three'
    print("{} {} {}".format("Test with user", user, pwd, " Should Fail to create records"))
    testUser(name, port, db_name, user, pwd)
    user = 'ThingFour'
    pwd = 'four'
    print("{} {} {}".format("Test with user", user, pwd, " Should Fail Access"))
    try:
        testUser(name, port, db_name, user, pwd)
    except:
        print("User failed")
    print("Done")

def test3():
    ''' create rep user '''
    name = 'fop4.urbanspacefarms.com'
    port = '6984'
    user = 'admin'
    pwd = 'cxsslecnpayzfich'
    server = getServer(name, port, user, pwd)
    createRep(server)

def testLogin():
    print("Test Login")
    print("Get Server")
    url = 'http://webbhm:admin@localhost:5984'
    name = 'localhost'
    port = '5984'
    user = 'webbhm'
    pwd = 'admin'

    server = getServer(name, port, user, pwd)
    print("Create User")
    createUsers(server)          
    
      
     
    

if __name__ == "__main__":
    testLogin()
    
