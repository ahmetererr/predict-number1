"""
This file makes the app directory a Python package.
""" 

from flask import Flask, send_from_directory
from flask_cors import CORS
import os

# Get the absolute path to the static directory
STATIC_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'static'))

app = Flask(__name__, 
           static_folder=STATIC_DIR,
           static_url_path='/static')

CORS(app)

# Serve React App
@app.route('/')
def serve_react():
    return send_from_directory(STATIC_DIR, 'index.html')

# Serve static files
@app.route('/<path:path>')
def serve_file(path):
    if os.path.exists(os.path.join(STATIC_DIR, path)):
        return send_from_directory(STATIC_DIR, path)
    return send_from_directory(STATIC_DIR, 'index.html')

# API routes
@app.route('/api/predict', methods=['POST'])
def predict():
    # Your prediction logic here
    pass

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port) 