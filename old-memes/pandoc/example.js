#!/usr/bin/env node

var pandoc = require('.'),
    fs = require('fs');

pandoc
  .from('markdown')
  .to('latex')
  .render(fs.createReadStream('./README.md'), function (err, res) {
    console.log(res);
  })
;
