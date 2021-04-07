var express = require('express');
var app = express();
var path = require("path");
var awsIot = require('aws-iot-device-sdk');

app.set("views", path.join(__dirname, "views")); 
app.set("view engine", "hbs"); 
app.use(express.static('assets'));

var device = awsIot.device({
   keyPath: "aws_auth/902d95efbc-private.pem.key",
  certPath: "aws_auth/902d95efbc-certificate.pem.crt",
    caPath: "aws_auth/AmazonRootCA1.pem",
  clientId: "WeatherWebApp",
      host: "a2mzhorq6795m9-ats.iot.us-east-2.amazonaws.com"
});

var timestamp;
var temperature;
var humidity;
var pressure;

device
  .on('connect', function() {
    console.log('Connected to AWS!');
    device.subscribe('thing/test');
	console.log('Subscribed to topic.');
  });

device
  .on('message', function(topic, payload) {
    console.log('message', topic, payload.toString());
	
	payload = JSON.parse(payload.toString());
	
	timestamp = payload.timestamp;
	temperature = payload.temperature;
	humidity = payload.humidity;
	pressure = payload.pressure;
  });

app.get("/", (req, res) => {
	res.render("index", { timestamp: timestamp, temperature: temperature, humidity: humidity, pressure: pressure });
});

app.listen(5000);