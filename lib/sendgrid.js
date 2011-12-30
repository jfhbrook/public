var url = require('url'),
    request = require('request');


module.exports = function(credentials) {
  this.send = function(opts, cb) {

    var multipart = [];

    multipart.push({ 'Content-Disposition': 'form-data; name="api_user"',
                     body: credentials.user });

    multipart.push({ 'Content-Disposition': 'form-data; name="api_key"',
                     body: credentials.key });

    for (var key in opts) {
      multipart.push({ 'Content-Disposition': 'form-data; name="' + key + '"',
                       body: opts[key] });
    }

    request({
      url: url.format({
        protocol: 'https:',
        slashes: true,
        hostname: 'sendgrid.com',
        pathname: '/api/mail.send.json',
      }),
      method: 'POST',
      multipart: multipart,
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
          cb(e);
        }

        if (returned.message === "error") {
          cb(new Error(returned.errors));
        } else {
          cb(null);
        }
      }
    });
  }
}
