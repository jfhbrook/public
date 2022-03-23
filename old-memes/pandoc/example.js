#!/usr/bin/env node

var pandoc = require('../lib/pandoc'),
    fs = require('fs');

pandoc
  .from('markdown')
  .to('latex')
  .render(fs.createReadStream('./example.md'), function (err, res) {
    console.log(res);
  })
;
