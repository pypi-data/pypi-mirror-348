![AlphaBot](https://i.imgur.com/JLBU5cs.png)

**Version:** 0.1.2  
**Author:** [@sadra-hub](https://github.com/sadra-hub)
**License:** MIT  
**Python Version:** 3.8+

---

## Description

`alphabot-interface` provides a modular and simple Python interface for interacting with key components of the [Waveshare AlphaBot 2](https://www.waveshare.com/wiki/AlphaBot2) platform, including:

- **Camera** module (using Picamera2)
- **Battery** monitoring
- **Motor** control

`alphabot-interface` is a lightweight Python package that lets you **comfortably use various components of the AlphaBot platform** and write **clean, readable, and modular code**.

This package is designed to abstract hardware-level interactions so developers and students can focus on high-level robotics programming and deply swarm intelligence algorithms

---

## Installation

You can install the package via `pip`:

```bash
pip install alphabot-interface
```

## Usage

This package let you comfortably use various components of AlphaBot and write clean, readable code. 


```python
from alphabot_interface import Camera, Battery, Motor

# Initialize components
camera = Camera()
battery = Battery()
motor = Motor()

target_x = 100
target_y = 0 
DURATION = 3  #in seconds

# Use the motor to go to position (100,0) in 3 seconds
motor.move(target_x, target_y, duration)

# How much battery is left?
battery_status = battery.get_status()

# Take a photo with camera and save it to output.jpg
camera.take_picture("output.jpg")
```