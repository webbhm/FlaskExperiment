#Log Test MVP sensors to CouchDB
from oneWireTemp import *
from TSL2561 import getLux
from VL53L0X import *
import NDIR
from Ada_CS811 import Adafruit_CCS811
from CouchUtil import saveList

activity_type="Environment_Observation"

def getAirAmbientTempObsv(test=False):
    '''Create json structure for temp'''

    try:
        temp = getTempC(ambientTemp)

        status_qualifier = 'Success'
        if test:
            status_qualifier = 'Test'
        saveList(activity_type, 'Air', 'Ambient', 'Temperature', "{:10.1f}".format(temp), 'DS18B20_1', status_qualifier)                
    except Exception as e:
        status_qualifier = 'Failure'
        if test:
            status_qualifier = 'Test'
        saveList(activity_type, 'Air', 'Ambient', 'Temperature', '', 'DS18B20_1', status_qualifier, comment=str(e))                            
    
def getAirBoxTempObsv(test=False):
    '''Create json structure for temp'''
    try:
        temp = getTempC(boxTemp)

        status_qualifier = 'Success'
        if test:
            status_qualifier = 'Test'
        saveList(activity_type, 'Air', 'Left_Side', 'Temperature', "{:10.1f}".format(temp), 'DS18B20_2', status_qualifier)                
    except Exception as e:
        status_qualifier = 'Failure'
        if test:
            status_qualifier = 'Test'
        saveList(activity_type, 'Air', 'Left_Side', 'Temperature', '', 'DS18B20_2', status_qualifier, comment=str(e))                          
    
def getAirTopTempObsv(test=False):
    '''Create json structure for temp'''
    try:
        temp = getTempC(topTemp)

        status_qualifier = 'Success'
        if test:
            status_qualifier = 'Test'
        saveList(activity_type, 'Air', 'Top', 'Temperature', "{:10.1f}".format(temp), 'DS18B20_3', status_qualifier)                
    except Exception as e:
        status_qualifier = 'Failure'
        if test:
            status_qualifier = 'Test'
        saveList(activity_type, 'Air', 'Top', 'Temperature', '', 'DS18B20_3', status_qualifier, comment=str(e))                          

    
def getNutrientReservoirTempObsv(test=False):
    '''Create json structure for temp'''
    try:
        temp = getTempC(reservoirTemp)

        status_qualifier = 'Success'
        if test:
            status_qualifier = 'Test'
        saveList(activity_type, 'Air', 'Reservoir', 'Temperature', "{:10.1f}".format(temp), 'DS18B20_4', status_qualifier)                
    except Exception as e:
        status_qualifier = 'Failure'
        if test:
            status_qualifier = 'Test'
        saveList(activity_type, 'Air', 'Reservoir', 'Temperature', '', 'DS18B20_4', status_qualifier, comment=str(e))                          
    
def getLightCanopyLUXObsv(test=False):
    '''Create json structure for LUX'''
    try:
        lux = getLux()
        
        status_qualifier = 'Success'
        if test:
            status_qualifier = 'Test'
        saveList(activity_type, 'Light', 'Canopy', 'LUX', '{:3.1f}'.format(lux), 'TSL2561', status_qualifier)                
    except Exception as e:
        status_qualifier = 'Failure'
        if test:
            status_qualifier = 'Test'
        saveList(activity_type, 'Light', 'Canopy', 'LUX', '', 'TSL2561', status_qualifier, comment=str(e))                          
 

def getNutrientReservoirDepthObsv(test=False):
    '''Create json structure for LUX'''
    try:
        temp = getTempC(boxTemp)

        status_qualifier = 'Success'
        if test:
            status_qualifier = 'Test'
        saveList(activity_type, 'Nutrient', 'Reservoir', 'Distance', '{:3.1f}'.format(depth), 'VL53L0X', status_qualifier)                
    except Exception as e:
        status_qualifier = 'Failure'
        if test:
            status_qualifier = 'Test'
        saveList(activity_type, 'Nutrient', 'Reservoir', 'Distance', '', 'VL53L0X', status_qualifier, comment=str(e))                          

def getAirCanopyCO2Obsv(test=False):
    '''Create json structure for LUX'''
    try:
        sensor = NDIR.Sensor()
        sensor.begin()
        co2=sensor.getCO2()

        status_qualifier = 'Success'
        if test:
            status_qualifier = 'Test'
        saveList(activity_type, 'Air', 'Canopy', 'CO2 (ppm)', '{:3.1f}'.format(co2), 'MH-Z16-NDIR', status_qualifier)                
    except Exception as e:
        status_qualifier = 'Failure'
        if test:
            status_qualifier = 'Test'
        saveList(activity_type, 'Air', 'Canopy', 'CO2 (ppm)', '', 'MH-Z16-NDIR', status_qualifier, comment=str(e))                          

def getSecondCO2(test=False):
    '''Create json structure for LUX'''
    try:
        sensor = Adafruit_CCS811()
        co2 = sensor.get_co2()

        status_qualifier = 'Success'
        if test:
            status_qualifier = 'Test'
        saveList(activity_type, 'Air', 'Canopy', 'CO2 (ppm)', '{:3.1f}'.format(co2), 'CCS811', status_qualifier)                
    except Exception as e:
        status_qualifier = 'Failure'
        if test:
            status_qualifier = 'Test'
        saveList(activity_type, 'Air', 'Canopy', 'CO2 (ppm)', '', 'CCS811', status_qualifier, comment=str(e))                          


def makeEnvObsv(test=False):
    '''Log all sensors'''
    getAirAmbientTempObsv(test)
    
    getAirBoxTempObsv(test)

    getAirTopTempObsv(test)

    getNutrientReservoirTempObsv(test)

    getLightCanopyLUXObsv(test)

    getNutrientReservoirDepthObsv(test)

    getAirCanopyCO2Obsv(test)

    getSecondCO2(test)


def test():
    makeEnvObsv(True)

if __name__=="__main__":
    '''Setup for calling from script'''
    makeEnvObsv()
    

       
