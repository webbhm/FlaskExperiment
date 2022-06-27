#!/bin/bash

DATE=$(date +"%Y-%m-%d_%H%M")

fswebcam -d /dev/video1 -r 1280x720 --delay 10 --no-banner /home/pi/Pictures/$DATE.jpg