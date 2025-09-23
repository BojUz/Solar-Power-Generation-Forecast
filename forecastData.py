
def get_values(dateString):

    import random
    import cv2 
    import numpy as np 
    import csv
    import datetime
    import math
    import time
    import os
    import cloudPicture

    #dateString = "2025-07-23"
    time_slots = ["06:00", "09:00", "12:00", "15:00", "18:00"]
    time_stamps = ["06", "09", "12", "15", "18"]
    values = {slot: range(1, 6) for slot in time_slots}
    for slots in time_stamps:
        date = datetime.datetime.strptime(f"{dateString} {slots}", "%Y-%m-%d %H")

        dateDiff = date - datetime.datetime(2024,6,23,6)
        print(dateDiff)
        print(type(dateDiff))
        ##################
        #x = 0.70
        ##################
        amortizacion = 0.95
        if(date.hour==6):
            radiationH = 2.7228 - 2.4
            
        elif(date.hour==9):
            radiationH = 56.5628 - 1
            
        elif(date.hour==12):
            radiationH = 99.9001 - 10
            
        elif(date.hour==15):
            radiationH = 70.2411 + 11
            
        elif(date.hour==18):
            radiationH = 8.8485 + 17
            
        else:
            print("ERRRRRRRRRRRRRRRRORRRR no such hour")
        dateStr = date.strftime('%d%m%Y_%H')
        for k in range(0,21):
           
            if(os.path.isfile('static/images/result_'+dateStr+'.png')):
                
                break
            elif(k==1):
                cloudPicture.getCloudPicture(dateString, slots)
            if (k==20):
                print("ERROR no file found")
                return "ERROR no file found"
            time.sleep(1)
                #return "Error"
        img = cv2.imread('static/images/result_'+dateStr+'.png')              
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        avg = np.mean(hsv[:,:, 2])
        per = (avg/255)*100
        # фиктивни данни за деня
        
        installPower=3565+dateDiff.days*1.5
        nagodeno =round(installPower*(per/11.972050911592707)*amortizacion*radiationH/100)
        if(nagodeno==0):
            print("Nagodeno e 0 prichini: ",per, radiationH, installPower*(per/11.972050911592707)*amortizacion*radiationH/100)
        M = installPower*0.95
        e = 2.711828
        a = 0.0009
        if nagodeno > M*0.67:
            nagodeno = M*(1 - math.pow(e, 1-a*nagodeno))
            if nagodeno < M*0.67: nagodeno = M*0.67

        values[str(slots+":00")] = round(nagodeno)

    print(values)

    return values