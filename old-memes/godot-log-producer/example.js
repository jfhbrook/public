var godot = require('godot'),
    logProducer = require('./index');

//
// I've ran this on my VPS with some success.
// One size does not fit all.
//
godot.createClient({
  type: 'tcp',
  producers: [
    logProducer({
      host: 'swablu',
      service: 'log/jesusabdullah.net',
      description: 'nginx logs for jesusabdullah.net',
      file: '/var/log/nginx/jesusabdullah.net.log',
      ttl: 10000
    }),
    logProducer({
      host: 'swablu',
      service: 'log/panco-ak.com',
      description: 'nginx logs for panco-ak.com',
      file: '/var/log/nginx/panco-ak.com.log',
      ttl: 10000
    })
  ]
}).connect(1337);

