#! python

"""
    Run when network is up
"""

from httplib import HTTPConnection
from os.path import dirname, abspath
from urllib import quote as percent_encode

path = dirname(abspath(__file__)) + "/"

# read file to get email and password
fin = open(path + "account.txt", "r")
username = percent_encode(fin.readline().strip())
password = percent_encode(fin.readline().strip())
redirect = percent_encode("https://meganet.com.vn")
fin.close()

# establish connection
connection = HTTPConnection("10.10.0.1:3992", timeout=10)

# header & body of request
body = "username=" + username + "&password=" + password + "&redirect=" + redirect
headers = {
    "Host": "10.10.0.1:3992",
    "Referer": "http://10.10.0.1:3992/wifi/pre_login/",
    "Content-Type": "application/x-www-form-urlencoded",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
}

# send request
connection.request("POST", "/wifi/login", body, headers)
connection.close()
