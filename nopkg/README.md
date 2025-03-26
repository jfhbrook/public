# nopkg

`nopkg` is a work in progress project to write a dependency manager for things which don't have packages. It will support pulling files downloaded over http, files unpacked from archives downloaded over http, and files copied from git repos.

Its initial empetus was managing dependencies for [love2d](https://love2d.org/) and [openscad](https://openscad.org/), but it's intended to be general purpose.

It is currently not useful. Stay tuned.

## TODO

- Cache
  - Implement `nopkg cache update`
  - Add `--since` and `--max-age` flags to relevant commands
  - Add TZ conversion to `nopkg cache show`
    - Add time zone conversion flag
  - Store and respect [etags](https://en.wikipedia.org/wiki/HTTP_ETag)
- Install
  - Load manifest
  - Load lockfile
  - For each dependency...
    - Is it in the lockfile? Does the ostensive file actually exist?
      - If so, leave alone (unless updating)
      - If not...
        - Is the file in the cache?
          - If not, download it
        - If an archive, is it unpacked?
          - If not, unpack it
        - Copy from cache to project
  - For each lock entry...
    - Is it represented by a dependency?
      - If not...
        - Remove it from the project (unless `--no-remove`)
        - Remove it from the lockfile (unless `--no-remove`)
- Remove command
  - Actually implement
  - Call install on remove
- Update
  - A special case of install
- Logging/formatting
  - `text` format should implement no-color log output
  - `cli` format should not include timestamps
  - `extended` format should more or less just use the "pretty" formatter
  - `json` format in `cache show` should print JSON, not a table
- Customize CLI
  - Descriptions for arguments
  - Descriptions for commands
  - Aliases for commands
  - Default behavior for no command
- `nopkg cache repair`
- Implement archive unpacking
- Implement git repos
- Move away from `anyhow`
  - Presumably `thiserror`
