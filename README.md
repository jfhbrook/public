# sendgrid-web

Send emails with [sendgrid](http://sendgrid.com) and node.js! This sendgrid module (there are others) uses their JSON web API and the [request](https://github.com/mikeal/request) module.

## Install:

    npm install sendgrid-web

## Example:

``` js
    var Sendgrid = require("sendgrid-web");

    var sendgrid = new Sendgrid({
      user: "josh.holbrook@gmail.com",
      key: "oh, like you need to know."
    });

    sendgrid.send({
      to: 'josh.holbrook@gmail.com',
      from: 'josh.holbrook@gmail.com',
      subject: 'Hello world!',
      html: '<h1>Hello world!</h1>'
    }, function (err) {
      if (err) {
        console.log(err);
      } else {
        console.log("Success.");
      }
    });
```

## Usage:

### new Sendgrid(credentials)

This constructor creates a new sendgrid object. The "credentials" object should contain:

* `user`: Your sendgrid username
* `key`: Your sendgrid API key/password

### sendgrid.send(options, cb)

Sends an email. Options are the same as those of the [sendgrid json web api](http://sendgrid.com/documentation/display/api/WebMail). Common ones include:

* **to:** The recipient of the email.
* **from:** The email address to reply back to.
* **subject:** The subject of the email.
* **html:** The body of the email, if it's intended to be treated like html.
* **text:** The body of the email, if it's intended to be treated like plaintext.

## Tests:

In order to run the tests, sendgrid needs a user, api key, and email addresses to send to and from. Before running these tests, open `./test/config-template.json`, edit it to contain your credentials and information, and save it as `./test/config.json`.

Then, you may run the tests with nodeunit:

    nodeunit test/*.js

**Author:** Joshua Holbrook
