from .helpers import preprocess_image , extract_table_data

def extract_table_from_image(img_path, save_excel=True, preprocess=True, use_easyocr=False):
    """
    Main function to extract table from image
    
    Args:
        img_path: Path to the image file
        save_excel: Whether to save the result as Excel
        preprocess: Whether to preprocess the image
        use_easyocr: Whether to use EasyOCR or Tesseract
    
    Returns:
        DataFrame containing the extracted table
    """
    # Preprocess image if requested
    if preprocess:
        img_path = preprocess_image(img_path)
    
    # Extract table data
    df = extract_table_data(img_path, use_easyocr)
    
    # Save to Excel if requested
    if save_excel:
        output_path = img_path.replace('.png', '.xlsx').replace('.jpg', '.xlsx').replace('.jpeg', '.xlsx')
        df.to_excel(output_path, index=False)
        print(f"Data saved to {output_path} with {len(df)} rows and {len(df.columns)} columns")
    
    return df