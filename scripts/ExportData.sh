#!/bin/bash

# Perform SSH file transfer of sensor data to server

scp /home/pi/data/*.txt flm@192.168.1.1:/C:/FLM/A1.csv