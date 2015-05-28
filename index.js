var five = require('johnny-five');
var Spark = require('spark-io');
var heya = require('heya');

var Driver = require('./driver');

var io = new Spark({
  token: process.env.SPARK_TOKEN,
  deviceId: process.env.SPARK_DEVICE_ID
});

heya.create({
  controller: new heya.controllers.WebKeyboard(),
  driver: new Driver({ io: io })
});
