# Process all the slots called from the inference function here

import config.functions as func
from config.functions import scan_devices
from system.gtts import play_audio_response


def device_info(inference):
    # Store the slots for the passed inference
    slots = inference.slots

    # If there hasn't been a network scan yet then do one now
    if func.network_devices is None:
        scan_devices()

    # Store the device index number, which is one less than the number of items
    deviceIndexNumber = int(slots["deviceNumber"]) - 1

    if len(func.network_devices) == 0:
        response = "There are no devices found on your network"
    elif len(func.network_devices) < (deviceIndexNumber + 1):
        response = "This device doesn't exist... Try scanning again by saying: picovoice, scan for devices"
    elif slots["info"] == "kernel version":
        response = (
            "The kernel version is %s"
            % func.network_devices[deviceIndexNumber]["KernelVersion"]
        )
    elif slots["info"] == "operating system":
        response = (
            "The operating system is %s"
            % func.network_devices[deviceIndexNumber]["OperatingSystem"]
        )
    elif slots["info"] == "architecture":
        response = (
            "The architecture is %s"
            % func.network_devices[deviceIndexNumber]["Architecture"]
        )
    print(response)

    # Play the responses generated based on the slots
    play_audio_response(response)


def device_scan(inference):
    # Store the slots for the passed inference
    slots = inference.slots

    if slots["devices"] == "many devices" and slots["location"] == "network":
        if func.network_devices is None:
            scan_devices()
            number_of_devices = len(func.network_devices)
            response = (
                "There are %d devices on your network" % number_of_devices
            )
        else:
            number_of_devices = len(func.network_devices)
            response = (
                "Your last scan found %d devices on your network. You can scan again by saying: picovoice, scan for devices again"
                % number_of_devices
            )

        # Play the responses generated based on the slots
        play_audio_response(response)
    elif slots["devices"] == "scan":
        scan_devices()
        number_of_devices = len(func.network_devices)
        response = "I found %d devices on your network" % number_of_devices

        # Play the responses generated based on the slots
        play_audio_response(response)
    elif slots["devices"] == "what devices":
        if func.network_devices is None:
            scan_devices()

        if len(func.network_devices) == 0:
            response = "I couldn't find any devices on your network"

            # Play the responses generated based on the slots
            play_audio_response(response)
        else:
            response = "There are %d devices found on your network" % len(
                func.network_devices
            )

            # Inform of the number of devices found
            play_audio_response(response)

            # For each device found inform of the device number and name
            i = 1
            for device in func.network_devices:
                eachDevice = "Device %d, %s" % (i, device["Name"])
                play_audio_response(eachDevice)
                i += 1

    print(response)
