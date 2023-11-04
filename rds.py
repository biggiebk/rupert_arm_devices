#!/usr/bin/env python3.11

import os

os.chdir('cfg')

from rupert_arm_devices.device_synapse import RupertDeviceSynapse

device_consumer = RupertDeviceSynapse('settings.json')

device_consumer.listen('bedroom_audio')
