#!/bin/bash

# ================ Start Nginx ================
echo "[INFO] Starting Nginx in foreground mode..."
nginx -g "daemon off;"

# ================ Activate Virtual Environment ================
echo "[INFO] Activating Python virtual environment..."
. /venv/bin/activate

# ================ Start JupyterLab ================
echo "[INFO] Starting JupyterLab..."
poetry run jupyter lab --ip=0.0.0.0 --port=8443 --no-browser --allow-root --NotebookApp.port_retries=0 --NotebookApp.allow_origin='*'

# ================ Main Execution Loop ================
echo "[INFO] Container startup complete. Ready to serve requests."

# Infinite loop to handle SIGINT, SIGTERM signals
while true; do
  sleep 1 &
  wait $!
done
