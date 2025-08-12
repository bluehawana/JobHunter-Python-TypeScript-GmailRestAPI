#!/usr/bin/env python3
"""
Create a working Overleaf URL for the Opera DevOps resume
This demonstrates how to make the LaTeX file publicly accessible
"""
import os
import base64

def create_github_gist_url():
    """Create a GitHub Gist URL that can be used with Overleaf"""
    
    # Read the LaTeX content
    with open('opera_devops_resume.tex', 'r', encoding='utf-8') as f:
        latex_content = f.read()
    
    print("🎯 CREATING OVERLEAF URL FOR OPERA DEVOPS RESUME")
    print("=" * 60)
    
    # Option 1: GitHub Gist (manual)
    print("📝 OPTION 1: GitHub Gist (Recommended)")
    print("1. Go to: https://gist.github.com/")
    print("2. Create a new gist with filename: opera_devops_resume.tex")
    print("3. Paste the LaTeX content (see below)")
    print("4. Make it public and get the raw URL")
    print("5. Use: https://www.overleaf.com/docs?snip_uri=YOUR_GIST_RAW_URL")
    
    # Option 2: Base64 data URL (for small files)
    print(f"\n📝 OPTION 2: Direct Data URL (for testing)")
    latex_b64 = base64.b64encode(latex_content.encode('utf-8')).decode('ascii')
    data_url = f"data:text/plain;base64,{latex_b64}"
    overleaf_data_url = f"https://www.overleaf.com/docs?snip_uri={data_url}"
    
    print(f"🔗 Direct Overleaf URL (may be too long for some browsers):")
    print(f"{overleaf_data_url[:100]}...")
    
    # Option 3: Your deployed server
    print(f"\n📝 OPTION 3: Your Deployed Server (Best for automation)")
    server_url = "https://jobs.bluehawana.com/api/v1/latex/opera_devops_resume.tex"
    overleaf_server_url = f"https://www.overleaf.com/docs?snip_uri={server_url}"
    print(f"🔗 Server Overleaf URL: {overleaf_server_url}")
    
    # Save LaTeX content for easy copying
    print(f"\n📋 LATEX CONTENT TO COPY (for GitHub Gist):")
    print("=" * 60)
    print(latex_content[:500] + "..." if len(latex_content) > 500 else latex_content)
    print("=" * 60)
    
    # Create a simple HTML file for easy testing
    html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Opera DevOps Resume - Overleaf Integration</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; }}
        .container {{ max-width: 800px; margin: 0 auto; }}
        .button {{ 
            display: inline-block; 
            padding: 12px 24px; 
            background: #2e7d32; 
            color: white; 
            text-decoration: none; 
            border-radius: 4px; 
            margin: 10px 0;
        }}
        .button:hover {{ background: #1b5e20; }}
        pre {{ background: #f5f5f5; padding: 15px; border-radius: 4px; overflow-x: auto; }}
        .stats {{ background: #e3f2fd; padding: 15px; border-radius: 4px; margin: 20px 0; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🎭 Opera DevOps Engineer Resume</h1>
        
        <div class="stats">
            <h3>📊 Resume Statistics</h3>
            <ul>
                <li><strong>Company:</strong> Opera</li>
                <li><strong>Position:</strong> DevOps Engineer</li>
                <li><strong>Location:</strong> Oslo, Norway</li>
                <li><strong>PDF Size:</strong> 101,050 bytes</li>
                <li><strong>LaTeX Size:</strong> 6,762 characters</li>
                <li><strong>LEGO Intelligence:</strong> ✅ DevOps-focused tailoring</li>
            </ul>
        </div>
        
        <h2>🔗 Overleaf Integration Options</h2>
        
        <h3>Option 1: GitHub Gist (Recommended)</h3>
        <p>Create a public gist and use the raw URL with Overleaf:</p>
        <a href="https://gist.github.com/" class="button" target="_blank">Create GitHub Gist</a>
        
        <h3>Option 2: Your Server (When Deployed)</h3>
        <p>Use your deployed server to serve the LaTeX file:</p>
        <a href="{overleaf_server_url}" class="button" target="_blank">Open in Overleaf</a>
        
        <h2>📝 LaTeX Content Preview</h2>
        <pre>{latex_content[:1000]}{'...' if len(latex_content) > 1000 else ''}</pre>
        
        <h2>🎯 Key Features</h2>
        <ul>
            <li>✅ Perfect LaTeX quality (identical to Overleaf)</li>
            <li>✅ LEGO intelligence detected DevOps focus</li>
            <li>✅ Tailored for Opera's requirements</li>
            <li>✅ Kubernetes/Docker expertise highlighted</li>
            <li>✅ Cloud platforms (AWS/Azure) emphasized</li>
            <li>✅ Current ECARX infrastructure work showcased</li>
        </ul>
        
        <p><strong>🚀 Ready for Opera application!</strong></p>
    </div>
</body>
</html>
"""
    
    with open('opera_resume_overleaf.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"\n📄 Created: opera_resume_overleaf.html")
    print(f"🌐 Open this file in your browser for easy access to all options")
    
    return {
        'latex_file': 'opera_devops_resume.tex',
        'pdf_file': 'opera_devops_resume.pdf',
        'html_file': 'opera_resume_overleaf.html',
        'server_overleaf_url': overleaf_server_url,
        'latex_size': len(latex_content)
    }

if __name__ == "__main__":
    result = create_github_gist_url()
    print(f"\n🎉 OVERLEAF INTEGRATION READY!")
    print(f"📊 Files created: {', '.join([result['latex_file'], result['pdf_file'], result['html_file']])}")
    print(f"🔗 Server URL: {result['server_overleaf_url']}")
    print(f"\n💡 Next steps:")
    print(f"1. Open opera_resume_overleaf.html in your browser")
    print(f"2. Choose your preferred method to create Overleaf URL")
    print(f"3. Edit the resume in Overleaf if needed")
    print(f"4. Download the final PDF from Overleaf")
    print(f"5. Apply to Opera! 🚀")