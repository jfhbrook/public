var tap = require('tap');

var verbosity = require('../minimist').verbosity;

tap.equal(verbosity({}, 'info'), 'info');
tap.equal(verbosity({v: true}, 'info'), 'debug');
tap.equal(verbosity({verbose: true}, 'info'), 'debug');
