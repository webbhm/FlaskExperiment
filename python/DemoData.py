'''
Create demo data for testing
'''

import csv
import couchdb
import sys
import random
from datetime import datetime
from datetime import timedelta

NBR_PLANTS = 6
TS = 0
FIELD = 1
ACTIVITY = 2
TRIAL = 3
PLOT = 4
SUBJECT = 5
ATTRIBUTE = 6
VALUE = 7
UNITS = 8
PARTICIPANT = 9
STATUS = 10
COMMENT = 11



url = 'http://webbhm:admin@localhost:5984'
db_name = 'mvp_demo_data'

usr = 'webbhm'
pwd = 'admin'
server = couchdb.Server()
server.resource.credentials = (usr, pwd)
db = server[db_name]

def buildDemo(timestamp, field_id, trial_id):
    print "Trial", trial_id, " Start ", timestamp
    dt = datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S')
    startTrial(timestamp, field_id, trial_id)
    # Process each week
    for week in range(1, 3):
        print "Week", week
        # Process each day
        for day in range(1, 7):
            print "Day", day
            if day == 1:
                getSize(timestamp, field_id, trial_id)
            lightOn(dt, field_id)
            lightOff(dt, field_id)                 
            for hour in range(1, 24):
                for period in range(1, 3):
                    dt = dt + timedelta(minutes=20)
                    timestamp = dt.isoformat()
                    logSensors(timestamp, field_id)
            dt = dt + timedelta(days=1)
            timestamp = dt.isoformat()

        endTrial(timestamp, field_id, trial_id)

def startTrial(timestamp, field_id, trial_id):
    makePlanting(timestamp, field_id, trial_id)

def endTrial(timestamp, field_id, trial_id):
    makeHarvest(timestamp, field_id, trial_id)
    makeHarvestWeights(timestamp, field_id, trial_id)

def makePlanting(timestamp, field_id, trial_id):
    rec = [timestamp, field_id, 'Agronomic_Activity', trial_id, 'Planted', '', '', '', '', getParticipant(), 'Success', '']
    processRow(rec)

def getSize(timestamp, field_id, trial_id):
    for plot in range(1, NBR_PLANTS):
        makePlantSize(timestamp, field_id, trial_id, plot)

def makeHarvest(timestamp, field_id, trial_id):
    rec = [timestamp, field_id, 'Agronomic_Activity', trial_id, 'Harvest', '', '', '', '', getParticipant(), 'Success', '']
    processRow(rec)

def makeHarvestWeights(timestamp, field_id, trial_id):
    for plot in range(1, NBR_PLANTS):
        makePlantWeight(timestamp, field_id, trial_id, plot)

def makePlantWeight(timestamp, field_id, trial_id, plot):
    rec = [timestamp, field_id, 'Phenotype_Observation', trial_id, plot, 'Plant', 'Weight', getWeight(), 'g', getParticipant(), 'Success', '']
    processRow(rec)
    
def makePlantSize(timestamp, field_id, trial_id, plot):
    part = getParticipant()
    rec = [timestamp, field_id, 'Phenotype_Observation', trial_id, plot, 'Plant', 'Length', getLength(), 'mm', part, 'Success', '']
    processRow(rec)
    rec = [timestamp, field_id, 'Phenotype_Observation', trial_id, plot, 'Plant', 'Width', getLength(), 'mm', part, 'Success', '']
    processRow(rec)
    rec = [timestamp, field_id, 'Phenotype_Observation', trial_id, plot, 'Plant', 'height', getLength(), 'mm', part, 'Success', '']
    processRow(rec)

def lightOn(dt, field_id):
    tm = dt.replace(hour=7, minute=00)
    timestamp = dt.isoformat()
    rec = [timestamp, field_id, 'State_Change','', 'Top', 'Light', 'state', 'ON', 'state', 'Light', 'Success', '']
    processRow(rec)
    
def lightOff(dt, field_id):
    dt = dt.replace(hour=22, minute=30)
    timestamp = dt.isoformat()    
    rec = [timestamp, field_id, 'State_Change', '', 'Top', 'Light', 'state', 'OFF', 'state', 'Light', 'Success', '']
    processRow(rec)

def logSensors(timestamp, field_id):
    logTemp(timestamp, field_id)
    logHumidity(timestamp, field_id)

def logTemp(timestamp, field_id):    
    rec = [timestamp, field_id, 'Environment_Observation','', 'Left_Side', 'Air', 'Temperature', getTemp(), 'fairenheight', 'SI7021', 'Success', '']
    processRow(rec)
    
def logHumidity(timestamp, field_id):    
    rec = [timestamp, field_id, 'Environment_Observation','', 'Left_Side', 'Air', 'Humidity', getHumidity(), 'percent', 'SI7021', 'Success', '']
    processRow(rec)

def getDateStruct(timestamp):
    fmt = timestamp.isoformat()
    parts = [timestamp.strftime('%Y'), timestamp.strftime('%m'), timestamp.strftime('%d'), timestamp.strftime('%H'), timestamp.strftime('%M'), timestamp.strftime('%S')]
    dt = {'timestamp':fmt, 'parts': parts, 'week':timestamp.strftime('%V')}
    return dt    
    
def getParticipant():
    part = ['hmw', 'abc', 'def', 'ghi']
    rnd = random.randrange(0, 3)
    return part[rnd]
    
