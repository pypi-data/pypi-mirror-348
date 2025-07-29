#!/bin/bash

# Wviz Tesseract OCR Installation Script
# Supports Linux (Debian/Ubuntu/RedHat), macOS, and Windows (via manual instructions)

set -e  # Exit on error

echo "🔍 Checking Tesseract OCR installation..."

# Check if Tesseract is already installed
if command -v tesseract &> /dev/null; then
    current_version=$(tesseract --version | head -n 1 | cut -d' ' -f2)
    echo "✅ Tesseract $current_version is already installed"
    exit 0
fi

# Platform-specific installation
case "$(uname -s)" in
    Linux*)
        echo "🖥️  Detected Linux system"
        if [ -f /etc/debian_version ]; then
            # Debian/Ubuntu
            echo "🔧 Installing Tesseract for Debian/Ubuntu"
            sudo apt-get update
            sudo apt-get install -y tesseract-ocr libtesseract-dev
        elif [ -f /etc/redhat-release ]; then
            # RedHat/CentOS
            echo "🔧 Installing Tesseract for RedHat/CentOS"
            sudo yum install -y tesseract tesseract-devel
        else
            echo "❌ Unsupported Linux distribution"
            echo "Please install Tesseract manually from: https://tesseract-ocr.github.io/tessdoc/Installation.html"
            exit 1
        fi
        ;;
    Darwin*)
        echo "🍏 Detected macOS"
        if command -v brew &> /dev/null; then
            echo "🔧 Installing Tesseract via Homebrew"
            brew install tesseract
        else
            echo "❌ Homebrew not found. Please install Homebrew first: https://brew.sh"
            exit 1
        fi
        ;;
    CYGWIN*|MINGW32*|MSYS*|MINGW*)
        echo "🪟 Detected Windows"
        echo "⚠️  Windows requires manual Tesseract installation:"
        echo "1. Download installer from: https://github.com/UB-Mannheim/tesseract/wiki"
        echo "2. Run the installer"
        echo "3. Add Tesseract to your system PATH"
        exit 1
        ;;
    *)
        echo "❌ Unsupported operating system: $(uname -s)"
        exit 1
        ;;
esac

# Verify installation
if ! command -v tesseract &> /dev/null; then
    echo "❌ Tesseract installation failed"
    exit 1
fi

final_version=$(tesseract --version | head -n 1 | cut -d' ' -f2)
echo "🎉 Successfully installed Tesseract $final_version"