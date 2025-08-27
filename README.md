# check_exif
A Python tool that recursively extracts EXIF metadata from images.  
Features:
- Recursive folder scan  
- Filter by minimum width  
- Filter by camera brand  

## Setup Guide

### 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/check_exif.git
cd check_exif

### 2. Install dependencies
The only requirement is Pillow:

pip install -r requirements.txt

### 3. Run the script
python check_exif.py "C:\path\to\images"

### 4. Optional: Add to PATH
If you want to run `check_exif` from anywhere:
1. Copy `check_exif.py` into your Python `Scripts` folder  
   (e.g. `C:\Users\YOURNAME\AppData\Local\Programs\Python\Python311\Scripts`)  
2. Make sure this folder is in your system PATH  
3. Now you can run:

check_exif "C:\path\to\images"
