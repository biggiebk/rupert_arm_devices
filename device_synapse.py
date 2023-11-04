"""
Description: Contains audio modules
"""
import json
from beartype import beartype
from rupert_arm_devices.tuya import Outlet
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
		control_dict = json.loads(consumer_message.value().decode("utf-8"))
		if control_dict['event_type'] == 'control':
			device = Outlet()
			device.set_status(control_dict)
		elif control_dict['event_type'] == 'status':
			pass
