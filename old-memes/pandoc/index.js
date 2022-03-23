var fs = require('fs'),
    util = require('util'),
    Stream = require('stream'),
    spawn = require('child_process').spawn;

function makeArgv(stack) {
  return stack.map(function (t) {
    var k = t[0], v = t[1];

    if (v === true) {
      return util.format('--%s', k);
    }
    else {
      return util.format('--%s=%s', k, v);
    }
  });
}

function camelCase(l) {
  return l.replace(/-(\w)/g, function (x) {
    return x.slice(1).toUpperCase();
  });
}

var Pandoc = module.exports = function (opts) {
  if (!(this instanceof Pandoc)) {
    return new Pandoc(opts);
  }

  opts = opts || {};

  var self = this;
  this.settings = [];
  this.settings.get = function (k) {
    return self.settings[self.settings.indexOf(k)];
  };
  this.settings.set = function (k, v) {
    var i = self.settings.indexOf(k);

    if (i !== -1) {
      self.settings = self.settings.slice(0, i).concat(self.settings.slice(i+1));
    }

    self.settings.push([k, v]);
  };

  Object.keys(opts).forEach(function (k) {
    if (typeof opts[k] !== 'undefined' && opts[k] !== null) {
      self.settings.push([k, opts[k]]);
    }
  });
  
};

function attach(flag, fxn) {
  flag = camelCase(flag);
  Pandoc.prototype[flag] = function (value) {
    return fxn.call(this, flag, value);
  };
  Pandoc[flag] = function () {
    var p = new Pandoc;
    return p[flag].apply(p, arguments);
  };
}

// TODO: Flesh this puppy out.
[
  'from',
  'read',
  'to',
  'write',
  'output',
  'data-dir',
  'strict',
  'parse-raw',
  'smart',
  'old-dashes',
  'base-header-level',
  'indented-code-classes',
  'normalize',
  'preserve-tabs',
  'tab-stop',
  'standalone',
  'template',
  'variable',
  'print-default-template',
  'no-wrap',
  'columns',
  'toc',
  'table-of-contents',
  'no-hilight',
  'hilight-style',
  'include-in-header',
  'include-before-body',
  'self-contained',
  'offline',
  'html5',
  'ascii',
  'reference-links',
  'atx-headers',
  'chapters',
  'number-sections',
  'listings',
  'incremental',
  'slide-level',
  'section-divs',
  'email-obfuscation',
  'title-prefix',
  'css',
  'reference-docx',
  'epub-stylesheet',
  'epub-cover-image',
  'epub-metadata',
  'epub-embed-font',
  'latex-engine',
  'bibliography',
  'csl',
  'citation-abbreviations',
  'natbib',
  'biblatex',
  'latexmathml',
  'mathml',
  'jsmath',
  'mathjax',
  'gladtex',
  'mimetex',
  'webtex'
].forEach(function (flag) {
  attach(flag, function (flag, value) {
    if (value) {
      this.settings.set(flag, value);
    }
    else if (
      typeof this.settings.get(flag) !== undefined &&
      this.settings.get(flag) !== null
    ) {

      this.settings.set(flag, !this.settings.get(flag));
    }
    else {
      this.settings.set(flag, true);
    }
    return this;
  });
});

Pandoc.prototype.variable = function (k, v) {
  this.settings.push([ 'variable', [ k, v ].join(':') ]);
  return this;
};

Pandoc.variable = function () {
  var p = new Pandoc;

  return p.variable.apply(p, arguments);
};

Pandoc.prototype.variables = function (o) {
  var self = this;
  Object.keys(o).forEach(function (k) {
    self.variable(k, o[k]);
  });
  return this;
};

Pandoc.variables = function () {
  var p = new Pandoc;

  return p.variables.apply(p, arguments);
};

Pandoc.prototype.render = function (input, cb) {
  var pandoc = spawn('pandoc', makeArgv(this.settings)),
      readStream = !(typeof input == 'string' || Buffer.isBuffer(input)),
      writeStream = !cb,
      goodBuffer = '',
      badBuffer = '';

  if (readStream) {
    input.pipe(pandoc.stdin);
  }
  else {
    pandoc.stdin.write(input);
  }

  if (!writeStream) {
    pandoc.stderr.on('data', function (data) {
      badBuffer += data.toString();
    });

    pandoc.stdout.on('data', function (data) {
      goodBuffer += data.toString();
    });
    pandoc.stdout.on('end', function () {
      var error = null;

      if (badBuffer.length) {
        error = new Error(badBuffer);
      }

      cb(error, goodBuffer);
    });
  }

  if (!readStream) {
      pandoc.stdin.end();
  }

  pandoc.stdout.stderr = pandoc.stderr;
  return pandoc.stdout;
}
