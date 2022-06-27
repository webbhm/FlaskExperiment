'''
Get statistics for each field in the database
'''

import couchdb

def getServer(url):
    if url == None:
        return couchdb.Server()
    else:
        return couchdb.Server(url)

def getDatabase(db_name, server):
    print "getting ", db_name, ' from server'
    try:
        if db_name in server:
            print "Got", db_name
            return server[db_name]
        for db in server:
            print db
    except Exception:
        print db_name, "Not Found in Server"
        for db in server:
            print db
        return None

def saveView(db, doc_name, doc):
    db[doc_name] = doc

def createView(view_name):
    '''
    Build a CouchDB view for field summary
    Args:
        trial_id: identifier (guid) of the trial
        start_date: start date of the trial, used to determine number of days
    Returns:
        doc: the view to be inserted into the database
    Raises:
        None
    '''
    field_view = {}
    views = {}
    doc = {}
    field_view['map'] = "function (doc){" \
           " emit([doc.location.field, doc.activity_type], 1);" \
           "}"
    field_view['reduce'] = "_stats"
    views[view_name] = field_view
    doc['views'] = views
    return doc

def groupQuery(db, view_name, level):
#    for item in db.view(view_name, group=True, group_level=level):
    for item in db.view(view_name, group=True, group_level=level):
        print item
    
        

def buildView(db, doc_name, view_name):

    print "View Name", doc_name
    doc = createView(view_name)
    print doc
    print "Save View"
    saveView(db, doc_name, doc)
    

def test():
    # Run the field query
#    doc_name = '_design/field_view'
#    view = '_view/field-view'
    doc_name = '_design/field_view2'
    view = '_view/field_view'
    
    view_name = doc_name + '/' + view
#    usr = 'webbhm'
#    pwd = 'admin'
    usr = 'admin'
    pwd = 'cxsslecnpayzfich'
#    url = 'https://openagbloom.ddns.net:6984'
#    url = 'http://webbhm:admin@openagbloom.ddns.net:6984'
    url = 'https://admin:cxsslecnpayzfich@fop4.urbanspacefarms.com:6984'    
    print "URL", url
    server = getServer(url)
    db_name = 'mvp_data'
    print 'Get Credentials'
    server.resource.credentials = (usr, pwd)
    print 'get Database ', db_name

    db = getDatabase(db_name, server)
    if db is None:
        return
    print 'Build View', view_name    
# Build and save the view document to the database
#    buildView(db, doc_name, view_name)
    print "Query ", view_name
    groupQuery(db, view_name, 0)
    print '\n\n'
    groupQuery(db, view_name, 1)
    print '\n\n'
    groupQuery(db, view_name, 2)
    
if __name__ == "__main__":
    test()
    

