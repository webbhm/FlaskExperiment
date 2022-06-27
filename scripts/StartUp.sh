#!/bin/bash

# Start flask server
sudo -u pi python3 /home/pi/python/app.py &> /home/pi/python/logs/flask.log &

# Start video feed
#sudo -u pi python3 /home/pi/python/VideoStream.py &> /home/pi/python/logs/video.log &