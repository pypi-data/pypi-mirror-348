"""
ByteDarkLock(BDL) Module
----------------------
This module implements a class for handling symmetric encryption using AES and Fernet.
It includes features for key generation, encryption and decryption, and support for HMAC, 
key expiration, and code obfuscation.

Author: FakeFountain548
Initials: FG
"""

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from base64 import urlsafe_b64encode, urlsafe_b64decode
import os
import json
import hmac
import hashlib
from datetime import datetime, timedelta
import random
import string
import re
import base64
import py_compile

class ByteDarkLock:
    """ByteDarkLock provides symmetric encryption, decryption, and file obfuscation utilities.
    Features:
    - Key generation for Fernet and AES modes, with optional HMAC authentication and TTL/expiration.
    - Encryption and decryption of strings using selected keys.
    - One-time decryption to prevent replay attacks.
    - Timed decryption (alias for standard decryption).
    - Python script obfuscation: removes docstrings/comments, renames identifiers, encodes literals, and optionally compiles to .pyc.
    Attributes:
        keys (dict): Stores key metadata indexed by key_id.
        _used_tokens (set): Tracks tokens already decrypted with decrypt_once.
    Methods:
        generate_key(key_id, mode='fernet', use_hmac=False, ttl=None, unlock_at=None) -> dict:
            Generates and stores a new encryption key with metadata.
        encrypt(data, key_id) -> str:
            Encrypts a string using the specified key.
        decrypt(token, key_id) -> str:
            Decrypts a token using the specified key.
        decrypt_once(token, key_id) -> str:
            Decrypts a token only once; raises error if reused.
        timed_decrypt(token, key_id) -> str:
            Alias for decrypt; intended for future timed access.
        obfuscate_file(input_path, output_path, pyc=True):
            Obfuscates a Python script by removing docstrings/comments, renaming identifiers,
            encoding literals, and optionally compiling to .pyc bytecode.
    Raises:
        KeyError: If a key is not found.
        ValueError: If a key has expired, HMAC verification fails, or a token is reused."""
    def __init__(self):
        self.keys = {}
        self._used_tokens = set()

    def generate_key(self, key_id: str, mode: str = "fernet", use_hmac: bool = False, ttl: int = None, unlock_at: datetime = None) -> dict:
        metadata = {"mode": mode, "use_hmac": use_hmac}
        if mode == "fernet":
            metadata["key"] = Fernet.generate_key()
        elif mode == "aes":
            metadata["key"] = os.urandom(32)
            if use_hmac:
                metadata["hmac_key"] = os.urandom(32)
        else:
            raise ValueError(f"Mode '{mode}' not supported.")
        if ttl:
            metadata["expires_at"] = (datetime.utcnow() + timedelta(seconds=ttl)).isoformat()
        if unlock_at:
            metadata["unlock_at"] = unlock_at.isoformat() if isinstance(unlock_at, datetime) else unlock_at
        metadata["created_at"] = datetime.utcnow().isoformat()
        self.keys[key_id] = metadata
        return metadata

    def encrypt(self, data: str, key_id: str) -> str:
        entry = self.keys.get(key_id)
        if not entry:
            raise KeyError("Key not found.")
        if entry.get("expires_at") and datetime.utcnow().isoformat() > entry["expires_at"]:
            raise ValueError("Key has expired.")
        key, mode = entry["key"], entry["mode"]
        if mode == "fernet":
            return Fernet(key).encrypt(data.encode()).decode()
        elif mode == "aes":
            iv = os.urandom(16)
            cipher = Cipher(algorithms.AES(key), modes.CFB(iv))
            ct = cipher.encryptor().update(data.encode()) + cipher.encryptor().finalize()
            payload = iv + ct
            if entry.get("use_hmac"):
                auth = hmac.new(entry["hmac_key"], payload, hashlib.sha256).digest()
                payload = auth + payload
            return urlsafe_b64encode(payload).decode()

    def decrypt(self, token: str, key_id: str) -> str:
        entry = self.keys.get(key_id)
        if not entry:
            raise KeyError("Key not found.")
        if entry.get("expires_at") and datetime.utcnow().isoformat() > entry["expires_at"]:
            raise ValueError("Key has expired.")
        key, mode = entry["key"], entry["mode"]
        data = urlsafe_b64decode(token.encode())
        if mode == "fernet":
            return Fernet(key).decrypt(token.encode()).decode()
        elif mode == "aes":
            if entry.get("use_hmac"):
                auth_recv, payload = data[:32], data[32:]
                auth_calc = hmac.new(entry["hmac_key"], payload, hashlib.sha256).digest()
                if not hmac.compare_digest(auth_recv, auth_calc):
                    raise ValueError("HMAC verification failed.")
            else:
                payload = data
            iv, ct = payload[:16], payload[16:]
            cipher = Cipher(algorithms.AES(key), modes.CFB(iv))
            return cipher.decryptor().update(ct) + cipher.decryptor().finalize().decode()

    def decrypt_once(self, token: str, key_id: str) -> str:
        if token in self._used_tokens:
            raise ValueError("This message has already been decrypted.")
        plaintext = self.decrypt(token, key_id)
        self._used_tokens.add(token)
        return plaintext

    def timed_decrypt(self, token: str, key_id: str) -> str:
        return self.decrypt(token, key_id)

    def obfuscate_file(self, input_path: str, output_path: str, pyc: True):
        """
        Obfuscates a Python script:
            - Keeps import and from statements intact.
            - Removes docstrings and comments.
            - Renames internal identifiers.
            - Encodes literals in Base64.
            - Wraps the obfuscated code in exec(base64...) with well-separated lines.
            - Optionally compiles to .pyc bytecode and removes the resulting .py file.
        """
        import pathlib, py_compile, os

        # Read lines from the original script
        lines = pathlib.Path(input_path).read_text(encoding='utf-8').splitlines(keepends=True)

        # Separate imports and the rest
        import_lines = []
        other_lines = []
        for line in lines:
            if line.lstrip().startswith(('import ', 'from ')):
                import_lines.append(line.rstrip() + '')
            else:
                other_lines.append(line)

        # Process main code
        code = ''.join(other_lines)
        code = re.sub(r'""".*?"""', '', code, flags=re.DOTALL)
        code = re.sub(r'#.*', '', code)
        # Identifier renaming
        tokens = set(re.findall(r'[_a-zA-Z][_a-zA-Z0-9]*', code))
        reserved = {...}
        mapping = {tok: '_' + ''.join(random.choices(string.ascii_letters + string.digits, k=6))
                for tok in tokens if tok not in reserved}
        code = re.sub(r'[_a-zA-Z][_a-zA-Z0-9]*', lambda m: mapping.get(m.group(0), m.group(0)), code)
        # Encode literals
        def encode_string(m):
            b64 = base64.b64encode(m.group(1).encode('utf-8')).decode('utf-8')
            return f"base64.b64decode('{b64}').decode('utf-8')"
        code = re.sub(r'"([^"]*)"', encode_string, code)
        code = re.sub(r"'([^']*)'", encode_string, code)

        # Obfuscated alias and payload
        alias = '_' + ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        alias_line = f"{alias} = symm.ByteDarkLock()"
        payload = base64.b64encode(code.encode('utf-8')).decode('utf-8')
        exec_line = f"exec(base64.b64decode('{payload}').decode('utf-8'))"

        # Write obfuscated .py file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('import base64\n')  # always separated
            for imp in import_lines:
                f.write(imp + '\n')
            f.write('\n')
            f.write(alias_line + '\n')
            f.write('\n')
            f.write(exec_line + '\n')

        if pyc:
            # Compile to bytecode and clean up
            try:
                py_compile.compile(output_path, cfile=output_path + 'c', optimize=2)
                os.remove(output_path)
            except Exception as e:
                print(f"Error compiling bytecode: {e}")
            else:
                # If not compiling, just leave the obfuscated .py
                pass