# Wviz - Computer Vision and OCR Toolkit

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

A powerful package for computer vision and OCR tasks, built on OpenCV, Tesseract, and EasyOCR.

## Features

- 📷 Image processing with OpenCV
- 🔍 Text extraction using Tesseract OCR
- 🚀 EasyOCR integration for multilingual support
- 🛠️ Unified API for common computer vision tasks

## Installation

### Prerequisites

- Python 3.8+
- Tesseract OCR (v5.0+ recommended)

### 1. Install Python Package

```bash
pip install Wviz

```

## Usage

```python
import wviz

image_path = "path/to/your/image.png"
df = wviz.Img2XL(image_path, use_first_model=True)
```