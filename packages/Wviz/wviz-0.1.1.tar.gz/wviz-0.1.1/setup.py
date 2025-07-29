from setuptools import setup, find_packages

setup(
    name='Wviz',
    version='0.1.1',
    packages=find_packages(),
    install_requires=[
        'opencv-python>=4.11.0,<5.0.0',  # Pinned to 4.x series
        'numpy>=2.0.2,<3.0.0',           # Pinned to 2.x series
        'pandas>=2.2.2,<3.0.0',          # Pinned to 2.x series
        'pytesseract>=0.3.13,<0.4.0',     # Pinned to 0.3.x series
        'easyocr>=1.7.0,<2.0.0',         # Latest stable version
    ],
    python_requires='>=3.8',  # Since numpy 2.0 requires Python 3.8+
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'wviz-install-ocr=Wviz.install:install_tesseract',
        ],
    },
)