def getLength():
    return random.randrange(0, 130)
            
def getWeight():
    return random.randrange(0, 80)

def getTemp():
    return random.randrange(20, 30)

def getHumidity():
    return random.randrange(30, 100)

def processRow(row):
    rec = {}
#    print row[2]
    if row[ACTIVITY] == 'Environment_Observation':
        rec = processEnv(row)
    
    elif row[ACTIVITY] == 'Phenotype_Observation':
        rec = processPheno(row)
    elif row[ACTIVITY] == 'Agronomic_Activity':
        rec = processAgro(row)
    elif row[ACTIVITY] == 'State_Change':
        rec = processState(row)
    else:
        print 'Unknown Activity', row[ACTIVITY]
    print rec
    saveRec(rec)

def processEnv(row):
    rec = buildCore(row)
    rec['activity_type'] = row[ACTIVITY]
    rec['subject'] = {'name':row[SUBJECT],'attribute':{'name':row[ATTRIBUTE], 'units':row[UNITS], 'value': row[VALUE]}, 'location': row[PLOT]}
    rec['participant']= {'type':'device', 'name':row[PARTICIPANT]}    
    rec['location'] = {'field':row[FIELD]}    
    return rec

def processState(row):
    rec = buildCore(row)
    rec['activity_type'] = row[ACTIVITY]
    rec['subject'] = {'name':row[SUBJECT],'attribute':{'name':row[ATTRIBUTE], 'units':row[UNITS], 'value': row[VALUE]}, 'location': row[PLOT]}
    rec['participant']= {'type':'device', 'name':row[PARTICIPANT]}    
    rec['location'] = {'field':row[FIELD]}    
    return rec
    
def processAgro(row):
    rec = buildCore(row)
    rec['activity_type'] = row[ACTIVITY]
    rec['sub-activity'] = row[PLOT]
    if len(row[SUBJECT]) > 0:
        rec['subject'] = {'name':row[SUBJECT],'attribute':{'name':row[ATTRIBUTE], 'units':row[UNITS], 'value': row[VALUE]}}
    rec['location'] = {'field':row[FIELD], 'trial':row[TRIAL]}
    return rec

def processPheno(row):
    rec = buildCore(row)
    rec['activity_type'] = row[ACTIVITY]
    rec['subject'] = {'name':row[SUBJECT],'attribute':{'name':row[ATTRIBUTE], 'units':row[UNITS], 'value': row[VALUE]}}
    rec['location'] = {'field':row[FIELD], 'trial':row[TRIAL], 'plot':row[PLOT]}    
    return rec

def buildCore(row):
    rec = {}
    rec['start_date'] = {'timestamp':row[TS]}
    rec['participant']= {'type':'person', 'name':row[PARTICIPANT]}
    if len(row[COMMENT]) == 0:
        rec['status'] = {'status':'Complete', 'status_qualifier': row[STATUS]}
    else:        
        rec['status'] = {'status':'Complete', 'status_qualifier': row[STATUS], 'comment':row[COMMENT]}
    return rec

def buildSubject(row, rec):
    return rec


def buildSubActivity(row, rec):
    return rec

def saveRec(rec):
    global db
    id, rev = db.save(rec)
    print id, rev

def loadIdx(db):
    import json
    with open('/home/pi/python/FullIdx.json') as f:
        doc = json.load(f)
        print doc
        db['_design/full_index'] = doc
    with open('/home/pi/python/TimestampIdx.json') as f:
        doc = json.load(f)
        print doc
        db['_design/timestamp_index'] = doc
    with open('/home/pi/python/trial_view.json') as f:
        doc = json.load(f)
        print doc
        db['_design/trial_d3ca243b-2740-4557-87f9-c07be9d929ad_view'] = doc
        
              

def test():
    field_id = '8e89e414-0181-440a-9170-702434c8f400'
    print "Field Id ", field_id
    trial_id = 'd3ca243b-2740-4557-87f9-c07be9d929ad'
    print "Trial Id ", trial_id    
    trial_date = '2018-07-22T12:34:55'
    timestamp = trial_date
    dt = datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S')    
    print "Trial Date ", trial_date
    plot = 1
    # Start Trial
    print "Make Planting"
    makePlanting(timestamp, field_id, trial_id)
    
    # Environment Activities
    print "Log Sensors"
    logSensors(timestamp, field_id)
    print "Light Off"
    lightOn(dt, field_id)
    print "Light On"
    lightOff(dt, field_id)

    # Phenotype Observations
    print "Plant Size"
    makePlantSize(timestamp, field_id, trial_id, plot)

    # End Trial
    print "Harvest"
    makeHarvest(timestamp, field_id, trial_id)
    print "Weight"
    makePlantWeight(timestamp, field_id, trial_id, plot)

def test2():    
    field_id = '8e89e414-0181-440a-9170-702434c8f400'
    print "Field Id ", field_id
    trial_id = 'd3ca243b-2740-4557-87f9-c07be9d929ad'
    print "Trial Id ", trial_id    
    trial_date = '2018-07-22T12:34:55'
    timestamp = trial_date

    buildDemo(timestamp, field_id, trial_id)
    global db
#    loadIdx(db)

def test3():
    print "Load Indexes"
    global db
    loadIdx(db)

if __name__=="__main__":
    test2()
#    test()
