#!/bin/bash

#-----------------------------------------------
# Automatically login to MegaNet networks
# Last update: July 28, 2017
# Version: 2.0
# Reference: http://www.fadvisor.net/blog/2012/06/autologin-to-open-wifi/
#-----------------------------------------------

# The parameters that get passed to the script are:
# $1 = The interface name ( eth0, wlan0, etc)
# $2 = Interface status ( "up", "down", etc )

email='duongthanhhung1998@yahoo.com'
password='thanhhung1998'

# function to send login request
function login {
    if curl http://10.10.0.1:3992/wifi/login \
             --connect-timeout 5 \
             --max-time 15 \
             -H "Host: 10.10.0.1:3992" \
             -H "Referer: http://10.10.0.1:3992/wifi/pre_login/"\
             -H "Content-Type: application/x-www-form-urlencoded" \
             -H "Connection: keep-alive" \
             -H "Upgrade-Insecure-Requests: 1"\
             --data-urlencode "username=${email}" \
             --data-urlencode "password=${password}"; 
    then
        notify-send -t 3000 "Auto Login Meganet" "You have been successfully login Meganet as ${email}"
    else
        notify-send -t 3000 "Auto Login Meganet" "Auto login as ${email} failed"
    fi
}


# Check if wireless status is not down
if [[ "$2" == "down" ]]; then
    exit 0
fi


# For wireless network
if [[ "$1" =~ ^w ]]; then
    # Get the network name from iwconfig
    wifi_name=$(/sbin/iwconfig $1 | grep ESSID | cut -d'"' -f2)

    # If the wireless name matches MegaNet pattern then send login request
    if [[ "$wifi_name" =~ ^MegaNet\ M[0-9]{2}-[0-9]{2}$ ]]; then
        login
    fi


# For wired network
elif [[ "$1" =~ ^e ]]; then
    # Try to send whether network is MegaNet or not
    login
fi
