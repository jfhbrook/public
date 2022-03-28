const { Just } = require('./');
const Registry = require('undertaker-registry');

class JustRegistry extends Registry {
  constructor(justfile) {
    super();
    this.just = new Just(justfile);
  }

  async init(gulp) {
    const dump = this.just.dumpSync();
    
    Object.keys(dump.recipes).forEach(recipe => {
      gulp.task(`just:${recipe}`, async () => {
        await this.just.run(recipe);
      });
    });
  }
}

module.exports = {
  JustRegistry
};
