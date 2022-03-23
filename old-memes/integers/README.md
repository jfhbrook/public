# integers

## install

    npm install integers

## require

    > var integers = require('integers');

## use

### integers([start], stop, [every])

Acts like the range operator from many languages, but was specifically inspired
by python. Examples:

    > integers(5)
    [ 0, 1, 2, 3, 4 ]

    > integers(2,5)
    [ 2, 3, 4 ]

    > integers(0,10,2)
    [ 0, 2, 4, 6, 8 ]

## test

    npm test

## license

MIT/X11
