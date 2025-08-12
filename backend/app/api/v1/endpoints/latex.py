"""
LaTeX file serving endpoints for Overleaf integration
"""
from fastapi import APIRouter, HTTPException, Response
from fastapi.responses import PlainTextResponse
import os
import logging
from typing import List, Dict, Any
from pydantic import BaseModel

logger = logging.getLogger(__name__)

router = APIRouter()

class LaTeXFileInfo(BaseModel):
    filename: str
    size: int
    modified: float
    overleaf_url: str

class LaTeXListResponse(BaseModel):
    files: List[LaTeXFileInfo]
    count: int
    directory: str

@router.get("/latex/{filename}")
async def serve_latex_file(filename: str):
    """Serve LaTeX files for Overleaf consumption"""
    try:
        # Security: only allow .tex files
        if not filename.endswith('.tex'):
            raise HTTPException(status_code=404, detail="File not found")
        
        # Look for file in latex_files directory
        latex_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'latex_files')
        file_path = os.path.join(latex_dir, filename)
        
        if not os.path.exists(file_path):
            logger.warning(f"LaTeX file not found: {filename}")
            raise HTTPException(status_code=404, detail="LaTeX file not found")
        
        # Read and serve the LaTeX content
        with open(file_path, 'r', encoding='utf-8') as f:
            latex_content = f.read()
        
        logger.info(f"📝 Serving LaTeX file: {filename} ({len(latex_content)} chars)")
        
        return PlainTextResponse(
            content=latex_content,
            headers={
                'Content-Disposition': f'inline; filename="{filename}"',
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'text/plain; charset=utf-8'
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error serving LaTeX file {filename}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/latex-list", response_model=LaTeXListResponse)
async def list_latex_files():
    """List available LaTeX files with Overleaf URLs"""
    try:
        latex_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'latex_files')
        
        if not os.path.exists(latex_dir):
            return LaTeXListResponse(
                files=[],
                count=0,
                directory=latex_dir
            )
        
        files = [f for f in os.listdir(latex_dir) if f.endswith('.tex')]
        
        file_info = []
        base_url = os.getenv('BASE_URL', 'https://jobs.bluehawana.com')
        
        for filename in files:
            file_path = os.path.join(latex_dir, filename)
            stat = os.stat(file_path)
            
            latex_url = f"{base_url}/api/v1/latex/{filename}"
            overleaf_url = f"https://www.overleaf.com/docs?snip_uri={latex_url}"
            
            file_info.append(LaTeXFileInfo(
                filename=filename,
                size=stat.st_size,
                modified=stat.st_mtime,
                overleaf_url=overleaf_url
            ))
        
        # Sort by modification time (newest first)
        file_info.sort(key=lambda x: x.modified, reverse=True)
        
        logger.info(f"📋 Listed {len(file_info)} LaTeX files")
        
        return LaTeXListResponse(
            files=file_info,
            count=len(files),
            directory=latex_dir
        )
        
    except Exception as e:
        logger.error(f"❌ Error listing LaTeX files: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/generate-overleaf-url")
async def generate_overleaf_url(job_data: Dict[str, Any]):
    """Generate LaTeX resume and return Overleaf URL"""
    try:
        from overleaf_pdf_generator import OverleafPDFGenerator
        import time
        
        # Generate LaTeX content
        generator = OverleafPDFGenerator()
        latex_content = generator._generate_latex_content(job_data)
        
        # Create filename
        company = job_data.get('company', 'company').lower().replace(' ', '_')
        job_title = job_data.get('title', 'position').lower().replace(' ', '_')
        timestamp = int(time.time())
        filename = f"resume_{company}_{job_title}_{timestamp}.tex"
        
        # Save LaTeX file
        latex_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'latex_files')
        os.makedirs(latex_dir, exist_ok=True)
        
        file_path = os.path.join(latex_dir, filename)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(latex_content)
        
        # Generate URLs
        base_url = os.getenv('BASE_URL', 'https://jobs.bluehawana.com')
        latex_url = f"{base_url}/api/v1/latex/{filename}"
        overleaf_url = f"https://www.overleaf.com/docs?snip_uri={latex_url}"
        
        logger.info(f"✅ Generated LaTeX resume for {company}: {filename}")
        logger.info(f"🔗 Overleaf URL: {overleaf_url}")
        
        return {
            'filename': filename,
            'latex_url': latex_url,
            'overleaf_url': overleaf_url,
            'company': job_data.get('company', 'Unknown'),
            'job_title': job_data.get('title', 'Unknown'),
            'latex_size': len(latex_content),
            'message': 'LaTeX resume generated successfully - click Overleaf URL to compile!'
        }
        
    except Exception as e:
        logger.error(f"❌ Error generating Overleaf URL: {e}")
        raise HTTPException(status_code=500, detail=str(e))