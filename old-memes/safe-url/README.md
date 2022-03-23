# safe-url

have you ever wanted to print out a url, but were worried about logging
basic auth credentials? this module will do its best to scrub them out.

note, this comes at ABSOLUTELY NO GUARANTEE on my part, and if you are truly
concerned about security, either fork and manually review or find a different
dependency.

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

## credits

this implementation was extracted from [@mikeal](https://twitter.com/mikeal)'s
[couchapp module](https://www.npmjs.com/package/couchapp) many years ago.

## license

this project would be covered under the same license as
[the couchapp](https://github.com/mikeal/node.couchapp.js) project.
unfortunately, it's what you might call "poorly licensed." using it in MIT
projects is probably safe, but if it's important to you then you'll have to
ask Mikeal.
