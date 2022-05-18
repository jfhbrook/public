const minimist = require('minimist');
const { quote } = require('shell-quote');

function varName(propName) {
  return `${propName.toUpperCase().replace('-', '_')}`;
}

function serializeValue(value) {
  let isArray = Array.isArray(value);
  if (!isArray) {
    value = [value];
  }

  value = value.map((v) => {
    if (typeof v === "boolean" || v == null) {
      return v ? '1' : '';
    }
    return v;
  });

  const quoted = quote(value);

  if (isArray) {
    return `(${quoted})`;
  }
  return quoted;
}

module.exports = function main(argv) {
  const opts = minimist(argv, {
    string: [
      "string",
      "boolean"
    ],
    alias: {
      string: ["S"],
      boolean: ["B"]
    },
    stopEarly: true
  });

  const args = {
    ...minimist(opts._, {
      string: opts.string,
      boolean: (opts.boolean || []).concat["help"]
    })
  };

  const names = new Set(Object.keys(args).concat(opts.string || []).concat(opts.boolean || []));
  names.add('help');

  for (let name of names) {
    let value = args[name];
    console.log(`${varName(name)}=${serializeValue(value)}`);
  }
}
