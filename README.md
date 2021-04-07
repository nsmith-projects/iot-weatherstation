# iot-weatherstation
Environment monitoring station developed in Python, Nodejs, and using Amazon's AWS IoT Core

School project undertaken to gain a working understanding of Amazon's AWS services, as well as an opportunity to dip my toes in to nodejs/python.
Our project group was fortunate enough to be provided with a nVidia Jetson Nano for use as our miniature IoT-connected weather station!

The python script loops on our Jetson Nano periodically taking snapshots of the environment conditions (temperature, humidity, pressure, and a photo) and publishing that as a 
JSON payload to AWS IoT. The webserver subscribes to our weatherstation topic to pull down that payload and parse the data for display on a simple web page.

Hardware used: nvidia Jetson Nano, BME280 Sensors, Camera, PC running the node webserver
Software libraries used: Adafruit BME280, OpenCV, nanocamera, awsIot, express

NOTE: Including your AWS certs and keys in your project files and in plain text should never be done! It was only done here for this school project as a means to an end, without
security being a thought. Amazon AWS offers their own technology that can be leveraged to avoid this, and is something that should be implemented.
