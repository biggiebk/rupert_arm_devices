"""
Description: Module for Tuya Devices.
"""
import json
import tinytuya

class DeviceController():
	"""
		Determines device type and passes to correct class based of string name.
		Supports:
			- Outlet
			- Light
	"""
	def __init__(self, control_dictionary):
		""" Construct """
		self.device = None
		if control_dictionary['name'].endswith("Light"):
			self.device = Light()
		elif control_dictionary['name'].endswith("Outlet"):
			self.device = Outlet()
		else:
			print(f"{control_dictionary['name']}: Unknown device type")
			return

		self.device.set_status(control_dictionary)


class Outlet():
	"""
		Handles outlet devices.
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
		if eval(f"{power}"):
			self.tiny_tuya.turn_on()
		else:
			self.tiny_tuya.turn_off()

	def set_status(self, control_dictionary):
		"""
		Set the status of a light. Requires:
			power = boolean value for on (True), off (False), None (Flip)
		"""
		with open("tuyaDevices.json", 'r', encoding='utf-8') as devices_file:
			devices_json = devices_file.read()
		devices = json.loads(devices_json)

		if control_dictionary['name'] in devices:
				self.tiny_tuya = tinytuya.OutletDevice(devices[control_dictionary['name']]['id'], devices[control_dictionary['name']]['ip'], devices[control_dictionary['name']]['key'])
				self.tiny_tuya.set_version(float(devices[control_dictionary['name']]['version']))
		else:
			print(f"{control_dictionary['name']} unknown device name")
			return

		if control_dictionary['on_off'] == None:
			self.flip()
		else:
			self.on_off(control_dictionary['on_off'])


class Light():
	"""
		Parent class for all devices.
		Supports:
			- On
			- Off
			- Flip
			- Color
			- Dim
	"""
	def __init__(self):
		""" Construct """
		self.tiny_tuya = None

	def brightness(self, brightness_level):
		"""
		Set brightness level. Requries:
			brightness_level = number indicating brightness level
		"""
		self.tiny_tuya.set_brightness(brightness_level)

	def color_rgb(self, red, green, blue):
		"""
		Set color using RGB
			red = number value for level of red
			green = number value for level of green
			blue = number value for level of blue
		"""
		self.tiny_tuya.set_colour(red, green, blue)

	def flip(self):
		"""Quickly flip a light on and off"""
		status = self.tiny_tuya.status()
		switch_state = status['dps']['20']
		self.on_off(not switch_state)

	def on_off(self, power):
		"""
		Power on or off a light. Requires:
			power = boolean value for on (True) or off (False)
		"""
		if eval(f"{power}"): # Used to convert a string to boolean, while still accepting a boolean to begin with.
			self.tiny_tuya.turn_on()
		else:
			self.tiny_tuya.turn_off()

	def set_status(self, control_dictionary):
		"""
		Set the status of a light. Requires:
			power = boolean value for on (True), off (False), None (Flip)
		"""
		with open("tuyaDevices.json", 'r', encoding='utf-8') as devices_file:
			devices_json = devices_file.read()
		devices = json.loads(devices_json)

		if control_dictionary['name'] in devices:
				self.tiny_tuya = tinytuya.BulbDevice(devices[control_dictionary['name']]['id'], devices[control_dictionary['name']]['ip'], devices[control_dictionary['name']]['key'])
				self.tiny_tuya.set_version(float(devices[control_dictionary['name']]['version']))
		else:
			print(f"{control_dictionary['name']} unknown device name")
			return

		if control_dictionary['on_off'] == None: # If value is None Flip from current status
			self.flip()
		else:
			self.on_off(control_dictionary['on_off'])

			# If light is powered on configure colors and brightness light
			if eval(f"control_dictionary['on_off']"): # Convert to boolean, however also accept as boolean.
				if control_dictionary['red'] == 0 and control_dictionary['green'] == 0 and control_dictionary['blue'] == 0:
					self.tiny_tuya.set_white(1000, control_dictionary['brightness_level'])
				else:
					self.color_rgb(control_dictionary['red'], control_dictionary['green'], control_dictionary['blue'])
					self.brightness(brightness_level=control_dictionary['brightness_level'])
