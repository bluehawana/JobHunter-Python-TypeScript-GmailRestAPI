#!/usr/bin/env python3
"""
Upload Documents to R2 with Public Development URL
Uses the public R2 URL for easier access
"""
import boto3
import os
from pathlib import Path
from datetime import datetime

def upload_with_public_url():
    """Upload all documents and create index with public URLs"""
    
    print("🌐 Uploading Documents with Public R2 URL")
    print("=" * 60)
    print("📡 Public URL: https://pub-da133e92739e4c21923a97fbce72d235.r2.dev")
    print()
    
    # Get credentials from environment
    account_id = os.getenv('R2_ACCOUNT_ID')
    access_key = os.getenv('R2_ACCESS_KEY_ID') 
    secret_key = os.getenv('R2_SECRET_ACCESS_KEY')
    
    if not all([account_id, access_key, secret_key]):
        print("❌ Missing R2 credentials")
        return False
    
    # Initialize R2 client
    s3_client = boto3.client(
        's3',
        endpoint_url=f'https://{account_id}.r2.cloudflarestorage.com',
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        region_name='auto'
    )
    
    # Public base URL
    public_base_url = "https://pub-da133e92739e4c21923a97fbce72d235.r2.dev"
    bucket_name = 'jobhunter'
    
    # Find all documents
    current_dir = Path(".")
    pdf_files = list(current_dir.glob("*.pdf"))
    latex_files = list(current_dir.glob("*.tex"))
    
    print(f"📄 Found {len(pdf_files)} PDF files")
    print(f"📝 Found {len(latex_files)} LaTeX files")
    
    timestamp = datetime.now().strftime("%Y-%m-%d")
    uploaded_docs = {
        'pdfs': [],
        'latex': []
    }
    
    # Upload ALL PDFs
    print(f"\\n📄 Uploading ALL PDF files...")
    for pdf_file in pdf_files:
        try:
            key = f"pdfs/{pdf_file.name}"
            
            with open(pdf_file, 'rb') as f:
                s3_client.upload_fileobj(
                    f, bucket_name, key,
                    ExtraArgs={'ContentType': 'application/pdf'}
                )
            
            file_size = pdf_file.stat().st_size / 1024
            public_url = f"{public_base_url}/{key}"
            
            print(f"✅ {pdf_file.name} ({file_size:.1f} KB)")
            
            uploaded_docs['pdfs'].append({
                'name': pdf_file.name,
                'size': file_size,
                'url': public_url,
                'company': extract_company_from_filename(pdf_file.name)
            })
            
        except Exception as e:
            print(f"❌ {pdf_file.name}: {e}")
    
    # Upload ALL LaTeX files  
    print(f"\\n📝 Uploading ALL LaTeX files...")
    for latex_file in latex_files:
        try:
            key = f"latex/{latex_file.name}"
            
            with open(latex_file, 'rb') as f:
                s3_client.upload_fileobj(
                    f, bucket_name, key,
                    ExtraArgs={'ContentType': 'text/plain'}
                )
            
            file_size = latex_file.stat().st_size / 1024
            public_url = f"{public_base_url}/{key}"
            
            print(f"✅ {latex_file.name} ({file_size:.1f} KB)")
            
            doc_type = "CV" if "_cv." in latex_file.name else "Cover Letter"
            
            uploaded_docs['latex'].append({
                'name': latex_file.name,
                'size': file_size,
                'url': public_url,
                'type': doc_type,
                'company': extract_company_from_filename(latex_file.name)
            })
            
        except Exception as e:
            print(f"❌ {latex_file.name}: {e}")
    
    # Create comprehensive index
    create_comprehensive_index(s3_client, bucket_name, public_base_url, uploaded_docs, timestamp)
    
    # Print summary with public URLs
    print_public_summary(public_base_url, uploaded_docs)
    
    return len(uploaded_docs['pdfs']) + len(uploaded_docs['latex']) > 0

def extract_company_from_filename(filename):
    """Extract company name from filename"""
    
    filename_lower = filename.lower()
    
    # Company mapping
    companies = {
        "thomthon": "Thomthon Retuer",
        "spotify": "Spotify",
        "volvo": "Volvo Group/Cars", 
        "ericsson": "Ericsson",
        "opera": "Opera Software",
        "skf": "SKF Group",
        "pagero": "Pagero Thomson Reuters",
        "king": "King Digital Entertainment",
        "techcorp": "TechCorp Sweden",
        "growing": "Growing Startup"
    }
    
    for key, company in companies.items():
        if key in filename_lower:
            return company
    
    return "Various Companies"

