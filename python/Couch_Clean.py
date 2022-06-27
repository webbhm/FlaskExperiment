"""
# Author: Howard Webb
# Date: 3/2/2018
# Clean records
    Change Environmental_Observation to Environment_Observation
    Create location for hierarchy of field, trial, plot
    Remove root field
"""

import json
import requests
from datetime import datetime
#from LogUtil import get_logger

#logger = get_logger('Clean_Couch')
counter = 0

def getRecords(skip, limit, test=False):
    '''Run a Mango query to get the data'''
    header={"Content-Type":"application/json"}
    payload={"selector":{"start_date.timestamp":{"$gt":''}}, 'limit':limit, 'skip':skip}
#    payload={"selector":{"start_date.timestamp":{"$gt":''}, "status.status_qualifier":{"$eq": "Success"}, "activity_type":{"$eq":"Environment_Observation"}, "subject.name":{"$eq": "Air"},"subject.location.name": {"$eq": "Top"}, "$or":[{"subject.attribute.name":"Humidity"}, {"subject.attribute.name":"Temperature"}]}, "fields":["start_date.timestamp", "subject.attribute.name", "subject.attribute.value"], "sort":[{"start_date.timestamp":"desc"}], "limit":250}        
    url='http://webbhm:admin@localhost:5984/mvp_test/_find'
    return requests.post(url, json=payload, headers=header)

def getInfo(test=False):
    '''Run a Mango query to get the data'''
    header={"Content-Type":"application/json"}
    payload={}
    url='http://webbhm:admin@localhost:5984/mvp_test'
    result = requests.get(url, headers=header)
    doc_count = result.json()['doc_count']
    return doc_count

def saveRecord(jsn):
    """Self test
           Args:
               jsn: json message to persist to the database
           Returns:
               status
           Raises:
               None
    """
    global counter
    headers = {'content-type': 'application/json'}
    database = 'http://localhost:5984/mvp_data'
    req = requests.post(database, data=json.dumps(jsn), headers=headers)
    counter += 1
#    print "Count:", counter
    return get_status(req)

def cleanRecord(rec):
#    print type(rec)
#    print len(rec), rec
    if rec['activity_type'] == 'Environmental_Observation':
        rec = cleanEnvironmental(rec)
    elif rec['activity_type'] == 'Environment_Observation':
        rec = cleanEnvironmental(rec)
    elif rec['activity_type'] == 'Agronomic_Activity':
        rec = cleanAgronomic(rec)
    elif rec['activity_type'] == 'Phenotype_Observation':
        rec = cleanPhenotype(rec)
    elif rec['activity_type'] == 'State_Change':
        rec = cleanState(rec)
    else:
        print rec['activity_type']
    del rec['_id']
    del rec['_rev']
    return rec

def cleanEnvironmental(rec):
    rec['activity_type'] = 'Environment_Observation'
    rec = cleanTime(rec)
    rec = cleanLocation(rec)
#    print rec
    return rec

def cleanEnvironment(rec):
    rec = cleanTime(rec)    
    rec = cleanLocation(rec)
    return rec


def cleanAgronomic(rec):
    rec = cleanTime(rec)
    rec = cleanLocation(rec)
    return rec

def cleanPhenotype(rec):
    rec = cleanTime(rec)
    rec = cleanLocation(rec)
    return rec

def cleanState(rec):
    rec = cleanTime(rec)
    rec = cleanLocation(rec)
    return rec


def cleanLocation(rec):
    if 'location' in rec:
        pass
    else:
        rec['location'] = {'field':rec['field']}
    del rec['field']
    return rec

def cleanTime(rec):
    timestamp = rec['start_date']['timestamp']
    if len(timestamp) == 19:
        ts = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
        dt = makeDateStruct(ts)
        rec['start_date'] = dt        
    elif len(timestamp) == 8:
        print timestamp
        ts = datetime.strptime(timestamp, '%m/%d/%y')
        dt = makeDateStruct(ts)
        rec['start_date'] = dt        
    elif len(timestamp) == 10:
        print timestamp
        ts = datetime.strptime(timestamp, '%Y-%m-%d')
        dt = makeDateStruct(ts)
        rec['start_date'] = dt        
    elif len(timestamp) == 17:
        print timestamp
        ts = datetime.strptime(timestamp, '%m/%d/%y %H:%M %p')
        dt = makeDateStruct(ts)
        rec['start_date'] = dt        

    else:
        print timestamp, len(timestamp)
        raise DateError(timestamp)
    return rec
        

def makeDateStruct(t):
    timestamp = t.isoformat()
    parts = [t.strftime('%Y'), t.strftime('%m'), t.strftime('%d'), t.strftime('%H'), t.strftime('%M'), t.strftime('%S')]
    dt = {'timestamp':timestamp, 'parts': parts, 'week':t.strftime('%V')}
    return dt        

def get_status(msg):
    """Self test
       Need to add testing around the return message
           Args:
               jsn: json message to persist to the database
           Returns:
               status
           Raises:
               None
    """
    return True


def main():
    """Self test
           Args:
               None
           Returns:
               None
           Raises:
               None
    """
    limit = 500
    rec_count = getInfo()
    print "Records:", rec_count
    skip = 0
    global counter
    while counter < rec_count:
        print "Skip:", skip, "Count:", counter, "Records:", rec_count
        print "Count:", counter            
        data = getRecords(skip, limit)
        records = data.json()['docs']
        for rec in records:
            rec = cleanRecord(rec)
            saveRecord(rec)
#            counter += 1
        skip += limit
    print "Done, Count:", counter        

def main2():
    """Self test
           Args:
               None
           Returns:
               None
           Raises:
               None
    """
    skip = 0
    limit = 5
    data = getInfo()
    print data
#    records = data.json()['docs']
    skip =+ limit        
    

if __name__ == "__main__":
    main()
