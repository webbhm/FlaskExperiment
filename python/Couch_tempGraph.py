import couchdb
from datetime import datetime, timedelta

def getServer(url):
    return couchdb.Server(url)

def getDatabase(db_name, server):
    if db_name in server:
        return server[db_name]
    else:
        print db_name, "Not Found in Server"
        return None

def getViewResults(db, view, start, end, lim):
    for item in db.view(view, startkey=start, endkey=end, limit=250):
        print item.key, item.id, item.value

def test():
    print 'Start Test'
    url = 'http://webbhm:admin@localhost:5984'
    db_name = 'mvp_data'
    view = '_design/TempGraph/_view/tempGraph'
# convert datetime to UTC    
    d=datetime.strptime('2018-11-08T10:30:20', '%Y-%m-%dT%H:%M:%S')
    epoch = datetime(1970,1,1,0,0,0, tzinfo=None)
    start_dt = timedelta.total_seconds(d - epoch)*1000
# take off span of chart    
    chart_span = 30
    chart_start = start_dt - (24*60*60*1000*chart_span)
    print "Start Chart", chart_start
# dummy out for now due to lack of data
    start_dt = 0
    
    start = [start_dt,'']
    end = [{},{}]
    print 'URL', url
    print 'View', view
    server = getServer(url)
    db = getDatabase(db_name, server)
    getViewResults(db, view, start, end, 250)
    

if __name__ == "__main__":
    test()
    

