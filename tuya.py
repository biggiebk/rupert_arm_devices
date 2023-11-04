"""
Description: Module for Tuya Devices.
"""
import json
import tinytuya

class Outlet():
	"""
		Parent class for all devices.
		Supports:
			- On
			- Off
			- Flip
	"""
	def __init__(self):
		""" Construct """
		self.tiny_tuya = None

	def flip(self):
		"""Quickly flip a light on and off"""
		status = self.tiny_tuya.status()
		switch_state = status['dps']['1']
		self.tiny_tuya.set_status(not switch_state)

	def on_off(self, power):
		"""
		Power on or off a light. Requires:
			power = boolean value for on (True) or off (False)
		"""
		if eval(power):
			self.tiny_tuya.turn_on()
		else:
			self.tiny_tuya.turn_off()

	def set_status(self, control_dictionary):
		"""
		Set the status of a light. Requires:
			power = boolean value for on (True), off (False), None (Flip)
		"""
		with open("cfg/tuyaDevices.json", 'r', encoding='utf-8') as devices_file:
			devices_json = devices_file.read()
		devices = json.loads(devices_json)

		if control_dictionary['name'] in devices:
				self.tiny_tuya = tinytuya.OutletDevice(devices[control_dictionary['name']]['id'], devices[control_dictionary['name']]['ip'], devices[control_dictionary['name']]['key'])
				version = 3.3
		else:
			print(f"{control_dictionary['name']} unknown device name")
			return

		if control_dictionary['on_off'] == None:
			self.flip()
		else:
			self.on_off(control_dictionary['on_off'])
