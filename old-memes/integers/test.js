var integers = require('./index'),
    util = require('util'),
    numbers = integers(5);

[ 0, 1, 2, 3, 4 ].forEach(function (n, i) {
  if (n === numbers[i]) {
    console.log('✓ (%d)th digit is %d', n, i);
  }
  else {
    throw new Error(util.format(
      '☠☠☠ (%d)th digit should have been %d but was actually %d ☠☠☠',
      n, n, i
    ));
  }
});
