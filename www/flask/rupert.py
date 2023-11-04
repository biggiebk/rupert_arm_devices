import json
import time
from flask import Flask
from markupsafe import escape
from rupert.shared.synapse import Synapse

app = Flask(__name__)

@app.route("/device/<name>/flip")
def flip(name):
  control_dictionary = { "event_type": "control", "name": escape(name), "on_off": None, "return_topic": "debug_topic"}
  kafka_producer = Synapse('/web/cfg/settings.json')
  kafka_producer.send("bedroom_audio_alpha",json.dumps(control_dictionary))
  return f"Device: {escape(name)} Flip"

@app.route("/device/<name>/<power>")
def power(name, power):
  control_dictionary =  { "event_type": "control", "name": escape(name), "on_off": escape(power), "return_topic": "debug_topic"}
  kafka_producer = Synapse('/web/cfg/settings.json')
  kafka_producer.send("devices_alpha",json.dumps(control_dictionary))
  return f"Device: {escape(name)} Power: {escape(power)}"
