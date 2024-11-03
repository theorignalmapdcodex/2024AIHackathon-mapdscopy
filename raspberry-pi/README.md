# Instruction to Run Code on Raspberry pi

## 1. Hardware setup
- RaspberryPi Version 4B
- camera version: raspberry pi camera rev 1.3 -> connect to camera port on RaspberryPi
- USB microphone -> attached to USB port
- green LED: GPIO19 -> 220 ohm resister -> GND
- red LED: GPIO21 -> 220 ohm resister -> GND

## 2. Package Installation
Install ffmpeg library on the RaspberryPi.

Python: picamera2, requests, sounddevice, wave, gpiozero, python-ffmpeg

## 3. How to run
```bash
python3 recording.py
```
