# GridAPPSD Certificate Store

[![Python Tests](https://github.com/GRIDAPPSD/gridappsd-certificate-store/actions/workflows/python-test.yml/badge.svg)](https://github.com/GRIDAPPSD/gridappsd-certificate-store/actions/workflows/python-test.yml)
[![PyPI version](https://badge.fury.io/py/gridappsd-certificate-store.svg)](https://badge.fury.io/py/gridappsd-certificate-store)
[![License](https://img.shields.io/badge/License-BSD_3--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A flexible and secure X.509 certificate generator and store for IEEE 2030.5 smart grid devices, IoT applications, and general TLS/HTTPS requirements.

## Features

- **Complete Certificate Generation**: Create CAs, device certificates, and self-signed certificates
- **IEEE 2030.5 Support**: Designed with IEEE 2030.5-2018 standard in mind for smart grid communications
- **Certificate Store**: Persistent storage and retrieval of certificates with lookup capabilities
- **Device Identity**: LFDI/SFDI calculation and extraction for IEEE 2030.5 device identification
- **Access Control**: Client registry with granular access control for secure device communications
- **Multiple Key Types**: Support for both RSA and Elliptic Curve cryptography
- **Flexible Subject Alternative Names**: Create certificates with URIs, DNS names, IP addresses, or email addresses
- **TLS 1.2+ Compliance**: Generate certificates that meet security requirements for modern TLS
- **Certificate Persistence**: Easily save and load certificates and private keys
- **Web Server Certificates**: Specialized method for generating HTTPS server certificates

## Installation

```bash
# Install from PyPI
pip install gridappsd-certificate-store

# Or with Poetry
poetry add gridappsd-certificate-store
```

## Quick Start

### Certificate Generation

```python
from gridappsd_certs import DeviceCertificateGenerator

# Initialize the generator
cert_gen = DeviceCertificateGenerator(key_type='rsa', key_size=2048)

# Create a CA certificate
ca_attrs = {
    'common_name': 'GridAPPSD Root CA',
    'organization': 'GridAPPSD',
    'country': 'US',
    'organizational_unit': 'Security'
}

ca_cert, ca_key = cert_gen.create_ca_certificate(ca_attrs, valid_days=3652)

# Create a device certificate for IEEE 2030.5
device_attrs = {
    'common_name': 'Smart Meter 101',
    'organization': 'GridAPPSD',
    'country': 'US',
    'organizational_unit': 'Smart Meters',
    'serial_number': 'SM101-12345'
}

device_cert, device_key = cert_gen.create_device_certificate(
    device_attrs,
    ca_cert,
    ca_key,
    device_id="11111111-2222-3333-4444-555555555555"
)

# Save certificates and keys
cert_gen.save_certificate(ca_cert, 'ca_cert.pem')
cert_gen.save_private_key(ca_key, 'ca_key.pem', password='secure-password')
cert_gen.save_certificate(device_cert, 'device_cert.pem')
cert_gen.save_private_key(device_key, 'device_key.pem')
```

### Certificate Store

```python
from gridappsd_certs import (
    CertificateStore,
    calculate_lfdi_from_certificate,
    calculate_sfdi_from_lfdi
)

# Create a certificate store with persistent storage
store = CertificateStore(storage_path="/path/to/cert/store")

# Add certificates to the store
ca_fingerprint = store.add_certificate(ca_cert, ca_key, alias="Root CA")
device_fingerprint = store.add_certificate(device_cert, device_key, alias="Device 101")

# Look up certificates by various attributes
cert_by_fingerprint = store.get_certificate_by_fingerprint(device_fingerprint)
certs_by_common_name = store.get_certificate_by_common_name("Smart Meter 101")

# Get IEEE 2030.5 identifiers
lfdi = calculate_lfdi_from_certificate(device_cert)
sfdi = calculate_sfdi_from_lfdi(lfdi)
print(f"Device LFDI: {lfdi}")
print(f"Device SFDI: {sfdi}")

# Get private key for a certificate
device_key = store.get_private_key(device_fingerprint)
```

### Client Registry with Access Control

```python
from gridappsd_certs import (
    ClientRegistry,
    ClientProfile,
    AccessControl,
    extract_identity_from_certificate
)

# Create a certificate store and registry
cert_store = CertificateStore(storage_path="/path/to/certs")
registry = ClientRegistry(cert_store=cert_store)

# Create access control rules
acl = AccessControl()
acl.add_rule("/dcap", "GET", allow=True) # Allow access to device capability
acl.add_rule("/edev/*", "GET", allow=True) # Allow read access to end devices
acl.add_rule("/drp/*", "*", allow=True) # Allow all methods on demand response

# Create a client profile
client_profile = ClientProfile(
    client_id="device-101",
    acl=acl
)

# Add client to registry with its certificate
registry.add_client("device-101", certificate=device_cert, profile=client_profile)

# Later, authenticate a client with its certificate
client = registry.get_client_by_certificate(device_cert)
if client:
    # Check if client can access a resource
    if client.can_access("/drp/1/dre", "GET"):
        print("Access granted to demand response events")
    else:
        print("Access denied")

# Save registry for persistence
registry.save("/path/to/registry.json")
```

## IEEE 2030.5 Integration

The library is designed with IEEE 2030.5-2018 standard in mind, which requires:

- TLS 1.2 with AES-CCM mode of operation
- X.509 certificates for mutual authentication
- Device identification via LFDI/SFDI and UUID in Subject Alternative Name

```python
# Extract IEEE 2030.5 device information from certificate
from gridappsd_certs import extract_device_information_from_certificate

device_info = extract_device_information_from_certificate(device_cert)
print(f"LFDI: {device_info['lfdi']}")
print(f"SFDI: {device_info['sfdi']}")
print(f"Device ID: {device_info['device_id']}")
```

## Certificate Validation

```python
from gridappsd_certs import CertificateValidator

# Create validator with trusted CA certificates
validator = CertificateValidator(trust_store=[ca_cert])

# Validate a device certificate
result = validator.validate(device_cert)
if result.valid:
    print("Certificate is valid")
else:
    print(f"Certificate validation failed: {', '.join(result.errors)}")
```

## Certificate Attributes

The following attributes can be included in certificate subject information:

| Dictionary Key | Description |
|----------------|-------------|
| `common_name` | The common name (CN) for the certificate |
| `country` | Two-letter country code (e.g., 'US') |
| `state` | State or province name |
| `locality` | City or locality name |
| `organization` | Organization name |
| `organizational_unit` | Department or unit within organization |
| `email` | Email address |
| `serial_number` | Serial number (useful for device identification) |

## Development

```bash
# Clone the repository
git clone https://github.com/GRIDAPPSD/gridappsd-certificate-store.git
cd gridappsd-certificate-store

# Install dependencies with Poetry
poetry install

# Run tests
poetry run pytest

# Run tests with coverage
poetry run pytest --cov=gridappsd_certs

# Format code
poetry run black gridappsd_certs
```
