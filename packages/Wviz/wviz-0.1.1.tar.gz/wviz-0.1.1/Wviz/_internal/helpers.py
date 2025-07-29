import cv2
import numpy as np
import pandas as pd
import pytesseract
from pytesseract import Output
import easyocr

def extract_table_data(img_path, use_easyocr=True):
    """
    Extract tabular data from an image combining structural detection with accurate text extraction
    
    Args:
        img_path: Path to the image file
        use_easyocr: Whether to use EasyOCR (True) or Tesseract (False) for text extraction
    
    Returns:
        DataFrame containing the extracted table data
    """
    # Initialize EasyOCR reader if needed
    if use_easyocr:
        reader = easyocr.Reader(['en'])
    
    # Read the image
    img = cv2.imread(img_path)
    if img is None:
        raise ValueError(f"Could not read image at {img_path}")
    
    # Store original image for text extraction
    original_img = img.copy()
    
    # Convert to grayscale
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Apply threshold to get binary image
    (thresh, img_bin) = cv2.threshold(img_gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    img_bin = cv2.bitwise_not(img_bin)
    
    # ---------- STRUCTURE DETECTION (from table_detection) ----------
    # Define kernels for vertical and horizontal line detection
    kernel_length_v = (np.array(img_gray).shape[1]) // 120
    vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, kernel_length_v))
    im_temp1 = cv2.erode(img_bin, vertical_kernel, iterations=3)
    vertical_lines_img = cv2.dilate(im_temp1, vertical_kernel, iterations=3)
    
    kernel_length_h = (np.array(img_gray).shape[1]) // 40
    horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_length_h, 1))
    im_temp2 = cv2.erode(img_bin, horizontal_kernel, iterations=3)
    horizontal_lines_img = cv2.dilate(im_temp2, horizontal_kernel, iterations=3)
    
    # Combine horizontal and vertical lines to get table structure
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    table_segment = cv2.addWeighted(vertical_lines_img, 0.5, horizontal_lines_img, 0.5, 0.0)
    table_segment = cv2.erode(cv2.bitwise_not(table_segment), kernel, iterations=2)
    thresh, table_segment = cv2.threshold(table_segment, 0, 255, cv2.THRESH_OTSU)
    
    # Find contours (cells) in the table structure
    contours, hierarchy = cv2.findContours(table_segment, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    # Sort contours by y-coordinate to organize by rows
    def get_y_coord(contour):
        x, y, w, h = cv2.boundingRect(contour)
        return y
    
    # Filter contours by size to get only cells
    cell_contours = []
    for c in contours:
        x, y, w, h = cv2.boundingRect(c)
        if h > 9 and h < 100:  # Cell height constraints
            cell_contours.append(c)
    
    # Sort contours by y-coordinate first
    cell_contours.sort(key=get_y_coord)
    
    # Group contours by rows based on y-coordinate proximity
    rows = []
    current_row = []
    last_y = -1
    
    for c in cell_contours:
        x, y, w, h = cv2.boundingRect(c)
        
        if last_y == -1:
            current_row.append((x, y, w, h))
        elif abs(y - last_y) < 10:  # Same row if y-coordinates are close
            current_row.append((x, y, w, h))
        else:
            # Sort cells in the current row by x-coordinate
            current_row.sort(key=lambda cell: cell[0])
            rows.append(current_row)
            current_row = [(x, y, w, h)]
        
        last_y = y
    
    # Add the last row if not empty
    if current_row:
        current_row.sort(key=lambda cell: cell[0])
        rows.append(current_row)
    
    # ---------- TEXT EXTRACTION ----------
    table_data = []
    
    # Process each row of cells
    for row_cells in rows:
        row_data = []
        
        # Process each cell in the row
        for x, y, w, h in row_cells:
            # Extract the cell region from the original image
            cell_img = original_img[y:y+h, x:x+w]
            
            # Skip very small cells
            if w * h < 100:
                row_data.append("")
                continue
                
            # Extract text from the cell
            if use_easyocr:
                # Use EasyOCR for text extraction
                bounds = reader.readtext(cell_img)
                cell_text = ' '.join([text[1] for text in bounds]) if bounds else ""
            else:
                # Use Tesseract for text extraction
                custom_config = r'-l eng --oem 3 --psm 6 -c tessedit_char_whitelist="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-:.$%./@& *"'
                cell_text = pytesseract.image_to_string(cell_img, config=custom_config).strip()
            
            row_data.append(cell_text)
        
        # Add row data if not empty
        if any(cell.strip() for cell in row_data):
            table_data.append(row_data)
    
    # Create DataFrame - determine number of columns from row with most columns
    max_cols = max(len(row) for row in table_data) if table_data else 0
    
    # Ensure all rows have the same number of columns
    for i in range(len(table_data)):
        while len(table_data[i]) < max_cols:
            table_data[i].append("")
    
    # Create DataFrame
    df = pd.DataFrame(table_data)
    
    # Use first row as header if it appears to be a header
    if len(df) > 0:
        headers = df.iloc[0]
        # Check if first row has non-empty values that could be headers
        if not headers.isna().all() and not (headers == '').all():
            df = df.iloc[1:].reset_index(drop=True)
            df.columns = headers
        else:
            # Use default column names
            df.columns = [f'Column_{i+1}' for i in range(len(df.columns))]
    
    return df

def preprocess_image(img_path, enhance_contrast=True, denoise=True):
    """
    Preprocess the image for better text extraction
    
    Args:
        img_path: Path to the image file
        enhance_contrast: Whether to enhance contrast
        denoise: Whether to denoise the image
    
    Returns:
        Path to the preprocessed image
    """
    img = cv2.imread(img_path)
    
    # Resize if too large
    max_dimension = 2000
    height, width = img.shape[:2]
    if max(height, width) > max_dimension:
        scale = max_dimension / max(height, width)
        img = cv2.resize(img, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)
    
    # Convert to grayscale
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Apply contrast enhancement
    if enhance_contrast:
        # Apply CLAHE (Contrast Limited Adaptive Histogram Equalization)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        img_gray = clahe.apply(img_gray)
    
    # Denoise
    if denoise:
        img_gray = cv2.fastNlMeansDenoising(img_gray, None, 10, 7, 21)
    
    # Apply threshold
    _, img_binary = cv2.threshold(img_gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    # Save preprocessed image
    preprocessed_path = img_path.replace('.', '_preprocessed.')
    cv2.imwrite(preprocessed_path, img_binary)
    
    return preprocessed_path




