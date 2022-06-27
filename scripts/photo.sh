#!/bin/bash

# Need to preload libatomic for OpenCV to work

LD_PRELOAD=/usr/lib/arm-linux-gnueabihf/libatomic.so.1 python3 /home/pi/python/Camera/photo.py