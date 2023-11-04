#!/usr/bin/env python3.11

from rupert_arm_devices.device_synapse import RupertDeviceSynapse

device_consumer = RupertDeviceSynapse('cfg/settings.json')

device_consumer.listen('bedroom_audio')
