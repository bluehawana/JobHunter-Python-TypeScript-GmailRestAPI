#!/usr/bin/env python3
"""
Simple LaTeX file server for Overleaf API integration
Serves temporary LaTeX files that can be opened in Overleaf
"""
from flask import Flask, Response, request, jsonify
import tempfile
import os
import time
import threading
from typing import Dict

app = Flask(__name__)

# In-memory storage for temporary LaTeX files
latex_files: Dict[str, str] = {}
file_timestamps: Dict[str, float] = {}

def cleanup_old_files():
    """Clean up files older than 1 hour"""
    current_time = time.time()
    expired_files = []
    
    for filename, timestamp in file_timestamps.items():
        if current_time - timestamp > 3600:  # 1 hour
            expired_files.append(filename)
    
    for filename in expired_files:
        latex_files.pop(filename, None)
        file_timestamps.pop(filename, None)
    
    print(f"🧹 Cleaned up {len(expired_files)} expired LaTeX files")

def start_cleanup_timer():
    """Start periodic cleanup of old files"""
    cleanup_old_files()
    timer = threading.Timer(1800, start_cleanup_timer)  # Clean every 30 minutes
    timer.daemon = True
    timer.start()

@app.route('/latex/<filename>')
def serve_latex(filename):
    """Serve LaTeX file for Overleaf consumption"""
    if filename not in latex_files:
        return "File not found", 404
    
    latex_content = latex_files[filename]
    return Response(latex_content, mimetype='text/plain')

@app.route('/upload-latex', methods=['POST'])
def upload_latex():
    """Upload LaTeX content and get URL for Overleaf"""
    try:
        data = request.get_json()
        latex_content = data.get('latex_content', '')
        
        if not latex_content:
            return jsonify({'error': 'No LaTeX content provided'}), 400
        
        # Generate unique filename
        timestamp = int(time.time())
        filename = f"resume_{timestamp}.tex"
        
        # Store in memory
        latex_files[filename] = latex_content
        file_timestamps[filename] = time.time()
        
        # Generate URLs
        base_url = request.host_url.rstrip('/')
        latex_url = f"{base_url}/latex/{filename}"
        overleaf_url = f"https://www.overleaf.com/docs?snip_uri={latex_url}"
        
        return jsonify({
            'latex_url': latex_url,
            'overleaf_url': overleaf_url,
            'filename': filename,
            'message': 'LaTeX file uploaded successfully'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/generate-resume', methods=['POST'])
def generate_resume():
    """Generate LaTeX resume and return Overleaf URL"""
    try:
        data = request.get_json()
        job = data.get('job', {})
        
        # Import the generator
        from overleaf_pdf_generator import OverleafPDFGenerator
        
        generator = OverleafPDFGenerator()
        latex_content = generator._generate_latex_content(job)
        
        # Generate unique filename
        timestamp = int(time.time())
        filename = f"resume_{job.get('company', 'company').lower()}_{timestamp}.tex"
        
        # Store in memory
        latex_files[filename] = latex_content
        file_timestamps[filename] = time.time()
        
        # Generate URLs
        base_url = request.host_url.rstrip('/')
        latex_url = f"{base_url}/latex/{filename}"
        overleaf_url = f"https://www.overleaf.com/docs?snip_uri={latex_url}"
        
        return jsonify({
            'latex_url': latex_url,
            'overleaf_url': overleaf_url,
            'filename': filename,
            'job_title': job.get('title', 'Unknown'),
            'company': job.get('company', 'Unknown'),
            'message': 'Resume LaTeX generated successfully - click Overleaf URL to compile!'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'active_files': len(latex_files),
        'uptime': time.time()
    })

@app.route('/')
def index():
    """Simple index page"""
    return """
    <h1>LaTeX Server for Overleaf Integration</h1>
    <p>This server provides LaTeX files that can be opened directly in Overleaf.</p>
    
    <h2>Endpoints:</h2>
    <ul>
        <li><code>POST /generate-resume</code> - Generate resume LaTeX and get Overleaf URL</li>
        <li><code>POST /upload-latex</code> - Upload custom LaTeX content</li>
        <li><code>GET /latex/&lt;filename&gt;</code> - Serve LaTeX file</li>
        <li><code>GET /health</code> - Health check</li>
    </ul>
    
    <h2>Example Usage:</h2>
    <pre>
curl -X POST http://localhost:5001/generate-resume \\
  -H "Content-Type: application/json" \\
  -d '{
    "job": {
      "title": "Senior DevOps Engineer",
      "company": "Spotify",
      "description": "Kubernetes, AWS, Docker, CI/CD"
    }
  }'
    </pre>
    """

if __name__ == '__main__':
    # Start cleanup timer
    start_cleanup_timer()
    
    print("🚀 Starting LaTeX server for Overleaf integration...")
    print("📝 Upload LaTeX files and get Overleaf URLs!")
    print("🔗 Example: POST /generate-resume with job data")
    
    app.run(host='0.0.0.0', port=5001, debug=True)