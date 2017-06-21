#!/usr/bin/env python

"""
    Automatically detect and connect to MegaNet network
    Parameter: name of the network
"""

from httplib import HTTPConnection, HTTPException
from urllib import quote as percent_encode
from sys import argv
from time import time, ctime
from socket import timeout
import platform
from Windows import windows
from Linux import linux


def finish(exit_code):
    """ clean up before quit"""
    # close connection
    connection.close()

    # write to log file
    logfile.seek(0, 0)
    logfile.write("\r\n".join(log))
    logfile.write("\r\n")
    logfile.close()

    exit(exit_code)


##########################################################
#                 Detect platform                        #
##########################################################

system_name = platform.system()
if system_name == "Windows":
    windows(argv)
elif system_name == "Linux":
    linux(argv)


##########################################################
#                  Open Log file                         #
##########################################################

# find the path to the script's folder
path = argv[0].replace("\\", "/")
path = path[:path.rfind("/")] + "/"

# open logfile
log_file_size = 50
logfile = open(path + "log.txt", "r+")
log = []
for line in logfile:
    log.append(line.rstrip())

# delete old log
if len(log) == log_file_size:
    log.pop(0)
    log.pop(0)

# add new log
log.append("[ " + ctime(time()) + " ]    Network: " + argv[1])


##########################################################
#                 Ready to login                         #
##########################################################

# read file to get email and password
try:
    fin = open(path + "account.txt", "r")
except IOError:
    log.append("    ERROR Unable to read account file")
    finish(1)

username = percent_encode(fin.readline().strip())
password = percent_encode(fin.readline().strip())
fin.close()

# establish connection
try:
    connection = HTTPConnection("10.10.0.1:3992", timeout=5)
except timeout:
    log.append("    ERROR Connection time out")
    finish(1)


##########################################################
#               Detect MegaNet Network                   #
##########################################################

# header of getting login page request
headers = {
    "Host": "10.10.0.1:3992",
    # "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:54.0) Gecko/20100101 Firefox/54.0",
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate",
    "Cache-Control": "no-cache",
    "Pragma": "no-cache",
    "Connection": "keep-alive",
}

# test whether login page available
try:
    connection.request("GET", "/wifi/pre_login?referral=http://detectportal.firefox.com/success.txt", headers=headers)
    response = connection.getresponse()
    if response.reason != "OK":
        raise HTTPException
except HTTPException:
    log.append("    ERROR A problem occurred when sending test request")
    finish(1)
except timeout:
    log.append("    Net work is not MegaNet or already login")
    finish(1)


##########################################################
#               Send login request                       #
##########################################################

# header & body of request
body = "username=" + username + "&password=" + password
headers = {
    # "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:54.0) Gecko/20100101 Firefox/54.0",
    # "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:53.0) Gecko/20100101 Firefox/53.0",
    # "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    # "Accept-Language": "en-US,en;q=0.5",
    # "Accept-Encoding": "gzip, deflate",
    "Host": "10.10.0.1:3992",
    "Referer": "http://10.10.0.1:3992/wifi/pre_login/",
    "Content-Type": "application/x-www-form-urlencoded",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1"
}

# send request
try:
    connection.request("POST", "/wifi/login", body, headers)
except HTTPException:
    log.append("    ERROR: Unable to send login request")
    finish(1)
except timeout:
    log.append("    ERROR: Connection timeout when sending login request")
    finish(1)

# get response
try:
    response = connection.getresponse()
except timeout:
    log.append("    Response time out")
    finish(1)
else:
    if response.status == 302:
        s = "    Successfully log in!"
    else:
        s = "    " + str(response.status) + " " + response.reason
    log.append(s)
    finish(0)
