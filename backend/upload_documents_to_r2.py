#!/usr/bin/env python3
"""
Upload All Generated Documents to R2 Storage
Uploads existing PDFs and LaTeX files for easy access
"""
import os
import sys
from pathlib import Path
from datetime import datetime

# Add the current directory to Python path
sys.path.append(str(Path(__file__).parent))

try:
    from r2_backup_service import R2BackupService
except ImportError:
    print("❌ Missing boto3 dependency. Run: pip install boto3")
    sys.exit(1)

def find_all_documents():
    """Find all PDF and LaTeX documents to upload"""
    
    current_dir = Path(".")
    documents = {
        "pdfs": [],
        "latex": []
    }
    
    # Find PDF files
    pdf_files = list(current_dir.glob("*.pdf"))
    latex_files = list(current_dir.glob("*.tex"))
    
    print(f"📄 Found {len(pdf_files)} PDF files")
    print(f"📝 Found {len(latex_files)} LaTeX files")
    
    return pdf_files, latex_files

def upload_all_documents():
    """Upload all documents to R2 storage"""
    
    print("📦 Uploading All Documents to R2 Storage")
    print("=" * 60)
    
    # Initialize R2 service
    r2_service = R2BackupService()
    
    if not r2_service.s3_client:
        print()
        print("❌ R2 credentials not configured!")
        print()
        print("🔧 To configure R2 access:")
        print("1. Go to Cloudflare Dashboard → R2 Object Storage")
        print("2. Click 'Manage R2 API tokens' → 'Create API token'")
        print("3. Set permissions for your bucket")
        print("4. Copy the credentials")
        print("5. Update your .env file with:")
        print()
        print("   R2_ACCOUNT_ID=your-cloudflare-account-id")
        print("   R2_ACCESS_KEY_ID=your-r2-access-key")
        print("   R2_SECRET_ACCESS_KEY=your-r2-secret-key")
        print()
        print("🔗 Your R2 bucket URL:")
        print("   https://2a35af424f8734e497a5d707344d79d5.r2.cloudflarestorage.com/jobhunter")
        print()
        return False
    
    # Find all documents
    pdf_files, latex_files = find_all_documents()
    
    if not pdf_files and not latex_files:
        print("❌ No documents found to upload")
        return False
    
    # Create timestamp for organization
    timestamp = datetime.now().strftime("%Y-%m-%d")
    
    # Upload PDFs
    pdf_success = 0
    if pdf_files:
        print(f"\\n📄 Uploading {len(pdf_files)} PDF files...")
        for pdf_file in pdf_files:
            r2_key = f"documents/{timestamp}/pdfs/{pdf_file.name}"
            if r2_service.upload_file(str(pdf_file), r2_key):
                pdf_success += 1
    
    # Upload LaTeX files
    latex_success = 0
    if latex_files:
        print(f"\\n📝 Uploading {len(latex_files)} LaTeX files...")
        for latex_file in latex_files:
            r2_key = f"documents/{timestamp}/latex/{latex_file.name}"
            if r2_service.upload_file(str(latex_file), r2_key):
                latex_success += 1
    
    # Create document index
    print("\\n📋 Creating document index...")
    create_document_index(r2_service, pdf_files, latex_files, timestamp, pdf_success, latex_success)
    
    # Summary
    total_uploaded = pdf_success + latex_success
    total_files = len(pdf_files) + len(latex_files)
    
    print(f"\\n📊 UPLOAD SUMMARY")
    print("=" * 40)
    print(f"📄 PDFs uploaded: {pdf_success}/{len(pdf_files)}")
    print(f"📝 LaTeX uploaded: {latex_success}/{len(latex_files)}")
    print(f"📦 Total uploaded: {total_uploaded}/{total_files}")
    
    if total_uploaded > 0:
        print()
        print("✅ Documents uploaded successfully!")
        print("🔗 Access your documents at:")
        print(f"   https://2a35af424f8734e497a5d707344d79d5.r2.cloudflarestorage.com/documents/{timestamp}/")
        print("📋 Document index:")
        print(f"   https://2a35af424f8734e497a5d707344d79d5.r2.cloudflarestorage.com/documents_index.html")
        return True
    else:
        print("❌ No documents were uploaded")
        return False

