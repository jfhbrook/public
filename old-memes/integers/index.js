module.exports = function () {
  var from = 0,
      to = 0,
      every = 1,
      output = [];

  switch(arguments.length) {
    case 1:
      to = arguments[0];
      break;

    case 3:
      every = arguments[2];
    case 2:
      from = arguments[0];
      to = arguments[1];
      break;
  }

  for (i=from; i < to; i+=every) {
    output.push(i);
  }

  return output;
}
