#!/usr/bin/env python3
"""
Open Tata Technologies CV and Cover Letter PDFs
"""

import subprocess
import sys

def open_pdfs():
    cv_path = "job_applications/tata_incident_management/Tata_Incident_Management_Harvad_CV.pdf"
    cl_path = "job_applications/tata_incident_management/Tata_Incident_Management_Harvad_CL.pdf"
    
    try:
        subprocess.run(['open', cv_path], check=True)
        print(f"✓ Opened CV: {cv_path}")
        
        subprocess.run(['open', cl_path], check=True)
        print(f"✓ Opened CL: {cl_path}")
        
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error opening PDFs: {e}")
        return False

if __name__ == "__main__":
    open_pdfs()
