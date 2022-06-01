#!/usr/bin/env node

const { spawn } = require('child_process');
const { readdir, readFile, stat } = require('fs/promises');
const path = require('path');
const { inspect } = require('util');

const colors = require('ansi-colors');
const { createLogger } = require('kenny-loggins');
const minimist = require('minimist');

// A few paths can be defined immediately, and here they are!
const appRoot = path.dirname(__filename);
const actionsRoot = path.join(appRoot, 'actions');
const coreRoot = path.join(appRoot, 'core');
const PATH = `${actionsRoot}:${coreRoot}:${process.env.PATH}`;

// first, what's truly important: LOGGING
const logger = createLogger({
  level: 'info',
  colors: {
    fatal: 'grey',
    error: 'red',
    warn: 'yellow',
    info: 'magenta',
    debug: 'cyan'
  }
});

let shrug = false;
let shellMode = false;

function greatSuccess() {
  if (!shellMode) {
    logger.info(colors.green('ok'));
  }
  process.exit(0);
}

function flagrantError(err) {
  // errors have a highlight designed for a BSOD, not appropriate for a
  // warning
  if (!shrug) {
    const { green, grey, red, yellow, white } = inspect.colors;
    inspect.styles = {
      bigint: yellow,
      boolean: yellow,
      date: yellow,
      module: yellow,
      name: yellow,
      null: red,
      number: yellow,
      regexp: red,
      special: red,
      string: green,
      symbol: red,
      undefined: grey
    };
  }

  // the stack is meaningless in shell mode
  let message = shellMode ? colors.white(String(err)) : inspect(err, { colors: true });

  // find the width of the message string
  let width = message.split('\n').reduce((n, l) => Math.max(l.length, n), 0) + 8;

  // split and add padding
  message = message.split('\n').map(l => {
    return '    ' + l + (' '.repeat(width - l.length - 4));
  });

  // be less shouty on a shrug
  let header = shrug ? 'houston, we got a problem!! ' : 'FLAGRANT ERROR';
  header = (
    ' '.repeat(Math.floor((width - header.length) / 2))
    + header
    + ' '.repeat(Math.ceil((width - header.length) / 2))
  );

  // stack 'em to the heavens!
  message = [
    ' '.repeat(width),
    header,
    '-'.repeat(width),
    ' '.repeat(width)
  ].concat(message).concat([
    ' '.repeat(width),
    '-'.repeat(width)
  ]);

  // in shrug
  if (shrug) {
    message.forEach(l => {
      logger.warn(colors.yellow(l));
    });
  } else {
    message.forEach(l => {
      logger.error(colors.bgBlue(l));
    });
  }

  // let the parent process log exit
  if (!shellMode && shrug) {
    logger.warn('ok ' + colors.yellow('~despite errors~'));
    process.exit(0);
  }

  if (!shellMode) {
    logger.error(colors.red('not') + ' ok');
    process.exit(1);
  }
}

function falconPunch() {
  // Hook the entire world to muh error handling lol
  process.on('uncaughtException', flagrantError);
  process.on('unhandledRejection', flagrantError);

  // gotta do everything myself!!
  Promise.prototype.done = function () {
    this.then(greatSuccess, flagrantError);
  }
}

if (require.main === module) {
  falconPunch();
  main().done();
}

