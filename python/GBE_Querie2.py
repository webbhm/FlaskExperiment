'''
Demo of Ploty reports

Author: Howard Webb
Date: 6/29/2021
'''

from pymongo import MongoClient
from pprint import pprint
import json
from datetime import datetime
from Ploty_Chart import *
from Plot import Plot
import pandas as pd
from GBE_Util import *

# logon string to get into the database
url = 'mongodb+srv://webbhm:sHzHKD9_vZUGCZ4@gbe-d.cc79x.mongodb.net/gbe'

# Source directories for data files, not used here

DB = "gbe"
COLLECTION = "2020"

FAILURE = "Failure"
SUCCESS = "Success"

class MongoUtil(object):
    
    def __init__(self):
        # Create a database client
        print("Init", url)
        self._client = MongoClient(url)
        print("Initialized")
        
    # save activity records
    def save_many(self, db, col, rec_set):
        # save array of records to database (db) and collection (col)
        db = self._client[db]
        col = db[col]
        ret = col.insert_many(rec_set)
        pprint(ret)
        
    def find(self, db, col, query):
        return self._client[db][col].find(query)
    
    # Main function used to access observtion data
    def aggregate(self, db, col, query):
        return self._client[db][col].aggregate(query)
    
    def count(self, db, col, query):
        return self._client[db][col].count(query)
    
    def distinct(self, db, col, item):
        return self._client[db][col].distinct(item)
    
def find(query):
    print("Find", query)
    mu = MongoUtil()
    docs = mu.find(DB, COLLECTION, query)
    dump(docs)
        
def get_distinct(item):
    # get distinct list of items
    print("Distinct", item)
    mu = MongoUtil()
    docs = mu.distinct(DB, COLLECTION, item)
    #print("Doc", type(docs), docs)
    data = []
    for doc in docs:
        print(doc)
        data.append(doc)
    print(data)    
    print("Done")

def growth_rate_chart(title, attribute):
    #Bar chart of weekly growth (height) by gbe_id
    # Optionally run for individual school
    print("By Week Growth Chart")
    group_name = "GBE_Id"
    x_axis_name = "week"
    y_axis_name = attribute
    title = "Change by Week: " + attribute
    match = {"$match":{
           "status.status_qualifier":SUCCESS,
           "subject.attribute.name": attribute,
           "subject.attribute.value":{"$ne":0}           
            }}
    
    #Group by GBE_Id and week, get avg, min, max
    # Name is not unique, so cannot put in id
    group = {"$group":{"_id":{"GBE_Id":"$subject.GBE_Id",
                   #"name":"$subject.type",
                   "week":{"$toString":"$time.week"}},
                    "name":{"$first":"$subject.type"},   
                    "avg":{"$avg":"$subject.attribute.value"},
                    "min":{"$min":"$subject.attribute.value"},
                    "max":{"$max":"$subject.attribute.value"}
                       }
                   }
    # Rearrange data into set
    add = {"$addFields": { "value":
       {"avg":"$avg", "min":"$min", "max":"$max"},
        "week":"$_id.week"}}
    
    # Remove old data
    remove = {"$unset":["_id.week", "avg", "min", "max"]}
    
    # Array data and pivot weeks
    # Stick unique name back in id
    group3 = {"$group":{"_id":{"GBE_Id":"$_id.GBE_Id", "name":"$name"},
                   "items":{"$addToSet":{
                   "week":"$week",
                   "value":"$value"}
                   }}}    
    
    # Pivot the weeks together
    project = {"$project":
        {"data":{"$arrayToObject":{
            "$zip":{"inputs":["$items.week", "$items.value"]}
            }}}}
    
    
    #q = [match]
    #q = [match, group]
    #q = [match, group, add]
    #q = [match, group, add, remove]
    #q = [match, group, add, remove, group3]
    q = [match, group, add, remove, group3, project]
    
    # run the query
    mu = MongoUtil()
    recs = mu.aggregate(DB, COLLECTION, q)
    #dump(recs)
    #return
    # extract data for plotting as dataframe
    gbe_id = []
    name = []
    wk2 = []
    wk3 = []
    wk4 = []
    wk2_e = []
    wk3_e = []
    wk4_e = []
    TWO = "2"
    THREE = "3"
    FOUR = "4"
    for doc in recs:
        #print(doc)
        #return
        gbe_id.append("G"+str(doc["_id"]["GBE_Id"]))
        name.append(doc["_id"]["name"])
        #print(doc["data"])
        if TWO in doc["data"]:
            #print("Found 2")
            wk2.append(doc["data"][TWO]["avg"])
            #print(doc["data"][TWO]["max"], doc["data"][TWO]["min"])
            er = doc["data"][TWO]["max"] - doc["data"][TWO]["min"]
            #print(er)
            wk2_e.append(er)
        else:
            wk2.append(None)
            wk2_e.append(None)
        if THREE in doc["data"]:
            wk3.append(doc["data"][THREE]["avg"])
            er = doc["data"][THREE]["max"] - doc["data"][THREE]["min"]
            wk3_e.append(er)
        else:
            wk3.append(None)
            wk3_e.append(None)
        if FOUR in doc["data"]:
            wk4.append(doc["data"][FOUR]["avg"])
            er = doc["data"][FOUR]["max"] - doc["data"][FOUR]["min"]
            wk4_e.append(doc["data"][FOUR]["max"] - doc["data"][FOUR]["min"])
        else:
            wk4.append(None)
            wk4_e.append(None)            
    print(title)
    #return
    fig = bar_confidence2(title, gbe_id, name, wk2, wk2_e, wk3, wk3_e, wk4, wk4_e)
    return fig
    
    
