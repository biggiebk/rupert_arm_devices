#!/usr/bin/env python3.11
import time
import datetime
import colorsys
import json
import os
from rupert.shared.synapse import Synapse
#from tuya import DeviceController

os.chdir('cfg')

def easy(control_dictionary, sleep):
	kafka_producer = Synapse('settings.json')
	kafka_producer.send("devices_alpha",json.dumps(control_dictionary))
	time.sleep(sleep)

def ascend(duration, increment, red, green, blue):
	hue, saturation, value = colorsys.rgb_to_hsv(red/255.0, green/255.0, blue/255.0)
	loop = round(value * 100/increment)
	sleep = duration / loop
	print(f"End Value: {value} Loop: {loop}, Inc: {increment} Sleep: {sleep}")
	# Loop
	for count in range(1, loop, 1):
		print(f"{count} - Value: {round((increment / 100) * (count), 2)}")

def descend(duration, increment, red, green, blue):
	hue, saturation, value = colorsys.rgb_to_hsv(red/255.0, green/255.0, blue/255.0)
	loop = round(value * 100/increment)
	sleep = duration / loop
	print(f"Start Value: {value} Loop: {loop}, Inc: {increment} Sleep: {sleep}")
	# Loop
	for count in range(0, loop, 1):
		print(f"{loop - count} - value: {round(value - (count * (increment/100)), 2)})")

#descend(100, 10, 0, 0, 102)
#ascend(600, 1, 255, 42, 0)

#print("Outlet Flip")
#easy({ "event_type": "control", "name": "LV Lamp Outlet", "on_off": None, "return_topic": "debug_topic"}, 5)

#print('Light Flip')
#easy({ "event_type": "control", "name": "Office Light", "on_off": None}, 5)
#easy({ "event_type": "control", "name": "Office Light", "on_off": None}, 5)

#print('Descend Cycle')
#easy({ "event_type": "control", "name": "Office Light", "cycle": "descend", "red": 0, "green": 0, "blue": 255, "duration": 600, "increment": 0.5, "return_topic": "debug_topic"}, 5)

#print('Ascend Cycle')
#easy({ "event_type": "control", "name": "Office Light", "cycle": "ascend", "red": 255, "green": 42, "blue": 0, "duration": 100, "increment": 1, "return_topic": "debug_topic"}, 5)

#print('Custom Cycle')
#easy({ "event_type": "control", "name": "Office Light", "cycle": "custom", "cycle_name": "christmas", "return_topic": "debug_topic"}, 5)

#print('Force Color')
#easy({ "event_type": "control", "name": "Office Light", "on_off": True, "red": 0, "green": 0, "blue": 255, "return_topic": "debug_topic"}, 10)

print('Set Full White')
easy({ "event_type": "control", "name": "Office Light", "on_off": True, "brightness_level": 100, "colour_temp": 100, "return_topic": "debug_topic"}, 10)

#print('Dim to 25')
#easy({ "event_type": "control", "name": "Office Light", "on_off": True, "brightness_level": 25, "return_topic": "debug_topic"}, 10)

#print('Back to Full')
#easy({ "event_type": "control", "name": "Office Light", "on_off": True, "brightness_level": 100, "return_topic": "debug_topic"}, 10)

#print('Temp to 25')
#easy({ "event_type": "control", "name": "Office Light", "on_off": True, "colour_temp": 25, "return_topic": "debug_topic"}, 10)

#print('Back to Full')
#easy({ "event_type": "control", "name": "Office Light", "on_off": True, "brightness_level": 100, "return_topic": "debug_topic"}, 10)

#print('Turn Off')
#easy({ "event_type": "control", "name": "Office Light", "on_off": False, "return_topic": "debug_topic"}, 5)

#print("Wink")
#easy({ "event_type": "control", "name": "Office Light", "cycle": "wink", "times": 5, "leave_on": True, "return_topic": "debug_topic"}, 5)