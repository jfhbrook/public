var fs = require('fs');

module.exports = function () {
  return fs.readdirSync(__dirname + '/licenses');
};
