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
		with open("devices.json", 'r', encoding='utf-8') as settings:
			settings_json = settings.read()
		settings = json.loads(settings_json)

		for device in settings:
			if device['name'] == control_dictionary['name']:
				self.tiny_tuya = tinytuya.OutletDevice(device['id'], device['ip'], device['key'])
				version = 3.3
				if "version" in control_dictionary:
					versions = control_dictionary['version']
				self.tiny_tuya.set_version(version)
				status = self.tiny_tuya.status()
				break

		if control_dictionary['on_off'] == None:
			self.flip()
		else:
			self.on_off(control_dictionary['on_off'])
			