#!/usr/bion3
"""
Create Kollmtent
"
import os
import sys
from datetime import datetime
from pathlib import Path

sys.path.append('backend')

fromator
from backend.smart_latex_editor import SmartLaTeXEditor
from backend.gemini_company_extracctor
from backend.geminisher


def load_env():
    env_p)
    if env_path.exists():
        for line in env_path.read_text(e():
    p()
            if not line or line.startswith('#') or '=' not in line:
                continue
            key, val = line.split('=', 1)
    ip()
            val = val.strip().strip('"').srip("'")
            if key a
                os.environ[key] = val


def build_job():
    return {
        "title": "on",
        "compa",
       en",
        "url": "https://career-agv.kollmorgen.com/jobs/59739
    ,
    }


def main():
    load_env()
    job = build_job()
    tY%m%d")
    
    print("🎨 Creating Kollmorgen application with Gemi
    
    # Test Gemini polisher
    polisher = GeminiContentPolisher()
    
    ")
    cl_content = polisher.polish_cover_lett
    print(f"Generated {len(cl_
    print(f"Preview: {cl_content[:150")
    
    print("\n📝 Testing ECARX bullets polishing...")
    ecarx_bullets = polisher.polish_ecarx_experience()
   ets")
    if ecarx_bullets:
        print(f"First: {ecarx_bullets[")
    
  e!")


if __name__ == "__main__":
    main()
