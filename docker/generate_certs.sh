#!/bin/bash

# Set working directory within the script
cd /etc/nginx/certs

# Certificate Generation Logic
openssl genrsa -out _wildcard.qiskitondocker.dev+3-key.pem 4096 && \
openssl req -new -key _wildcard.qiskitondocker.dev+3-key.pem -out _wildcard.qiskitondocker.dev+3.csr -subj "/CN=*.qiskitondocker.dev" -config <( \
cat <<-EOF \
[req]
default_bits = 2048
prompt = no
default_md = sha256
distinguished_name = dn

[dn]
CN = *.qiskitondocker.dev 

[SAN]
subjectAltName = DNS:*.qiskitondocker.dev, DNS:localhost, IP:127.0.0.1, IP:::1
EOF
) && \
openssl x509 -req -days 365 -in _wildcard.qiskitondocker.dev+3.csr -signkey _wildcard.qiskitondocker.dev+3-key.pem -out _wildcard.qiskitondocker.dev+3.pem && \
openssl dhparam -out dhparam.pem 4096
