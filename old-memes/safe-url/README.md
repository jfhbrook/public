# safe-url

Want to print out urls with BASIC AUTH CREDS in them? Use this module to
SCRUB THEM PUPPIES OUT.

## example

```js
> var safeUrl = require('./');
undefined
> var url = 'https://iamauser:supersekritpassword@this.is.my.couch.trashfire.xyz'
undefined
> safeUrl(url)
'https://iamauser:******@this.is.my.couch.trashfire.xyz'
> 
```

## thx

Thanks to [Mikeal Rogers](http://twitter.com/mikeal) for putting this one-liner
in his node couchapp module.

## license

Same as [node.couchapp.js](https://github.com/mikeal/node.couchapp.js). You'll
have to ask Mikeal.
