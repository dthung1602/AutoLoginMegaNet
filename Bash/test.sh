#!/bin/bash

email='duongthanhhung1998@yahoo.com.vn'
password='thanhhung1998'
redirect='https://meganet.com.vn'

curl http://10.20.0.1:3992/wifi/pre_login \
             --connect-timeout 5 \
             --max-time 15 \
             -H "Host: 10.20.0.1:3992" \
             -H "Referer: http://10.10.0.1:3992/wifi/pre_login/"\
             -H "Content-Type: application/x-www-form-urlencoded" \
             -H "Connection: keep-alive" \
             -H "Upgrade-Insecure-Requests: 1"\
             --data-urlencode "username=${email}" \
             --data-urlencode "password=${password}" \
             --data-urlencode "redirect=${redirect}";
