import csv
from CouchDB import log_env_obsv_json
import sys


def getFile():
    filename = '/home/pi/MVP-Test/data/Exp_1.csv'
    return filename

def getReader(filename):
   with open(filename, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar="'")            
        for row in reader:
            print ', '.join(row)
            rec = processRow(row)
            print rec
            saveRec(rec)
            


def processRow(row):
#    print row
    rec = {}
    print row[2]
    if row[2] == 'Environment_Observation':
        rec = processEnv(row)
    
    elif row[2] == 'Phenotype_Observation':
        rec = processPheno(row)
    elif row[2] == 'Agronomic_Activity':
        rec = processAgro(row)
    else:
        print 'Unknown Activity', row[2]
    return rec

def processEnv(row):
    rec = buildCore(row)
    rec['activity_type'] = row[2]
    rec['subject'] = {'location':row[6],'attribute':{'name':row[7], 'units':row[9], 'value': row[8]}}
    rec['location'] = {'field':row[1]}    
    return rec

    
def processPheno(row):
    rec = buildCore(row)
    rec['activity_type'] = row[2]
    rec['subject'] = {'name':row[6],'attribute':{'name':row[7], 'units':row[9], 'value': row[8]}}
    rec['location'] = {'field':row[1], 'trial':row[4], 'plot':row[5]}    
    return rec


def processAgro(row):
    rec = buildCore(row)
    rec['activity_type'] = row[2]
    rec['sub-activity'] = row[4]
    if len(row[5]) > 0:
        rec['subject'] = {'name':row[6],'attribute':{'name':row[7], 'units':row[9], 'value': row[8]}}
    rec['location'] = {'field':row[1], 'trial':row[4]}
    return rec

def buildCore(row):
    rec = {}
    rec['start_date'] = {'timestamp': row[0]}
    rec['field']={'uuid':row[1]}
    rec['participant']= {'type':'person', 'name':row[10]}

    if len(row[12]) == 0:
        rec['status'] = {'status':'Complete', 'status_qualifier': row[11]}
    else:        
        rec['status'] = {'status':'Complete', 'status_qualifier': row[11], 'comment':row[12]}
    return rec

def buildSubject(row, rec):
    return rec


def buildSubActivity(row, rec):
    return rec

def saveRec(rec):
    res = log_env_obsv_json(rec)
    print res

def main():
    filename = getFile()
    reader = getReader(filename)

if __name__=="__main__":
    main()    
