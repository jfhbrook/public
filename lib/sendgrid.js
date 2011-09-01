var url = require('url'),
    request = require('request');


module.exports = function(credentials) {
  var options = credentials;

  this.send = function(opts, cb) {

    opts.api_user = credentials.user;
    opts.api_key = credentials.key;

    request({
      url: url.format({
        protocol: 'https:',
        slashes: true,
        hostname: 'sendgrid.com',
        query: opts,
        pathname: '/api/mail.send.json' 
      }),
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
