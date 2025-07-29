# ByteDarkLock (BDL)

**ByteDarkLock** is a Python module for advanced symmetric encryption and script obfuscation, designed to protect your logic and data easily.

## Main Features

* **Symmetric encryption** with **AES-256** (CFB mode) and **Fernet** (AES-128 + HMAC-SHA256).
* Optional **HMAC authentication** to detect tampering in AES.
* **Key expiration** (`ttl`) and **scheduled unlock** (`unlock_at`).
* **One-time decryption** (`decrypt_once`) to prevent replay attacks.
* **Python script obfuscation**:

    * Keeps `import` and `from` statements intact.
    * Removes docstrings and comments.
    * Renames internal identifiers.
    * Encodes literals in Base64.
    * Packages into `exec(base64...)` for maximum opacity.
    * **Option** to automatically compile to bytecode (`.pyc`) and remove the obfuscated `.py`.

## Requirements

Dependencies are listed in `requirements.py` (or install manually):

```text
cryptography>=3.4.7
Pillow>=8.1.0
```

Quick installation with `pip`:

```bash
pip install cryptography Pillow
```

## Quick Start Guide

```python
from BDL.ByteDarkLock import ByteDarkLock

# Initialize
bdl = ByteDarkLock()

# 1. Generate a Fernet key with a TTL of 3600s
meta = bdl.generate_key(
        key_id="my_key",
        mode="fernet",
        ttl=3600
)

# 2. Encrypt and decrypt
token = bdl.encrypt("Hello World", "my_key")
print("Encrypted:", token)

plain = bdl.decrypt(token, "my_key")
print("Decrypted:", plain)

# 3. One-time decryption
bdl.decrypt_once(token, "my_key")  # works once
# bdl.decrypt_once(token, "my_key")  # now fails

# 4. Obfuscate a script and generate bytecode
bdl.obfuscate_file(
        input_path="app.py",
        output_path="app_obf.py",
        pyc=True  # compiles to app_obf.pyc and deletes the .py
        #pyc=False (Does not convert to .pyc)
)
```

## API Reference

### Class `ByteDarkLock`

#### `generate_key(key_id, mode='fernet', use_hmac=False, ttl=None, unlock_at=None) -> dict`

Generates and stores a key.

* **key\_id** (`str`): Unique identifier.
* **mode** (`'fernet'|'aes'`): Algorithm.
* **use\_hmac** (`bool`): AES only.
* **ttl** (`int`): Lifetime in seconds.
* **unlock\_at** (`datetime`|`str`): Unlock date/time.

Returns metadata with `key`, `expires_at`, `created_at`, etc.

#### `encrypt(data, key_id) -> str`

Encrypts `data` with the key `key_id`.

#### `decrypt(token, key_id) -> str`

Decrypts `token` with the key `key_id`.

#### `decrypt_once(token, key_id) -> str`

Like `decrypt`, but allows only one use.

#### `timed_decrypt(token, key_id) -> str`

Alias for `decrypt` (for future time-lock feature).

#### `obfuscate_file(input_path, output_path, pyc=True)`

Obfuscates and optionally compiles to `.pyc`:

* **input\_path** (`str`): Original script.
* **output\_path** (`str`): Obfuscated `.py` output file.
* **pyc** (`bool`): Compile to `.pyc` and remove `.py`.

## Contributions

1. Fork the repository.
2. Create a branch (`git checkout -b feature/new-function`).
3. Make your changes and commit (`git commit -m 'Add xyz'`).
4. Submit a pull request.

## License

This project is under the \[MIT License].