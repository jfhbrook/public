var fs = require('fs');
var path = require('path');

var read = require('read'),
    async = require('async'),
    hb = require('handlebars');

var log = require('kenny-loggins'),
    colors = require('ansicolors');

module.exports = function (license, cb) {

  log.info('Loading up `%s`', license);

  var file, tmpl, props = {};
  try {
    file = fs.readFileSync(__dirname + '/licenses/' + license + '/LICENSE').toString('utf8');
    tmpl = hb.compile(file);
  }
  catch (err) {
    return process.nextTick(function () {
      cb(err);
    });
  }
  try {
    props = require('./licenses/' + license + '/properties.json');
  }
  catch (err) {}

  if (Object.keys(props).length) {
    log.info(colors.yellow('NOW IT\'S TIME TO FILL IN THE BLANKS!'));
    log.info('');
  }

  var defaults = {
    YEAR: new Date().getFullYear()
  };

  try {
    var pkg = require(path.resolve('./package.json'));

    if (pkg.author) {
      if (typeof pkg.author == 'string') {
        defaults.OWNER = pkg.author;
      } else {
        defaults.OWNER = pkg.author.name;
      }
    }
  } catch (e) {
    // Will do my job even if I found no pkg
  }

  async.eachSeries(Object.keys(props), function (k, next) {
    read({ prompt: '????: ' + props[k] + '? > ', default: defaults[k] }, function (err, ans) {
      if (err) return next(err);
      props[k] = ans;
      next();
    });
  }, function (err) {
    log.info('');
    if (err) throw err;

    var location = process.cwd() + '/LICENSE';

    log.info('Writing your LICENSE to `%s`', location);

    try {
      fs.writeFileSync(location, tmpl(props));
    }
    catch (err) {
      return cb(err);
    }

    log.info('Cool, worked');

    cb(null);
  });
}

