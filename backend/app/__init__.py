"""
This file makes the app directory a Python package.
""" 

from flask import Flask, send_from_directory
from flask_cors import CORS
import os

app = Flask(__name__, static_folder='../../web/build', static_url_path='')
CORS(app)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

# API routes will be added here
@app.route('/predict', methods=['POST'])
def predict():
    # Your prediction logic here
    pass

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port) 