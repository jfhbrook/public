var assert = require("assert"),
    Sendgrid = require(__dirname + "/../lib/sendgrid"),
    fs = require("fs"),
    configFile = __dirname + "/config.json",
    config = JSON.parse(fs.readFileSync(configFile)),
    sendgrid;

exports["Constructor returns object with send method"] = function (test) {
  sendgrid = new Sendgrid({
    user: config.user,
    key: config.key
  });

  test.ok(sendgrid.send);
  test.equal(typeof(sendgrid.send), "function");
  test.done();
};

exports["Given legitimate options, sends an email"] = function (test) {
  sendgrid.send({
    to: config.to,
    from: config.from,
    subject: 'This is a test of node-sendgrid.',
    html: "<h1> This is a test of node-sendgrid.</h1><p>If you are reading this, node-sendgrid was able to send your email properly.</p>"
  }, function (err) {
    test.equal(err, null);
    test.done();
  });
}

exports["Given bad options, returns an error"] = function (test) {
  sendgrid.send({
    to: config.to,
    from: config.from,
    subject: 'This is a test of node-sendgrid.',
    body: "<h1> This is a test of node-sendgrid.</h1><p>If you are reading this, node-sendgrid somehow send you an email when it should've broke.</p>"
  }, function (err) {
    test.equal(err.name, "Error");
    test.done();
  });
}
