#!/usr/bin/env python

"""
    Provide platform-independent functions to login automatically
"""

from httplib import HTTPConnection, HTTPException
from urllib import quote as percent_encode
from socket import timeout
from os.path import *

connection = None

path = dirname(abspath(__file__)) + "/"
logfile = None
log_file_size = 20
log = []

username = ""
password = ""


def logging():
    """handle logging to text file"""
    global logfile, log

    # open logfile
    logfile = open(path + "log.txt", "r+")
    for line in logfile:
        log.append(line.rstrip())

    # delete old log
    if len(log) == log_file_size:
        log.pop(0)
        log.pop(0)


def ready_login():
    """read email, pass & establish connection"""
    global username, password, connection

    # read file to get email and password
    try:
        fin = open(path + "account.txt", "r")
        username = percent_encode(fin.readline().strip())
        password = percent_encode(fin.readline().strip())
        fin.close()
    except IOError:
        log.append("    ERROR Unable to read account file")
        finish(1)

    # establish connection
    try:
        connection = HTTPConnection("127.0.0.1:1998", timeout=5)
    except timeout:
        log.append("    ERROR Connection time out")
        finish(1)


def check_mega_net():
    """determine whether this is MegaNet network or not"""
    # header of getting login page request
    headers = {
        "Host": "192.168.1.5:1998",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate",
        "Cache-Control": "no-cache",
        "Pragma": "no-cache",
        "Connection": "keep-alive",
    }

    # test whether login page available
    try:
        connection.request("GET", "/wifi/pre_login?referral=http://detectportal.firefox.com/success.txt",
                           headers=headers)
        response = connection.getresponse()
        if response.reason != "OK":
            raise HTTPException
    except HTTPException:
        log.append("    ERROR A problem occurred when sending test request")
        finish(1)
    except timeout:
        log.append("    Network is not MegaNet or already login")
        finish(1)


def login():
    """send user name and password to login"""
    # header & body of request
    body = "username=" + username + "&password=" + password
    headers = {
        "Host": "127.0.0.1:1998",
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
        print response.read()
    except timeout:
        log.append("    Response time out")
        finish(1)
    else:
        if response.status == 302:
            s = "    Successfully log in!"
        else:
            s = "    " + str(response.status) + " " + response.reason
        print response
        log.append(s)
        finish(0)


def finish(exit_code):
    """ clean up before quit"""
    try:
        # close connection
        connection.close()

        # write to log file
        if logfile is not None:
            logfile.seek(0, 0)
            logfile.write("\r\n".join(log))
            logfile.write("\r\n")
            logfile.close()
    finally:
        exit(exit_code)
