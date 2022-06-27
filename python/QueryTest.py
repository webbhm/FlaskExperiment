# Temperature chart with data from CouchDB
# Author: Howard Webb
# Date: 3/5/2018

import requests
import json
from datetime import datetime

#Use a view in CouchDB to get the data
#use the first key for attribute type
#order descending so when limit the results will get the latest at the top

MVP = 'http://192.168.2.24:5984/mvp_test/_find'
MVP_TEST = 'http://192.168.2.22:5984/mvp_test/_design/_views/daily_average'
#SERVER = 'http://webbhm:admin@openagbloom.ddns.net:5985/mvp_dummy_data/_design/test/views/humidity_stat'
SERVER = 'http://webbhm:admin@localhost:5984/reduce_test/_design/cars/_view/array'

def getResults(selector, url, test=False):
    '''Run a Mango query to get the data'''
    header={"Content-Type":"application/json"}
    if test:
        print url
        print selector
#    return requests.get(url, params=selector, headers={'content-type:application/json'})
    return requests.get(url, params=selector)
    
def test():
    ts = str('{:%Y-%m-%d %H:%M:%S}'.format(datetime.utcnow()))    
#    selector = {"selector":{"location.field":{"$eq":1}, "start_date.timestamp":{"$lt":ts}, "status.status_qualifier":{"$eq": "Success"}, "activity_type":{"$eq":"Environment_Observation"}, "subject.name":{"$eq": "Air"},"subject.location.name": {"$eq": "Canopy"},"subject.attribute.name": {"$eq": "CO2 (ppm)"}}, "fields":["start_date.timestamp", "subject.attribute.value"], "sort":[{"start_date.timestamp":"desc"}], "limit":25}
#    selector = {"selector":{"location.field":{"$eq":1}, "activity_type":{"$eq":"Environment_Observation"}, "subject.name":{"$eq": "Air"},"subject.location.name": {"$eq": "Canopy"},"subject.attribute.name": {"$eq": "temperature"}}, "fields":["start_date.timestamp", "subject.attribute.value"], "sort":[{"start_date.timestamp":"desc"}], "limit":25}
#    selector = {"selector":{"location.field":{"$eq":1}, "activity_type":{"$eq":"Environment_Observation"}, "subject.name":{"$eq": "Air"},"subject.attribute.name": {"$eq": "temperature"}}, "fields":["start_date.timestamp", "subject.attribute.value"], "sort":[{"start_date.timestamp":"desc"}], "limit":25}
#    selector = {"selector":{"location.field":{"$eq":1},"subject.attribute.name": {"$eq": "temperature"}},"limit":25}
    selector = {'startkey':[{'VW', 'Golf', 2009}]}
    url = SERVER
    data=getResults(selector, url, True)
    print "URL", data.url
    if data.status_code == 200:
        print "Type", type(data)
        print data.json()
        print "Records: ", len(data.json()["rows"])
        for rec in data.json()["rows"]:
            print "\n", rec
    else:
        print "No Data, Reason: ", data.reason

if __name__=="__main__":
    test()

