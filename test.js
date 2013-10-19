var tap = require('tap');

var parse = require('./index');

tap.test('parsing this example from the apache guys totally works', function (t) {

  var parsed = parse(
    '127.0.0.1 - frank [10/Oct/2000:13:55:36 -0700] "GET /apache_pb.gif HTTP/1.0" 200 2326'
  );

  t.equal(parsed.remote_addr, '127.0.0.1', 'we have an ip address!');
  t.equal(parsed.remote_user, 'frank', 'we have a user!');
  t.type(parsed.time_local, Date, 'we have a date!');
  t.equal(parsed.request, 'GET /apache_pb.gif HTTP/1.0', 'we have a request!');
  t.equal(parsed.http_method, 'GET', 'we have an http method!');
  t.equal(parsed.status, 200, 'we have a status code!');
  t.equal(parsed.body_bytes_sent, 2326, 'we have bytes sent!');

  // Check timezone consistency of parser by constructing a line with the
  // current local time so we can predict what ought to happen
  var now = new Date();
  var months = [
    'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
  ];
  // Sign in standard string representations is REVERSED from sign in JavaScript:
  // http://stackoverflow.com/questions/1091372/getting-the-clients-timezone-in-javascript/1091399#1091399
  var sign = now.getTimezoneOffset() > 0 ? '-' : '+';
  var abs = Math.abs(now.getTimezoneOffset());
  var line = '127.0.0.1 - frank [' + pad(now.getDate(), 2) + '/' + months[now.getMonth()] + '/' + now.getFullYear() + ':' + pad(now.getHours(), 2) + ':' + pad(now.getMinutes(), 2) + ':' + pad(now.getSeconds(), 2) + ' ' + sign + pad(Math.floor(abs / 60), 2) + pad(abs % 60, 2) + '] "GET /apache_pb.gif HTTP/1.0" 200 2326';
  parsed = parse(line);
  // Milliseconds are not represented in the log format, so round them off
  t.equal(Math.floor(parsed.time_local.getTime() / 1000.0), Math.floor(now.getTime() / 1000.0), 'Dates and timezones are parsed correctly!');
  t.end();
});

function pad(s, n) {
  s = s.toString();
  while (s.length < n) {
    s = '0' + s;
  }
  return s;
}
