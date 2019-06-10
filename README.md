
# gage-cam

About project

## Requirements

  **Hardware** (Monitor and keyboard only necessary for initial setup):  
  - raspberry pi microSD card  
  - micro USB power supply  
  - HDMI cable  
  - monitor  
  - keyboard  


  **Software**: 
  - Rasbian OS image (tesed using **June 2018** release) [here](https://www.raspberrypi.org/downloads/raspbian/)
  - Raspberry Pi image flashing software Etcher [here](https://etcher.io)
  - Putty SSH Client (optional) [here](https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html)

## Install raspbian

Follow steps from raspbian installation guide [here](https://www.raspberrypi.org/documentation/installation/installing-images/README.md)

- Flash image to microSD card using Etcher.io
- Insert microSD card into pi and plug in

## Configure raspbian

Once the pi has booted, log in using: user `pi` password `raspberry`

Run `sudo raspi-config` to run raspberry pi config wizard:

- setup and enable wifi [optional] (network options)
- enable camera
- enable SSH for remote access (interface options)
- set keyboard layout (localization options)
- set timezone (localization options)
- require user to log in (boot options/ Desktop/CLI)

**Wireless config**:  
Use `raspi-config` tool network options

Reboot necessary after any network configuration change:  
`sudo reboot` 

Get your pi's IP address, record the IP address from the following command:    
`hostname -I`

## Use SSH for remaining configuration steps

Using your SSH client, enter the IP address found above to connect to your Pi:  
`ssh pi@192.168.1.195`

### Create a new user

Add a new user, and delete default 'pi' user:  
 `sudo adduser hawdis`

To make new user part of the sudo group:  
`sudo adduser hawdis sudo`  

Reboot:  
`sudo reboot`

Your SSH session will disconnect.  Wait a minute or two and login with Putty again as your new user:  
`ssh hawdis@192.168.1.195`

Delete 'pi' user:  
`sudo deluser --remove-home pi`  

### Install system wide app dependencies

Update rasbian:  
`sudo apt-get update` then `sudo apt-get upgrade`

### Disable unneeded features for battery consumption

Add lines boot configuration file
`sudo nano /boot/config.txt` then add the following:

```
#disable HDMI
hdmi_blanking=2

#disable bluetooth
dtoverlay=pi3-disable-bt

#disable wifi
dtoverlay=pi3-disable-wifi

#disable onboard LED
dtparam=act_led_trigger=none
dtparam=act_led_activelow=on
```

To disable HDMI:

Add `/usr/bin/tvservice -o` to `/etc/rc.local` to disable HDMI on boot. `/usr/bin/tvservice -p` to enable

### install and configure gage-cam

clone from github:  
`git clone https://github.com/marsmith/gage-cam`

### Set script to run on startup

### Power consumption notes
Raspian Stretch lite fresh boot, HDMI, keyboard and mouse: 150 Milliamps

Same with Enabled Camera, SSH in raspi-config:  150 Milliamps

Same with Enabled Wifi in raspi-config: 170 Milliamps

Same with bluetooth disabled: 170 Milliamps

Same with LED disabled: 170 Milliamps

Same with HDMI disabled: 160 Milliamps

Same with HDMI disabled, Keyboard and mouse unplugged: 80-90 Milliamps




