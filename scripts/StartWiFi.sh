#!/bin/bash

# Start wifi so can use for file transfer

# rfkill can block the call to wlan0
sudo rfkill unblock 0
ifconfig wlan0 up