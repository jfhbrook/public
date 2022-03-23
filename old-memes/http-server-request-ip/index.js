module.exports = function requestIPAddress(req) {
  return ( req.headers["X-Forwarded-For"]
    || req.headers["x-forwarded-for"]
    || req.client.remoteAddress );
};
