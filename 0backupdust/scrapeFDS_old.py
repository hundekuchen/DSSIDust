import urllib.request
import urllib
import re
import os
import network
import time
import subprocess
import sqlite3

#graphing
#import matplotlib.pyplot as plt
#import matplotlib.dates as mdates
from dateutil import parser
#from matplotlib import style
#style.use('fivethirtyeight')

#webscraping
from pathlib import Path
from datetime import datetime
from bs4 import *
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException


def writeSQLite(dustData):
    sqlite_file = 'fineDustDSSI.sqlite'


    # Connecting to the database file
    conn = sqlite3.connect(sqlite_file)
    c = conn.cursor()

    c.execute("""CREATE TABLE IF NOT EXISTS airquality (
                pm25 INTEGER NOT NULL,
                pm10 INTEGER NOT NULL,
                time TEXT NOT NULL UNIQUE)""")

    #c.execute("""DELETE FROM airquality""")

    c.execute("""INSERT INTO airquality (pm25,pm10,time)
                VALUES(?,?,?);""", (dustData[0],dustData[1], dustData[2]))

    #c.execute("""SELECT * FROM airquality""")
    #all_rows = c.fetchall()
    #print('1):', all_rows)
    conn.commit()
    conn.close()

#def createGraph():
    #testing only for pm2.5
#    print("opening database")
 #   sqlite_file = 'fineDustDSSI.sqlite'

    # Connecting to the database file
#    conn = sqlite3.connect(sqlite_file)
#    c = conn.cursor()
 #   print("get data from database")
  #  c.execute("""SELECT time, pm25, pm10 FROM airquality;""")
   # #c.execute("""SELECT time, pm25, pm10 FROM airquality 
    #           ORDER BY time DESC LIMIT 3;""")
    
    #c.execute("""SELECT time, pm25,pm10 FROM airquality 
    #       WHERE "time" >=datetime('now', 'localtime', '-15 minute') 
    #       AND "time" < datetime('now','localtime');""")
    
    #TESTING: AVERAGE for each hour
    #first try: average of last hour
    #c.execute("""SELECT time, avg(pm25),avg(pm10) FROM airquality 
    #       WHERE "time" >=datetime('now', 'localtime', '-1 hour') 
    #       AND "time" < datetime('now','localtime');""")
    
    #data = c.fetchall()
    
    #print("convert data for python and matplotlib")
   # dates = []
   # valuespm25 = []
   # valuespm10 = []
   # if len(data)>0:
   #     for row in data:
    #        dates.append(parser.parse(row[0]))
     #       valuespm25.append(row[1])
      #      valuespm10.append(row[2])
    #else:
     #   print("no data")
 #       
  #  print("Generating plot")    
  #  plt.plot_date(dates,valuespm25,'-')
   # plt.plot_date(dates,valuespm10,'.')
#
#
 #   plt.savefig('dust.png')
  #  plt.close()
   # conn.close()
    
def checkWlan(wlanName):
    #check if correct wlan is used
    mstr = subprocess.check_output("netsh wlan show interface", encoding = 'utf-8', errors='ignore')
    if wlanName in mstr:
        print(wlanName + " is correctly used")
        return True
    else:
        print(wlanName + " is NOT used")
        return False

def readDust():
    # create a new Chrome session
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--incognito')
    options.add_argument('--headless')
    print("creating webdriver with option")
    driver = webdriver.Chrome('/usr/bin/chromedriver',chrome_options=options)
    print("wait implicitly")
    #wait not working?
    driver.implicitly_wait(15)
    driver.set_page_load_timeout(15)
    url = 'http://dssifds.iptime.org:8080/'
    print("load url")
    driver.set_page_load_timeout(5)
    try :
        driver.get(url)
        print("URL successfully Accessed")
        #create the webpage with dynamic content
        print("waiting for fds to write data")
        time.sleep(300)
        print("create webpage source")
        page_source = driver.page_source
    
        #parse the webpage
        print("hand webpage source to beautifulsoup")
        soup = BeautifulSoup(page_source,'html.parser')
        dust="string"
        dust = soup.find(id="dust")
        print(dust)
        print("dusttype is " , type(dust))
        if dust is not None:
            dustText = dust.get_text()
            driver.quit()
            return dustText
        else:
            driver.quit()
            return "error"
    except TimeoutException as e:
        print("Page load Timeout Occured. Quiting !!!")
        return "error"



def formatData(dustRaw):
    #make dustsensor data readable
    dustWithTime = "error"
    if dustRaw!="error" and dustRaw is not None and len(dustRaw)>35:
        dustRaw=dustRaw[13:]
        print(dustRaw)
        dataSplit = dustRaw.split(" ")
        pm25=dataSplit[0].split()[0]
        pm10=dataSplit[3].split()[0]
        pm10=pm10.strip("<b>")
        print ("pm25" , pm25, " pm10 ", pm10)
        now = datetime.now()
        nowString = now.strftime('%Y-%m-%d %H:%M:%S')
        dustWithTime=[pm25 ,pm10 , nowString]
        print(dustWithTime)
        return dustWithTime
    else:
        print("error") #todo tell which error
        return("error")

def writeData(filename, data):
    # Open the file with writing permission
    fn=Path(filename)
    myfile = open(fn, 'a')
    
    for item in data:
        myfile.write(item)
        myfile.write(", ")
    myfile.write("\n")
    #Write a line to the file
    #myfile.write(data)
    #Close the file
    myfile.close()

#change wlan test
n=0
while True:
    #Computer should be connected to the school net beforehand
    #subprocess.call(['netsh', 'wlan','disconnect'])
    #subprocess.call(['netsh', 'wlan','connect', "name=\"FDS_19002\""])
    n+=1
    print("number of iterations: " , n)
    dustRaw=readDust()
    #dustRaw="Dust act: 38 µg/m3(PM2.5),  39 µg/m3(PM10)"
    dustList = formatData(dustRaw)
    if dustList is not None and dustList!="error":
        #writeData("/dustOutput.txt", dustList)
        writeSQLite(dustList)
    #createGraph()
    