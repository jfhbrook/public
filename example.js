var LogProducer = require('./index');  

var prod = new LogProducer({
  file: '/var/log/syslog'
});

prod.on('data', function (d) {
  console.log(d);
});