def create_document_index(r2_service, pdf_files, latex_files, timestamp, pdf_success, latex_success):
    """Create an HTML index of all uploaded documents"""
    
    html_content = f"""<!DOCTYPE html>
<html>
<head>
    <title>JobHunter Documents - {timestamp}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }}
        .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        .header {{ text-align: center; margin-bottom: 30px; color: #333; }}
        .section {{ margin: 20px 0; }}
        .file-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 15px; }}
        .file-card {{ background: #f8f9fa; border: 1px solid #ddd; border-radius: 8px; padding: 15px; }}
        .file-name {{ font-weight: bold; color: #0066cc; margin-bottom: 5px; }}
        .file-type {{ background: #007bff; color: white; padding: 2px 8px; border-radius: 4px; font-size: 0.8em; }}
        .company {{ color: #666; font-size: 0.9em; }}
        .stats {{ background: #e9ecef; padding: 15px; border-radius: 8px; text-align: center; }}
        a {{ color: #0066cc; text-decoration: none; }}
        a:hover {{ text-decoration: underline; }}
        .pdf {{ background: #dc3545; }}
        .latex {{ background: #28a745; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📋 JobHunter Documents</h1>
            <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
        
        <div class="stats">
            <strong>📊 Upload Summary:</strong> 
            {pdf_success} PDFs + {latex_success} LaTeX files = {pdf_success + latex_success} total documents
        </div>
        
        <div class="section">
            <h2>📄 PDF Documents ({len(pdf_files)} files)</h2>
            <div class="file-grid">
"""
    
    # Add PDF files
    for pdf_file in pdf_files:
        file_url = f"https://2a35af424f8734e497a5d707344d79d5.r2.cloudflarestorage.com/documents/{timestamp}/pdfs/{pdf_file.name}"
        company = extract_company_from_filename(pdf_file.name)
        
        html_content += f"""
                <div class="file-card">
                    <div class="file-name">
                        <a href="{file_url}" target="_blank">{pdf_file.name}</a>
                    </div>
                    <span class="file-type pdf">PDF</span>
                    <div class="company">{company}</div>
                </div>
"""
    
    html_content += f"""
            </div>
        </div>
        
        <div class="section">
            <h2>📝 LaTeX Sources ({len(latex_files)} files)</h2>
            <div class="file-grid">
"""
    
    # Add LaTeX files
    for latex_file in latex_files:
        file_url = f"https://2a35af424f8734e497a5d707344d79d5.r2.cloudflarestorage.com/documents/{timestamp}/latex/{latex_file.name}"
        company = extract_company_from_filename(latex_file.name)
        doc_type = "CV" if "_cv." in latex_file.name else "Cover Letter"
        
        html_content += f"""
                <div class="file-card">
                    <div class="file-name">
                        <a href="{file_url}" target="_blank">{latex_file.name}</a>
                    </div>
                    <span class="file-type latex">LaTeX {doc_type}</span>
                    <div class="company">{company}</div>
                </div>
"""
    
    html_content += f"""
            </div>
        </div>
        
        <div class="section">
            <h3>🔗 Quick Access</h3>
            <p><strong>R2 Bucket:</strong> <a href="https://2a35af424f8734e497a5d707344d79d5.r2.cloudflarestorage.com" target="_blank">JobHunter Storage</a></p>
            <p><strong>Today's Documents:</strong> <a href="https://2a35af424f8734e497a5d707344d79d5.r2.cloudflarestorage.com/documents/{timestamp}/" target="_blank">View Folder</a></p>
        </div>
    </div>
</body>
</html>"""
    
    # Upload index
    r2_service.upload_file_content(html_content, "documents_index.html", "text/html")

def extract_company_from_filename(filename):
    """Extract company name from filename"""
    
    # Common company patterns
    companies = {
        "spotify": "Spotify",
        "volvo": "Volvo",
        "ericsson": "Ericsson", 
        "thomthon": "Thomthon Retuer",
        "opera": "Opera",
        "skf": "SKF Group",
        "pagero": "Pagero Thomson Reuters",
        "king": "King Digital"
    }
    
    filename_lower = filename.lower()
    for key, company in companies.items():
        if key in filename_lower:
            return company
    
    return "Various Companies"

def main():
    """Main function"""
    
    print("🎯 JobHunter Document Upload to R2")
    print()
    print("This will upload all your generated resumes and cover letters")
    print("to your R2 Cloudflare storage for easy access and backup.")
    print()
    
    # Check if user wants to proceed
    proceed = input("Continue with upload? (y/N): ").strip().lower()
    if proceed not in ['y', 'yes']:
        print("❌ Upload cancelled")
        return
    
    success = upload_all_documents()
    
    if success:
        print()
        print("🎉 All done! You can now access your documents online.")
    else:
        print()
        print("💡 Configure R2 credentials and try again.")

if __name__ == "__main__":
    main()