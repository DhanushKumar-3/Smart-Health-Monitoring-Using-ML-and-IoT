import os
import urllib.request
import http
import pandas as pd
import re
from time import sleep
from datetime import datetime

import pickle
filename = 'model.sav'
loaded_model = pickle.load(open(filename, 'rb'))

base = "http://192.168.137.226/"

def transfer(my_url):   #use to send and receive data
    try:
        n = urllib.request.urlopen(base + my_url).read()
        n = n.decode("utf-8")
        return n
    except http.client.HTTPException as e:
        return e


# Create an empty list to store data
data_list = []


ct = 0
while True:
    res = transfer(str(ct))
    response = str(res)
    print(response)
    
    # Split the received data
    values = response.split(',')
    print(values)
    if len(values) == 5:
        v1, c1, ch, dh,ah = values
        #save_to_excel(v1, c1, v2, c2)
        reports = [[v1, c1, ch,ah]]
        predicted = loaded_model.predict(reports)
        ty=predicted[0]
        ty=ty.replace(" ", "")
        print(ty)
        conn = urllib.request.urlopen("https://api.thingspeak.com/update?api_key=16I4KHP9BXOUK1I7&field1="+str(v1)+"&field2="+str(c1)+"&field3="+str(ch)+"&field4="+str(dh)+"&field5="+str(ah)+"&field6="+str(ty))        #response = conn.read()
        print ("http status code=%s" % (conn.getcode()))
        print(predicted)
    
    sleep(1)

