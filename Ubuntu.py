#!/usr/bin/env python

"""
    Run when there's a change in network
    :parameter
        0: script's name
        1: network interfaces (eth0, wlan0, etc)
        2: status (up, down, change, etc)
"""

from Login import *
from time import ctime, time
from sys import argv
from os import popen

# TODO other circumstances
# check network status
if argv[2] == "down":
    exit(0)

# record activities to text file
logging()

# get network name
if argv[1][0] == "e":  # wired network (eth0 or enp3s0)
    network_name = "WiredNetwork"
elif argv[1][0] == "w":  # wifi network (wlan0 or wl3s0)
    network_name = popen("/sbin/iwconfig | grep ESSID | cut -d'\"' -f2").read().strip()
else:
    network_name = "N/A"

# add new entry to log file
log.append("[ " + ctime(time()) + " ]    Network: " + network_name)

# login
ready_login()
check_mega_net()
login()
