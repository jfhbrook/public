module.exports = function addRudder(board, pin) {
  var setting = 0;
  var step = 0.3;

  board.pinMode(pin, board.MODES.SERVO);

  var rudder = board.rudder = function(direction) {
    if (Math.abs(direction) > 1) {
      direction = direction > 0 ? 1 : -1;
    }
    board.servoWrite(pin, direction * 90 + 90);
  };

  rudder.left = function() {
    setting += step;
    rudder(setting);
  };

  rudder.right = function() {
    setting -= step;
    rudder(setting);
  };

  rudder.straight = function() {
    setting = 0;
    rudder(setting);
  };
};
