# Process all your intents here. Based on the initial understanding,
# the appropriate function is called to process the slots

from config.slots import device_info
from config.slots import device_scan
from system.gtts import play_audio_response


def process_inference(inference):
    if inference.is_understood:
        if inference.intent == "deviceScan":
            device_scan(inference)
        elif inference.intent == "deviceInfo":
            device_info(inference)
        else:
            raise NotImplementedError()
    else:
        play_audio_response("I'm afraid I don't understand")
