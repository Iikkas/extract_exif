import sys
import time
import shutil
from pathlib import Path
from PIL import Image, ExifTags

def extract_exif(image_path):
    """Extract EXIF data and image size from an image."""
    try:
        img = Image.open(image_path)

        # Always include actual image size
        data = {
            "ImageWidth": img.size[0],
            "ImageHeight": img.size[1]
        }

        # Try to get EXIF metadata
        exif = img.getexif()
        if exif:
            for key, val in exif.items():
                tag = ExifTags.TAGS.get(key, key)
                data[tag] = val
        return data

    except Exception as e:
        return {"Error": str(e)}

def ask_yes_no(prompt):
    """Prompt user until they enter 'y', 'yes', 'n', or 'no'."""
    while True:
        answer = input(prompt).strip().lower()
        if answer in ("y", "yes"):
            return True
        elif answer in ("n", "no"):
            return False
        else:
            print("Please enter 'y', 'yes', 'n', or 'no'.")

def main():
    if len(sys.argv) < 2:
        print("Usage: check_exif <folder_path>")
        sys.exit(1)

    folder = Path(sys.argv[1])
    if not folder.is_dir():
        print(f"{folder} is not a valid directory.")
        sys.exit(1)

    # Ask min width
    min_width = None
    if ask_yes_no("Do you want to filter images by minimum width? (y/n): "):
        try:
            min_width = int(input("Enter minimum width in pixels: ").strip())
            print(f"Only images with width >= {min_width}px will be included.\n")
        except ValueError:
            print("Invalid input. No width filter applied.\n")

    # Ask max width
    max_width = None
    if ask_yes_no("Do you want to filter images by maximum width? (y/n): "):
        try:
            max_width = int(input("Enter maximum width in pixels: ").strip())
            print(f"Only images with width <= {max_width}px will be included.\n")
        except ValueError:
            print("Invalid input. No width filter applied.\n")

    # Ask camera brand filter
    brands = None
    if ask_yes_no("Do you want to filter images by camera brand? (y/n): "):
        brand_input = input("Enter camera brand(s), separated by commas (e.g., Canon,Nikon,Apple): ").strip()
        brands = [b.strip().lower() for b in brand_input.split(",") if b.strip()]
        if brands:
            print(f"Filtering: only images from {', '.join(brands)} will be included.\n")
        else:
            brands = None
            print("No valid brands entered. No brand filter applied.\n")

    # Prepare output file with daily counter
    output_dir = Path.cwd()
    date_str = time.strftime("%Y_%m_%d")
    today_files = sorted(output_dir.glob(f"{date_str}_*.txt"))
    next_index = len(today_files) + 1
    filename = f"{date_str}_{next_index:04d}.txt"
    output_file = output_dir / filename

    # Store matching files
    matching_files = []

    # Process images and write EXIF data
    with open(output_file, "w", encoding="utf-8") as f:
        for file in folder.rglob("*"):
            if file.suffix.lower() in [".jpg", ".jpeg", ".png", ".heic", ".raw"]:
                exif_data = extract_exif(file)
                if not exif_data:
                    continue  # skip images with no data

                # Apply width filters
                width = exif_data.get("ImageWidth", 0)
                if min_width is not None and width < min_width:
                    continue
                if max_width is not None and width > max_width:
                    continue

                # Apply camera brand filter
                if brands is not None:
                    make = str(exif_data.get("Make", "")).lower()
                    if not any(brand in make for brand in brands):
                        continue

                # Save this file as matching
                matching_files.append(file)

                # Write results
                rel_path = file.relative_to(folder)
                f.write(f"\n[FILE] {rel_path}\n")
                for tag, val in exif_data.items():
                    f.write(f"   - {tag}: {val}\n")

    print(f"\nData written to {output_file}")
    print(f"Found {len(matching_files)} matching image(s).")

    # Ask if user wants to copy
    if matching_files and ask_yes_no(f"Do you want to copy {len(matching_files)} files to a new folder? (y/n): "):
        # Find next available copy folder
        i = 1
        while True:
            copy_folder = output_dir / f"copy_{i:02d}"
            if not copy_folder.exists():
                copy_folder.mkdir()
                break
            i += 1

        # Copy files
        for file in matching_files:
            destination = copy_folder / file.name
            
            # If file with same name already exists, add _1, _2, etc.
            counter = 1
            while destination.exists():
                stem = file.stem
                suffix = file.suffix
                destination = copy_folder / f"{stem}_{counter}{suffix}"
                counter += 1
            try:
                shutil.copy2(file, destination)
            except Exception as e:
                print(f"Failed to copy {file}: {e}")

        print(f"\nAll files copied to {copy_folder}")

if __name__ == "__main__":
    main()
