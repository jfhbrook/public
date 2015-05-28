module.exports = function addSail(board, pin) {
  var setting = 0;
  var speed = 0.5;
  var t = 0.1;

  board.pinMode(pin, board.MODES.SERVO);

  var sail = board.sail = function(direction) {
    board.servoWrite(pin, direction * 90 + 90);
  };

  sail.halt = function() {
    sail(0);
  }

  sail.clockwise = sail.cw = function() {
    sail(-speed);
    setTimeout(sail.halt, 1000 * t);
  };

  sail.counterclockwise = sail.ccw = function() {
    sail(speed);
    setTimeout(sail.halt, 1000 * t);
  };

  sail.move = function(x, y) {
    if (y === 0) {
      // nothing :v
    }
    else if (y > 0) {
      sail.clockwise();
    }
    else {
      sail.counterclockwise();
    }
  };

};
