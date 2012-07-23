var url = require('url'),
    request = require('request');


var Sendgrid = module.exports = function (credentials) {
  var creds = this.creds = credentials || {};
  creds.user = creds.username || creds.user;

  if (!creds.user) {
    throw new Error('sendgrid-web requires a user.');
  }
  if (!creds.key) {
    throw new Error('sendgrid-web requires a key.');
  }
};

Sendgrid.prototype.send = function (opts, cb) {

  var sendgrid = this,
      multipart = [];

  multipart.push({
    'Content-Disposition': 'form-data; name="api_user"',
    body: sendgrid.creds.user
  });

  multipart.push({
    'Content-Disposition': 'form-data; name="api_key"',
    body: sendgrid.creds.key
  });

  Object.keys(opts).forEach(function (key) {
    if (opts[key] instanceof Array) {
      for (var i = 0; i < opts[key].length; i++) {
        multipart.push({
          'Content-Disposition': 'form-data; name="' + key + '[]"',
          body: opts[key][i]
        });
      }
    } else {
      multipart.push({
        'Content-Disposition': 'form-data; name="' + key + '"',
        body: opts[key]
      });
    }
  });

  request({
    url: url.format({
      protocol: 'https:',
      slashes: true,
      hostname: 'sendgrid.com',
      pathname: '/api/mail.send.json',
    }),
    method: 'POST',
    multipart: multipart,
    headers: { 'content-type': 'multipart/form-data' }
  }, function (err, response, body) {
    var returned;

    // If there's no immediate error, try to parse the json, and if there was
    // an error on sendgrid's end, propogate it.

    if (err) {
      cb(err);
    } else {
      try {
        returned = JSON.parse(body);
      } catch (e) {
        return cb(e);
      }

      if (returned.message === "error") {
        cb(new Error(returned.errors));
      } else {
        cb(null);
      }
    }
  });
}
