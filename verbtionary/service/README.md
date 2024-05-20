# Verbtionary API Service

This is the code for the Azure function that powers Verbtionary.

## Prerequisites

You will need to install a few things in order to be effective here:

- The Azure CLI. In Homebrew, `brew install azure-cli`.
- Azure Functions Core Tools v4. In Homebrew, `brew install azure/functions/azure-functions-core-tools@4`.
- Dotnet 6(?) SDK. In Homebrew, `brew install --cask isen-ng/dotnet-sdk-versions/dotnet-sdk6-0-400`, via <https://github.com/isen-ng/homebrew-dotnet-sdk-versions>.

## Local Development

For local development to work, you'll need to create a file called
`local.settings.json` in this directory with the following contents:

```json
{
    "IsEncrypted": false,
    "Values": {
        "AzureWebJobsStorage": "UseDevelopmentStorage=true",
        "FUNCTIONS_WORKER_RUNTIME": "powershell",
        "MERRIAM_WEBSTER_API_KEY": "CHANGEME"
    }
}
```

If that looks good and you have prerequisites installed, you should be able to
run `just start` and have it spin up.

To test the API locally, I like to use curl:

```sh
curl 'http://localhost:7071/api/FindVerbTrigger?query=add'
```

`Invoke-WebRequest` works just as well, but old habits die hard and it turns
out curl doesn't time out as quickly - which is beneficial for cold starts.

## Deployment

To deploy, first log into the Azure CLI:

```sh
az login
```

Then, go ahead and run publish:

```sh
just publish
```

If it grumbles about the app name, it's because you need to set the
`VERBTIONARY_APP_NAME` environment variable in the justfile's `.env` to the
name of the function app you created with Terraform.
