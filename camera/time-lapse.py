from time import sleep
from picamera import PiCamera
import os, requests, datetime
 
 
class Timelapse:
    def __init__(self):
        self.imageLocation = '/home/pi/gage-cam/camera/images'
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

            #capture image
            camera = PiCamera()
            camera.resolution = (1024, 768)

            # Camera warm-up time
            sleep(2)
            camera.capture(filename)
            camera.close()
            
            date_time_string = str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            print 'DATE',date_time_string
            files = {'fileToUpload': open(filename, 'rb')}
            values = {'site_id': 'martysOffice', 'date_time': date_time_string,'water_level': None}
            print 'STARTING IMAGE UPLOAD', values
            r = requests.post(self.uploadURL, files=files, data=values)
            if r:
                print 'UPLOAD TO SERVER WAS SUCCESSFUL'
            else:
                'UPLOAD UNSUCCESSFUL', r.text

            print 'WAITING',self.captureInterval,'FOR NEXT IMAGE...'
            sleep(self.captureInterval) # Wait
 
Timelapse()
