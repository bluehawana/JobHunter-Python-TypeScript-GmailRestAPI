#!/usr/bin/env python3
"""
Simple LaTeX file server endpoint for your existing Flask app
Add this to your main app to serve LaTeX files for Overleaf
"""
from flask import Flask, Response, send_file, abort
import os
import logging

logger = logging.getLogger(__name__)

def add_latex_routes(app: Flask):
    """Add LaTeX serving routes to your existing Flask app"""
    
    @app.route('/latex/<filename>')
    def serve_latex_file(filename):
        """Serve LaTeX files for Overleaf consumption"""
        try:
            # Security: only allow .tex files
            if not filename.endswith('.tex'):
                abort(404)
            
            # Look for file in latex_files directory
            latex_dir = os.path.join(os.path.dirname(__file__), 'latex_files')
            file_path = os.path.join(latex_dir, filename)
            
            if not os.path.exists(file_path):
                logger.warning(f"LaTeX file not found: {filename}")
                abort(404)
            
            # Read and serve the LaTeX content
            with open(file_path, 'r', encoding='utf-8') as f:
                latex_content = f.read()
            
            logger.info(f"📝 Serving LaTeX file: {filename} ({len(latex_content)} chars)")
            
            return Response(
                latex_content,
                mimetype='text/plain',
                headers={
                    'Content-Disposition': f'inline; filename="{filename}"',
                    'Access-Control-Allow-Origin': '*'
                }
            )
            
        except Exception as e:
            logger.error(f"❌ Error serving LaTeX file {filename}: {e}")
            abort(500)
    
    @app.route('/latex-list')
    def list_latex_files():
        """List available LaTeX files (for debugging)"""
        try:
            latex_dir = os.path.join(os.path.dirname(__file__), 'latex_files')
            
            if not os.path.exists(latex_dir):
                return {'files': [], 'message': 'No LaTeX files directory'}
            
            files = [f for f in os.listdir(latex_dir) if f.endswith('.tex')]
            
            file_info = []
            for filename in files:
                file_path = os.path.join(latex_dir, filename)
                stat = os.stat(file_path)
                file_info.append({
                    'filename': filename,
                    'size': stat.st_size,
                    'modified': stat.st_mtime,
                    'overleaf_url': f"https://www.overleaf.com/docs?snip_uri={request.host_url}latex/{filename}"
                })
            
            return {
                'files': file_info,
                'count': len(files),
                'directory': latex_dir
            }
            
        except Exception as e:
            logger.error(f"❌ Error listing LaTeX files: {e}")
            return {'error': str(e)}, 500

# Example integration with your main app
if __name__ == "__main__":
    # Test server
    app = Flask(__name__)
    add_latex_routes(app)
    
    @app.route('/')
    def index():
        return """
        <h1>LaTeX File Server</h1>
        <p>Serves LaTeX files for Overleaf integration</p>
        <ul>
            <li><a href="/latex-list">List LaTeX files</a></li>
            <li>Access files: <code>/latex/filename.tex</code></li>
        </ul>
        """
    
    print("🚀 Starting LaTeX file server...")
    print("📝 LaTeX files will be served at /latex/<filename>")
    print("🔗 Use with Overleaf: https://www.overleaf.com/docs?snip_uri=YOUR_URL/latex/filename.tex")
    
    app.run(host='0.0.0.0', port=5002, debug=True)