def school_by_week(attribute, school):
    #Bar chart of weekly growth (height) for specific school
    # Optionally run for individual school
    #school = 'Academir Charter School West'
    #print("By Week Growth Chart for School", school)
    title = "Heigh Change By Week - " + school
    group_name = "GBE_Id"
    x_axis_name = "week"
    y_axis_name = attribute
    #print("Var", school, attribute)
    match = {"$match":{
           "status.status_qualifier":SUCCESS,
           "subject.attribute.name": attribute,
           "location.farm.name":school,
           "subject.attribute.value":{"$ne":0}
            }}
    
    #Group by GBE_Id and week, get avg, min, max
    # Name is not unique, so cannot put in id
    group = {"$group":{"_id":{"GBE_Id":"$subject.GBE_Id",
                    "plot":"$location.plot",
                   #"name":"$subject.type",
                   "week":{"$toString":"$time.week"}},
                    "name":{"$first":"$subject.type"},   
                    "avg":{"$avg":"$subject.attribute.value"},
                    "min":{"$min":"$subject.attribute.value"},
                    "max":{"$max":"$subject.attribute.value"}
                       }
                   }
    # Rearrange data into set
    add = {"$addFields": { "value":
       {"avg":"$avg", "min":"$min", "max":"$max"},
        "week":"$_id.week"}}
    
    # Remove old data
    remove = {"$unset":["_id.week", "avg", "min", "max"]}
    
    # Array data and pivot weeks
    # Stick unique name back in id
    group3 = {"$group":{"_id":{"GBE_Id":"$_id.GBE_Id", "plot":"$_id.plot", "name":"$name"},
                   "items":{"$addToSet":{
                   "week":"$week",
                   "value":"$value"}
                   }}}    
    
    # Pivot the weeks together
    project = {"$project":
        {"data":{"$arrayToObject":{
            "$zip":{"inputs":["$items.week", "$items.value"]}
            }}}}
    
    
    #q = [match]
    #q = [match, group]
    #q = [match, group, add]
    #q = [match, group, add, remove]
    #q = [match, group, add, remove, group3]
    q = [match, group, add, remove, group3, project]
    
    # run the query
    mu = MongoUtil()
    recs = mu.aggregate(DB, COLLECTION, q)
    #dump(recs)
    #return
    # extract data for plotting as dataframe
    gbe_id = [] #storing plot
    name = []
    wk2 = []
    wk3 = []
    wk4 = []
    wk2_e = []
    wk3_e = []
    wk4_e = []
    TWO = "2"
    THREE = "3"
    FOUR = "4"
    for doc in recs:
        #print(doc)
        #return
        #gbe_id.append("G"+str(doc["_id"]["GBE_Id"]))
        gbe_id.append((doc["_id"]["plot"]+"-"+str(doc["_id"]["GBE_Id"])))
        name.append(doc["_id"]["name"])
        #print(doc["data"])
        if TWO in doc["data"]:
            #print("Found 2")
            wk2.append(doc["data"][TWO]["avg"])
            #print(doc["data"][TWO]["max"], doc["data"][TWO]["min"])
            er = doc["data"][TWO]["max"] - doc["data"][TWO]["min"]
            #print(er)
            wk2_e.append(er)
        else:
            wk2.append(None)
            wk2_e.append(None)
        if THREE in doc["data"]:
            wk3.append(doc["data"][THREE]["avg"])
            er = doc["data"][THREE]["max"] - doc["data"][THREE]["min"]
            wk3_e.append(er)
        else:
            wk3.append(None)
            wk3_e.append(None)
        if FOUR in doc["data"]:
            wk4.append(doc["data"][FOUR]["avg"])
            er = doc["data"][FOUR]["max"] - doc["data"][FOUR]["min"]
            wk4_e.append(doc["data"][FOUR]["max"] - doc["data"][FOUR]["min"])
        else:
            wk4.append(None)
            wk4_e.append(None)            
    #print(gbe_id)
    #return
    fig = bar_confidence2(title, gbe_id, name, wk2, wk2_e, wk3, wk3_e, wk4, wk4_e)
    return fig
    #show(fig)
    
