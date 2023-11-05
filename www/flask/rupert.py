
@app.route("/device/<name>/flip")
def flip(name):
  control_dictionary = { "event_type": "control", "name": escape(name), "on_off": None, "return_topic": "debug_topic"}
  kafka_producer = Synapse('/web/cfg/settings.json')
  kafka_producer.send("devcies_alpha",json.dumps(control_dictionary))
  return f"Device: {escape(name)} Flip"

@app.route("/device/<name>/<power>")
def power(name, power):
  control_dictionary = { "event_type": "control", "name": escape(name), "on_off": escape(power), "return_topic": "debug_topic"}
  kafka_producer = Synapse('/web/cfg/settings.json')
  kafka_producer.send("devcies_alpha",json.dumps(control_dictionary))
  return f"Device: {escape(name)} Power: {escape(power)}"

@app.route("/light/<name>/<power>/<red>/<green>/<blue>/<brightness_level>")
def light(name, power, red, green, blue, brightness_level):
  control_dictionary = { "event_type": "control", "name": "Bedroom Light", "on_off": escape(power), "red": int(escape(red)), "green": int(escape(green)), "blue": int(escape(blue)), "brightness_level": int(escape(brightness_level)), "return_topic": "debug_topic"}
  kafka_producer = Synapse('/web/cfg/settings.json')
  kafka_producer.send("devcies_alpha",json.dumps(control_dictionary))
  return f"Device: {escape(name)} Power: {escape(power)} Red {escape(red)} Green {escape(green)} Blue {escape(blue)} Brightness_level {escape(brightness_level)}"
