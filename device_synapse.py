"""
Description: Contains audio modules
"""
import multiprocessing
import json
from beartype import beartype
from rupert_arm_devices.tuya import DeviceController
from rupert.shared.synapse import Synapse

class RupertDeviceSynapse(Synapse):
	"""
		Description: Audio Synapse class.
		Responsible for:
			1. Basic constructor for connecting/starting
			2. Initiates Kafka cosumer
			3. Contains method to push to Kafka as producer
	"""
	@beartype
	def __init__(self, settings_file: str) -> None:
		super().__init__(settings_file=settings_file)
		self.controllers = {}

	@beartype
	def process_event(self, consumer_message) -> None:
		"""
			Description: Initiats events for the requested light
			Responsible for:
				1. Converts the messages value to dictionary
				2. Runs the light event as a daemon thread
			Requires:
				consumer_message
		"""
		control_dictionary = json.loads(consumer_message.value().decode("utf-8"))
		print(f"rcv: {control_dictionary}")
		if control_dictionary['event_type'] == 'control':
			# Do we already process controller for the device?
			if control_dictionary['name'] in self.controllers:
				print(f"Found process for: {control_dictionary['name']}")
				# Is the process still running? Terminate if it is.
				if self.controllers[control_dictionary['name']].is_alive():
					print(f"Killing process for: {control_dictionary['name']}")
					self.controllers[control_dictionary['name']].terminate()
			# Start new Process
			print(f"Setting process controller for: {control_dictionary['name']}")
			device_controller = DeviceController(control_dictionary['name'])
			print(f"Configuring new process for: {control_dictionary['name']}")
			new_processes = multiprocessing.Process(target=device_controller.run, args=(control_dictionary, ))
			print(f"Starting new process for: {control_dictionary['name']}")
			new_processes.start()
			self.controllers[control_dictionary['name']] = new_processes
			print(f"Started process for: {control_dictionary['name']}")
		elif control_dictionary['event_type'] == 'status':
			pass
		else:
			print("Unknown Event Type")