def create_comprehensive_index(s3_client, bucket_name, public_base_url, uploaded_docs, timestamp):
    """Create a beautiful comprehensive index"""
    
    print(f"\\n📋 Creating comprehensive document index...")
    
    # Group documents by company
    companies = {}
    
    for pdf in uploaded_docs['pdfs']:
        company = pdf['company']
        if company not in companies:
            companies[company] = {'pdfs': [], 'latex': []}
        companies[company]['pdfs'].append(pdf)
    
    for latex in uploaded_docs['latex']:
        company = latex['company'] 
        if company not in companies:
            companies[company] = {'pdfs': [], 'latex': []}
        companies[company]['latex'].append(latex)
    
    html_content = f"""<!DOCTYPE html>
<html>
<head>
    <title>🎯 JobHunter Documents - Professional Resume Collection</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            overflow: hidden;
        }}
        
        .header {{
            background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }}
        
        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
            font-weight: 300;
        }}
        
        .header p {{
            font-size: 1.2em;
            opacity: 0.9;
        }}
        
        .stats {{
            background: #f8f9fa;
            padding: 30px;
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            text-align: center;
        }}
        
        .stat-card {{
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }}
        
        .stat-number {{
            font-size: 2em;
            font-weight: bold;
            color: #3498db;
        }}
        
        .content {{
            padding: 40px;
        }}
        
        .company-section {{
            margin-bottom: 40px;
            border: 1px solid #e9ecef;
            border-radius: 12px;
            overflow: hidden;
        }}
        
        .company-header {{
            background: linear-gradient(135deg, #3498db, #2980b9);
            color: white;
            padding: 20px;
            font-size: 1.3em;
            font-weight: 600;
        }}
        
        .documents-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            padding: 30px;
        }}
        
        .doc-card {{
            background: #f8f9fa;
            border-radius: 10px;
            padding: 20px;
            border-left: 4px solid #3498db;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }}
        
        .doc-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 10px 25px rgba(0,0,0,0.15);
        }}
        
        .doc-card.pdf {{
            border-left-color: #e74c3c;
            background: linear-gradient(135deg, #fff5f5, #fff);
        }}
        
        .doc-card.latex {{
            border-left-color: #27ae60;
            background: linear-gradient(135deg, #f5fff5, #fff);
        }}
        
        .doc-title {{
            font-weight: 600;
            margin-bottom: 10px;
            color: #2c3e50;
        }}
        
        .doc-meta {{
            color: #7f8c8d;
            font-size: 0.9em;
            margin-bottom: 15px;
        }}
        
        .doc-link {{
            display: inline-block;
            background: #3498db;
            color: white;
            padding: 10px 20px;
            text-decoration: none;
            border-radius: 6px;
            transition: background 0.3s ease;
            font-weight: 500;
        }}
        
        .doc-link:hover {{
            background: #2980b9;
        }}
        
        .doc-link.pdf-link {{
            background: #e74c3c;
        }}
        
        .doc-link.pdf-link:hover {{
            background: #c0392b;
        }}
        
        .doc-link.latex-link {{
            background: #27ae60;
        }}
        
        .doc-link.latex-link:hover {{
            background: #229954;
        }}
        
        .footer {{
            background: #2c3e50;
            color: white;
            padding: 30px;
            text-align: center;
        }}
        
        .quick-links {{
            margin: 30px 0;
            padding: 20px;
            background: #e8f4f8;
            border-radius: 10px;
        }}
        
        .quick-links h3 {{
            color: #2c3e50;
            margin-bottom: 15px;
        }}
        
        .link-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 10px;
        }}
        
        .quick-link {{
            display: block;
            padding: 10px 15px;
            background: white;
            color: #3498db;
            text-decoration: none;
            border-radius: 6px;
            border: 1px solid #bdc3c7;
            transition: all 0.3s ease;
        }}
        
        .quick-link:hover {{
            background: #3498db;
            color: white;
        }}
        
        @media (max-width: 768px) {{
            .header h1 {{ font-size: 2em; }}
            .documents-grid {{ grid-template-columns: 1fr; }}
            .stats {{ grid-template-columns: repeat(2, 1fr); }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎯 JobHunter Document Portal</h1>
            <p>Professional Resume & Cover Letter Collection</p>
            <p>Updated: {datetime.now().strftime('%B %d, %Y at %H:%M')}</p>
        </div>
        
        <div class="stats">
            <div class="stat-card">
                <div class="stat-number">{len(uploaded_docs['pdfs'])}</div>
                <div>PDF Documents</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{len(uploaded_docs['latex'])}</div>
                <div>LaTeX Sources</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{len(companies)}</div>
                <div>Companies</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{len(uploaded_docs['pdfs']) + len(uploaded_docs['latex'])}</div>
                <div>Total Files</div>
            </div>
        </div>
        
        <div class="content">
            <div class="quick-links">
                <h3>🚀 Quick Access - Ready-to-Send PDFs</h3>
                <div class="link-grid">"""
    
    # Add quick links for important PDFs
    important_pdfs = [doc for doc in uploaded_docs['pdfs'] if 'thomthon' in doc['name'].lower()]
    important_pdfs.extend([doc for doc in uploaded_docs['pdfs'] if any(x in doc['name'].lower() for x in ['spotify', 'volvo', 'ericsson', 'opera'])])
    
    for doc in important_pdfs[:6]:  # Show top 6
        html_content += f"""
                    <a href="{doc['url']}" target="_blank" class="quick-link">
                        📄 {doc['name'].replace('.pdf', '')} - {doc['company']}
                    </a>"""
    
    html_content += """
                </div>
            </div>"""
    
    # Add company sections
    for company, docs in sorted(companies.items()):
        if not docs['pdfs'] and not docs['latex']:
            continue
            
        html_content += f"""
            <div class="company-section">
                <div class="company-header">
                    🏢 {company}
                </div>
                <div class="documents-grid">"""
        
        # Add PDFs
        for pdf in docs['pdfs']:
            html_content += f"""
                    <div class="doc-card pdf">
                        <div class="doc-title">📄 {pdf['name']}</div>
                        <div class="doc-meta">PDF Document • {pdf['size']:.1f} KB</div>
                        <a href="{pdf['url']}" target="_blank" class="doc-link pdf-link">
                            Download PDF
                        </a>
                    </div>"""
        
        # Add LaTeX files
        for latex in docs['latex']:
            html_content += f"""
                    <div class="doc-card latex">
                        <div class="doc-title">📝 {latex['name']}</div>
                        <div class="doc-meta">LaTeX Source • {latex['type']} • {latex['size']:.1f} KB</div>
                        <a href="{latex['url']}" target="_blank" class="doc-link latex-link">
                            View Source
                        </a>
                    </div>"""
        
        html_content += """
                </div>
            </div>"""
    
    html_content += f"""
        </div>
        
        <div class="footer">
            <p>🔗 <strong>Public URL:</strong> {public_base_url}</p>
            <p>💼 All documents are professionally formatted and ready for job applications</p>
            <p>📱 This portal is mobile-friendly and accessible from anywhere</p>
        </div>
    </div>
</body>
</html>"""
    
    try:
        s3_client.put_object(
            Bucket=bucket_name,
            Key='index.html',
            Body=html_content.encode('utf-8'),
            ContentType='text/html'
        )
        
        print(f"✅ Comprehensive index created!")
        
    except Exception as e:
        print(f"❌ Index creation failed: {e}")

