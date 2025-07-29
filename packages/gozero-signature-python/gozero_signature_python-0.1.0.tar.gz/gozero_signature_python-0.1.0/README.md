# Python Implementation of go-zero Signature Framework

A Python package that implements the signature mechanism compatible with the go-zero framework. This package allows Python applications to generate security signatures that can be verified by go-zero services.

## Features

- 🔐 Compatible with go-zero framework's signature mechanism
- 🔑 Generates HMAC-SHA256 signatures
- 🔒 Encrypts content with RSA public key
- 📝 Calculates MD5 fingerprints
- 🛡️ Supports the same security header format as go-zero
- 🚀 Easy to integrate with existing Python applications

## Requirements

- Python 3.6+
- pycryptodome

## Installation

You can install the package using pip:

```bash
# Install from PyPI
pip install gozero-signature-python

# Or install from source
git clone https://github.com/yourusername/gozero-signature-python.git
cd gozero-signature-python
pip install -r requirements.txt
pip install -e .
```

## Quick Start

Here's a simple example of how to use this package:

```python
from gozero_signature import GoZeroSigner

# Your RSA public key
public_key = """-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCyeDYV2ieOtNDi6tuNtAbmUjN9
pTHluAU5yiKEz8826QohcxqUKP3hybZBcm60p+rUxMAJFBJ8Dt+UJ6sEMzrf1rOF
YOImVvORkXjpFU7sCJkhnLMs/kxtRzcZJG6ADUlG4GDCNcZpY/qELEvwgm2kCcHi
tGC2mO8opFFFHTR0aQIDAQAB
-----END PUBLIC KEY-----"""

# Your secret key (can be plain text or base64 encoded)
key = "1234567890"

# Create a signer instance
signer = GoZeroSigner(public_key, key)

# Payload to sign
payload = {"msg": "hello world!"}

# Generate the post signature header
signature = signer.generate_post_signature(
    method="POST",
    url="http://example.com/api/endpoint",
    payload=payload
)

# Use the signature in your request
headers = {
    "Content-Type": "application/json",
    "X-Content-Security": signature
}

# Make your API request using requests or any other HTTP library
# requests.post("http://example.com/api/endpoint", json=payload, headers=headers)
```

## Advanced Usage

### Custom Headers

You can customize the security header name:

```python
signature = signer.generate_post_signature(
    method="POST",
    url="http://example.com/api/endpoint",
    payload=payload,
    header_name="X-Custom-Security"  # Optional: customize header name
)
```

### Error Handling

The package includes proper error handling for invalid keys and malformed requests:

```python
try:
    signature = signer.generate_post_signature(...)
except ValueError as e:
    print(f"Invalid input: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## Testing

Run the test suite:

```bash
python -m unittest test_gozero_signature.py
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## About go-zero

go-zero is a web and RPC framework with many built-in engineering practices. This package implements the signature functionality used in go-zero to secure API requests, but for Python applications that need to communicate with go-zero services.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
