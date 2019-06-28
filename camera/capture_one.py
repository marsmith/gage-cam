from picamera import PiCamera
from astral import Astral
import os
import requests
import datetime
import logging
import time

# set up logging
logging.basicConfig(
    filename='/home/pi/gage-cam/camera/camera.log', level=logging.DEBUG,
                    format='%(asctime)s %(levelname)-10s %(processName)s %(name)s %(message)s')
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

        # call main function
        self.singleCaptureImage()

    def getDateTime(self):
        return(str(datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S")))

    def singleCaptureImage(self):
        if not os.path.exists(self.imageLocation):
            os.makedirs(self.imageLocation)

        filename = '{}/{}-Capture.jpg'.format(
            self.imageLocation, self.getDateTime())

        # capture image
        camera = PiCamera()
        camera.resolution = (3280, 2464)

        # Camera warm-up time
        time.sleep(2)

        try:
            # need to turn on LEDs if between sunset and dawn
            if (self.checkForDark()):
                logging.info("Using LEDs for photo because its dark")

                #all LED settings here
                import smbus
                bus = smbus.SMBus(1)
                DEVICE_ADDRESS = 0x70
                LED_CONTROL_ALL_WHITE = 0x5a
                LED_CONTROL_ALL_IR = 0xa5
                LED_CONTROL_ALL = 0xFF
                LED_CONTROL_OFF = 0x00
                LED_GAIN_REGISTER = 0x09
                gain = 15
                bus.write_byte_data(DEVICE_ADDRESS, LED_GAIN_REGISTER, gain)
                bus.write_byte_data(DEVICE_ADDRESS, 0x00, LED_CONTROL_ALL_IR)
                time.sleep(2)

                #modify camera exposure for night
                camera.brightness = 50
                camera.sharpness = 50
                camera.saturation = -75
                camera.ISO = 800
                camera.shutter_speed = 2000000

                # capture image
                camera.capture(filename)

                #reset LED
                time.sleep(1)
                bus.write_byte_data(DEVICE_ADDRESS, LED_GAIN_REGISTER, 0b1000)
                bus.write_byte_data(DEVICE_ADDRESS, 0x00, LED_CONTROL_OFF)

            # otherwise just normal capture
            else:
                logging.info("No LED needed taking normal photo")
                # capture image
                camera.capture(filename)

            logging.info("Captured Image: " + filename)

            # create upload body
            file_to_upload = {'fileToUpload': open(filename, 'rb')}

            logging.info("Starting image upload")

            # upload
            # self.uploadToDB(file_to_upload)
            self.uploadToFile(file_to_upload)
            pass
        except:
            logging.error("Image capture failed")
        finally:
            camera.close()

    def uploadToDB(self, file_to_upload):

        # time string for database
        date_time_string = str(
            datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        # add values
        values = {'site_id': 'martysOffice', 'date_time':
                  date_time_string, 'water_level': None}

        # start upload
        r = requests.post(self.uploadToDBURL, files=files, data=values)
        if r:
            logging.info("Image successfully uploaded to database")
        else:
            'UPLOAD UNSUCCESSFUL', r.text
            logging.error("Database upload unsuccessful: " + r.status_code)

    def uploadToFile(self, file_to_upload):

        # start upload
        r = requests.post(self.uploadToFileURL, files=file_to_upload)
        if r:
            logging.info("Image successfully uploaded as file")
        else:
            logging.error("File upload unsuccessful: " + r.status_code)

    def checkForDark(self):

        # get dawn and sunset times
        city_name = 'Albany'
        a = Astral()
        a.solar_depression = 'civil'
        city = a[city_name]
        sun = city.sun(date=datetime.datetime.now(), local=True)

        start = sun['dusk'].replace(tzinfo=None)
        end = sun['dawn'].replace(tzinfo=None)
        now = datetime.datetime.now()

        # print(start,end,now)
        if start <= end:
            return start <= now <= end
        else:
            return start <= now or now <= end


# call main class
Capture()
