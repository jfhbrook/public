var spawn = require('child_process').spawn;

var nodeTail = require('tailing-stream').createReadStream,
    which = require('which').sync;

module.exports = function tail(p) {
  var useNode = false;
  try {
    which('tail');
  }
  catch (err) {
    useNode = true;
  }

  if (useNode) {
    return nodeTail(p, { timeout: false });
  }
  else {
    var tail = spawn('tail', [ '-fn', '1' ]);
    tail.stdout.stderr = tail.stderr;
    return tail.stdout;
  }
};
