"""
Description: Module for Tuya Devices.
"""
import time
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

	def run(self, in_queue):
		status_time = time.time() + 30
		heartbeat_time = time.time() + 10
		while(True):
			while(True):
				if time.time() >= status_time:
					status = self.tiny_tuya.status()
					status_time = time.time() + 30
					heartbeat_time = time.time() + 10
				elif time.time() >= heartbeat_time:
					payload = self.tiny_tuya.generate_payload(tinytuya.HEART_BEAT)
					status = self.tiny_tuya.send(payload)
					heartbeat_time = time.time() + 10
				else:
					status = self.tiny_tuya.receive()
				
				if not status:
					continue
				elif "Error" in status:
					self.tiny_tuya = tinytuya.BulbDevice(self.settings['id'], self.settings['ip'], self.settings['key'])
					self.tiny_tuya.set_version(float(self.settings['version']))
					self.tiny_tuya.set_socketPersistent(True)
					self.tiny_tuya.set_socketRetryLimit(1)
				else:
					break
			
			self.set_status(in_queue.get())

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


	def run(self, in_queue):
		heartbeat_time = time.time() + 10
		while(True):
			while(True):
				if time.time() >= heartbeat_time:
					payload = self.tiny_tuya.generate_payload(tinytuya.HEART_BEAT)
					status = self.tiny_tuya.send(payload)
					print(f"Hearbeat: {status}")
					heartbeat_time = time.time() + 10
				break
			print("  - Check Queue")
			control_dictionary = in_queue.get()
			try:
				self.set_status(control_dictionary)
			except Exception as e:
				print("Dude it like broke... trying again")
				self.set_status(control_dictionary)

	def set_status(self, control_dictionary):
		"""
		Set the status of a light. Requires:
			power = boolean value for on (True), off (False), None (Flip)
		"""
		print(f"  - set: {control_dictionary} for {self.name}")
		try:
			self.__set_status(control_dictionary)
		except Exception as e:
			print(e)
			print("If at first you don't succeed try again")
			self.tiny_tuya = tinytuya.BulbDevice(self.settings['id'], self.settings['ip'], self.settings['key'])
			self.tiny_tuya.set_version(float(self.settings['version']))
			self.tiny_tuya.set_socketPersistent(True)
			self.tiny_tuya.set_socketRetryLimit(1)
			self.__set_status(control_dictionary)

## Private Classes
	def __set_status(self, control_dictionary):
		if 'cycle' in control_dictionary:
			print("  - cycle found for {self.name}")
			rgb = {"red": control_dictionary['red'], "green": control_dictionary['green'], "blue": control_dictionary['blue']}
			self.__descend(control_dictionary['seconds'], control_dictionary['initial'], 0, control_dictionary['increment'], rgb)
		elif control_dictionary['on_off'] == None: # If value is None Flip from current status
			self.flip()
		else:
			self.on_off(control_dictionary['on_off'])
			# If light is powered on configure colors and brightness light
			if eval(f"control_dictionary['on_off']"): # Convert to boolean, however also accept as boolean.
				if control_dictionary['red'] == 255 and control_dictionary['green'] == 255 and control_dictionary['blue'] == 255:
					self.tiny_tuya.set_white( control_dictionary['brightness_level'], control_dictionary['colour_temp'])
				else:
					if not (control_dictionary['red'] == -1 and control_dictionary['green'] == -1 and control_dictionary['blue'] == -1):
						self.color_rgb(control_dictionary['red'], control_dictionary['green'], control_dictionary['blue'])
					self.brightness(brightness_level=control_dictionary['brightness_level'])



	def __descend(self, seconds, initial, end, inc, rgb):
		# Calculate
		sleep = seconds / (initial / inc)
		self.set_status({ "event_type": "control", "name": "Bedroom Light", "on_off": True, "red": rgb['red'], "green": rgb['green'], "blue": rgb['blue'], "brightness_level":  initial, "return_topic": "debug_topic"})
		time.sleep(sleep)
		# Loop
		for count in range(10, 1000, 10):
			print(f"  - Counter for {initial - count} for {self.name}")
			self.set_status({ "event_type": "control", "name": "Bedroom Light", "on_off": True, "red": -1, "green": -1, "blue": -1, "brightness_level":  initial - count, "return_topic": "debug_topic"})
			time.sleep(sleep)
		# Turn off the light
		self.set_status({ "event_type": "control", "name": "Bedroom Light", "on_off": False, "red": rgb['red'], "green": rgb['green'], "blue": rgb['blue'], "brightness_level":  initial, "return_topic": "debug_topic"})
