import couchdb

def getServer(url):
    if url == None:
        return couchdb.Server()
    else:
        return couchdb.Server(url)

def getDatabase(db_name, server):
    if db_name in server:
        return server[db_name]
    else:
        print db_name, "Not Found in Server"
        return None

def saveView(db, doc_name, doc):
    db[doc_name] = doc

def createView(field_id, trial_date):
    '''
    Build a CouchDB view for trial date summary
    Args:
        trial_id: identifier (guid) of the trial
        start_date: start date of the trial, used to determine number of days
    Returns:
        doc: the view to be inserted into the database
    Raises:
        None
    '''
    activity_type = 'Environment_Observation'
    trial_view = {}
    views = {}
    doc = {}
    trial_view['map'] = "function (doc){" \
           "if(doc.activity_type == '" + activity_type + "'&&doc.location.field == " + str(field_id) + "){" \
           " var trial_start = Date.parse('" + trial_date + "');" \
           " var day = Date.parse(doc.start_date.timestamp);" \
           " var trial_day = Math.floor((day - trial_start)/(1000 * 60 * 60 * 24));" \
           " var wk = Math.ceil(trial_day/7);" \
           " emit([doc.subject.attribute.name, wk, trial_day], doc.subject.attribute.value);" \
           "};}"
    trial_view['reduce'] = "_stats"
    views['trial_view'] = trial_view
    doc['views'] = views
    return doc

def queryView(db, view, start, end):
    for item in db.view(view, startkey=start, endkey=end, reduce=False):
        print item.key, item.id, item.value

def weeklySummary(db, view_name, start, end):
    for item in db.view(view_name, startkey=start, endkey=end, group=True, group_level=2):
        print "Week ", item.key[1], "Average ", item.value['sum']/item.value['count'], "Min ", item.value['min'], " Max ", item.value['max']

def dailySummary(db, view_name, start, end):
    for item in db.view(view_name, startkey=start, endkey=end, group=True, group_level=3):
        print "Day ", item.key[2], "Average ", item.value['sum']/item.value['count'], "Min ", item.value['min'], " Max ", item.value['max']

def groupQuery(db, view_name, level):
    for item in db.view(view_name, group=True, group_level=level):
        print item
    
        

def buildView(db, doc_name, field_id, trial_id, trial_date):

    print "View Name", doc_name
    doc = createView(field_id, trial_date)
    print doc
    print "Save View"
    saveView(db, doc_name, doc)
    

def test():
    field_id = 1
    trial_id = 'a234bss'
    trial_date = '2018-07-22T12:34:55'


    usr = 'webbhm'
    pwd = 'admin'
    url = 'localhost:5984'    
    print "URL", url
    server = getServer(url)
    db = 'mvp_dummy_data'
    print 'Database', db
    server.resource.credentials = (usr, pwd)
    doc_name = '_design/trial_' + str(field_id) + '_' + str(trial_id) + '_view'    
    view_name = doc_name + '/_view/trial_view'
    print 'View', view_name
    db = server[db]
# Build and save the view document to the database
#    buildView(db, doc_name, field_id, trial_id, trial_date)

    test2(db, view_name)

def test2(db, view_name):    
    '''Query view test'''
    
    attrib = 'temperature'
    start = [attrib, 1, 1]
    end = [attrib,{}, {}]

    print "Daily Average Temperature"
    dailySummary(db, view_name, start, end)
    print "Weekly Average Temperature"    
    weeklySummary(db, view_name, start, end)    

    attrib = 'humidity'
    start = [attrib, 1, 1]
    end = [attrib, {}, {}]
    print "Daily Average Humidity"    
    dailySummary(db, view_name, start, end)
    print "Weekly Average Humidity"    
    weeklySummary(db, view_name, start, end)
    print "All Records"
    queryView(db, view_name, start, end)

def test3():
    ''' check fields in database'''
    usr = 'Rep'
    pwd = 'copy'
    url = 'https://fop4.urbanspacefarms.com:6984'    
    print "URL", url
    server = getServer(url)
    db_name = 'mvp_data'
    print 'Database', db_name
    view_name = '_design/field_view/_view/field-view'
    server.resource.credentials = (usr, pwd)
    db = server[db_name]    
    groupQuery(db, view_name, 1)    
    
     
    
if __name__ == "__main__":
    test3()
    

