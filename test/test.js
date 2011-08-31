var vows = require("vows"),
    assert = require("assert"),
    Sendgrid = require(__dirname + "/../lib/sendgrid"),
    fs = require("fs"),
    configFile = __dirname + "/config.json",
    config = JSON.parse(fs.readFileSync(configFile));

vows.describe("Sending emails with Sendgrid").addBatch({
  "When constructing a new sendgrid object,": {
    topic: function () {
      return new Sendgrid({
        user: config.user,
        key: config.key
      });
    },
    "The resulting object has a 'send' property": function (sendgrid) {
      assert.isTrue(Object.hasOwnProperty.call(sendgrid, "send"));
    },
    "This property is a function": function (sendgrid) {
      assert.equal(typeof(sendgrid.send), "function");
    },

    "and then calling it with legitimate options": {
      topic: function (sendgrid) {
        sendgrid.send({
          to: config.to,
          from: config.from,
          subject: 'This is a test of node-sendgrid.',
          html: "<h1> This is a test of node-sendgrid.</h1><p>If you are reading this, node-sendgrid was able to send your email properly.</p>"
        }, this.callback ); 
      },
      "Successfully sends an email without error": function (err) {
        assert.isNull(err);
      }
    }
  }
}).export(module);
