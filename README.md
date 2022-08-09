# Picovoice balena CLI Demo

[Picovoice](https://picovoice.ai) is a platform for adding your own customised voice control to your product. It allows complete control over the voice commands your device listens for, and the actions it takes in response, all wrapped in an easy to use web interface and generous free tier account.

This repository provides an example of running Picovoice on a Raspberry Pi 4 using [balena.io](https://balena.io). It wraps the balena `scan` CLI command to allow listing of devices on your network and some of the configurations of those devices. It is designed as a demo and starter project to use Picovoice and instructions on how to build it for your own uses are included below.

[![balena deploy button](https://www.balena.io/deploy.svg)](https://dashboard.balena-cloud.com/deploy?repoUrl=https://github.com/maggie0002/picovoice-balena-cli)

## Using Picovoice CLI

Get started by saying `picovoice`. Picovoice will reply `yes` and wait for your instruction, which can include one of the following:

`What devices are on my network?`

- Performs a scan of your network for balena devices and returns a numbered list

`Scan for devices again`

- After the first scan the results are cached and future commands will return data from that cache until either a restart or you ask picovoice to `scan for devices again`.

`How many devices are on my network?`

- Scans for devices if a scan hasn't already taken place and reports the number of available devices

`What is the kernel version of device 1?`

- Reports the kernel version of device 1

`What is the operating system of device 2?`

- Reports the operating system of device 2

`What is the architecture of device 2`

- Reports the architecture of device 2

## Hardware

This project is built for the Raspberry Pi 4. Picovoice says it also works perfectly well on Raspberry Pi Zero 2 although I was unable to source the hardware to test on and therefore this repository is currently only compatible with Raspberry Pi 4.

On top of the Raspberry Pi 4 goes the [ReSpeaker 2-Mics Pi Hat](https://www.seeedstudio.com/ReSpeaker-2-Mics-Pi-HAT.html) which provides the microphones and speaker output for Picovoice.

I then used a [3w Mono Enclosed Speaker](https://thepihut.com/products/mono-enclosed-speaker-3w-4-ohm) plugged in to the HAT for sound output.

All of this hardware is push fit, with no soldering required.

Internet access is required to communicate with the Google Translate API that allows voice responses.

## Installation

1. Register for an account on the [Picovoice console](https://console.picovoice.ai/login) where you will be able to obtain an access key.

2. Deploy the application as a fleet to the balena Cloud. Don't worry, we have you covered, there is one-click setup link at the top of this README.

3. Expand the advanced option on the `Create and deploy to fleet` window that appears for your balena account. Configure the `Fleet configuration` with the following:

   | Name                        | Value                                           |
   | --------------------------- | ----------------------------------------------- |
   | RESIN_HOST_CONFIG_dtparam   | "i2c_arm=on","spi=on","audio=on","i2s=on"       |
   | RESIN_HOST_CONFIG_dtoverlay | "vc4-kms-v3d","i2s-mmap","seeed-2mic-voicecard" |

4. In the same window, configure the `Fleet environment variables` with your access key:

   | Name       | Value                   |
   | ---------- | ----------------------- |
   | ACCESS_KEY | your-key-from-picovoice |

   **Example configuration**

   <img width="699" alt="Screenshot 2022-08-08 at 18 17 30" src="https://user-images.githubusercontent.com/64841595/183704678-712eded1-b061-4638-8149-32f7ab7d61ab.png">

   Then hit the `Create and deploy` button.

5. In the next screen, press `Add device`. Select OS version `v2.99.27` which is the OS configuration the overlays provided in this repo are built for. Then configure the other options including WiFi settings as required (you may need to tick the `Show outdated versions` checkbox to see the `2.99.27` OS version).

6. Click `Flash` and you will be taken to balena Etcher ready to flash the image to your SD card.

7. Once you have flashed the image to your card, mount the card on to your system and open the root of the filesystem. Copy `overlays/2.99.27/seeed-2mic-voicecard.dtbo` found in this repository to the `/overlays/` folder on your mounted SD card.

8. Plug your SD card in to your Raspberry Pi, boot the device and it will begin to download and install the required software.

## Building your own or adding features

Picovoice is designed to be completely customisable. I have chosen to demonstrate Picovoice by wrapping the balena CLI, but it can be used for any purpose and you can easily configure your own voice commands in the [Picovoice console](https://console.picovoice.ai/login). This code repository is designed to try and make that build as easy as possible.

Here are some steps to build this project for your own purpose:

1. Login to the [Picovoice console](https://console.picovoice.ai/login), navigate to `rhino` - which is the Picovoice `speech-to-intent` engine - and follow the Picovoice docs to build your own voice commands through their web interface.
2. Once you have configured your voice commands you can export a `.rhn` file from the Picovoice console. Replace the current `config/pv_config_files/picovoice_voice_commands.rhn` with your new `.rhn` file.
3. You can now configure what you want the device to do when it hears your chosen commands. All of the configuration is done through the `config` directory of this repository.

   - The `intents.py` processes the `Intents` configured in the dashboard
   - `slots.py` processes the slots configured in the dashboard, based on the available slots under the `intent`.

   Much of the language of `intents` and `slots` will become clearer when configuring your voice commands in the Picovoice console.

4. Feedback here or on the [balena Forums](http://forums.balena.io) on the experience and lessons learnt.

5. Enjoy your own custom built voice assistant!
