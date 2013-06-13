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
  t.equal(parsed.status, 200, 'we have a status code!');
  t.equal(parsed.body_bytes_sent, 2326, 'we have bytes sent!');
  t.end();
});
