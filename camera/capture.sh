#!/bin/sh

DATEVAR=date +%Y-%m-%d_%H%M%S
PATH="/home/pi/gage-cam/camera/images"
FILENAME="$PATH/$DATEVAR-Capture.jpg"
TIME=$(date +%H:%M)

#do nighttime settings
if [[ "$TIME" > "22:00" ]] || [[ "$TIME" < "06:30" ]]; then
    raspistill -w 2592 -h 1944 -ISO 800 -ss 6000000 -br 80 -co 100 -o $FILENAME
#otherwise default camera settings
else
    raspistill -w 2592 -h 1944 -o $FILENAME
fi


#curl -F 'fileToUpload=@/mnt/c/Users/marsmith/Desktop/IMG_20190607_142957.jpg' https://ny.water.usgs.gov/maps/gage-cam/upload-as-file.php