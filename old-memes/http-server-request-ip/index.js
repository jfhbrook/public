module.exports = function requestIPAddress(req) {
  return ( req.headers["X-Forwarded-For"]
    || req.headers["x-forwarded-for"]
    || req.client.remoteAddress );
};

var getAccept = function (req) {
  //I found this regexp on stack overflow.
  //It's no real parser but probably good enough.
  return req.headers.accept.match(/([^()<>@,;:\\"\/[\]?={} \t]+)\/([^()<>@,;:\\"\/[\]?={} \t]+)/)[0];
}
