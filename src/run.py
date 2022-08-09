# Options:
# What devices are on my network? <-- returns a list with numbers to be used in next section
# How many devices are on my network?
# Scan for devices again

# What is the kernel version of device 1?
# What is the operating system of device 2?
# What is the architecture of device 1?

# Reconfiguration of the processed voice commands can all be done through the files in ./config/

import os
import sys
from pv.pv import PicovoiceCLI
from system.gtts import create_default_sound_files
from system.network import check_internet
from system.parser import parser


# Provide the filenames of the files provided by the Picovoice CLI and stored in config/pv_config_files
picoPpnFile = "picovoice_wake_word.ppn"
picoRhnFile = "picovoice_voice_commands.rhn"

if __name__ == "__main__":
    # Check there is internet access. It is required for the Google Text to Speech API.
    if check_internet() is False:
        print(
            "No internet connection found. It is required for Google Text to Speech. Exiting."
        )
        sys.exit(1)

    # Process any arguments passed to the script.
    args = parser()

    # Create reusable sound files to avoid repeating the build
    create_default_sound_files()

    # Set the access key obtained from Picovoice console
    if args.access_key is None:
        access_key = os.environ["ACCESS_KEY"]
    else:
        access_key = args.access_key

    # Configure the Picovoice instance
    picoConfigFilesDir = "config/pv_config_files/"
    o = PicovoiceCLI(
        os.path.join(
            os.path.dirname(__file__),
            picoConfigFilesDir + picoPpnFile,
        ),
        os.path.join(
            os.path.dirname(__file__),
            picoConfigFilesDir + picoRhnFile,
        ),
        access_key,
        args.audio_device_index,
    )

    # Start the Picovoice instance
    o.run()
