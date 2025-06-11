# pgp-dm

Use PGP to encrypt and decrypt direct messages. Based on the following blog post:

<https://blog.nthia.dev/pgp-dm.html>

## Install

I may package this in the future. But for now, copy [`./bin/pgp-dm`](./bin/pgp-dm) into your PATH.

## Getting Started

### Dependencies

* `pgp`
* For clipboard support, `wl-copy`/`wl-paste` or `pbcopy`/`pbpaste`
* For QR code support, `qrencode` and `zbar-tools`

### Generating and Exchanging Keys

First, you will need to create PGP keys:

```bash
pgp-dm generate-primary-key "${YOUR_NAME}" "${YOUR_EMAIL}"
pgp-dm generate-signing-key 
pgp-dm generate-encryption-key 
```

Then, export your key:

```bash
pgp-dm export-public-key "${YOUR_NAME}" --clipboard
```

This will write your key to the clipboard. You can then share it publicly over HTTP, for instance with GitHub.

Now, import your friend's key:

```bash
pgp-dm import-public-key "${KEY_URL}"
```

After this step, you should see your friend's key if you list them out:

```bash
pgp-dm list-keys
```

### Sending and Receiving Messages

To encrypt a message, you can run:

```bash
pgp-dm encrypt "${FRIEND_NAME}" --clipboard
```

This will open a text buffer in vim, and then encrypt it and send it to your clipboard after the ol' save and quit.

Finally, once your friend responds, you can copy their message to the clipboard and decrypt it by running:

```bash
pgp-dm decrypt
```

This tool also supports encrypting and decrypting to QR codes with:

```bash
pgp-dm encrypt-qr "${FRIEND_NAME}" --clipboard
pgp-dm decrypt-qr
```

## License

MIT/X11. See `LICENSE` for details.
