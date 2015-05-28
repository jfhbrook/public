var five = require('johnny-five');
var Spark = require('spark-io');

var rudder = require('./rudder');
var sail = require('./sail');

var board = new five.Board({
  io: new Spark({
    token: process.env.SPARK_TOKEN,
    deviceId: process.env.SPARK_DEVICE_ID
  })
});

board.on('ready', function() {
  rudder(board, 'D0');
  sail(board, 'D1');
});
