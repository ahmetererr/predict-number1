#!/bin/bash

# Frontend build
echo "Building frontend..."
cd web
npm install
npm run build
cd ..

# Backend setup
echo "Setting up backend..."
cd backend
pip install -r requirements.txt 