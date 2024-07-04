#!/bin/bash

# Set working directory within the script
cd /etc/nginx/certs

# Install mkcert and generate the local CA
mkcert -install

# Generate the wildcard certificate using mkcert
mkcert -cert-file _wildcard.qiskitondocker.dev+3.pem -key-file _wildcard.qiskitondocker.dev+3-key.pem "*.qiskitondocker.dev" localhost 127.0.0.1 ::1

# Generate the DH parameters file if it doesn't exist
if [ ! -f "dhparam.pem" ]; then
    echo "[INFO] Generating DH parameters..."
    openssl dhparam -out dhparam.pem 2048
fi

# Set permissions and ownership for certificates
echo "[INFO] Setting permissions and ownership for certificates..."
chown nginx:nginx /etc/nginx/certs/*.pem
chmod 600 /etc/nginx/certs/*.pem
