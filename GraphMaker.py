from FDSHandler import FDSHandler
from aqiCalc import AQICalc
from SQLiteHandler import SQLiteHandler

from flask import Flask, render_template
import datetime
import sqlite3
import time

#for loggin with flask running
import sys

#exception handling
import requests
from requests.exceptions import Timeout

#The way Graphs are handled is shit. It would be nice, to link 
#the sql-data with the position of the graph, instead of suggesting
#that the graph is 7(or dirty approximated: 6.8)  days long from left to right.

class GraphMaker:
    
    def __init__(self):
        self.html_to_graph = ""

    def generate_canvas_html(self, x_size,y_size, dust_data):
        aqih = AQICalc('hello')
        n = len(dust_data[0])
        print('n = ', n)
        pm25 = dust_data[0]
        pm10 = dust_data[1]
        dates = dust_data[2]
        aqi = []
        for i in range(n):
            dust_list = [dust_data[0][i],dust_data[1][i],dust_data[2][i]]
            #print('aqi = ', aqih.get_aqi_list(dust_list)[0])
            aqi.append(aqih.get_aqi_list(dust_list)[0])
        #max_aqi = max(aqi)
        #print('max_aqi = ', max_aqi)
        step = 0.0
        if(n is not 0):
            step = float(x_size-25)/float(n)
        print('n = ', n, '   step  = ', step, file=sys.stderr)
        
        html_string = ''
        
        #preamble
        html_string = html_string + '<canvas id="myCanvas" width="'
        html_string = html_string + str(x_size)
        html_string = html_string + '" height="' + str(y_size) +  '''style="border:1px solid #d3d3d3;">
Your browser does not support the HTML5 canvas tag.</canvas>
<script>
var c = document.getElementById("myCanvas");
var ctx = c.getContext("2d");
'''
        #create graph
        for i in range(n-1):
            html_string = html_string + 'ctx.moveTo(' + str(round(i*step)+20) + ',' + str(y_size - aqi[i]-10) + ');'
            html_string = html_string + '\n'
            html_string = html_string + 'ctx.lineTo(' + str(round((i+1)*step)+20) + ',' + str(y_size - aqi[i+1]-10) + ');'
            html_string = html_string + '\n'
        #print(html_string)
        
        #create grid
        html_string = html_string + 'ctx.moveTo(' + str(x_size - 5) + ',' + str(y_size-10) + ');'
        html_string = html_string + '\n'
        html_string = html_string + 'ctx.lineTo(' + str(20) + ',' + str(y_size-10)+ ');'
        html_string = html_string + '\n'
        
        html_string = html_string + 'ctx.moveTo(' + str(20) + ',' + str(y_size-10) + ');'
        html_string = html_string + '\n'
        html_string = html_string + 'ctx.lineTo(' + str(20) + ',' + str(5)+ ');'
        html_string = html_string + '\n'
        
        
        #testline for whole screen
        #html_string = html_string + 'ctx.moveTo(' + str(0) + ',' + str(0) + ');'
        #html_string = html_string + '\n'
        #html_string = html_string + 'ctx.lineTo(' + str(x_size) + ',' + str(y_size)+ ');'
        #html_string = html_string + '\n'
        
        #parallel to x-axis
        for i in range(5):
            #ys=(round(float(y_size)/6))
            ys=i*50
            html_string = html_string + 'ctx.fillText(' + str(ys) + ','+ str(0)+ ',' + str(y_size - ys-10)+ ');'
            html_string = html_string + 'ctx.moveTo(' + str(20) + ',' + str(ys-10) + ');'
            html_string = html_string + '\n'
            html_string = html_string + 'ctx.lineTo(' + str(x_size-5) + ',' + str(ys-10)+ ');'
            html_string = html_string + '\n'
        
        #parallel to y-axis
        #TODO: offset, so each day start at 0:00:00
        now = datetime.datetime.now()
        #seconds since midnight
        ssm = (now- now.replace(hour=0,minute=0,second=0, microsecond=0)).total_seconds()
        s=float(ssm)/86400.0
        
        for i in range(7):
            xd=(round(float(x_size-30)/7))
            j=5-i
            day = datetime.datetime.now()-datetime.timedelta(days=j+1)
            
            html_string = html_string + 'ctx.fillText(' 
            html_string = html_string + ''' ' ''' + day.strftime("%b %d") + ''' ' ''' +  ','+ str(x_size - round(xd*(j+1)+15+s*xd))+ ',' + str(round(y_size ))+ ');'
            html_string = html_string + '\n'
            html_string = html_string + 'ctx.moveTo(' + str(x_size-round(xd*(j+1)+5 +s*xd)) + ',' + str(-10) + ');'
            html_string = html_string + '\n'
            html_string = html_string + 'ctx.lineTo(' + str(x_size-round(xd*(j+1)+5+s*xd)) + ',' + str(y_size-10)+ ');'
            html_string = html_string + '\n'
            
        
                
        #postamble
        html_string = html_string + '''ctx.stroke();
</script>'''
        
        self.html_to_graph = html_string
        #print(self.html_to_graph, file=sys.stderr)


    def make_graph(self):
        #print(datetime.datetime.now())
        dts = datetime.datetime.now()
        sqlh = SQLiteHandler('./fineDustDSSI.sqlite')
        dust =  sqlh.read_sqlite_before('-6.8 days')
        self.generate_canvas_html(400, 250, dust)
        print("hallo",file=sys.stderr)
        html_out =  self.html_to_graph
        return html_out
        #diff = datetime.datetime.now()- dts
        #print(diff)

        



