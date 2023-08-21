# -*- coding: utf-8 -*-
"""
Created on Sat Apr 13 16:15:12 2019

@author: Suriya Prakash
"""
import paho.mqtt.client as mqttClient
import time
brokerAddress="mqtt.cumulocity.com"
port=1883
user="team7/team7"
password="rotronyx"
def on_connect(client,userdata,flags,rc):
    if rc==0:
        print("CTB")
    else:
        print("CF")
client=mqttClient.Client("python")
client.on_connect=on_connect
client.username_pw_set(user,password=password)
client.connect(brokerAddress,port)
client.loop_start()
time.sleep(4)
client.loop_stop()