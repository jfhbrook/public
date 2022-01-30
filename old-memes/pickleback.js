#!/usr/bin/env node

const path = require('path');
const { spawn } = require('child_process');

const minimist = require('minimist');

const opts = minimist(process.argv.slice(2));

const setRemotes = `if git remote -v | grep -E '^upstream'; then
  git remote set-url upstream "$UPSTREAM_REMOTE"
else
  git remote add upstream "$UPSTREAM_REMOTE"
fi`

const pushBranches = `git push origin master
git push --force origin patches`;

const publish = `npm publish`;

const sync = `set -euo pipefail

${setRemotes}

git checkout master
git pull --ff-only upstream master
git checkout patches
git pull --ff-only origin patches
if git rebase master; then
  echo 'rebase successful - pushing!'
else
  echo "EVERYTHING IS WHACK!"
  echo "dropping into a SUBSHELL - complete the rebase and exit to finish!"
  PS1="updating pickleback> " bash
  echo 'thank you for your cooperation - pushing!'
fi

${pushBranches}

${publish}`;

const push = `set -euo pipefail

${setRemotes}

${pushBranches}`;

let command = null;
if (opts._[0] === 'sync') {
  command = sync;
} else if (opts._[0] === 'push') {
  command = push;
}

if (!command) {
  console.error('no command specified!');
  process.exit(1);
}

const job = spawn('bash', [ '-c', command], {
  cwd: path.join(path.dirname(__filename), 'pickleback'),
  env: {
    ...process.env,
    UPSTREAM_REMOTE: 'git@github.com:hapijs/shot.git'
  },
  stdio: ['inherit', 'inherit', 'inherit' ]
});

job.on('end', process.exit);
