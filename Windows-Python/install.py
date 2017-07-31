#! python

"""
        Installation script for auto login to megenet
"""

import os
import shutil
import io
import time
import subprocess


##############################################################
#                Constants & Functions                       #
##############################################################

def error_of_command(cmd):
    stdout, stderr = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                      stderr=subprocess.STDOUT).communicate()
    if 'ERROR' in stdout:
        return stdout
    return None if stderr == '' else stderr


def exit_with_error(error):
    print error
    print "Installation failed"
    raw_input("Press enter to close ... ")
    exit(1)


install_directory_path = "C:\Program Files\AutoLoginMeganet"
user_name = os.environ['USERNAME'].strip()
computer_name = os.environ['COMPUTERNAME'].strip()
datetime = time.strftime("%Y-%m-%dT%H:%M:%S")

print "\n                  ---- AUTO LOGIN MEGANET INSTALLATION ----\n"
print "To update username(email) and/or password,"
print "edit file %s\\account.txt\n" % install_directory_path

##############################################################
#                     Create xml file                        #
##############################################################

try:
    print "Creating temporary xml file\n"
    fin = io.open("AUTO_LOGIN_MEGANET.xml", "r", encoding="utf-16-le")
    content = fin.read()
    fin.close()

    content = content.replace("__COMPUTER-NAME__", computer_name)
    content = content.replace("__USER-NAME__", user_name)
    content = content.replace("__DATETIME__", datetime)

    fout = io.open("tmp.xml", "w", encoding="utf-16-le")
    fout.writelines(content)
    fout.close()
except IOError as e:
    print e
    print "ERROR: Can not create temporary file 'tmp.xml'"
    print "Installation failed"
    exit(1)

##############################################################
#                  Create scheduled task                     #
##############################################################

# check whether task exist in task scheduler

# task doesn't exist
if error_of_command('schtasks /TN "Auto Login MegaNet"'):
    print "Creating new task in task scheduler\n"

# task exists
else:
    # get user option
    print "There has already been task name 'Auto Login MegaNet' in task scheduler"
    print "New installation will override old one"
    choice = None
    options = ['y', 'Y', 'n', 'N']
    while choice not in options:
        choice = raw_input("Do you want to continue installation? (y/n) ")

    # if no then cancel install
    if choice in 'nN':
        exit_with_error("\nInstallation canceled by user")

    # if yes then delete old task
    if error_of_command('schtasks /Delete /TN "Auto Login MegaNet" /f'):
        exit_with_error("ERROR: Can not delete task in task scheduler")

    print "Re-creating new task in task scheduler\n"  # creating new task

# create task
if error_of_command('schtasks /Create /TN "Auto Login MegaNet" /XML "tmp.xml"'):
    exit_with_error("ERROR: Can not create a new task in task scheduler")

##############################################################
#               Create install directory                     #
##############################################################

try:
    print "Creating install directory\n"
    if not os.path.exists(install_directory_path):
        os.mkdir(install_directory_path)
except OSError:
    exit_with_error("ERROR: Can not create folder %s" % install_directory_path)

# copy main program to install directory
try:
    print "Copying main program to install directory\n"
    shutil.copy2("AutoLoginMeganet-Windows.py", install_directory_path)
except IOError:
    exit_with_error("ERROR: Can not copy file 'AutoLoginMeganet-Windows.py' to %s" % install_directory_path)

# ask for login username(email) and password
email = raw_input("\nEnter Meganet username(email): ")
password = raw_input("Enter Meganet password       : ")

# save username and password to file
try:
    print "\nCreating account file"
    f = open(install_directory_path + "\\" + "account.txt", "w")
    f.writelines(email + '\r\n' + password)
    f.close()
except IOError:
    exit_with_error("ERROR: Can not create file 'account.txt' in %s" % install_directory_path)

# pause program before ending
print "\nInstallation finished successfully."
raw_input("Press enter to close ... ")
