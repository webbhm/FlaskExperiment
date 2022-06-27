import couchdb

def getServer(url):
    return couchdb.Server(url)

def getDatabase(db_name, server):
    if db_name in server:
        return server[db_name]
    else:
        print db_name, "Not Found in Server"
        return None

def getViewResults(db, view, start, end):
    for item in db.view(view, startkey=start, endkey=end):
        print item.key, item.id, item.value

def test():
    url = 'http://localhost:5984'
    db_name = 'reduce_test'
    view = '_design/cars/_view/array'
    start = ['VW','Golf',2000]
    end = ['VW',{},{}]    
    server = getServer(url)
    db = getDatabase(db_name, server)
    getViewResults(db, view, start, end)
    

if __name__ == "__main__":
    test()
    

