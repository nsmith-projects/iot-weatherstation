import board
import digitalio
import busio
import time
import math as math
import adafruit_bme280
import nanocamera as nano
import cv2
import boto3
from botocore.exceptions import NoCredentialsError
from datetime import date, datetime
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

ACCESS_KEY = 'AKIAJFCLOCFVYKB534IQ'
SECRET_KEY = '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'

def upload_to_aws(local_file, bucket, s3_file):
    s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY,
                      aws_secret_access_key=SECRET_KEY)

    try:
        s3.upload_file(local_file, bucket, s3_file)
        print("Upload Successful")
        return True
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False

#this initializes a CSI camera device
#camera = nano.Camera(flip=0,width=640,height=480,fps=30)

#this initializes a USB camera device
camera = nano.Camera(camera_type=1,device_id=1,width=640,height=480,fps=30)

myMQTTClient = AWSIoTMQTTClient("JetsonNano")
myMQTTClient.configureEndpoint("a2mzhorq6795m9-ats.iot.us-east-2.amazonaws.com", 8883)
myMQTTClient.configureCredentials("AmazonRootCA1.pem", "902d95efbc-private.pem.key", "902d95efbc-certificate.pem.crt")
myMQTTClient.configureOfflinePublishQueueing(-1)  
myMQTTClient.configureDrainingFrequency(2)  
myMQTTClient.configureConnectDisconnectTimeout(10)  
myMQTTClient.configureMQTTOperationTimeout(5) 

allowedConnectingTime = time.time() + 10

if time.time() < allowedConnectingTime:  
    myMQTTClient.connect()
    myMQTTClient.publish("thing/test", "connected", 0)
    print("Weatherstation connected to AWS!")
else:
    print("Failed to connect to AWS.")

i2c = busio.I2C(board.SCL, board.SDA)
bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c,0x76)

while True:
	#read in an image from the camera
	img = camera.read()
	#write image to SD card in local directory
	cv2.imwrite('snapshot.png',img)
	time.sleep(1)
	
	#upload image to amazon s3 in specified public bucket
	upload_to_aws('snapshot.png', 'weatherstationbucket', 'snapshot.png')

	#grab the current date & time
	now = datetime.now()
	#format the date and time
	current_time = now.strftime('%A, %B %d %Y %H:%M:%S')
	
	#read in the temperature from the sensor
	temperature = bme280.temperature
	#cut off the trailing decimal point numbers
	temperature = math.trunc(temperature)
	print("Temperature: %s C" % temperature)
	
	#read in the humidity from the sensor
	humidity = bme280.humidity
	humidity = math.trunc(humidity)
	print("Humidity: %s%%" % humidity)
	
	#read in the atmospheric pressure from the sensor
	pressure = bme280.pressure
	pressure = math.trunc(pressure)
	print("Pressure: %s hPa" % pressure)
	
	#construct the payload to send to amazon AWS IoT
	payload = '{ "timestamp": "' + current_time + '","temperature": ' + str(temperature) + ',"humidity": '+ str(humidity) + ', "pressure": '+ str(pressure) +'}'
	#publish the payload to AWS IoT topic
	myMQTTClient.publish("thing/test", payload, 0)
	print(payload)
	
	#wait before starting over again
	time.sleep(60)

#camera.release()
#del camera
    
