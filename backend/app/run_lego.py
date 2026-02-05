#!/usr/bin/env python3
"""
Flask wrapper to run the lego_api blueprint
"""
from flask import Flask
from flask_cors import CORS
from lego_api import lego_api_bp
import os

app = Flask(__name__)
CORS(app)

# Register the lego_api blueprint
app.register_blueprint(lego_api_bp)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    print(f"🚀 Starting Lego API on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False)
