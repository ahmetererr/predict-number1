"""
This file makes the app directory a Python package.
""" 

from flask import Flask, send_from_directory, send_file
from flask_cors import CORS
import os

# Get the absolute path to the build directory
BUILD_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'web', 'build'))

app = Flask(__name__)
CORS(app)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path and os.path.exists(os.path.join(BUILD_DIR, path)):
        return send_from_directory(BUILD_DIR, path)
    return send_file(os.path.join(BUILD_DIR, 'index.html'))

@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory(os.path.join(BUILD_DIR, 'static'), path)

# API routes
@app.route('/predict', methods=['POST'])
def predict():
    # Your prediction logic here
    pass

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port) 