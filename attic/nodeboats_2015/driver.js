var five = require('johnny-five');

var rudder = require('./rudder');
var sail = require('./sail');

var Driver = module.exports = function(options) {
  this._options = options || {};
};

Driver.prototype.connect = function(callback) {
  var options = this._options;
  var board = this.board = new five.Board({
    io: this._options.io,
    id: 'ss-duplicate-callback'
  });

  board.on('ready', function() {
    rudder(board, options.rudder || 'D0');
    sail(board, options.sail || 'D1');
    callback();
  });
};

Driver.prototype.move = function(x, y) {
  this.board.rudder.move(x, y);
  this.board.sail.move(x, y);
};
