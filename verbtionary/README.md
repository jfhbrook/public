# Verbtionary

Look up synonyms for a word that are also 
[approved PowerShell verbs](https://docs.microsoft.com/en-us/powershell/scripting/developer/cmdlet/approved-verbs-for-windows-powershell-commands?view=powershell-7)
Uses the
[Merriam-Webster thesaurus API](https://dictionaryapi.com/products/api-collegiate-thesaurus)
via an Azure function app.

## Install

You can install the client from PSGallery:

```powershell
Install-PSResource -Name Verbtionary -Repository PSGallery
```

## Usage

Usage is simple:

```powershell
PS> Find-Verb look

Verb    AliasPrefix Group          Description
----    ----------- -----          -----------
Copy    cp          Common         Copies a resource to another name or to another container
Get     g           Common         Specifies an action that retrieves a resource
Grant   gr          Security       Allows access to a resource
Measure ms          Diagnostic     Identifies resources that are consumed by a specified opera…
New     n           Common         Creates a resource
Receive rc          Communications Accepts information sent from a source
Sync    sy          Data           Assures that two or more resources are in the same state
Unblock ul          Security       Removes restrictions to a resource
Watch   wc          Common         Continually inspects or monitors a resource for changes
```

## Development

The PSGallery package is in the root of this directory. Development is fairly
straightforward. There's also a [justfile](https://github.com/casey/just) that
includes some common recipes.

`just install` will install powershell dev dependencies to your user. Right
now, that's just ScriptAnalyzer.

`just console` will start powershell with the module imported. From there, you
can try running it against the production API.

`just format` will format both the powershell and terraform code, in all
parts of the project.

`just publish` will publish the module to PSGallery. Note you'll need to set
`NUGET_API_KEY` in `.env`.

Recipes relevant to app development are `just start` and `just deploy`. See
[the dedicated README](./service/README.md) for more details.

Verbtionary also includes [an Azure function app](./service) and
[accompanying infrastructure](./infrastructure). These have brief READMEs with
more details of their use.

## License

I've released this under an MIT license. See the [LICENSE](./LICENSE) file for
more details.
