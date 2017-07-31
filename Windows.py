
"""
    Run when there's a change in network
"""

# from Login import *
import time


f = open("E:\PYTHON\Workspace\AutoLogin\\tmp.txt", "a+")
f.write(time.ctime(time.time()) + "\n")
f.close()

# ready_login()
# check_mega_net()
# login()
