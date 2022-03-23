var range = require('lodash.range');

module.exports = function linspace(a,b,n) {
  var every = (b-a)/(n-1),
      ranged = range(a,b,every);

  return ranged.length == n ? ranged : ranged.concat(b);
}

