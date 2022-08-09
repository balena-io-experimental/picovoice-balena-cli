# Misc. custom functions used by the slots are stored here

import requests
from system.gtts import play_audio_response

# Set a global vars
api_url = "http://0.0.0.0:7878/v1/scan"


# Create a global var used to store the network devices for duration of the session
network_devices = None


# A custom process used for this particular application. Used
# for scanning the network for devices
def scan_devices():
    global network_devices
    play_audio_response("Scanning for devices")
    network_devices = requests.get(api_url, timeout=30).json()
