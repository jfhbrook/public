using namespace System.Net

param($Request, $TriggerMetadata)

$VerbosePreference = 'Continue'

$KeyVaultName = $Env:VERBTIONARY_KEYVAULT_NAME
$ThesaurusAPIKey = Get-AzKeyVaultSecret -VaultName $KeyVaultName -Name "merriam-webster-api-key" -AsPlainText

$Ok = $False
$ResError = $null
$ResBody = $null

$MicrosoftSynonyms = @{
    accept = @('receive');
    acknowledge = @('confirm');
    acquire = @('get', 'read');
    aggregate = @('group');
    agree = @('confirm');
    allocate = @('new');
    allow = @('grant', 'unblock');
    analyze = @('measure', 'test');
    append = @('add');
    arrange = @('group');
    assign = @('set');
    associate = @('group', 'join');
    attach = @('add');
    backup = @('export');
    begin = @('enable');
    block = @('deny', 'hide');
    boot = @('start');
    broadcast = @('send');
    build = @('new');
    bulkload = @('import');
    burn = @('backup');
    bypass = @('skip');
    calculate = @('measure');
    cancel = @('stop');
    cat = @('get');
    certify = @('assert', 'confirm');
    change = @('convert', 'edit', 'rename');
    clear = @('remove', 'unblock');
    clone = @('copy');
    coerce = @('sync');
    combine = @('join', 'merge');
    compact = @('compress');
    concatenate = @('add');
    configure = @('set');
    connect = @('join', 'mount');
    correlate = @('group');
    create = @('new');
    cut = @('remove');
    decrypt = @('unprotect');
    deny = @('block');
    deploy = @('publish');
    determine = @('measure', 'resolve');
    diagnose = @('debug', 'test');
    diff = @('checkpoint', 'compare');
    dig = @('trace');
    dir = @('get');
    disable = @('revoke');
    discard = @('remove');
    display = @('show');
    dispose = @('remove');
    dump = @('get');
    duplicate = @('copy');
    enable = @('grant');
    encrypt = @('protect');
    end = @('stop');
    erase = @('clear', 'initialize', 'remove');
    examine = @('get');
    expand = @('resolve');
    explode = @('expand');
    export = @('convertfrom');
    extract = @('export');
    fax = @('send');
    find = @('get', 'search', 'select');
    fix = @('repair', 'restore');
    flush = @('clear');
    follow = @('trace');
    generate = @('new');
    get = @('read');
    halt = @('disable');
    hide = @('disable', 'unpublish');
    import = @('convertto');
    in = @('convertto');
    init = @('initialize');
    initiate = @('start');
    input = @('convertto');
    insert = @('add');
    inspect = @('trace');
    install = @('publish');
    into = @('enter');
    invoke = @('start');
    join = @('connect', 'merge');
    jump = @('skip');
    kill = @('stop');
    launch = @('start');
    limit = @('block');
    load = @('import');
    locate = @('select');
    mail = @('send');
    make = @('new');
    match = @('sync');
    migrate = @('move');
    modify = @('edit');
    name = @('move');
    new = @('set');
    nullify = @('clear');
    object = @('deny');
    obtain = @('get');
    open = @('get');
    out = @('convertfrom', 'exit');
    output = @('convertfrom');
    pause = @('suspend', 'wait');
    peek = @('receive');
    ping = @('test');
    pop = @('exit');
    post = @('submit');
    prevent = @('block');
    print = @('write');
    produce = @('show');
    prompt = @('read');
    push = @('enter');
    put = @('send', 'write');
    quota = @('limit');
    read = @('get', 'receive');
    rebuild = @('initialize');
    recalculate = @('update');
    recycle = @('restart');
    refresh = @('update');
    refuse = @('deny');
    reindex = @('update');
    reinitialize = @('initialize');
    reject = @('deny');
    release = @('clear', 'publish', 'unlock');
    remove = @('revoke', 'unregister');
    renew = @('initialize', 'update');
    repair = @('restore');
    replicate = @('backup', 'copy', 'sync');
    resample = @('convert');
    reset = @('set');
    resize = @('convert');
    restore = @('repair');
    restrict = @('lock');
    return = @('restore');
    revert = @('unpublish');
    safeguard = @('protect');
    salvage = @('test');
    save = @('backup');
    seal = @('protect');
    search = @('get','find');
    secure = @('lock');
    separate = @('split');
    set = @('new');
    setup = @('initialize', 'install');
    sleep = @('wait');
    start = @('enable', 'invoke');
    sync = @('backup', 'copy');
    telnet = @('connect');
    terminate = @('stop');
    track = @('trace');
    transfer = @('move');
    type = @('get');
    uncompress = @('expand');
    undo = @('restore');
    uninstall = @('unpublish');
    unite = @('join');
    unlink = @('dismount');
    unmark = @('clear');
    unmount = @('dismount');
    unrestrict = @('unlock');
    unseal = @('unprotect');
    unsecure = @('unlock');
    unset = @('clear');
    update = @('edit');
    validate = @('confirm');
    verify = @('confirm', 'test');
    write = @('set');
}

$Query = $Request.Query.Query
if (-not $Query) {
    $Query = $Request.Body.Query
}

if ($Query) {
    $ErrorActionPreference = 'Stop'
    
    try {
        $Lookup = @{}

        Write-Verbose 'Collecting approved verbs...'

        Get-Verb | ForEach-Object {
            $Key = $_.Verb.ToLower()
            $Lookup[$Key] = $_
            if ($MicrosoftSynonyms[$Key]) {
              $MicrosoftSynonyms[$Key] += $Key
            } else {
              $MicrosoftSynonyms[$key] = @($Key)
            }
        }

        Write-Verbose $Lookup

        $Search = [uri]::EscapeDataString($Query.ToLower())

        $MerriamWebsterSynonyms = ( `
            ( `
                Invoke-WebRequest "https://www.dictionaryapi.com/api/v3/references/thesaurus/json/${Search}?key=${ThesaurusAPIKey}" `
            ).Content | `
            ConvertFrom-Json | `
            ForEach-Object { $_.meta.syns } | `
            Where-Object { $_ } | `
            ForEach-Object { $_ } `
        )

        $Synonyms = ($MerriamWebsterSynonyms + ($Query.ToLower())) | `
            ForEach-Object { $MicrosoftSynonyms[$_] } | `
            Where-Object { $_ } | `
            ForEach-Object { $_ }

        $ResBody = ($Synonyms | Sort-Object | Get-Unique | ForEach-Object { $Lookup[$_] } | Where-Object { $_ })
        
        $Status = [HttpStatusCode]::OK
        $Ok = $True
    } catch {
        $Status = [HttpStatusCode]::InternalServerError
        $ResError = @{
            Type = $_.GetType()
            Message = $_.Message
        }
        Write-Warning $_
    }
}
else {
    Write-Verbose "No query passed in"

    $Status = [HttpStatusCode]::BadRequest
    $ResError = @{
        Type = 'NoQueryException'
        Message = 'You need to pass a ?query to the URL!'
    }
}

Push-OutputBinding -Name Response -Value ([HttpResponseContext]@{
    StatusCode = $Status
    ContentType = 'application/json'
    Body = (@{Ok = $Ok; Query = $Query; Error = $ResError; Body = $ResBody} | ConvertTo-Json)
})
