# Copyright 2024 Josh Holbrook
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to
# deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
# sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.

$Global:VerbtionaryUrl = "https://verbtionary.azurewebsites.net/api/findverbtrigger"

function Find-Verb {
  <#
  .Synopsis
  Search the Merriam-Webster thesaurus for synonyms that are also approved
  PowerShell verbs.

  .Description
  Uses the Verbtionary API to search the Merriam-Webster thesaurus for synonyms
  that are also in the output of Get-Verb.

  .Parameter Query
  A word to search for synonyms.

  .Outputs
  The entries in the output of the Verbtionary API.

  .Notes
  Written by Josh Holbrook (@jfhbrook).
#>

  param(
    [string]$Query
  )

  $Response = Invoke-WebRequest "${Global:VerbtionaryUrl}?query=${Query}"

  ($Response.Content | ConvertFrom-Json).Body | Write-Output
}
