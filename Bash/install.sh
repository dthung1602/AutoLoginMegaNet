#!/bin/bash

#
#   install script for MegaNet auto login
#   reference: https://unix.stackexchange.com/questions/28791/prompt-for-sudo-password-and-programmatically-elevate-privilege-in-bash-script
#


# check for super user privilege
if [ $EUID != 0 ]; then
    sudo "$0" "$@"
    exit $?
fi

# function exit with error
function exit_with_error {
    echo $1
    echo "Installation failed."
    exit 1
}

# get username and password
echo -e "----  Auto login to MegaNet installation  ----\n"
echo -n "Enter username(email): "
read email
echo -n "Enter password: "
read password

# put username and password to main script
if ! cat auto-login-meganet.sh | sed "s/__EMAIL__/${email}/" | sed "s/__PASSWORD__/${password}/" > tmp.sh; then
    exit_with_error "ERROR: can not create customized login script from the original auto-login-meganet.sh"
fi

destination_script="/etc/NetworkManager/dispatcher.d/00auto-login-meganet.sh"

# copy main script to the right place
if ! cp tmp.sh ${destination_script}; then
    exit_with_error "ERROR: can not copy script to /etc/NetworkManager/dispatcher.d"
fi

# change privileges of script
if ! chmod 700 ${destination_script}; then
    exit_with_error "ERROR: can not change privileges of ${destination_script}"
fi

# remove tmp script
rm tmp.sh
echo -e "\nInstallation finished successfully!"
echo "This folder is not required for the main script to run."
echo "Re-run this installation script to change the username and/or password,"