def germination_rate():
    # time between planting and germination, with number germinated as bubble
    match = {"$match":{
           "status.status_qualifier":SUCCESS,
           "subject.attribute.name":{"$in":[GERMINATION, PLANTING]}
           }}
           
    group = {"$group":{"_id":{"GBE_Id":"$subject.GBE_Id",
                    "name":"$subject.type",
                    "school":"$location.farm.name",
                    "plot":"$location.plot",
                    "attribute":"$subject.attribute.name"},
                    "timestamp":{"$max":"$time.timestamp"},
                    "max":{"$max":"$subject.attribute.value"},
                    "avg":{"$avg":"$subject.attribute.value"},
                    "min":{"$min":"$subject.attribute.value"}   
             }}
    
    # Array data and pivot weeks
    group3 = {"$group":{"_id":{"GBE_Id":"$_id.GBE_Id",
                    "name":"$_id.name",
                    "school":"$_id.school",           
                    "plot":"$_id.plot",
                    "attribute":"$subject.attribute.name"},
                   "items":{"$addToSet":{
                   "attribute":"$_id.attribute",
                   "value":{"max":"$max",
                            "avg":"$avg",
                            "min":"$min",
                            "timestamp":"$timestamp"}
                   }}}}
    
    group4 = {"$group":{"_id":{"GBE_Id":"$subject.GBE_Id",
                    "name":"$subject.type",
                    "school":"$location.farm.name",            
                    "plot":"$location.plot",
                    "attribute":"$subject.attribute.name"},
                   "items":{"$addToSet":{
                   "attribute":"$subject.attribute.name",
                   "value":"$subject.attribute.value",
                   "timestamp":"$time.timestamp"
                   }}}}       
    
    # Pivot the weeks together
    project = {"$project":
        {"data":{"$arrayToObject":{
            "$zip":{"inputs":["$items.attribute", "$items.value"]}
            }}}}
    
    project2 = {"$project":
        {"data":{"$arrayToObject":{
            "$zip":{"inputs":["$subject.attribute.name", "$subject.attribute.value"]}
            }}}}       
    
    #q = [match]
    #q = [match, group]
    #q = [match, group, group3]
    q = [match, group, group3, project]
    #q = [match, group4]
    #q = [match, group4, project]
    #q = [match, project2]
    
    mu = MongoUtil()
    recs = mu.aggregate(DB, COLLECTION, q)
    #dump(recs)
    #return

    gbe_id = []
    name = []
    plot = []
    days_to_germination = []
    germinated = []
    for rec in recs:
        gbe_id.append(rec["_id"]["GBE_Id"])
        name.append(rec["_id"]["name"])
        plot.append(rec["_id"]["plot"])
        days_to_germination.append((rec["data"]["Germination"]["timestamp"]-rec["data"]["Planting"]["timestamp"])/86400)
        germinated.append(rec["data"]["Planting"]["max"]-rec["data"]["Germination"]["max"])
    data = {GBE_ID:gbe_id, "name":name, "days_to_germination":days_to_germination}
    title = "Days to Germination"
    #return
    return express_box(data, title, GBE_ID, "days_to_germination")
    
