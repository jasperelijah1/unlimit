# -*- coding: utf-8 -*-
"""
Created on Sun Apr 14 02:17:59 2019

@author: Suriya Prakash
"""

from __future__ import print_function
import pyzbar.pyzbar as pyzbar
import numpy as np
import cv2
import os
import pyrebase
import paho.mqtt.client as mqtt
import time, threading, ssl, random
from threading import Thread
rack_a=0
rack_b=0
tot=0
# client, user and device details
serverUrl   = "managment.unlimitenablement.co.in"
port        = 1883
clientId    = "my_mqtt_python_client"
device_name = "My Python MQTT device"
tenant      = "team7"
username    = "team7"
password    = "rotronyx"

receivedMessages = []

# display all incoming messages
def on_message(client, userdata, message):
    print("Received operation " + str(message.payload))
    if (message.payload.startswith("510")):
        print("Simulating device restart...")
        publish("s/us", "501,c8y_Restart");
        print("...restarting...")
        time.sleep(1)
        publish("s/us", "503,c8y_Restart");
        print("...done...")

# send temperature measurement
def sendB():
    global rack_b
    try:
        print("Sending rack B occupancy...")
        publish("s/us/M1", "211," + str(rack_b+10))
        #thread = threading.Timer(2, sendB)
        #thread.daemon=True
        #thread.start()
        time.sleep(0.2)
        #return(0)
    except (KeyboardInterrupt, SystemExit):
        print ('Received keyboard interrupt, quitting ...')

def sendA():
    global rack_a
    try:
        print("Sending rack A occupancy...")
        publish("s/us/M2", "211," + str(rack_a))
        #thread = threading.Timer(2, sendA)
        #thread.daemon=True
        #thread.start()
        time.sleep(.25)
        #return(0)
    except (KeyboardInterrupt, SystemExit):
        print ('Received keyboard interrupt, quitting ...')

def sendtot():
    global tot
    try:
        print("Sending warehouse efficiency...")
        publish("s/us/M3", "211," + str(tot))
        #thread = threading.Timer(2, sendtot)
        #thread.daemon=True
        #thread.start()
        #time.sleep(.25)
        #return(0)
    except (KeyboardInterrupt, SystemExit):
        print ('Received keyboard interrupt, quitting ...')
# publish a message
def publish(topic, message, waitForAck = False):
    mid = client.publish(topic, message, 2)[1]
    if (waitForAck):
        while mid not in receivedMessages:
            time.sleep(0.25)

def on_publish(client, userdata, mid):
    receivedMessages.append(mid)

# connect the client to Cumulocity and register a device
client = mqtt.Client(clientId)
client.username_pw_set(tenant + "/" + username, password)
client.on_message = on_message
client.on_publish = on_publish

client.connect(serverUrl, port)
client.loop_start()
publish("s/us", "100," + device_name + ",c8y_MQTTDevice", True)
publish("s/us", "110,S123456789,MQTT test model,Rev0.1")
publish("s/us", "114,c8y_Restart")
print ("Device registered successfully!")

client.subscribe("s/ds")


     
     
  
config = {
  "apiKey": "AIzaSyDKZDZifcM1E9UTw_-iU6CZ1DBKj-YvMqo",
  "authDomain": "mine-53ab0.firebaseapp.com",
  "databaseURL": "https://mine-53ab0.firebaseio.com/",
  "storageBucket": "mine-53ab0.appspot.com",
  "serviceAccount": "serviceAccountCredentials.json"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()


 
# =============================================================================
# import barcode
# EAN = barcode.get_barcode_class('code128')
# from barcode.writer import ImageWriter
# ean = EAN('123456,LG,fridge,H', writer=ImageWriter())
# fullname = ean.save('foo')
# ean = EAN('721768,Xiaomi,TV,M', writer=ImageWriter())
# fullname = ean.save('foo1')
# 
# ean = EAN('816274,Samsung,AC,H', writer=ImageWriter())
# fullname = ean.save('foo2')
# =============================================================================
 
def decode(im) : 
 
  decodedObjects = pyzbar.decode(im)
 
  
  for obj in decodedObjects:
    #print('Type : ', obj.type)
    #print('Data : ', str(obj.data)[2:-1],'\n')
    var = str(obj.data)[2:-1] 
  return decodedObjects,var
 
 
# Display barcode and QR code location  
def display(im, decodedObjects):
 
  # Loop over all decoded objects
  for decodedObject in decodedObjects: 
    points = decodedObject.polygon
 
    # If the points do not form a quad, find convex hull
    if len(points) > 4 : 
      hull = cv2.convexHull(np.array([point for point in points], dtype=np.float32))
      hull = list(map(tuple, np.squeeze(hull)))
    else : 
      hull = points;
     
    # Number of points in the convex hull
    n = len(hull)
 
    # Draw the convext hull
    for j in range(0,n):
      cv2.line(im, hull[j], hull[ (j+1) % n], (255,0,0), 3)
 
  # Display results 
  cv2.imshow("Results", im);
  cv2.waitKey(3000);
  cv2.destroyAllWindows()
   
def load():
    user = db.child("workers").get()
    global rack_a
    global rack_b
    global tot
    free_workers=[i for i in user.val()]
    count_free_a=9
    count_free_b=9
    loop_count=0
    for filename in os.listdir("D:\Projects\interthrone\list"):  
        im = cv2.imread('D:/Projects/interthrone/list/'+filename)

        decodedObjects,var = decode(im)
        display(im, decodedObjects)
        assigned_rack=''
        if var[-1] == 'H':
            assigned_rack='a'
        
        elif var[-1] == 'M':
            assigned_rack='b'            
        assigned_worker=-1
        for i in range(0,3):
            if free_workers[i]==0:
                assigned_worker=i
                break
        data = {assigned_worker: 1}
        #   
        rack_data = db.child("racks").child(assigned_rack).get()
        rack_data = [i for i in rack_data.val()]
        flag=False
        rack_pos=-1
        print(rack_data)

                
        #db.child("workers").set(data)

        db.child("workers").update(data)

        for i in range(len(rack_data)):
            
            
            if rack_data[i]==0 and flag==False:
                rack_pos=i
                if rack_data[i]==0 and assigned_rack=='a':
                    count_free_a-= 1
                elif rack_data[i]==0 and assigned_rack=='b':
                    count_free_b-= 1    
                flag=True
                print('freea',count_free_a)
        if rack_pos!=-1:
            
            data={rack_pos:var}
            
            db.child('racks').child(assigned_rack).update(data)
        else:
            print('Warehouse is full')
        data={assigned_worker:'rack '+assigned_rack+' and position '+str(rack_pos)}
        db.child('workers_task').update(data)        
        print('freeb',count_free_b)
        rack_a=(1-(count_free_a/9))*100
        rack_b=(1-(count_free_b/9))*100
        tot = (1-((count_free_a+count_free_b)/18))*100
        print("a",rack_a)
        print('b',rack_b)
        print('tot',tot)        
        loop_count+=1
        if loop_count==1:
            break
load()
while(True):
    
    sendA()
    sendB()
    sendtot()
# =============================================================================
# Thread(target=sendB).start()
# Thread(target=sendA).start()
# Thread(target=sendtot).start()
# Thread(target=sendA).stop()
# Thread(target=sendB).stop()
# Thread(target=sendtot).stop()
# =============================================================================
