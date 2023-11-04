#!/usr/bin/env python3.11
from tuya import Outlet

outlet = Outlet()

control_dictionary = { "event_type": "control", "name": "LV Lamp", "on_off": True, "version": 3.3, "return_topic": "debug_topic"}
outlet.set_status(control_dictionary)
