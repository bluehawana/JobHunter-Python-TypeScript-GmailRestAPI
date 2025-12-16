"""
🧱 LEGO Bricks Job Application Generator - Flask App
Main application entry point
"""

from flask import Flask
from flask_cors import CORS
from app.lego_api import lego_api
from pathlib import Path

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend

# Register blueprints
app.register_blueprint(lego_api)

# Create necessary directories
Path('generated_applications').mkdir(exist_ok=True)

@app.route('/')
def index():
    return {
        'message': '🧱 LEGO Bricks Job Application Generator API',
        'version': '1.0.0',
        'endpoints': {
            'analyze': '/api/analyze-job',
            'generate': '/api/generate-lego-application',
            'regenerate': '/api/regenerate-application',
            'download': '/api/download/<folder>/<filename>',
            'preview': '/api/preview/<folder>/<filename>'
        }
    }

@app.route('/health')
def health():
    return {'status': 'healthy'}

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
