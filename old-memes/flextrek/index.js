const path = require('path');

const minimist = require('minimist');

const { Just } = require('./just');


async function main(argv) {
  const justfile = path.join(__dirname, 'justfile');
  // TODO: mrs commanderson obviously
  const opts = minimist(argv);

  const env = {
    ...process.env
  };

  const just = new Just(justfile, env);

  await just('update-step-1');
  await just(yourStep2);
  await just('update-step-3');
  await just('update-step-4');
  await just(yourStep5);
}

main(process.argv.slice(2));