async function main() {
  // load options
  const opts = await parseArgs(process.argv.slice(2));

  // configure logging and exit handling
  if (opts.verbose) {
    logger.level = 'debug';
  } else if (opts.quiet) {
    logger.level = 'warn';
  } else {
    logger.level = 'info';
  }

  if (opts.shrug) {
    shrug = true;
  }

  logger.debug(colors.yellow(' _ __  _ __ _ __ ___  '));
  logger.debug(colors.yellow('| \'_ \\| \'__| \'_ ` _ \\ '));
  logger.debug(colors.yellow('| |_) | |  | | | | | |'));
  logger.debug(colors.yellow('| .__/|_|  |_| |_| |_|'));
  logger.debug(colors.yellow('|_|') + colors.blue(' "but who will manage'));
  logger.debug(colors.blue('     the package managers?"'));
  logger.debug('');
  logger.debug('it worked if it ends with ok');

  // load known features
  const features = await getFeatures();

  // try to read the file in
  let file = null;
  try {
    file = await readFile(opts.filename, 'utf8');
  } catch (err) {
    if (err.code !== 'ENOENT') {
      throw err;
    }
  }

  // if the read was successful, attempt to parse it
  let spec = null;
  if (file) {
    spec = parseFile(file);
  }

  if (!spec) {
    logger.debug("no prm.sh file found at ${filename}");
  }

  // top-level help
  // TODO: enumerate available recipes and their required features
  if (opts.help && !opts.actions && !opts.recipe) {
    logger.info('USAGE: prm [FILENAME] [RECIPE] [...FLAGS]');

    logger.info('RECIPES:');
    // TODO: move this recipe-wide feature extraction to the parser
    Object.entries(spec.recipes).forEach(([recipe, { actions }]) => {
      const features = Array.from(
        new Set(actions.map(h => h.feature))
      ).map(feature => `#${feature}`).join(' ');
      logger.info(`    ${recipe} ${features}`);
    });
    return;
  }

  // recipe specific help - enumerate parsed actions in the recipe, log
  // required features, etc
  if (opts.help && !opts.actions && opts.recipe) {
    if (spec) {
      logger.info(`HELP: ${recipe} will run:`);
      // TODO: this can be much more sophisticated!
      spec.recipes[recipe].actions.forEach(action => {
        logger.info(` - ${action.name} #${action.feature}`);
      });
    } else {
      logger.info(`mfer what the heck is a ${recipe}?!`);
    }
    return;
  }

  // top-level action help - list actions
  if (opts.help && opts.actions && !opts.recipe) {
    // do up a little action perusal and help
    const actions = await getActions();
    Object.values(actions).forEach(action => {
      logger.info(inspect(action));
    });
    return;
  }

  // let's collect a command to run
  let command = null;

  // load the environment
  const env = await createEnv(opts);

  // action-level action help - run the command in help mode
  if (opts.help && opts.actions && opts.recipe) {
    command = `${opts.recipe}`;
  } else if (!opts.recipe) {
    logger.info('USAGE: prm [FILENAME] [RECIPE] [...FLAGS]');
    logger.info("(try running 'prm --help')");
    return;
  } else {
    command = `${file}\n\n${opts.recipe}`;
  }

  logger.debug(colors.cyan('running command:'));
  command.split('\n').forEach(l => {
    logger.debug(l);
  });

  // where the rubber meets the road!
  logger.info(colors.bgYellow(colors.black(' LEROY JENKINS! ')));
  return new Promise((resolve, reject) => {
    const job = spawn('bash', ['-c', `${opts['dump-env'] ? 'env' : ''}\n\n${command}`], {
      cwd: opts.configRoot,
      env,
      stdio: ['inherit', 'inherit', 'inherit']
    });

    job.on('exit', (code) => {
      if (code) {
        reject(new Error(`${opts.recipe} failed with exit code ${code} T__T`));
      } else {
        logger.info(`${opts.recipe} exited with code ${code}`);
        resolve();
      }
    });
  });
}

// ## ACTION ENVIRONMENT
//
// actions are run in an environment with standard variables.
//
// ### PATH
//
// the PATH is set to its value for the prm process, with the directory of
// actions prepended to the front. Booleans are encoded with a '`' for true
// and '' for false.
//
// ### FLAGS
//
// - HELP: when set, actions will print their help and exit
// - PRETEND: when set, actions will log actions instead of taking them
// - PLXKTHX: when set, actions will continue even if ill-advised
// - SHRUG: when set, will warn and exit with a success code on errors
// - DEBUG: when set, log at the debug level
// - QUIET: when set, log at the warning level
//
//
// #### FEATURES
//
// features are represented by environment variables of the form
// FEATURE_${feature.toUpperCase()}. For example, if copr is enabled, then
// FEATURE_COPR=1.
//
exports.createEnv = createEnv;
async function createEnv(opts) {
  const features = await getFeatures();
  const featureFlags = Object.fromEntries(
    features.map(f => {
      return [`FEATURE_${f.toUpperCase()}`, opts[f] ? '1': ''];
    })
  );

  const env = {
    ...featureFlags,
    HELP: opts.help ? '1' : '',
    PRETEND: opts.pretend ? '1' : '',
    PLZKTHX: opts.plzkthx ? '1' : '',
    SHRUG: opts.shrug ? '1' : '',
    DEBUG: opts.verbose ? '1' : '',
    QUIET: opts.quiet ? '1' : ''
  };

  Object.entries(env).forEach(([key, value]) => {
    let stringified = null;
    if (value === '1') {
      stringified = colors.yellow('activated');
    } else if (value === '') {
      stringified = colors.red('deactivated');
    } else {
      stringified = colors.cyan(value);
    }

    logger.debug(`${key}=${stringified}`);
  });

  return { ...process.env, ...env, PATH };
}

