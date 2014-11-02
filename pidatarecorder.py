#!/usr/bin/python
'''
Temp/Humidity Monitor - written by Joshua Hughes, 10/20/14

Must be run as root.
Records temperature and percent humidity from Adafruit DHT11/22 or AM2302 sensors once per minute
Calculates absolute humidity and dumps data into a database

Create an sqlite3 database and setup table with something like:
create table data(temp INTEGER, relhum INTEGER, abshum INTEGER, stamp DATETIME default CURRENT_TIMESTAMP);
'''

import time, datetime, sys, logging, Adafruit_DHT, math
import sqlite3 as sql

#Type of Adafruit sensor:
#DHT11 = 11
#DHT22 = 22
#AM2302 = 22
sensor = 22
pin = 18
db = '/home/pi/recorder.db'
log = '/var/log/temp.log'


#Math Constants for Humidity conversion
c1 = -7.85951783
c2 = 1.84408259
c3 = -11.7866497
c4 = 22.6807411
c5 = -15.9618719
c6 = 1.80122502
c7 = 2.16679
Tc = 647.096 # Critical Temp, K
Pc = 22064000 # Critical Pressure, Pa

#Calculate measured/saturation temp ratio
def v(T, p):
    return math.pow(1 - (273.15 + T) / Tc, p)

#Calculate Water Vapor Saturation Pressure, Pws
def Pws(T):
    return Pc * math.exp( Tc * (c1*v(T,1) + c2*v(T,1.5) + c3*v(T,3) + c4*v(T,3.5) + c5*v(T,4) + c6*v(T,7.5)) / (273.15+T) )

#Calculate Water Vapor Pressure, Pw
def Pw(T,RH):
    return Pws(T) * RH / 100

#Calculate Absolute Humidity
def AbsHum(T,RH):
    return c7 * Pw(T,RH) / (273.15 + T)

def InitLogger():
    global logger
    logger = logging.getLogger('Temp')
    hdlr = logging.FileHandler(log)
    hdlr.setFormatter(logging.Formatter('%(message)s'))
    logger.addHandler(hdlr)
    logger.setLevel(logging.WARNING)

if __name__ == "__main__":
    global logger
    InitLogger()
    con = sql.connect(db)
    ts = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    logger.warning('\n'+ts+' - Sensor Startup')
    while True:
	relhum, temperature = Adafruit_DHT.read_retry(sensor,pin)
	abshum = AbsHum(temperature, relhum)
	#convert temp from C to F:
	temperature = temperature * 9 / 5 + 32
	ts = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
	output = ts + ' - Temp={0:0.1f}*F  Relative Humidity={1:0.1f}%  Absolute Humidity={2:0.1f}'.format(temperature, relhum, abshum)
	logger.warning(output)
	print output
	sqlinsert = "INSERT INTO data(temp, relhum, abshum, stamp) VALUES("+"{0:.2f}".format(temperature)+","+"{0:.2f}".format(relhum)+","+"{0:.2f}".format(abshum)+",CURRENT_TIMESTAMP)"
	with con:
	    cur = con.cursor()
	    cur.execute(sqlinsert)
#TODO - add averager instead of sleep?
	time.sleep(60)





