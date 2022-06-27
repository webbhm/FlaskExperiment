# Author: Howard Webb
# Data: 7/25/2017
# Get temperature and send out as mqtt messge
# For production, pingMQTT should be broken out as a separate utility file from the data gathering.

from BME280 import BME280
from GPSTest import Location
import paho.mqtt.client as mqtt
from datetime import datetime
from time import sleep

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+mqtt.connack_string(rc))
    pass

def on_publish(client, userdata, mid):
    print( "Published", userdata, " ", mid)

def on_disconnect(client, userdata, rc):
    print( "Disconnected: ", userdata, " Result: ", mqtt.connack_string(rc))

def pingMQTT(name, msg, test=False):
    host="mqtt.eclipse.org"
    #host="test.mosquitto.org"
    port=1883
    keepalive=60
    client = mqtt.Client()
    print( "Client: ", type(client))
    client.on_connect = on_connect
    client.on_publish=on_publish
    client.on_disconnect=on_disconnect
    q=client.connect(host=host, port=port, keepalive=keepalive)        
    print( "Connection: host, port, keepalive ", host, port, keepalive)
    topic='OpenAgBloom/' + name 
    result,mid=client.publish(topic, msg)
    client.disconnect()
    if test:
        print( "Topic: ", topic, " Msg: ", msg)
        print( "Result: ", mqtt.connack_string(result), "Msg Id: ", mid)

def msgBME(test=False):
    bme = BME280()
    msg = {}    
    timestamp = datetime.utcnow()
    ts_str = timestamp.isoformat()[:19]    
    msg['timestamp'] = ts_str
    temperature,pressure,humidity = bme.getData()    
    msg['temp'] = temperature
    msg['pressure'] = pressure
    msg['humidity'] = humidity
    pingMQTT('Air/BME', str(msg), test)
    return msg

def msgGPS(test=False):
    gps = Location()
    msg = gps.getLoc()
    pingMQTT('GPS/Loc', str(msg), test)
    return msg

def test():
    print( "Send Temp")
    msg=msgBME(True)
    print( "Temp: ", msg)

def test2():
    print( "Test Connection")
    msg="TEST"
    pingMQTT('Test', msg, True)
    
def main():
    msg = msgBME()
    msg = msgGPS()
    
if __name__=="__main__":
    main()
