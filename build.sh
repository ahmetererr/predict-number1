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

# Debug: Print Python version
python --version
which python

# Debug: Print current directory and list files
pwd
ls -la

# Create static directory if it doesn't exist
echo "Creating static directory..."
rm -rf static
mkdir -p static

# Copy frontend build files to backend/static
echo "Copying frontend build files to backend/static..."
cp -r ../web/build/* static/

# Verify static files were copied correctly
echo "Verifying static files..."
if [ ! -f "static/index.html" ]; then
    echo "Error: index.html not found in static directory!"
    exit 1
fi

if [ ! -d "static/static" ]; then
    echo "Error: static/static directory not found!"
    mkdir -p static/static
    cp -r ../web/build/static/* static/static/
fi

echo "Installing Python packages..."
pip install -r requirements.txt

# Debug: Verify installed packages
pip list

# Verify critical files
if [ ! -f "app/__init__.py" ]; then
    echo "Error: app/__init__.py not found!"
    exit 1
fi

if [ ! -f "wsgi.py" ]; then
    echo "Error: wsgi.py not found!"
    exit 1
fi

# Debug: Check static directory contents
echo "Checking static directory contents:"
ls -la static/

echo "Build process completed successfully" 