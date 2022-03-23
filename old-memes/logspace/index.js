var linspace = require('linspace');

module.exports = function logspace(a,b,n) {
  return linspace(a,b,n).map(function(x) { return Math.pow(10,x); });
}
