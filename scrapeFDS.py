from SQLiteHandler import SQLiteHandler
from FDSHandler import FDSHandler
import datetime

#fdsh = FDSHandler('/usr/lib/chromium-browser/chromedriver', 'http://dssifds.iptime.org:8080/', 300)
fdsh = FDSHandler('/usr/bin/chromedriver', 'http://dssifds.iptime.org:8080/', 300)
sqlh = SQLiteHandler('fineDustDSSI.sqlite')

n=0

while(True):
    dust_list = fdsh.get_dust_list()
    sqlh.write_sqlite(dust_list)
    n=n+1
    print("iteration = ",n)



