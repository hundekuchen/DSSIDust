import tkinter as tk
from tkinter import ttk

from aqiCalc import AQICalc
from FDSHandler import FDSHandler

import datetime

class FdsGui:
    def __init__(self):
        self.root = tk.Tk()
        
        #helper class for aqi calc (including dssi specific points (kindergarten etc.)
        self.aqih =AQICalc("fromTkinterChildrenTesting")
        #helper class for fds handling
        self.fdsh =FDSHandler('/usr/lib/chromium-browser/chromedriver', 'http://dssifds.iptime.org:8080/', 30)
        #self.fdsh.chromedriver_path='C:/Users/kontr/AppData/Local/Programs/Python/Python37-32/chromedriver'
        #self.fdsh.wait = 30
        #self.fdsh.fds_url='http://dssifds.iptime.org:8080/'

        
        #GUI Layout and Initialization
        self.root.title('Air Quality DSSI')
        self.root.geometry("1024x600")
        self.label_names = ['AQI', 'pm25', 'pm10', 'Kindergarten', 'Grundschule','Sekundarstufe', 'Letzte Messung']
        self.label_data = ['init']*len(self.label_names)
        self.label_list_a=[]
        self.label_list_b=[]
        text_size_a = [20]*len(self.label_names)
        text_size_b = [60]+[20]*(len(self.label_names)-1)
        height_list = [3,1,1,4,4,4,1]


        r=0
        for x in self.label_names:
            self.label_list_a.append(tk.Label(self.root, height = height_list[r], width=15, text = x,  font=("Courier", text_size_a[r])))
            self.label_list_b.append(tk.Label(self.root,wraplength = 770, justify = tk.CENTER, text = self.label_data[r], font=("Courier", text_size_b[r])))
            self.label_list_a[r].grid(column=0, row=2*r)
            self.label_list_b[r].grid(column=2, row=2*r)
            ttk.Separator(self.root, orient=tk.HORIZONTAL).grid(row=2*r+1, columnspan=10, sticky=(tk.W,tk.E))
            r=r+1
        ttk.Separator(self.root, orient=tk.VERTICAL).grid(column=1, row=0, rowspan=15, sticky='ns')
        
        #start the recursive clock function
        self.clock()
        
        self.root.attributes("-fullscreen",True)
        self.root.mainloop()

            
    def refresh_fds(self):
        dust_list = self.fdsh.get_dust_list()
        #dust_list=['17','430', 'dadfasfas time'] #FOR TESTING
        print("dust List = ", dust_list)
        if dust_list is not None and dust_list!="error":
            aqi_list = self.aqih.get_aqi_list(dust_list)
            aqi = aqi_list[0]
            last_measure_time = datetime.datetime.now()
            r=0
            for x in aqi_list:
                self.label_list_b[r].config(text = x)
                r=r+1
            self.label_list_b[0].config(background = self.aqih.aqi_color)
            self.label_list_b[3].config(background = self.aqih.kg_color)
            self.label_list_b[4].config(background = self.aqih.gs_color)
            self.label_list_b[5].config(background = self.aqih.ss_color)
            

    def clock(self):
        self.refresh_fds()
        self.root.after(2000,self.clock)
        
fds_gui = FdsGui()