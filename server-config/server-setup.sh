#!/bin/sh

#args
USER_HOME=$(getent passwd $SUDO_USER | cut -d: -f6)
APP_PATH="/home/pi"
USER=$SUDO_USER
LIST_OF_MAIN_APPS="git python3-astral python3-picamera python3-smbus"

#install apps
apt-get update  # To get the latest package lists
apt-get install -y $LIST_OF_MAIN_APPS

#get repo from github
git clone https://github.com/marsmith/gage-cam

#configure raspbian
raspi-config nonint do_change_locale en_US.UTF-8
raspi-config nonint do_configure_keyboard us
raspi-config nonint do_boot_splash 0
systemctl enable ssh
systemctl start ssh

#enable camera
sed -i "s/start_x=0/start_x=1/g" /boot/config.txt

echo "'Finished configuring gage-cam'\n"

echo "'Please change the user password NOW'\n"