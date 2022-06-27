import couchdb

def getServer(url):
    # Simple localhost:5984
    return couchdb.Server()

def getDatabase(db_name, server):
    if db_name in server:
        return server[db_name]
    else:
        print db_name, "Not Found in Server"
        return None

def getViewResults(db, view, start, end):
    print "In Results", view, start, end
    count =  db.view(view, startkey=start, endkey=end, reduce=True, group_level = 3)
    print type(count)
    print "Return", count

def test():
    url = 'http://localhost:5984'
    db_name = 'mvp_dummy_data'
    view = '_design/array_key/_view/env_view_avg'
    start = [1,'temperature',2018, 7]
    end = [1, 'temperature', 2018, 12]    
    server = getServer(url)
    db = getDatabase(db_name, server)
    getViewResults(db, view, start, end)
    

if __name__ == "__main__":
    test()
    

