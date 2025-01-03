#!/bin/bash

# Exit on error
set -e

echo "Starting build process..."

# Frontend build
echo "Building frontend..."
cd web
echo "Installing npm packages..."
npm install --legacy-peer-deps
echo "Running production build..."
npm run build

# Verify build directory and files
if [ ! -d "build" ]; then
    echo "Error: build directory not found!"
    exit 1
fi

if [ ! -f "build/index.html" ]; then
    echo "Error: index.html not found in build directory!"
    exit 1
fi

if [ ! -d "build/static" ]; then
    echo "Error: static directory not found in build directory!"
    exit 1
fi

echo "Frontend build completed successfully"
cd ..

# Backend setup
echo "Setting up backend..."
cd backend

echo "Installing Python packages..."
pip install -r requirements.txt

# Verify critical files
if [ ! -f "app/__init__.py" ]; then
    echo "Error: app/__init__.py not found!"
    exit 1
fi

if [ ! -f "wsgi.py" ]; then
    echo "Error: wsgi.py not found!"
    exit 1
fi

echo "Build process completed successfully" 