exports.parseFile = parseFile;
function parseFile(file) {
  // collect actions happening outside recipes
  let outside = [];

  // the recipes
  const recipes = {};

  // currently-collecting recipe state
  let recipeName = null;
  let actions = [];

  // currently-collecting action state
  let actionName = null;
  let feature = null;
  let verb = null;
  let message = null;
  let lines = [];

  // whether we're collecting an action or not
  let collectingLines = false;

  file.split('\n').forEach((line, i) => {
    const whitespace = line.match(/^\W*$/);
    const comment = line.match(/^\W+#/);
    const variable = line.match(/^\W*(\w+)=(.*)$/);
    const recipeStart = line.match(/^function\W+(\w+)\W+\{\W*$/);
    const escapedNewLine = line.match(/\\$/);
    const actionCall = line.match(/^\W+(\w+)-(\w+)\W+/);
    const recipeEnd = line.match(/^\}\W*$/);

    /*
    logger.info({
      n: i + 1,
      line,
      recipeStart,
      escapedNewLine,
      actionCall,
      recipeEnd,
      recipeName,
      actionName,
      feature,
      verb,
      message,
      lines
    });

    logger.info({ actions, recipes });
    */

    // it's a shebang
    if (!i && line.slice(0, 2) === '#!') {
      outside.push({ cmd: line.slice(2), line: { n: i + 1, line }});
      return;
    }

    // handle any collecting cases first
    if (collectingLines) {
      // we're collecting the line I guess
      lines.push({ n: i + 1, line });
      if (escapedNewLine) {
        // keep collecting!
        return
      }

      // we've been collecting an action, but no more!!
      actions.push({
        name: actionName,
        feature,
        verb,
        message,
        lines
      });

      actionName = null;
      feature = null;
      verb = null;
      message = '???';
      lines = [];

      // not collecting lines anymore lol
      collectingLines = false;

      // do go to the next line though
      return;
    }

    // start collecting a recipe?
    if (recipeStart) {
      // it is however possible to accidentally not close a prior recipe, lol
      if (recipeName) {
        actions.push({
          name: 'shenanigan-perpetuate',
          feature: 'shenanigan',
          verb: 'perpetuate',
          message: `starting recipe ${recipeStart[1]} while ${recipeName} is still open?? lol`,
          lines,
        });

        // add our abruptly closed recipe D:
        recipes[recipeName] = { name: recipeName, actions };
      } else if (actions.length) {
        // actions collected across open recipes
        outside = outside.concat(actions);
      }

      // initialize the new recipe either way
      recipeName = recipeStart[1];
      // recipe open/close do not collect their lines
      actions = [];

      return;
    }

    // finish collecting a recipe?
    if (recipeEnd) {
      if (recipeName) {
        // let's close off our successfully collected recipe!
        recipes[recipeName] = {
          recipeName,
          actions
        }
        recipeName = null;
        actions = [];
      } else {
        // if there's not an open recipe, let's note some shenanigans
        actions.push({
          name: 'shenanigan-perpetuate',
          feature: 'shenanigan',
          verb: 'perpetuate',
          message: "ending a recipe that isn't even open?? weird flex but ok",
          lines: [{ n: i + 1, line}],
        });
      }
      return;
    }

    // collect an action
    if (whitespace) {
      actionName = 'code-spacing';
      feature = 'code';
      verb = 'spacing';
      message ='some cheeky whitespace!';
      lines = [{ n: i + 1, line }];
    } else if (comment) {
      actionName = 'code-comment';
      feature = 'code';
      verb = 'comment';
      message = 'a cheeky comment!';
      lines = [{ n: i + 1, line }];
    } else if (variable) {
      actionName = 'variable-set';
      feature = 'variable';
      verb = 'set';
      message = { name: variable[1], definition: variable[2] };
      lines = [{ n: i + 1, line }];
    } else if (actionCall) {
      actionName = `${actionCall[1]}-${actionCall[2]}`;
      feature = actionCall[1];
      verb = actionCall[2];
      lines.push({ n: i + 1, line });
      message = `action: ${actionName}`;
    } else {
      actionName = 'effects-affect';
      feature = 'effects';
      verb = 'affect';
      lines.push({ n: i + 1, line });
      message = '~totally wild shit~';
    }

    // if there's an escaped newline then, well, let's GOOOO
    if (escapedNewLine) {
      collectingLines = true;
      return
    }

    // otherwise we're already done, so push the action and clean up the
    // state mess we made
    actions.push({
      name: actionName,
      feature,
      verb,
      lines,
      message
    });
    actionName = null;
    feature = null;
    verb = null;
    lines = [];
    message = null;
  });

  outside = outside.concat(actions);

  const shenanigans = [];
  const variables = [];

  outside.forEach(a => {
    // comments and whitespace
    if (a.feature === 'code') {
      return;
    }

    if (a.feature === 'variable') {
      variables.push(a);
      return;
    };

    // side effects
    if (a.feature === 'effects') {
      // treated as a shenanigan for now
      shenanigans.push(a);
      return;
    }
    // either a shenanigan or *should* be
    shenanigans.push(a);
  });

  return {
    recipes,
    variables,
    shenanigans
  };
}

class ParseError extends Error {}
exports.ParseError = ParseError;

// ## ACTIONS
//
// action names match this format:
//
//     /(?<feature>\w+)-(?<verb>\w+)/
//
// in the context of actions, features operate as a namespace. verbs should
// loosely follow the ones used by powershell. the noun from powershell
// commands should manifest itself as the first argument to the action.
exports.getActions = getActions;
async function getActions(validate) {
  const names = await readdir(actionsRoot);
  const actions = {};
  names.forEach((name) => {
    const components = name.split('-');
    if (components.length === 2) {
      const [ feature, verb ] = components;
      actions[name] = { name, feature, verb };
    } else {
      const message =`could not parse action name: ${name}`; 

      // in the cli we don't want to stop the presses because of a dumb bug,
      // but I might use this in a testing situation?
      if (validate) {
        throw ParseError(message);
      } else {
        logger.warn(message);
      }
    }
  });
  return actions;
}

const flags = [ 'help', 'actions', 'pretend', 'plzkthx', 'shrug', 'dump-env' ]

function uniq(xs) {
  return Array.from(new Set(xs));
}

let _features = null;
exports.getFeatures = getFeatures;
async function getFeatures() {
  if (!_features) {
    const actions = await getActions();
    _features = uniq(Object.values(actions).map(({feature}) => feature));
  }
  return _features;
}


// ## FLAGS
//
// * `--help`: get help for available recipes (and actions)
// * `--actions`: inspect available actions (and their help)
// * `--pretend`: do a "dry run", logging what *would* happen
// * `--plzkthx`: take drastic actions even if they're ill-advised
// * `--shrug`: on unrecoverable errors, warn and exit successfully
// * `--verbose`: turn on debug logging (or: set `DEBUG=1`) 
//
// ## FEATURES
//
// actions in recipes may be enabled or disabled with the `--${feature}` and
// `--no-${feature}` flags. for example, COPR may be enabled and disabled with
// the --copr and --no-copr flags, respectively.
//
// if no such flags are passed in, or if all flags are of the `--no-${feature}`
// form, features will be enabled by default. if there are any `--${feature}`
// flags, the default becomes disabled and `--no-${feature}` flags have no
// effect.
//
// `--${feature}-only` flags will enable their respective features with the same
// default as `--${feature}`. however, `--${feature}-only` flags will also ensure
// that it is the ONLY feature that's enabled. if a second feature has the
// `--${feature}-only` flag set, that feature will not be enabled unless the
// `--plzkthx` flag is set. note that `--no-${feature}` will override
// `--${feature}-only`.
//
// ## FILE PATH
//
// when there are two positional arguments, the first is the location of prm.sh
// (either the file or its directory) and the second is a recipe to call.
//
// when there is one argument, we detect whether or not it is a file. if it
// is a file, then there is no supplied recipe. otherwise, the first argument
// is the route and the file is defaulted to ./prm.sh.
exports.parseArgs = parseArgs
async function parseArgs(argv) {
  const actions = await getActions();
  const features = await getFeatures();

  const opts = minimist(argv, {
    // features and flags are boolean flags
    boolean: features.concat(flags),
    default: {
      // null is unset, but will be bool if --{feature} or --no-{feature} is
      // called
      ...Object.fromEntries(features.map(f => [f, null])),
      // the --{feature}-only variants are false by default (--no-feature-only
      // is nonsense)
      ...Object.fromEntries(features.map(f => [`${f}-only`, false])),
      // a falsey default is just fine for other flags,
    }
  });

  // verbose/quiet flags
  if (opts.v || opts.verbose) {
    opts.verbose = true;
    delete opts.v;
  }

  if (opts.q || opts.quiet) {
    if (opts.v || opts.verbose) {
      logger.warn('--verbose overrides quiet!');
      opts.quiet = false;
    } else {
      opts.quiet = true;
    }
    delete opts.q;
  }

  flags.forEach(f => {
    if (opts[f]) {
      logger.debug(`${f}: ${colors.green('activated')}.`);
    }
  });

  // if any feature has been explicitly enabled, the default is disabled,
  // otherwise enabled
  const featureDefault = features.every(f => opts[f] !== true);

  // this will contain any features which were enabled with a
  // --${feature}-only flag. we end up actually needing the values
  // later so we store them here.
  const onlyFeatures = features.filter(f => opts[`${f}-only`])
  // if there are any --${feature}-only flags, then we have to deal with
  // special logic ;)
  const onlyMode = onlyFeatures.length;
  // to track the last seen only-mode feature (indexes onlyFeatures)
  let onlyIdx = -1;

  // aside from the core logic --${feature}/--no-${feature} is relatively
  // straightforward and down the page. however, the --${feature}-only logic
  // is both needlessly complex and not at all handled by minimist.
  //
  // this was ABSOLUTELY worth the joke.
  if (onlyMode) {
    features.forEach(f => {
      let enabled = opts[f] === true;
      let disabled = opts[f] === false;
      const only = opts[`${f}-only`] === true;

      // --${feature}-only flag special behavior
      if (only) {
        if (disabled) {
          // --${feature}-only --no-${feature}
          logger.warn('YOU know what time it is, RINSE AND SPIN');
          logger.warn(`--${f}-only and of course, --no-${f}.`);
          logger.warn('*washing machine jingle beep boops*');
          logger.info(`(the two options cancel each other out, leaving ${f} disabled.)`);
          opts[f] = false;
        } else if (onlyIdx > -1) {
          // --${other}-only --${feature}-only
          logger.warn(
            `only one feature will be enabled and it's ${onlyFeatures[onlyIdx]}, bud`
          );

          if (!opts.plzkthx) {
            logger.info('to override this behavior, call prm with the --plzkthx flag.');
            logger.info(`feature ${f} disabled.`);
            opts[f] = false;
          } else {
            logger.warn(
              `option plzkthx detected - feature ${f} additionally enabled!!`
            );
            opts[f] = true;
          }
        } else {
          if (enabled) {
            // --${feature} --${feature}-only
            logger.warn(`--${f} is redundant with --${f}-only, ya dunce!`)
          }

          // --${feature}-only enables the feature
          opts[f] = true;
        }

        // clean up the flag so args print nice
        delete opts[`${f}-only`];
      }
    });
  }

  // now that all the "rockin' cools" are off the screen, logic is pretty
  // straightforward for flags: if it's explicitly enabled or disabled at
  // this point, log it if it's different than the default, and otherwise
  // set it to the feature default.
  features.forEach(f => {
    let enabled = opts[f] === true;
    let disabled = opts[f] === false;

    if (enabled && !featureDefault) {
      logger.debug(`feature ${f} ${colors.cyan('enabled')}.`);
      return;
    }

    if (disabled && featureDefault) {
      logger.debug(`feature ${f} ${colors.yellow('disabled')}.`);
      return;
    }

    opts[f] = featureDefault;
  });

  // positional args time!!

  let configRoot = null;

  // first arg is (usually) a filename
  let filename = opts._.shift();
  // second arg is (typically) the recipe
  let recipe = opts._.shift();

  // is our filename a file? or a directory w/ the file in it?
  let [
    isFile,
    isDirectory
  ] = await Promise.all(
    [
      filename,
      filename ? path.join(filename, 'prm.sh') : null
    ].map(async (fn) => {
      if (!fn) return false;
      try {
        const st = await stat(fn);
        return st.isFile();
      } catch (err) {
        logger.debug(`${fn}: ${err}`);
        return false;
      }
    })
  );

  if (isDirectory) {
    // if its the directory then we'd better go for it
    filename = path.join(filename, 'prm.sh')
  } else if (!isFile && filename && !recipe) {
    // it's not a file or a directory, but it's defined and there's no
    // recipe - this must be the recipe!
    recipe = filename;
    filename = null;
  }

  // if no filename, just read ./prm.sh
  if (!filename) {
    configRoot = process.cwd();
    filename = path.join(configRoot, 'prm.sh');
    isFile = (await stat(filename)).isFile();
  } else {
    configRoot = path.dirname(filename);
  }

  const parsed =  {
    configRoot,
    filename,
    recipe,
    ...opts
  };

  return parsed;
}
