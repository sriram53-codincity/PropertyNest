#!/bin/bash
# setup.sh - PACE26 Track 1 Deployment Script

# Exit immediately if a command exits with a non-zero status
set -e

echo "=== 1. Installing Python Dependencies ==="
pip install --upgrade pip
pip install -r requirements.txt

echo "=== 2. Installing Node Dependencies ==="
# Ensure Node is available or this will fail
if [ -d "frontend" ]; then
    cd frontend
    npm install
    # Optional: Build the React app if required by the environment
    # npm run build
    cd ..
else
    echo "Warning: frontend directory not found. Skipping Node dependencies."
fi

echo "=== 3. Starting Nginx ==="
# Note: Nginx usually requires sudo. If running in an unprivileged environment, this will gracefully warn.
if command -v systemctl >/dev/null 2>&1; then
    sudo systemctl restart nginx || echo "Warning: Nginx failed to restart (are you running with correct permissions?)"
elif command -v service >/dev/null 2>&1; then
    sudo service nginx restart || echo "Warning: Nginx failed to restart"
else
    echo "Warning: systemctl or service commands not found. Skipping Nginx restart."
fi

echo "Setup completed successfully!"
