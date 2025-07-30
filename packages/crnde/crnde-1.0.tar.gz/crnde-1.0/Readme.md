# CRNEN (Cryptographic Robust Nested Encryption)

An advanced multi-layer encryption/decryption system that provides high security by combining AES-256-GCM and ChaCha20.

## Features

- Multi-layer encryption (AES-256-GCM + ChaCha20)
- Secure key derivation using PBKDF2
- Message integrity verification using HMAC-SHA512

## how to use

### install
```
pip install crnde
```
### use in .py file
```
import crnde

crnde.encrypt(text,key)
crnde.decrypt(encrypted text,key)
```