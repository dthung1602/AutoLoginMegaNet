#!/bin/bash

#
#   uninstall script for MegaNet auto login
#   reference: https://unix.stackexchange.com/questions/28791/prompt-for-sudo-password-and-programmatically-elevate-privilege-in-bash-script
#


# check for super user privilege
if [ $EUID != 0 ]; then
    sudo "$0" "$@"
    exit $?
fi

script="/etc/NetworkManager/dispatcher.d/00auto-login-meganet.sh"

# remove main script
if ! rm ${script}; then
    echo "ERROR: can not remove ${script}"
    echo "Uninstall failed."
    exit 1
fi

echo "Uninstall finished successfully!"
