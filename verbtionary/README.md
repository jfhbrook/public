# Verbtionary

A problem I run into a lot while working with PowerShell is trying to find the right verb to use for a function. PowerShell functions are by convention named with the form `{Verb}-{Noun}`, and while the Noun can vary wildly (and is in fact often more "the rest of the sentence" than a noun *per se*), the Verb is supposed to conform to a [list of approved PowerShell verbs](https://docs.microsoft.com/en-us/powershell/scripting/developer/cmdlet/approved-verbs-for-windows-powershell-commands?view=powershell-7). Sometimes finding the right verb is easy, especially if the verb you're looking for is already in the list, but sometimes it can be a challenge!

I hacked up an [Azure function](https://azure.microsoft.com/en-us/services/functions/) that hits the [Merriam-Webster thesaurus API](https://dictionaryapi.com/products/api-collegiate-thesaurus) to look up synonyms for a given search and then sees which of them are included in the output of [Get-Verb](https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.utility/get-verb?view=powershell-7). In addition, I manually coded lookups for the synonyms/alternatives in Microsoft's list of approved PowerShell verbs and do a secondary lookup based on the results from Merriam-Webster. The results are a little broad, but it works!

The API itself is quite simple. It takes a single querystring parameter, `Query`, and returns a JSON response payload with the following fields:

* Ok - `$True` for successful searches and `$False` for cases where something went horribly wrong
* Error - A simple JSON representation of the Exception that I caught when trying to make the search
* Body - A JSON representation of the filtered output of `Get-Verb` that matches a search term

The attached script is a thin wrapper around that API. It just calls it and then extracts the Body, counting on PowerShell's non-terminating errors and my naive status codes to properly message any API issues. I wrapped it in a function and put it inside my `profile.ps1`.

For an example: Let's say I have a function I want to write that looks at something, and I know that "look" isn't a PowerShell approved verb:

```powershell
(base) PS C:\Users\Josh> Search-Verbtionary look

Verb    AliasPrefix Group          Description
----    ----------- -----          -----------
Copy    cp          Common         Copies a resource to another name or to another container
Get     g           Common         Specifies an action that retrieves a resource
Grant   gr          Security       Allows access to a resource
Measure ms          Diagnostic     Identifies resources that are consumed by a specified operation, or retrieves st...
New     n           Common         Creates a resource
Receive rc          Communications Accepts information sent from a source
Sync    sy          Data           Assures that two or more resources are in the same state
Unblock ul          Security       Removes restrictions to a resource
Watch   wc          Common         Continually inspects or monitors a resource for changes
```

In this case, the Verbtionary gave us a number of verbs, some of which seem more applicable than others. `Watch` might be the right idea, especially if we're looking at a resource and waiting for something to happen, as could `Measure`, if we're looking at something to ascertain some quality of it. This is also a good example of the limitations of this approach - the other verbs are less relevant, because Merriam-Webster casts a wide net and because the Microsoft synonyms/alternatives cause us to sometimes choose words two steps removed instead of just one. Moreover, `Search` doesn't show up in this list, even though if I was trying to look *for* something it would probably be a sensible choice. Such are computers and afternoon hack projects.

Cheers!
