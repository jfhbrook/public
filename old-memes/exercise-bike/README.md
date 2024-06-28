# exercise-bike
## a command line interface for nunjucks

exercise-bike is a command line interface for nunjucks. it uses
[minimist](https://npm.im/minimist) to parse options as variables to pass
to nunjucks, and reads/writes templates and renders to/from stdio and/or
the filesystem.

this library is named after [handlebars](https://npm.im/handlebars), but I do
more jinja than mustache now, and so gave it an upgrade.

## install

exercise-bike is distributed on npm. you can for instance run:

```bash
npx exercise-bike --help
```

## examples

you can run this example in this repo:

```bash
WORLD=world ./exb input.html.njk --title TITLE --hello hello
```

that takes a template which looks like this:

```html
<h1>{{title}}</h1>
<p>{{hello}} {{ENV.WORLD}}</p>
```

and outputs something like this:

```html
<h1>TITLE</h1>
<p>hello world</h1>
```

you can also read templates from stdin, and write to a file. for example, if
you wanted to use [marked](https://npm.im/marked) to generate an HTML file
from a markdown README, you could do something like:

```bash
marked README.md | exb --readme :stdin: ./templates/index.html.njk  ./public/index.html
```

## usage

this is what the command help outputs today, and it really says it all:

```
exb: a command line interface for nunjucks

USAGE: exb [INPUT] <OUTPUT>

where INPUT and OUTPUT are file paths. If INPUT is the value ':stdin:',
input will be read from stdin. If no output is specified, it will be logged
to the console.

Options:
    --autoescape    configure nunjucks to use autoescape.

    --{NAME} VALUE  define a variable to pass to nunjucks. if the value starts
                    with a '@', exb will treat it as a file. if the value
                    is ':stdin:', exb will populate the variable with the
                    value of stdin. if the value is valid JSON, it will be
                    parsed before getting passed to nunjucks.

Environment variables are available in 'ENV'.
```

# License

exercise-bike uses an MIT license. See the LICENSE file for details.
