module.exports = function requestAccept(req) {
  // I found this regexp on stack overflow.
  // It's no real parser but probably good enough.
  return req.headers.accept.match(/([^()<>@,;:\\"\/[\]?={} \t]+)\/([^()<>@,;:\\"\/[\]?={} \t]+)/)[0];
}
