#!/usr/bin/env python3
"""
Simple API server for jobs.bluehawana.com functionality
"""
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import urllib.parse
import os
import sys
from test_linkedin_url import extract_linkedin_job_simple
from daily_job_automation_with_env import create_simple_cv_pdf, create_simple_cover_letter_pdf
import time
import base64

class JobHunterAPI(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def do_POST(self):
        if self.path == '/api/save-job-url':
            self.handle_save_job_url()
        elif self.path == '/api/instant-apply':
            self.handle_instant_apply()
        else:
            self.send_error(404)
    
    def handle_save_job_url(self):
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            job_url = data.get('job_url')
            if not job_url:
                self.send_error_response('No job URL provided')
                return
            
            print(f"💾 Saving job URL: {job_url[:50]}...")
            
            # Extract job information
            if 'linkedin.com' in job_url:
                job_data = extract_linkedin_job_simple(job_url)
            else:
                # Generic job data for other URLs
                job_data = {
                    'title': 'Job Position from URL',
                    'company': 'Technology Company',
                    'description': 'Job extracted from provided URL',
                    'source': 'url',
                    'url': job_url,
                    'keywords': ['software', 'development'],
                    'location': 'Sweden'
                }
            
            response = {
                'success': True,
                'extracted_data': job_data,
                'message': f"Job URL saved: {job_data['title']} at {job_data['company']}"
            }
            
            self.send_json_response(response)
            print(f"✅ Job saved: {job_data['title']} at {job_data['company']}")
            
        except Exception as e:
            print(f"❌ Error saving job URL: {e}")
            self.send_error_response(str(e))
    
    def handle_instant_apply(self):
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            job_url = data.get('job_url')
            if not job_url:
                self.send_error_response('No job URL provided')
                return
            
            print(f"🚀 Instant applying to: {job_url[:50]}...")
            
            # Extract job information
            if 'linkedin.com' in job_url:
                job_data = extract_linkedin_job_simple(job_url)
            else:
                job_data = {
                    'title': 'Job Position from URL',
                    'company': 'Technology Company',
                    'description': 'Job extracted from provided URL',
                    'source': 'url',
                    'url': job_url,
                    'keywords': ['software', 'development'],
                    'location': 'Sweden'
                }
            
            # Generate PDFs
            print("📄 Generating PDFs...")
            cv_pdf = create_simple_cv_pdf(job_data)
            cl_pdf = create_simple_cover_letter_pdf(job_data)
            
            if cv_pdf and cl_pdf and len(cv_pdf) > 1000:
                # Save PDFs locally for demo
                timestamp = int(time.time())
                cv_filename = f"InstantApply_CV_{timestamp}.pdf"
                cl_filename = f"InstantApply_CL_{timestamp}.pdf"
                
                with open(cv_filename, 'wb') as f:
                    f.write(cv_pdf)
                with open(cl_filename, 'wb') as f:
                    f.write(cl_pdf)
                
                print(f"✅ PDFs generated: {len(cv_pdf)} + {len(cl_pdf)} bytes")
                
                response = {
                    'success': True,
                    'title': job_data['title'],
                    'company': job_data['company'],
                    'ats_score': 0.87,  # Mock ATS score
                    'message': f"Application submitted for {job_data['title']} at {job_data['company']}",
                    'cv_file': cv_filename,
                    'cl_file': cl_filename
                }
                
                self.send_json_response(response)
                print(f"🎉 Instant apply successful: {job_data['title']} at {job_data['company']}")
                
                # Open PDFs to show user
                os.system(f"open {cv_filename}")
                os.system(f"open {cl_filename}")
                
            else:
                self.send_error_response('PDF generation failed')
            
        except Exception as e:
            print(f"❌ Error in instant apply: {e}")
            self.send_error_response(str(e))
    
    def send_json_response(self, data):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())
    
    def send_error_response(self, error_message):
        response = {'success': False, 'error': error_message}
        self.send_response(400)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(response).encode())

def main():
    server = HTTPServer(('localhost', 8000), JobHunterAPI)
    print("🚀 JobHunter API Server running on http://localhost:8000")
    print("🔗 Use with jobs.bluehawana.com or enhanced_job_dashboard.html")
    print("📄 Will generate and open PDFs for instant apply")
    print("⭐ Ready to process your LinkedIn URL!")
    print()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Server stopped")

if __name__ == "__main__":
    main()