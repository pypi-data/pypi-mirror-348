import os
import platform
import subprocess
import sys
from pathlib import Path

def install_tesseract():
    """Cross-platform Tesseract installation handler"""
    script_path = Path(__file__).parent / 'scripts' / 'install_tesseract.sh'
    
    try:
        if platform.system() == "Windows":
            print("Please install Tesseract manually on Windows:")
            print("1. Download from: https://github.com/UB-Mannheim/tesseract/wiki")
            print("2. Add it to your PATH")
            return False
        
        # Run the shell script for Linux/Mac
        subprocess.run(['bash', str(script_path)], check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Tesseract installation failed: {e}")
        return False

if __name__ == "__main__":
    install_tesseract()