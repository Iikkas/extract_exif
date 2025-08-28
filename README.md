# extract_exif
A Python tool that recursively extracts EXIF metadata from images.  
Features:
- Recursive folder scan  
- Filter by minimum width  
- Filter by camera brand  

## Setup Guide

### 1. Clone the repository
git clone https://github.com/iikkas/extract_exif
cd extract_exif

### 2. Install dependencies
The only requirement is Pillow:

pip install -r requirements.txt

### 3. Run the script
python extract_exif.py "C:\path\to\images"

### 4. Optional: Add to PATH
If you want to run `extract_exif` from anywhere:
1. Copy `extract_exif.py` and  `extract_exif.bat` into your Python `Scripts` folder  
   (e.g. `C:\Users\YOURNAME\AppData\Local\Programs\Python\Python311\Scripts`)  
2. Make sure this folder is in your system PATH by running  
setx PATH "$env:PATH;C:\Users\YOURNAME\AppData\Local\Programs\Python\PythonYOURVERSION\Scripts
(change values of YOURNAME and YOURVERSION)

4. Now you can run:

extract_exif "C:\path\to\images"