def box_test(attribute, week):
    # test of box chart

    group_name = "GBE_Id"
    if week not in [2, 3, 4]:
        week = 2
    x_axis_name = "week"
    y_axis_name = attribute
    title = "Attribute by GBE_Id: " + attribute + " week: " + str(week)
    print("Box Test", title)
    match = {"$match":{
           "status.status_qualifier":SUCCESS,
           "subject.attribute.name": attribute,
           "subject.attribute.value":{"$ne":0}           
            }}
    
    #Group by GBE_Id and week, get avg, min, max
    # Name is not unique, so cannot put in id
    group = {"$group":{"_id":{"GBE_Id":"$subject.GBE_Id",
                   "name":"$subject.type",
                   "week":{"$toString":"$time.week"}},
                    "value":{"$first":"$subject.attribute.value"},
                       }
                   }
    # Array data and pivot weeks
    # Stick unique name back in id
    group3 = {"$group":{"_id":{"GBE_Id":"$_id.GBE_Id", "name":"$name"},
                   "items":{"$addToSet":{
                   "week":"$week",
                   "value":"$value"}
                   }}}    
    
    # Pivot the weeks together
    project = {"$project":
        {"data":{"$arrayToObject":{
            "$zip":{"inputs":["$items.week", "$items.value"]}
            }}}}
    
    
    q = [match]
    #q = [match, group]
    #q = [match, group, add]
    #q = [match, group, add, remove]
    #q = [match, group, add, remove, group3]
    #q = [match, group, add, remove, group3, project]
    
    # run the query
    mu = MongoUtil()
    recs = mu.aggregate(DB, COLLECTION, q)
    #dump(recs)
    #return
    # extract data for plotting as dataframe
    gbe_id = []
    name = []
    value = []
    for doc in recs:
        #print(doc)
        #return
        gbe_id.append("GBE"+str(doc["subject"]["GBE_Id"]))
        name.append(doc["subject"]["type"])
        value.append(doc["subject"]["attribute"]["value"])
    data = {GBE_ID:gbe_id, "name":name, attribute:value}
    #return
    return express_box(data, title, GBE_ID, attribute)
   
    

def grouped_bar_test():
    # value change over week
    y_title = "height"
    x_title = "week"
    color = "week"
    name = "name"
    plant = "plant"
        # extract data for plotting as dataframe
    i = [] # identifier
    v = [] # value
    y = [] # y axis
    data = {"plant":["G1", "G1", "G1", "G2", "G2", "G2"], y_title:[10, 15, 20, 15, 20, 25], x_title:[1,2,3, 1, 2, 3], name:["Crispy","Crispy","Crispy","Red","Red","Red"] }
    #for rec in recs:
    #    print(rec)
    #    i.append(rec["_id"]["farm"])
    #    v.append(rec["_id"][x_name])
    #    y.append(rec["attributes"]["Irrigation"])
        
    data = pd.DataFrame.from_dict(data)
    print(data) 
    p = Plot()
               #data, title, x_title, y_title, color, hover     
    p.group_bar(data, "Height over Week", plant, y_title, color, name)
    
def histogram(attribute, title="None", reduce=1):
    #RANGE = {TEMPERATURE:100, HUMIDITY:100, AMBIENT_TEMP:100}
    #range = RANGE[attribute]
    range = 100
    hist = [0] * (range + 1)
    #print(hist)
        
    mu = MongoUtil()
    match = {"$match":{
           "status.status_qualifier":SUCCESS,
           "subject.attribute.name":attribute
         }}
    
    group = {"$group":{"_id":None,
                "bucket":{"$first":{"$round":["$subject.attribute.value"]}},
                "value":{"$count":"$subject.attribute.value"},
                   }}
    sort = {"$sort":{"$subject.attribute.value":1}}  
    
    q = [match]
    recs = mu.aggregate(DB, COLLECTION, q)    
    for doc in recs:
        #pprint(doc)
        val = doc[SUBJECT][ATTRIBUTE][VALUE]
        val = int(round((val/reduce), 0))
        #print("Val", val)
        hist[val] += 1
    print(hist)
    p = Plot()
    return p.chart_list(hist, title)

def scatter(var1, var2, title):
    print("Two test", var1, var2)
    group_name = GBE_ID

    match = {"$match":{
        "status.status_qualifier":SUCCESS,
        "subject.attribute.name":{"$in":[var1, var2]}
        }}    
    if var2 == "edible_mass":
        match = {"$match":{
            "status.status_qualifier":SUCCESS,
            "time.week":4,
            "subject.attribute.name":{"$in":[var1, var2]}
        }}

   
    # Array data and pivot weeks
    
    group2 = {"$group":{"_id":{"GBE_Id":"$subject.GBE_Id",
                    "name":"$subject.type",
                    "school":"$location.farm",           
                    "plot":"$location.plot",
                    "week":"$time.week",
                    #"attribute":"$subject.attribute.name"
                    },
                   "items":{"$addToSet":{
                   "attribute":"$subject.attribute.name",
                   "value":"$subject.attribute.value"}
                   }}}        

    
    # Pivot the weeks together
    project = {"$project":
        {"attributes":{"$arrayToObject":{
            "$zip":{"inputs":["$items.attribute", "$items.value"]}
            }}}}
    
    #q = [match]
    #q = [match, group2]
    q = [match, group2, project]    
    mu = MongoUtil()
    recs = mu.aggregate(DB, COLLECTION, q)
    gbe_id = []
    val1 = []
    val2 = []
    hover = []
    data = {var1:val1, var2:val2, "GBE_Id":gbe_id, "text":hover}        
    for doc in recs:
        #pprint(doc)
        #continue


        if var1 in doc["attributes"] and var2 in doc["attributes"]:
            gbe_id.append(doc["_id"]["GBE_Id"])
            val1.append(doc["attributes"][var1])
            val2.append(doc["attributes"][var2])
            hover.append(doc["_id"])
            #print(data)
    #print(data)
    #return None
    return two_variable_scatter(data, var2, var1, "GBE_Id", "text", title)

