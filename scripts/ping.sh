#!/bin/bash

# send out data as mqtt message

timestamp="$(date +"%D %T")"
echo timestamp &> /home/pi/python/logs/mqtt.log &
python3 /home/pi/python/pingEnv.py &> /home/pi/python/logs/mqtt.log &