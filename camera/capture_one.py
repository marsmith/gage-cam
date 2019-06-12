from time import sleep
from picamera import PiCamera
import os, requests, datetime
 
class Capture:
    def __init__(self):
        self.imageLocation = '/home/pi/gage-cam/camera/images'
        self.uploadURL = 'https://ny.water.usgs.gov/maps/gage-cam/upload-to-database.php'
        #call main function
        self.singleCaptureImage()
 
    def getDateTime(self):
        return(str(datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S")))
 
    def singleCaptureImage(self):
        if not os.path.exists(self.imageLocation):
            os.makedirs(self.imageLocation)

        print 'STARTING IMAGE CAPTURE'
        filename = '{}/{}-Capture.jpg'.format(self.imageLocation, self.getDateTime())

        #capture image
        camera = PiCamera()
        camera.resolution = (1024, 768)

        # Camera warm-up time
        sleep(2)
        camera.capture(filename)
        camera.close()
        
        #time string for database
        date_time_string = str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        #create upload body
        files = {'fileToUpload': open(filename, 'rb')}
        values = {'site_id': 'martysOffice', 'date_time': date_time_string,'water_level': None}
        print 'STARTING IMAGE UPLOAD', values

        #start upload
        r = requests.post(self.uploadURL, files=files, data=values)
        if r:
            print 'UPLOAD TO SERVER WAS SUCCESSFUL'
        else:
            'UPLOAD UNSUCCESSFUL', r.text
            
        print 'SCRIPT FINISHED'

Capture()
