#!/bin/bash

# Exit on error
set -e

echo "Starting build process..."

# Frontend build
echo "Building frontend..."
cd web
npm install
npm run build

# Verify build directory exists
if [ ! -d "build" ]; then
    echo "Error: build directory not found!"
    exit 1
fi

echo "Frontend build completed successfully"
cd ..

# Backend setup
echo "Setting up backend..."
cd backend
pip install -r requirements.txt

echo "Build process completed successfully" 