#!/bin/bash

#-----------------------------------------------
# Automatically login to MegaNet networks
# Last update: June 19, 2017
# Version: 1.0
# Reference: http://www.fadvisor.net/blog/2012/06/autologin-to-open-wifi/
#            https://geekexplains.blogspot.com/2008/06/whats-http-explain-http-request-and.html
#-----------------------------------------------

export LC_ALL=C
LogFile="/home/hung/foo/log"

# The parameters that get passed to the script are:
# $1 = The interface name ( eth0, wlan0, etc)
# $2 = Interface status ( "up" or "down" )

# Check if wireless status is up
if [[ "$1" == wlp3s0 && "$2" == "up" ]]; then

    # Get the network name from "iwconfig" or (can also locate the network based on IP or MAC address if needed)
    ESSID=$(/sbin/iwconfig $1 | grep ESSID | cut -d'"' -f2)

    # Record the date and time for debugging purposes only
    echo "[`date`] ESSID=($ESSID)" >> $LogFile

    # If the wireless name matches then run its python script
    if [[ "$ESSID" =~ ^MegaNet\ M[0-9]{2}-[0-9]{2}$ ]]; then
        /home/hung/opt/autologin/Wireless.py 1>> $LogFile 2>&1
    fi
fi


# Check if wired network status is up
if [[ "$1" == enp2s0 && "$2" == "up" ]]; then

    # Record the date and time for debugging purposes only
    echo "[`date`] ESSID=(WiredNetwork)" >> $LogFile

    /home/hung/opt/autologin/Wired.py 1>> $LogFile 2>&1
fi
