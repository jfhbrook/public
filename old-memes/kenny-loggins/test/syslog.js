var tap = require('tap');

var syslog = require('../syslog');

tap.equal(syslog.toSysLog('fatal'), 2);
tap.equal(syslog.toSysLog('debug'), 7);

tap.equal(syslog.fromSysLog(1), 'fatal');
tap.equal(syslog.fromSysLog(2), 'fatal');
tap.equal(syslog.fromSysLog(3), 'error');
tap.equal(syslog.fromSysLog(4), 'warn');
tap.equal(syslog.fromSysLog(5), 'warn');
tap.equal(syslog.fromSysLog(6), 'info');
tap.equal(syslog.fromSysLog(7), 'debug');
