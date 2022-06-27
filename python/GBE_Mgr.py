'''
Called by Flask app
Coordinates:
  Getting data (GBE_Query)
  Formatting Charting (GBE_Chart)
  Build Chart (Plotly_Chart)
Author: Howard Webb
Date: 2/3/2022
'''
from GBE_Data import *
from Ploty_Chart import *

def gbe_trial(school, trial):
    data = get_trial(school, trial)
    return data

def humidity_chart(school, trial, timestamp):
    print("Humidity Data")
    data = env_data(HUMIDITY, timestamp)
    #return data
    print(data)
    #return data
    title = "Humidity Chart"
    ht = {
      TIME: True,
      HUMIDITY:True,
      }

    fmt = {TITLE:title,
            COLOR: None,
            X_COL:TIME,
            Y_COL:HUMIDITY,
            HOVER_DATA:ht,
            ERROR_PLUS:None,
            ERROR_MINUS:None,
            TEMPLATE:None}
    return line_chart(data, fmt)    

def temp_chart(school, trial, timestamp):
    print("Humidity Data")
    data = env_data(TEMPERATURE, timestamp)
    #return data
    print(data)
    #return data
    title = "Temperature Chart"
    ht = {
      TIME: True,
      TEMPERATURE:True,
      }

    fmt = {TITLE:title,
            COLOR: None,
            X_COL:TIME,
            Y_COL:TEMPERATURE,
            HOVER_DATA:ht,
            ERROR_PLUS:None,
            ERROR_MINUS:None,
            TEMPLATE:None}
    return line_chart(data, fmt)    

def env_chart(attribute, school, start_time, end_time):
    beginning = 6000000000000
    print(attribute, " Data", "Start: ", start_time, "End:", end_time)
    data = env_data(attribute, start_time, end_time)
    print(data)
    #return data
    title = attribute + " Chart"
    ht = {
      TIME: True,
      attribute:True,
      }
    fmt = {TITLE:title,
            COLOR: None,
            X_COL:TIME,
            Y_COL:attribute,
            HOVER_DATA:ht,
            ERROR_PLUS:None,
            ERROR_MINUS:None,
            TEMPLATE:None}
    
    return line_chart(data, fmt)
    
def dew_point_chart(school, start_time, end_time):
    beginning = 6000000000000
    print(" Data", "Start: ", start_time, "End:", end_time)
    data = dew_point_data(start_time, end_time)
    print(data)
    #return data
    title = "Dew Point Chart"
    ht = {
      TIME: True,
      "attribute":True,
      "value": True
      }
    

    fmt = {TITLE:title,
            COLOR: "attribute",
            X_COL:TIME,
            Y_COL:"value",
            HOVER_DATA:ht,
            ERROR_PLUS:None,
            ERROR_MINUS:None,
            TEMPLATE:None}
    return line_chart(data, fmt)    

if __name__ == "__main__":
    #humidity_chart("OpenAgBloom", "GBE_T1", 0).show()
    #fig = temp_chart("OpenAgBloom", "GBE_T1", 1626177603787)
    #co2_chart("OpenAgBloom", 0, datetime.now().timestamp()).show()
    #data = gbe_trial("OpenAgBloom", "GBE_T1")
    dew_point_chart("OpenAgBloom", 0, datetime.now().timestamp()*1000).show()
    pass