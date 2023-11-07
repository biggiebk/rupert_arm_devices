#!/usr/bin/env python3.11
import time
import json
from rupert.shared.synapse import Synapse

def easy(control_dictionary, sleep):
	kafka_producer = Synapse('/home/rupert/.local/lib/python3.11/site-packages/rupert_arm_devices/cfg/settings.json')
	kafka_producer.send("devices",json.dumps(control_dictionary))
	time.sleep(sleep)

# Wake Up
easy({ "event_type": "control", "name": "Bedroom Light", "on_off": True, "red": 255, "green": 42, "blue": 0, "brightness_level":  10, "return_topic": "debug_topic"}, 5.5)
for count in range(10, 1000, 10):
	easy({ "event_type": "control", "name": "Bedroom Light", "on_off": True, "red": -1, "green": -1, "blue": -1, "brightness_level": count + 10, "return_topic": "debug_topic"}, 5.5)
