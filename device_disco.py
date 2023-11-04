#!/usr/bin/env python3.11
import json
import os
import tinytuya

os.chdir('cfg')

# Discover tinytuya devices
TEMPTUYA = tinytuya.deviceScan(False, 50)
devices = {}
for key in TEMPTUYA:
	devices[TEMPTUYA[key]['name']] = TEMPTUYA[key]
	devices[TEMPTUYA[key]['name']].pop('name')

# Save devices
with open('tuyaDevices.json', 'w') as file:
	json.dump(devices, file, indent=4)
