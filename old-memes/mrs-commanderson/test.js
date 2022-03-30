const { Router } = require('./router');

const router = new Router();

router.on("init", async (ctx) => { console.log(ctx); });
router.on("install :pkg", async (ctx, pkg) => { console.log(ctx, pkg); });

async function test() {
  console.log("init:", await router.dispatch("init", {}));
  console.log("install:", await router.dispatch("install some-pkg", {}));
}

test();
