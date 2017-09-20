#! python


# -----------------------------------------------
# Automatically login to MegaNet networks
# Last update: September 17, 2017
# Version: 2.0
# Reference: http://www.fadvisor.net/blog/2012/06/autologin-to-open-wifi/
# -----------------------------------------------


from httplib import HTTPConnection
from os.path import dirname, abspath
from urllib import quote_plus as percent_encode


path = dirname(abspath(__file__)) + "/"

# read file to get email and password
fin = open(path + "account.txt", "r")
username = percent_encode(fin.readline().strip())
password = percent_encode(fin.readline().strip())
fin.close()

# establish connection
connection = HTTPConnection("10.10.0.1:3992", timeout=10)

# header & body of request
body = "username=" + username + "&password=" + password + "&redirect="
headers = {
    "Host": "10.10.0.1:3992",
    "Referer": "http://10.10.0.1:3992/wifi/pre_login/",
    "Content-Type": "application/x-www-form-urlencoded",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
}

# send request
connection.request("POST", "/wifi/login", body, headers)
response = connection.getresponse()
print response.status
print response.read()
connection.close()
