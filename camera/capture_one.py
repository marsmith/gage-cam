from time import sleep
from picamera import PiCamera
import os, requests, datetime, logging
 
class Capture:
    def __init__(self):
        self.imageLocation = '/home/pi/gage-cam/camera/images'
        self.phpPath = 'https://ny.water.usgs.gov/maps/gage-cam/'
        self.uploadToDBURL = self.phpPath + 'upload-to-database.php'
        self.uploadToFileURL = self.phpPath + 'upload-as-file.php'

        #setup logging
        logging.getLogger().addHandler(logging.StreamHandler())
        logging.basicConfig(level = logging.INFO, filename = "camera.log", format = '%(asctime)s  %(levelname)-10s %(processName)s  %(name)s %(message)s')

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
        try:
            # do something with the camera
            camera.capture(filename)
            pass
        except:
            print 'IMAGE CAPTURE FAILED', values
            logging.error("Image capture failed")
        finally:
            camera.close()

        logging.info("Captured Image: " + filename) 

        print 'STARTING IMAGE UPLOAD', values

        #create upload body
        files = {'fileToUpload': open(filename, 'rb')}

        #upload
        #self.uploadToDB(files)
        self.uploadToFile(files)
        
    def uploadToDB(self, files):
        #time string for database
        date_time_string = str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        #add values
        values = {'site_id': 'martysOffice', 'date_time': date_time_string,'water_level': None}

        #start upload
        r = requests.post(self.uploadToDBURL, files=files, data=values)
        if r:
            print 'UPLOAD TO DATABASE WAS SUCCESSFUL'
            logging.info("Image successfully uploaded to database") 
        else:
            'UPLOAD UNSUCCESSFUL', r.text
            logging.error("Database upload unsuccessful: " + r.status_code) 
            
        print 'SCRIPT FINISHED'

    def uploadToFile(self, file):

        #start upload
        r = requests.post(self.uploadToFileURL, files=files)
        if r:
            print 'UPLOAD TO SERVER WAS SUCCESSFUL'
            logging.info("Image successfully uploaded as file") 
        else:
            'UPLOAD UNSUCCESSFUL', r.text
            logging.error("File upload unsuccessful: " + r.status_code) 
            
        print 'SCRIPT FINISHED'

Capture()
