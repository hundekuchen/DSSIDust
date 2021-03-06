class AQICalc:
    
    dust_list = [50,50,'time'] #pm25,pm10,measure_time
    #pm25_is_worse = True   #in most cases pm25 is worse than pm10 aqi-wise.
    s_bg = '#ffffcc' # 'Standard_BackGround'
    kg_color=s_bg
    gs_color=s_bg
    ss_color=s_bg
    aqi_color=s_bg
    dust_alarm_color = 'red'
    
    pm25_breakpoints = [0,12,35.4,55.4,150.4,250.4,350.4,500]
    pm25_aqi=[0,50,100,150,200,300,400,500]
    
    pm10_breakpoints = [0,54,154,254,354,424,504,604,99999]
    pm10_aqi =[0,50,100,150,200,300,400,500,999]
    
    aqi_color_breakpoints = [0,50,100,150,200,300,500]
    aqi_color_text = ['green', 'yellow', 'orange', 'red', 'purple', 'brown']
    
    aqi_kg_breakpoints = [0,101, 125, 500]
    kg_text = ['Keine Konsequenzen','Keine Ausflüge mehr (Seoul Forest, Tipiwald); nur noch Hofpausen draußen','Keine Außenaktivitäten mehr']
    kg_color_l = [s_bg, s_bg, dust_alarm_color]
    
    aqi_gs_breakpoints = [0,125,151,175,500]
    gs_text = ['Keine Konsequenzen', 'Keine Sportliche Aktivität im Freien; Schülerinnen und Schüler halten sich weiterhin in Hofpausen draußen auf. Keine Ausgabe von Sportgeräten an Schülerinnen und Schüler.', 'Keine sportliche Aktivität/ Ausflüge im Freien; Schülerinnen und Schüler halten sich weiterhin in Hofpausen draußen auf. Keine Ausgabe von Sportgeräten an Schülerinnen und Schüler.', 'Keine Außenaktivtät mehr']
    gs_color_l = [s_bg, s_bg, s_bg, dust_alarm_color]
    
    aqi_ss_breakpoints = [0,151,176,500]
    ss_text = ['Keine Konsequenzen', 'Keine sportliche Aktivität/ Ausflüge im Freien; Schülerinnen und Schüler halten sich weiterhin in Hofpausen draußen auf. Keine Ausgabe von Sportgeräten an Schülerinnen und Schüler.', 'Keine Außenaktivtät mehr']
    ss_color_l = [s_bg, s_bg, dust_alarm_color]
    
    def __init__(self, var1):
        self.var1 = var1

    def lin_interpol(self,lb,ub,lba,uba,pm):
        aqi = 0.0
        d=ub-lb
        x=pm-lb
        px=x/d
        aqi=(1-px)*lba+px*uba
        aqi=round(aqi)
        return aqi

    def pm_to_aqi(self, pm_breakpoints, pm_aqi, pm): #works for both pm25 and pm10
        aqi=0
        for r in range(len(pm_breakpoints)-1):
            if(pm<pm_breakpoints[r+1] and pm >=pm_breakpoints[r]):
                aqi = self.lin_interpol(pm_breakpoints[r], pm_breakpoints[r+1],pm_aqi[r],pm_aqi[r+1],pm)
        return aqi
    
    def aqi_to_text(self, breakpoints, text_list, aqi):
        text = 'error'
        for r in range(len(breakpoints)-1):
            if(aqi<breakpoints[r+1] and aqi >=breakpoints[r]):
                text=text_list[r]
        return text
    
    def get_aqi_list(self, mdust_list):
        self.dust_list = mdust_list
        pm25_aqi = self.pm_to_aqi(self.pm25_breakpoints, self.pm25_aqi, int(self.dust_list[0]))
        pm10_aqi = self.pm_to_aqi(self.pm10_breakpoints, self.pm10_aqi, int(self.dust_list[1]))
        aqi = max(pm25_aqi, pm10_aqi)
        self.aqi_color = self.aqi_to_text(self.aqi_color_breakpoints, self.aqi_color_text, aqi)
        
        self.kg_color=self.aqi_to_text(self.aqi_kg_breakpoints,self.kg_color_l, aqi)
        self.gs_color=self.aqi_to_text(self.aqi_gs_breakpoints,self.gs_color_l, aqi)
        self.ss_color=self.aqi_to_text(self.aqi_ss_breakpoints,self.ss_color_l, aqi)
        
        kg_text = self.aqi_to_text(self.aqi_kg_breakpoints,self.kg_text, aqi)
        gs_text = self.aqi_to_text(self.aqi_gs_breakpoints,self.gs_text, aqi)
        ss_text = self.aqi_to_text(self.aqi_ss_breakpoints,self.ss_text, aqi)
        
        aqi_list = [aqi, str(self.dust_list[0])+"μg/m³ (AQI = " + str(pm25_aqi)+ ")", str(self.dust_list[1]) + "μg/m³ (AQI = "+ str(pm10_aqi)+")", kg_text, gs_text, ss_text,'                            '+ str(self.dust_list[2])]
        return aqi_list

#ac = AQICalc("hello")
#print(ac.pm25_breakpoints)
#print(ac.pm25_aqi)
#for x in range(500):
#    print(x, ac.aqi_to_text(ac.aqi_color_breakpoints, ac.aqi_color_text, x),ac.aqi_to_text(ac.aqi_kg_breakpoints, ac.kg_text, x))

    #print(x, "   pm2.5 = ", ac.pm_to_aqi(ac.pm25_breakpoints, ac.pm25_aqi, x))
    #print(x, "   pm10 = ", ac.pm_to_aqi(ac.pm10_breakpoints, ac.pm10_aqi, x))
            
        
        