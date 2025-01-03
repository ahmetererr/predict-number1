"""
This file makes the app directory a Python package.
""" 

from flask import Flask, send_from_directory
from flask_cors import CORS
import os

app = Flask(__name__, 
           static_folder=os.path.abspath(os.path.join(os.path.dirname(__file__), '../../web/build/static')),
           static_url_path='/static')

CORS(app)

# Serve static files from the React app
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path.startswith('static/'):
        return app.send_static_file(path.replace('static/', ''))
    return send_from_directory(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../web/build')), 
                             'index.html')

# API routes
@app.route('/predict', methods=['POST'])
def predict():
    # Your prediction logic here
    pass

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port) 