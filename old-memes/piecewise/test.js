var tap = require('tap');

var piecewise = require('./'),
    kronecker = piecewise.kronecker,
    sgn = piecewise.sgn;


var KRONECKER_TESTS = [
  { x: -1, y: 1, d: 0 },
  { x: 1, y: -1, d: 0},
  { x: 1, y: 0, d: 0 },
  { x: 0, y: 1, d: 0 },
  { x: -1, y: 0, d: 0 },
  { x: 0, y: -1, d: 0 },
  { x: 1, y: 1, d: 1 },
  { x: 0, y: 0, d: 1 },
  { x: -1, y: -1, d: 1 }
];


var SGN_TESTS = [
  { x: -2, s: -1 },
  { x: -1, s: -1 },
  { x: -0.5, s: -1 },
  { x: -0, s: 0 },
  { x: 0, s: 0 },
  { x: 0.0, s: 0 },
  { x: 0.5, s: 1 },
  { x: 1, s: 1 }, 
  { x: 1.5, s: 1 },
  { x: 2, s: 1 }
];

tap.plan(KRONECKER_TESTS.length + SGN_TESTS.length);

KRONECKER_TESTS.forEach(function (scenario) {
  tap.equal(kronecker(scenario.x, scenario.y), scenario.d);
});

SGN_TESTS.forEach(function (scenario) {
  tap.equal(sgn(scenario.x), scenario.s);
});
