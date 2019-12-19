
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

### Set static IP on raspberry pi
Edit the dhcpcd conf: `sudo nano /etc/dhcpcd.conf`

Add or uncomment the following:
```
interface eth0

static ip_address=166.252.48.111/24
static routers=166.252.48.112
static domain_name_servers=166.252.48.112
```

## Configure raspbian

Once the pi has booted, log in using: user `pi` password `raspberry`

2 options:

#### Option 1 (scripted)
Run setup script
`wget https://raw.githubusercontent.com/marsmith/gage-cam/master/server-config/server-setup.sh`

--OR-- 

#### Option 2 (manual)

Run `sudo raspi-config` to run raspberry pi config wizard:

- change user password
- enable SSH
- enable camera
- change locale (en_US.UTF-8)
- change keyboard layout (generic 105 key US)

Install required apps:

```bash
sudo apt-get update
sudo apt-get install -y git python3-astral python3-picamera python3-smbus
git clone https://github.com/marsmith/gage-cam

```

### WittyPi setup info

#### WittyPi2
Install wittyPi: `wget http://www.uugear.com/repo/WittyPi2/installWittyPi.sh`
Run setup script: `sudo sh installWittyPi.sh`

#### WittyPi3
Install wittyPi: `wget http://www.uugear.com/repo/WittyPi2/install.sh`
Run setup script: `sudo sh install.sh`

#### WItty Pi create script to run every hour

create new schedule script to turn on 5 mins every hour.  In `/home/pi/wittyPi/schedules`:

```bash
cp on_5m_every_20m.wpi on_5m_every_60m.wpi
nano on_5m_every_60m.wpi
```

change `OFF  M515` to `OFF M55`

save and exit

Open wittyPi setup script: `sudo sh ./wittyPi.sh` and select your new schedule script

### Set script to run on startup

Edit file  `sudo nano /etc/rc.local` and add the following after `fi` and before `exit 0:`

```

/usr/bin/python3 /home/pi/gage-cam/camera/capture_one.py

```

### How to manually copy images from remote pi server to local machine
`scp -r pi@166.252.48.111:/home/pi/gage-cam/camera/images c:\NYBackup\GitHub\gage-cam\camera\images\`

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



#### Misc info

In the `/home/pi` there are 2 folders: `wittyPi` and `gage-cam`

The script `/home/pi/gage-cam/camera/capture_one.py` runs on startup via the `/etc/rc.local` startup script

WittyPi3 user manual: http://www.uugear.com/doc/WittyPi3_UserManual.pdf

Configure it you run: `sudo sh wittyPi.sh`  inside of `/home/pi/wittyPi`
The log i posted is from `/home/pi/wittyPi/wittyPi.log`

There is also a camera log from my script at: `/home/pi/gage-cam/camera/camera.log`