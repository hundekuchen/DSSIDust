import urllib.request
import urllib
import re
import os
import network
import time
import subprocess
import sqlite3
import datetime

#graphing
#import matplotlib.pyplot as plt
#import matplotlib.dates as mdates
from dateutil import parser
#from matplotlib import style
#style.use('fivethirtyeight')


class SQLiteHandler:
    def __init__(self, path_to_sql_file):
        self.sqlite_file = path_to_sql_file

    def read_sqlite(self):
        #sqlite_file = 'fineDustDSSI.sqlite'
        # Connecting to the database file
        conn = sqlite3.connect(self.sqlite_file)
        c = conn.cursor()
        #c.execute("""SELECT * FROM airquality""")
        #all_rows = c.fetchall()
        #print('1):', all_rows)
        c.execute("""SELECT pm25, pm10, time FROM airquality ORDER BY datetime(time) DESC LIMIT 1;""")
        data = c.fetchall()
        print(data)
        dates = []
        valuespm25 = []
        valuespm10 = []
        if len(data)>0:
            for row in data:
                valuespm25.append(row[0])
                valuespm10.append(row[1])
                dates.append(parser.parse(row[2]))
        conn.commit()
        conn.close()
        last = len(dates)-1;
        dust_data=[valuespm25[last],valuespm10[last],dates[last]]
        return dust_data
    
    
    def read_sqlite_before(self, time_diff):
        #sqlite_file = 'fineDustDSSI.sqlite'
        # Connecting to the database file
        conn = sqlite3.connect(self.sqlite_file)
        c = conn.cursor()
        #c.execute("""SELECT * FROM airquality""")
        #all_rows = c.fetchall()
        #print('1):', all_rows)
        c.execute("""SELECT pm25, pm10, time FROM airquality WHERE time > datetime('now', ?);""", (time_diff,))
        data = c.fetchall()
        dates = []
        valuespm25 = []
        valuespm10 = []
        if len(data)>0:
            for row in data:
                valuespm25.append(row[0])
                valuespm10.append(row[1])
                dates.append(parser.parse(row[2]))
        conn.commit()
        conn.close()
        dust_data = [valuespm25, valuespm10, dates]
        #print(dust_data)
        return dust_data
    
    #dustD
    def write_sqlite(self,dust_data):
        if dust_data is not None and dust_data is not "error":
            # Connecting to the database file
            conn = sqlite3.connect(self.sqlite_file)
            c = conn.cursor()
            c.execute("""CREATE TABLE IF NOT EXISTS airquality (
                pm25 INTEGER NOT NULL,
                pm10 INTEGER NOT NULL,
                time TEXT NOT NULL UNIQUE)""")
            c.execute("""INSERT INTO airquality (pm25,pm10,time)
                VALUES(?,?,?);""", (dust_data[0],dust_data[1], dust_data[2]))
            conn.commit()
            conn.close()