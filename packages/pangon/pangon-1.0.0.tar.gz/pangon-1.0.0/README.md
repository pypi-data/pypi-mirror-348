# Pangon

A simple Python package for secure password encryption and verification using AES-SIV and Argon2.

## Features

- Self-encryption using AES-SIV
- Argon2 password hashing with peppering

## Installation

```bash
pip install pangon
```

## Usage

```python
from pangon import hash_password, verify_password

hashed = hash_password("my_password123")
is_valid = verify_password("my_password123", hashed)
```
