# @jfhbrook/piecewise

Some old piecewise functions I found in the attic.

## install

```bash
npm install @jfhbrook/piecewise
```

## example

```js
var piecewise = require('piecewise'),
    kronecker = piecewise.kronecker,
    sgn = piecewise.sgn;

console.log(kronecker(1, 2)); // 0
console.log(kronecker(1, 1)); // 1
console.log(sgn(-10)); // -1
console.log(sgn(0)); // 0
console.log(sgn(10)); // 1
```

## tests

```bash
npm test
```

## license

MIT
