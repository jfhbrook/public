# nopkg

## TODO

- Logging - `tracing` and `tracing_subscriber`
- Create cache
  - `~/.local/cache/nopkg/files`
  - `~/.local/cache/nopkg/index.json`
    - url -> hash
  - Store file in `~/.local/cache/nopkg/files/{{ hash }}`
  - `get_file(url) -> Utf8PathBuf`
  - `has_file(url) -> bool`
  - `download_file(url) -> Utf8PathBuf`
- Install
  - For each dependency, `get_file_path(hash(url))`
