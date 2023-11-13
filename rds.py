#!/usr/bin/env python3.11
from rupert_arm_devices.device_synapse import RupertDeviceSynapse

if __name__ == '__main__': # Required to support multiprocessing in the Devices Synapse
	device_consumer = RupertDeviceSynapse('cfg/settings.json')
	device_consumer.listen('devices')
