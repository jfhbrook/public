const path = require('path');

const { registry, series } = require('gulp');

const { JustRegistry } = require('./gulp');

registry(new JustRegistry(path.join(__dirname, 'justfile')));

exports.default = series('just:task');
