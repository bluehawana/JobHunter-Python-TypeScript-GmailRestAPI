#!/usr/bin/env python3
"""
LaTeX to PDF Compiler - Compiles your exact LaTeX template to beautiful PDFs
"""
import subprocess
import tempfile
import os
import logging
from pathlib import Path
from typing import Dict, Any

logger = logging.getLogger(__name__)

class LaTeXPDFCompiler:
    """Compiles LaTeX content to PDF using pdflatex"""
    
    def __init__(self):
        self.temp_dir = None
    
    def compile_latex_to_pdf(self, latex_content: str, filename_prefix: str = "resume") -> bytes:
        """Compile LaTeX content to PDF and return PDF bytes"""
        try:
            # Create temporary directory
            with tempfile.TemporaryDirectory() as temp_dir:
                self.temp_dir = temp_dir
                
                # Write LaTeX content to file
                tex_file = os.path.join(temp_dir, f"{filename_prefix}.tex")
                with open(tex_file, 'w', encoding='utf-8') as f:
                    f.write(latex_content)
                
                # Compile LaTeX to PDF
                pdf_file = self._compile_with_pdflatex(tex_file, filename_prefix)
                
                if pdf_file and os.path.exists(pdf_file):
                    # Read PDF content
                    with open(pdf_file, 'rb') as f:
                        pdf_content = f.read()
                    
                    logger.info(f"✅ Successfully compiled LaTeX to PDF ({len(pdf_content)} bytes)")
                    return pdf_content
                else:
                    logger.error("❌ PDF compilation failed - no output file")
                    return self._fallback_pdf_generation(latex_content)
                    
        except Exception as e:
            logger.error(f"❌ LaTeX compilation error: {e}")
            return self._fallback_pdf_generation(latex_content)
    
    def _compile_with_pdflatex(self, tex_file: str, filename_prefix: str) -> str:
        """Compile LaTeX file using pdflatex"""
        try:
            # Run pdflatex twice for proper cross-references
            for i in range(2):
                result = subprocess.run([
                    'pdflatex',
                    '-interaction=nonstopmode',
                    '-output-directory', self.temp_dir,
                    tex_file
                ], capture_output=True, text=True, timeout=30)
                
                if result.returncode != 0:
                    logger.warning(f"pdflatex run {i+1} failed: {result.stderr}")
                    if i == 0:  # Try once more
                        continue
                    else:
                        return None
            
            pdf_file = os.path.join(self.temp_dir, f"{filename_prefix}.pdf")
            return pdf_file if os.path.exists(pdf_file) else None
            
        except subprocess.TimeoutExpired:
            logger.error("❌ pdflatex compilation timed out")
            return None
        except FileNotFoundError:
            logger.error("❌ pdflatex not found - LaTeX not installed")
            return None
        except Exception as e:
            logger.error(f"❌ pdflatex compilation error: {e}")
            return None
    
    def _fallback_pdf_generation(self, latex_content: str) -> bytes:
        """Fallback PDF generation when LaTeX compilation fails"""
        logger.warning("⚠️ Using fallback PDF generation - LaTeX compilation failed")
        
        try:
            from reportlab.lib.pagesizes import A4
            from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
            from reportlab.lib.styles import getSampleStyleSheet
            from io import BytesIO
            
            buffer = BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=A4)
            styles = getSampleStyleSheet()
            
            content = []
            content.append(Paragraph("HONGZHI LI", styles['Title']))
            content.append(Paragraph("LaTeX compilation failed - using fallback", styles['Normal']))
            content.append(Spacer(1, 20))
            content.append(Paragraph("Please install LaTeX (pdflatex) for proper resume generation", styles['Normal']))
            
            doc.build(content)
            buffer.seek(0)
            return buffer.getvalue()
            
        except Exception as e:
            logger.error(f"❌ Fallback PDF generation failed: {e}")
            return b"PDF generation failed"

# Global compiler instance
latex_compiler = LaTeXPDFCompiler()

def compile_resume_to_pdf(job_data: Dict[str, Any]) -> bytes:
    """Main function to compile LEGO-tailored resume to PDF"""
    from templates.cv_template import generate_tailored_cv
    
    # Generate LEGO-tailored LaTeX content
    latex_content = generate_tailored_cv(job_data)
    
    # Compile to PDF
    company = job_data.get('company', 'Company').replace(' ', '_')
    title = job_data.get('title', 'Position').replace(' ', '_')
    filename = f"Hongzhi_Li_{title}_{company}"
    
    return latex_compiler.compile_latex_to_pdf(latex_content, filename)