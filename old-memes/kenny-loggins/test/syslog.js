var tap = require('tap');

var syslog = require('../syslog');

tap.equal(syslog.toSyslog('fatal'), 2);
tap.equal(syslog.toSyslog('debug'), 7);

tap.equal(syslog.fromSyslog(1), 'fatal');
tap.equal(syslog.fromSyslog(2), 'fatal');
tap.equal(syslog.fromSyslog(3), 'error');
tap.equal(syslog.fromSyslog(4), 'warn');
tap.equal(syslog.fromSyslog(5), 'warn');
tap.equal(syslog.fromSyslog(6), 'info');
tap.equal(syslog.fromSyslog(7), 'debug');
