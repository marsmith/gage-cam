
from time import sleep
from picamera import PiCamera
import os, requests, datetime, logging

logging.basicConfig(filename='/home/pi/gage-cam/camera/camera.log', level=logging.DEBUG, format = '%(asctime)s %(levelname)-10s %(processName)s %(name)s %(message)s')
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)

class Capture:
    def __init__(self):
        self.imageLocation = '/home/pi/gage-cam/camera/images'
        self.phpPath = 'https://ny.water.usgs.gov/maps/gage-cam/'
        self.uploadToDBURL = self.phpPath + 'upload-to-database.php'
        self.uploadToFileURL = self.phpPath + 'upload-as-file.php'

        #call main function
        self.singleCaptureImage()

    def getDateTime(self):
        return(str(datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S")))

    def singleCaptureImage(self):
        if not os.path.exists(self.imageLocation):
            os.makedirs(self.imageLocation)

        if (self.checkForDark()):
            logging.info("Skipping image capture because its dark: " + filename)
            return

        logging.info("It's not dark, starting image capture")

        filename = '{}/{}-Capture.jpg'.format(self.imageLocation, self.getDateTime())

        #capture image
        camera = PiCamera()
        camera.resolution = (1024, 768)

        # Camera warm-up time
        sleep(2)
        try:
		camera.capture(filename)
		pass
        except:
		logging.error("Image capture failed")
        finally:
		camera.close()

        logging.info("Captured Image: " + filename)

        #create upload body
        file_to_upload = {'fileToUpload': open(filename, 'rb')}

        logging.info("Starting image upload")

        #upload
        #self.uploadToDB(file_to_upload)
        self.uploadToFile(file_to_upload)

    def uploadToDB(self, file_to_upload):

        #time string for database
        date_time_string = str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        #add values
        values = {'site_id': 'martysOffice', 'date_time': date_time_string,'water_level': None}

        #start upload
        r = requests.post(self.uploadToDBURL, files=files, data=values)
        if r:
		logging.info("Image successfully uploaded to database")
        else:
		'UPLOAD UNSUCCESSFUL', r.text
		logging.error("Database upload unsuccessful: " + r.status_code)

    def uploadToFile(self, file_to_upload):

        #start upload
        r = requests.post(self.uploadToFileURL, files=file_to_upload)
        if r:
		logging.info("Image successfully uploaded as file")
        else:
		logging.error("File upload unsuccessful: " + r.status_code)

    def checkForDark():
        start = datetime.time(22, 0, 0)
        end = datetime.time(4, 0, 0)
        now = datetime.datetime.now().time()
        if start <= end:
            return start <= now <= end
        else:
            return start <= now or now <= end


#call main class
Capture()