def environmental(env_var, attr, title):
    print("Environmental", env_var, attr)
    group_name = GBE_ID

    match = {"$match":{
        "status.status_qualifier":SUCCESS,
        "subject.attribute.name":attr
        }}    
    if attr == "edible_mass":
        match = {"$match":{
            "status.status_qualifier":SUCCESS,
            "time.week":4,
            "subject.attribute.name":attr
        }}

    #join to get environmental data
    join = {
      "$lookup": {
         "from": "2020",
         "let": { "school":"$location.farm",
                "timestamp": "$time.timestamp" },
         "pipeline": [ {
            "$match": {
               "$expr": {
                  "$and": [
                     { "$eq": [ "$$school", "$location.farm" ] },
                     { "$eq": [ "$$timestamp", "$time.timestamp" ] },
                     { "$eq": [ "$activity_type","Environment_Observation"]},
                     { "$eq": [ "$subject.attribute.name",env_var]}
                  ]
               }
            }
         } ],
         "as": "env"
      }}
    
    
        
    # Array data and pivot weeks
    
    group2 = {"$group":{"_id":{"GBE_Id":"$subject.GBE_Id",
                    "name":"$subject.type",
                    "school":"$location.farm",           
                    "plot":"$location.plot",
                    "week":"$time.week",
                    #"attribute":"$subject.attribute.name"
                    },
                   "items":{"$addToSet":{
                   "attribute":"$subject.attribute.name",
                   "value":"$subject.attribute.value"}
                   }}}        

    
    # Pivot the weeks together
    project = {"$project":
        {"attributes":{"$arrayToObject":{
            "$zip":{"inputs":["$items.attribute", "$items.value"]}
            }}}}
    
    #q = [match]
    q = [match, join]
    #q = [match, group2, project]    
    mu = MongoUtil()
    recs = mu.aggregate(DB, COLLECTION, q)
    #for doc in recs:
    #    print(doc)
    #return
    gbe_id = []
    env_val = []
    attr_val = []
    hover = []
    data = {env_var:env_val, attr:attr_val, "GBE_Id":gbe_id, "text":hover}        
    for doc in recs:
        #pprint(doc)
        #continue


        #if var1 in doc["attributes"] and var2 in doc["attributes"]:
        gbe_id.append(doc["subject"]["GBE_Id"])
        attr_val.append(doc["subject"]["attribute"]["value"])
        env_val.append(doc["env"][0]["subject"]["attribute"]["value"])
        hover.append(str(doc["subject"]["GBE_Id"]) + "-" + str(doc["subject"]["type"]) + ": " + str(doc["location"]))
            #print(data)
    #print(data)
    #return None
    return two_variable_scatter(data, env_var, attr, "GBE_Id", "text", title)
    

def dump(cursor):
    #print("Len", len(cursor))
    print("Print Recs")
    for rec in cursor:
        pprint(rec)
    

if __name__=="__main__":
    #grouped_bar_test()
    #fig = growth_rate_chart("Height Change", HEIGHT)
    #fig = histogram(TEMPERATURE, "Histogram of Temperature")
    #school_by_week(HEIGHT, 'Our Lady of Lourdes Academy')
    fig = school_by_week(HEIGHT, 'Academir Charter School West')
    #fig = school_by_week(HEIGHT, 'Florida Christian School MS')
    #fig = germination_rate()
    #fig = box_test(HEIGHT, 2)
    #fig = box_test(EDIBLE_MASS, 4)
    #get_distinct("location.farm.name")
    
    #get_distinct("subject.attribute.name")
    #get_distinct("subject.type")
    #find({"subject.GBE_Id":'152'})
    #find({"subject.attribute.name":"Irrigation"})
    #find({"status.status_qualifier":'Success', "subject.attribute.value":0})    
    #find({"status.status_reason":"Inval#id Data", "subject.attribute.value":{"$not":{"$eq":""}}})
    #fig = scatter("height", "edible_mass", "Relation height to mass")
    #fig = scatter("Irrigation", "edible_mass", "Relation height to mass")
    #fig = environmental("temp", "edible_mass", "Environmental Variable and attribute")
    show(fig)
    print("Finished")