def print_public_summary(public_base_url, uploaded_docs):
    """Print summary with public URLs"""
    
    total_files = len(uploaded_docs['pdfs']) + len(uploaded_docs['latex'])
    
    print(f"\\n🎉 UPLOAD COMPLETE!")
    print("=" * 60)
    print(f"📦 Uploaded {total_files} files to R2 storage")
    print(f"📄 {len(uploaded_docs['pdfs'])} PDF documents")
    print(f"📝 {len(uploaded_docs['latex'])} LaTeX sources")
    print()
    
    print("🔗 PUBLIC ACCESS URLS:")
    print("=" * 40)
    print(f"📋 Document Portal: {public_base_url}/index.html")
    print(f"📁 PDF Folder: {public_base_url}/pdfs/")
    print(f"📁 LaTeX Folder: {public_base_url}/latex/")
    print()
    
    print("🎯 KEY DOCUMENTS:")
    print("=" * 30)
    
    # Highlight important documents
    important_docs = [doc for doc in uploaded_docs['pdfs'] if 'thomthon' in doc['name'].lower()]
    for doc in important_docs:
        print(f"📄 {doc['name']}: {doc['url']}")
    
    volvo_docs = [doc for doc in uploaded_docs['pdfs'] if 'volvo' in doc['name'].lower()][:2]
    for doc in volvo_docs:
        print(f"📄 {doc['name']}: {doc['url']}")
    
    spotify_docs = [doc for doc in uploaded_docs['pdfs'] if 'spotify' in doc['name'].lower()][:1] 
    for doc in spotify_docs:
        print(f"📄 {doc['name']}: {doc['url']}")
    
    print()
    print("✨ All documents are now publicly accessible and ready for job applications!")

def main():
    """Main function"""
    print("🌐 R2 Public URL Document Upload")
    
    success = upload_with_public_url()
    
    if success:
        print("\\n🎉 SUCCESS! Your documents are now publicly accessible!")
        print("\\n📱 You can access them from any device with the public URLs above")
    else:
        print("\\n❌ Upload failed")

if __name__ == "__main__":
    main()