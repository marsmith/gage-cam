from picamera import PiCamera
import os
import datetime
import logging
import time

# set up logging
logging.basicConfig(
    filename='./camera.log', level=logging.DEBUG,
                    format='%(asctime)s %(levelname)-10s %(processName)s %(name)s %(message)s')
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)


class Capture:

    def __init__(self):
        self.imageLocation = './images'
        self.phpPath = 'https://ny.water.usgs.gov/maps/gage-cam/'
        self.uploadToDBURL = self.phpPath + 'upload-to-database.php'
        self.uploadToFileURL = self.phpPath + 'upload-as-file.php'
        self.piVoltage = 0
        self.piCurrent = 0

        # call main function
        self.getPiPower()

    def getDateTime(self):
        return(str(datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S")))

    def getPiPower(self):

        try:
            import smbus
            bus = smbus.SMBus(1)
            WITTYPI_ADDRESS = 0x69
            I2C_VOLTAGE_OUT_I = 3
            I2C_VOLTAGE_OUT_D = 4
            I2C_CURRENT_OUT_I = 5
            I2C_CURRENT_OUT_D = 6

            #get voltage
            v_i = bus.read_byte_data(WITTYPI_ADDRESS,I2C_VOLTAGE_OUT_I)
            v_d = bus.read_byte_data(WITTYPI_ADDRESS,I2C_VOLTAGE_OUT_D)
            self.piVoltage = v_i + (v_d/100)

            #get current
            c_i = bus.read_byte_data(WITTYPI_ADDRESS,I2C_CURRENT_OUT_I)
            c_d = bus.read_byte_data(WITTYPI_ADDRESS,I2C_CURRENT_OUT_D)
            self.piCurrent = c_i + (c_d/100)

            logging.info('pi power usage | Vout: ' + str(self.piVoltage) + 'V, Iout: ' + str(self.piCurrent) + 'A')

        except:
            logging.error("Power capture failed")
        finally:
            self.singleCaptureImage()        

    def singleCaptureImage(self):
        if not os.path.exists(self.imageLocation):
            os.makedirs(self.imageLocation)

        filename = '{}/{}-Capture.jpg'.format(
            self.imageLocation, self.getDateTime())

        try:
            # need to turn on LEDs if between sunset and dawn

            #run self.checkforDark() here if needed
            if (1 == 2):

                logging.info("Its too dark, skipping photo capture")
                return

            # otherwise just normal capture
            else:
                logging.info("No LED needed taking normal photo")

                 # capture image
                camera = PiCamera()
                #camera.resolution = (3280, 2464)
                #camera.resolution = (1024, 768)
                camera.resolution = (1600, 1200)

                # Camera warm-up time
                time.sleep(2)

                # capture image
                camera.capture(filename)

                camera.close()

                logging.info("Captured Image: " + filename)
            pass
        except:
            logging.error("Image capture failed")
        finally:
            logging.info("Starting image upload")

            # upload
            self.emailFile(filename)

    def emailFile(self, filename):
        #https://www.geeksforgeeks.org/send-mail-attachment-gmail-account-using-python/

        # Python code to illustrate Sending mail with attachments 
        # from your Gmail account  

        # libraries to be imported 
        import smtplib 
        from email.mime.multipart import MIMEMultipart 
        from email.mime.text import MIMEText 
        from email.mime.base import MIMEBase 
        from email import encoders
        import secrets

        fromaddr = "martynjsmith@gmail.com"
        toaddr = "martynjsmith@gmail.com"

        # instance of MIMEMultipart 
        msg = MIMEMultipart() 

        # storing the senders email address   
        msg['From'] = fromaddr 

        # storing the receivers email address  
        msg['To'] = toaddr 

        # storing the subject  
        msg['Subject'] = "Image captured: " + os.path.basename(filename)

        # string to store the body of the mail 
        body = 'pi power usage | Vout: ' + str(self.piVoltage) + 'V, Iout: ' + str(self.piCurrent) + 'A'

        # attach the body with the msg instance 
        msg.attach(MIMEText(body, 'plain')) 

        # open the file to be sent  
        #filename = "File_name_with_extension"
        attachment = open(filename, "rb") 

        # instance of MIMEBase and named as p 
        p = MIMEBase('application', 'octet-stream') 

        # To change the payload into encoded form 
        p.set_payload((attachment).read()) 

        # encode into base64 
        encoders.encode_base64(p) 

        p.add_header('Content-Disposition', "attachment; filename= %s" % filename) 

        # attach the instance 'p' to instance 'msg' 
        msg.attach(p) 

        # creates SMTP session 
        s = smtplib.SMTP('smtp.gmail.com', 587) 

        # start TLS for security 
        s.starttls() 

        # Authentication 
        s.login(fromaddr, secrets.password) 

        # Converts the Multipart msg into a string 
        text = msg.as_string() 

        # sending the mail 
        s.sendmail(fromaddr, toaddr, text) 

        # terminating the session 
        s.quit() 

    def checkForDark(self):

        from astral import Astral

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
