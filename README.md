
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
  - Rasbian OS image (tesed using **July 2019** release) [here](https://www.raspberrypi.org/downloads/raspbian/)
  - Raspberry Pi image flashing software Etcher [here](https://etcher.io)

## Install raspbian

Follow steps from raspbian installation guide [here](https://www.raspberrypi.org/documentation/installation/installing-images/README.md)

- Flash image to microSD card using Etcher.io
- Insert microSD card into pi and plug in

## Configure raspbian

Once the pi has booted, log in using: user `pi` password `raspberry`

Run `sudo raspi-config` to run raspberry pi config wizard:

- change user password
- enable SSH

Run setup script
`wget https://raw.githubusercontent.com/marsmith/gage-cam/master/server-config/server-setup.sh`

### Set static IP on raspberry pi
Edit the dhcpcd conf: `sudo nano /etc/dhcpcd.conf`

Add or uncomment the following:
```
interface eth0

static ip_address=166.252.48.111/24
static routers=166.252.48.112
static domain_name_servers=166.252.48.112
```

### Set script to run on startup
https://raspberrypi.stackexchange.com/questions/54416/running-a-command-on-pi-boot-after-ip-is-assigned
https://raspberrypi.stackexchange.com/questions/93538/run-a-system-startup-script-after-network-and-dns-resolution-are-available

Create new service file: `sudo touch /etc/systemd/system/capture.service`
Edit file and add the following: `sudo nano /etc/systemd/system/capture.service`

```
[Unit]
Description=This service runs an image capture script after network is up
Wants=network-online.target
After=network-online.target

[Service]
Type=oneshot
User=pi
ExecStart=/usr/bin/python3 /home/pi/gage-cam/camera/capture_one.py

[Install]
WantedBy=multi-user.target
```

Restart daemon: `sudo systemctl daemon-reload`
Start service on boot: `sudo systemctl enable capture`

### How to manually copy images from remote pi server to local machien
`scp -r pi@166.252.48.111:/home/pi/gage-cam/camera/images c:\NYBackup\GitHub\gage-cam\camera\images\`

### Boot config settings
###Set GPIO pin to high for power device

`sudo nano /boot/config.txt` then add the following at the end:

```bash
#dtoverlay=gpio-poweroff,active_high,gpiopin=26
dtoverlay=pi3-disable-bt
dtoverlay=pi3-disable-wifi
```

### Disable unneeded features for battery consumption

Add lines boot configuration file
`sudo nano /boot/config.txt` then add the following:

```bash
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


### Power consumption notes
Raspian Stretch lite fresh boot, HDMI, keyboard and mouse: 150 Milliamps

Same with Enabled Camera, SSH in raspi-config:  150 Milliamps

Same with Enabled Wifi in raspi-config: 170 Milliamps

Same with bluetooth disabled: 170 Milliamps

Same with LED disabled: 170 Milliamps

Same with HDMI disabled: 160 Milliamps

Same with HDMI disabled, Keyboard and mouse unplugged: 80-90 Milliamps

upload file with curl:
curl -F 'fileToUpload=@/mnt/c/Users/marsmith/Desktop/IMG_20190607_142957.jpg' https://ny.water.usgs.gov/maps/gage-cam/upload-as-file.php