from time import sleep
import subprocess, os, requests, datetime
 
 
class Timelapse:
    def __init__(self):
        self.imageLocation = '/home/pi/gage-cam/images'
        self.captureInterval = 300
        self.uploadURL = 'https://ny.water.usgs.gov/maps/gage-cam/upload-to-database.php'
        #call main function
        self.continuousCaptureImage()
 
    def getDateTime(self):
        return(str(datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S")))
 
    def continuousCaptureImage(self):
        if not os.path.exists(self.imageLocation):
            os.makedirs(self.imageLocation)
        while True:
            print 'STARTING IMAGE CAPTURE'
            filename = '{}/{}-Continuous.jpg'.format(self.imageLocation, self.getDateTime())
            command = 'fswebcam -i 0 -d v4l2:/dev/video0 -r 1280x720 --fps 10 -S 2 --jpeg 100 --shadow --title "gage-cam" --subtitle "Ruler Test #1" --info "Troy, NY" --save ' + filename
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
 
            process.wait()
            
            date_time_string = str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            print 'DATE',date_time_string
            files = {'fileToUpload': open(filename, 'rb')}
            values = {'site_id': 'martysOffice', 'date_time': date_time_string,'water_level': None}
            print 'STARTING IMAGE UPLOAD', values
            r = requests.post(self.uploadURL, files=files, data=values)
            print r.text
            sleep(self.captureInterval) # Wait
 
Timelapse()
