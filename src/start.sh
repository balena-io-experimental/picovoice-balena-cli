#!/usr/bin/env bash

lockfile="/tmp/start.lock"
modules=$(lsmod)

# Check if modules are installed or lock file exists
if grep -q i2c_dev <<< "$modules" && \
    grep -q snd_soc_wm8960 <<< "$modules" && \
    grep -q snd_soc_ac108 <<< "$modules" && \
    grep -q snd_soc_seeed_voicecard <<< "$modules"  ||
    [ -f "$lockfile" ]
then
    alsactl restore
else
    # Use a basic lock file on first try to stop a loop if there is an issue
    touch "$lockfile"

    # Not all modules loaded so loading them and restarting the container
    echo "Required modules are not yet installed. Going to install them and restart the container."
    insmod modules/snd-soc-seeed-voicecard.ko
	insmod modules/snd-soc-ac108.ko
	insmod modules/snd-soc-wm8960.ko
	modprobe i2c-dev
    # Exiting 1 so that restart is triggered on restart-on-failure policy
    exit 1
fi

# All modules loaded so starting the application
echo "Ready. Starting Picovoice..."
exec python3 run.py
