#! python

"""
        Uninstall script for auto login to megenet
"""

import os
import shutil
import subprocess

install_directory_path = "C:\Program Files\AutoLoginMeganet"

print "\n                  ---- AUTO LOGIN MEGANET UNINSTALL ----\n"
print "Auto login Meganet will be uninstalled from this computer"
print "Saved username(email) and password will also be deleted\n"

# confirm uninstall
choice = None
options = ['y', 'Y', 'n', 'N']
while choice not in options:
    choice = raw_input("Are your sure to uninstall? (y/n) ")

# if no then cancel
if choice in 'Nn':
    print "\nUninstall canceled by user"
    raw_input("Press enter to exit ...")
    exit(1)

# delete install directory
try:
    if os.path.exists(install_directory_path):
        shutil.rmtree(install_directory_path)
except Exception:
    print "ERROR: Can not delete folder %s" % install_directory_path
    print "Uninstall failed"
    exit(1)

# check whether task exist in task scheduler
stdout, stderr = subprocess.Popen('schtasks /TN "Auto Login MegaNet"', stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE).communicate()

# task exists
if stdout != '':
    output = os.system('schtasks /Delete /TN "Auto Login MegaNet" /f')

    if output != 0:
        print "ERROR: Can not delete task in task scheduler"
        print "Uninstall failed"
        exit(1)  # pause program before ending

print "\nUninstall finished successfully."
raw_input("Press enter to close ... ")
