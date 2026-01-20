#!/usr/bin/env bash
# Exit on error
set -o errexit

echo "Installing Python dependencies..."
pip install -r backend/requirements.txt

# NOTE: Frontend build is handled by Netlify in this split-deployment architecture.
# If you were deploying a monolith, you would uncomment the following:
# echo "Building Frontend..."
# cd frontend
# npm install
# npm run build
# cd ..

echo "Backend Build complete."
