#!/usr/bin/env python3.11
#from tuya import Outlet
from tuya import DeviceController

control_dictionary = { "event_type": "control", "name": "LV Lamp Outlet", "on_off": None, "return_topic": "debug_topic"}
device = DeviceController(control_dictionary)

control_dictionary = { "event_type": "control", "name": "Bedroom Light", "on_off": None, "red": 0, "green": 0, "blue": 255, "brightness_level": 1000, "return_topic": "debug_topic"}
device = DeviceController(control_dictionary)

# Should Error
control_dictionary = { "event_type": "control", "name": "You don't know me", "on_off": True, "return_topic": "debug_topic"}
device = DeviceController(control_dictionary)
