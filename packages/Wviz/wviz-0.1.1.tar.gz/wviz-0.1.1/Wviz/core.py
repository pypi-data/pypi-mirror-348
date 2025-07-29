from ._internal.implementation import extract_table_from_image

def Img2XL(image_path , use_first_model=False):
    """Public method that users can call directly"""
    result_df = extract_table_from_image(
        image_path, 
        save_excel=True,
        preprocess=True,
        use_easyocr=use_first_model
    )
    return result_df

def check_tesseract_installed():
    try:
        import pytesseract
        pytesseract.get_tesseract_version()
        return True
    except (ImportError, pytesseract.TesseractNotFoundError):
        return False