var pinocchio = require('pinocchio');

module.exports = function (err) {
  if (!(err instanceof Error)) { err = pinocchio(err); }

  var s = err.stack + '\n';

  Object.keys(err).forEach(function (k) {
    s += '\t* ' + k + ': ' + JSON.stringify(err[k]) + '\n';
  });

  return s;
}
