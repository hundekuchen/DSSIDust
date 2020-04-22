from FDSHandler import FDSHandler
from aqiCalc import AQICalc
from SQLiteHandler import SQLiteHandler

from flask import Flask, render_template
import datetime
import sqlite3

#exception handling
import requests
from requests.exceptions import Timeout

#graphing
#import matplotlib.pyplot as plt
#import matplotlib.dates as mdates
#from dateutil import parser
#from matplotlib import style
#style.use('fivethirtyeight')

app = Flask(__name__)
@app.route("/")

    
def getDust():
       sqliteh = SQLiteHandler('fineDustDSSI.sqlite') #helper calss for sql-handling
       aqic = AQICalc("test") #helper class for aqi-handling including DSSI specific points "Konsequenz für pause" etc.
       
       now = datetime.datetime.now()
       timeString = now.strftime("%Y-%m-%d %H:%M")
       dust_data_fromsql=sqliteh.read_sqlite() #returns most current entry from dust database (time,pm25,pm10 )
       dust_data = [str(dust_data_fromsql[0]),str(dust_data_fromsql[1]),str(dust_data_fromsql[2])]
       
       #FOR TESTING
       #dust_data = ['100',str(dust_data_fromsql[1]),str(dust_data_fromsql[2])]
       
       aqi_list = aqic.get_aqi_list(dust_data)
       templateData = {
          'title' : 'Dust DSSI',
          'time' : dust_data[2],
          'pm25' : aqi_list[1],
          'pm10' : aqi_list[2],
          'AQI' : aqi_list[0],
          'AQIColor' : aqic.aqi_color,
          'KindergartenText' : aqi_list[3],
          'GrundschuleText' : aqi_list[4],
          'SekundarstufeText' : aqi_list[5],
          'kg_color' : aqic.kg_color,
          'gs_color' : aqic.gs_color,
          'ss_color' : aqic.ss_color
          }
        #  'pm25': pm25str
       return render_template('index.html', **templateData)
    
if __name__ == "__main__":
   app.run(host='0.0.0.0', port=8080, debug=True)
