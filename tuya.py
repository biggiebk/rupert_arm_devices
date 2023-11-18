"""
Description: Module for Tuya Devices.
"""
import time
import colorsys
import json
import tinytuya

class DeviceController():
	"""
		Determines device type and passes to correct class based of string name.
		Supports:
			- Outlet
			- Light
	"""
	def __init__(self, name):
		""" Construct """
		# Locate device settings
		with open("cfg/tuyaDevices.json", 'r', encoding='utf-8') as devices_file:
			devices_json = devices_file.read()
		devices = json.loads(devices_json)
		self.name = name

		# Setup devie to control
		self.device = None
		if name.endswith("Light"):
			self.device = Light(name, devices[name])
		elif name.endswith("Outlet"):
			self.device = Outlet(name, devices[name])
		else:
			print(f"{name}: Unknown device type")
			return
	
	def run(self, control_dictionary):
		print(f"  - Running: {control_dictionary}")
		self.device.set_status(control_dictionary)

class Outlet():
	"""
		Handles outlet devices.
		Supports:
			- On
			- Off
			- Flip
	"""
	def __init__(self, name, settings):
		""" Construct """
		self.settings = settings
		self.tiny_tuya = tinytuya.OutletDevice(settings['id'], settings['ip'], settings['key'])
		self.tiny_tuya.set_version(float(settings['version']))
		self.name = name

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
		if eval(f"{power}"): # Used to convert a string to boolean, while still accepting a boolean to begin with.
			self.tiny_tuya.turn_on()
		else:
			self.tiny_tuya.turn_off()

	def set_status(self, control_dictionary):
		"""
		Set the status of a light. Requires:
			power = boolean value for on (True), off (False), None (Flip)
		"""
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
	def __init__(self, name, settings):
		""" Construct """
		self.settings = settings
		self.tiny_tuya = tinytuya.BulbDevice(self.settings['id'], self.settings['ip'], self.settings['key'])
		self.tiny_tuya.set_version(float(self.settings['version']))
		self.tiny_tuya.set_socketPersistent(True)
		self.tiny_tuya.set_socketRetryLimit(1)
		self.name = name

	def brightness(self, brightness_level):
		"""
		Set brightness level. Requries:
			brightness_level = number indicating brightness level
		"""
		print(f"  - brightness to {brightness_level} on {self.name}")
		self.tiny_tuya.set_brightness(brightness_level)

	def color_hsv(self, hue, saturation, value):
		"""
		Set color using RGB
			red = number value for level of red
			green = number value for level of green
			blue = number value for level of blue
		"""
		print(f"  - HSV: {hue} {saturation} {value}")
		self.tiny_tuya.set_hsv(hue, saturation, value)

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
		print(f"  - set: {control_dictionary} for {self.name}")
		try: # Required to capture random KeyError: '24' and try again. Possible connectivity hicup? 
			self.__set_status(control_dictionary)
		except Exception as e: # A simple retry fails, so pretty much start from stratch and try again.
			print(e)
			print("If at first you don't succeed try again")
			self.tiny_tuya = tinytuya.BulbDevice(self.settings['id'], self.settings['ip'], self.settings['key'])
			self.tiny_tuya.set_version(float(self.settings['version']))
			self.tiny_tuya.set_socketPersistent(True)
			self.tiny_tuya.set_socketRetryLimit(1)
			self.__set_status(control_dictionary)

## Private Classes
	def __ascend(self, duration, increment, red, green, blue):
		hue, saturation, value = colorsys.rgb_to_hsv(red/255.0, green/255.0, blue/255.0)
		loop = round(value * 100/increment)
		sleep = duration / loop
		print(f"  - Ascending: End Value: {value} Loop: {loop}, Inc: {increment} Sleep: {sleep}")
		# Loop
		for count in range(1, loop, 1):
			print("\n---Next Cycle---")
			print(f"  - Counter for {count} for {self.name}")
			self.set_status({ "event_type": "control", "name": "Bedroom Light", "on_off": True, "hue": hue, "saturation": saturation, "value": round((increment / 100) * (count), 2), "return_topic": "debug_topic"})
			time.sleep(sleep)
		print("  - Last one")
		self.set_status({ "event_type": "control", "name": "Bedroom Light", "on_off": True, "hue": hue, "saturation": saturation, "value": value, "return_topic": "debug_topic"})
		print("\n---Cycle Completed---\n")

	def __descend(self, duration, increment, red, green, blue):
		# Calculate HSV values
		hue, saturation, value = colorsys.rgb_to_hsv(red/255.0, green/255.0, blue/255.0)

		# Calculate
		loop = round(value * 100/increment)
		sleep = duration / loop
		print(f"  - DESCENDING: Start Value: {value} Loop: {loop}, Inc: {increment} Sleep: {sleep}")

		# Loop
		for count in range(0, loop, 1):
			print("\n---Next Cycle---")
			print(f"  - Counter for {100 - count} for {self.name}")
			self.set_status({ "event_type": "control", "name": "Bedroom Light", "on_off": True, "hue": hue, "saturation": saturation, "value": round(value - (count * (increment/100)), 2), "return_topic": "debug_topic"})
			time.sleep(sleep)
		# Turn off the light
		print("  - Turn off")
		self.set_status({ "event_type": "control", "name": "Bedroom Light", "on_off": False, "red": -1, "green": -1, "blue": -1, "brightness_level":  0, "return_topic": "debug_topic"})
		print("\n---Cycle Completed---\n")

	def __set_status(self, control_dictionary):
		if 'cycle' in control_dictionary:
			print(f"  - cycle found for {self.name}")
			if "descend" == control_dictionary['cycle']:
				self.__descend(control_dictionary['duration'], control_dictionary['increment'], control_dictionary['red'], control_dictionary['green'], control_dictionary['blue'])
			elif "ascend" == control_dictionary['cycle']:
				self.__ascend(control_dictionary['duration'], control_dictionary['increment'], control_dictionary['red'], control_dictionary['green'], control_dictionary['blue'])
		elif control_dictionary['on_off'] == None: # If value is None Flip from current status
			self.flip()
		else:
			self.on_off(control_dictionary['on_off'])
			# If light is powered off return
			if not control_dictionary['on_off']:
				return
			if all(key in control_dictionary for key in ('red', 'green', 'blue')):
				if eval(f"control_dictionary['on_off']"): # Convert to boolean, however also accept as boolean.
					print("on_off = true")
					if (control_dictionary['red'] == 255 and control_dictionary['green'] == 255 and control_dictionary['blue'] == 255):
						print("Regular")
						self.tiny_tuya.set_white( control_dictionary['brightness_level'], control_dictionary['colour_temp'])
					elif not (control_dictionary['red'] == -1 and control_dictionary['green'] == -1 and control_dictionary['blue'] == -1):
						hue, saturation, value = colorsys.rgb_to_hsv(control_dictionary['red']/255.0, control_dictionary['green']/255.0, control_dictionary['blue']/255.0)
						print("convert")
						self.color_hsv(hue, saturation, value)
					else:
						self.brightness(brightness_level=control_dictionary['brightness_level'])
			else:
				if all(key in control_dictionary for key in ('hue', 'saturation', 'value')):
					self.color_hsv(control_dictionary['hue'], control_dictionary['saturation'], control_dictionary['value'])