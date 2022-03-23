exports.kronecker = function (x,y) {
  return Number(x === y);
}

exports.sgn = function(x) {
  return Boolean(x) * Math.pow(-1, x < 0);
}
