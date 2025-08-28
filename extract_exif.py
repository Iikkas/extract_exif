import sys
from pathlib import Path
from PIL import Image, ExifTags

def extract_exif(image_path):
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

def main():
    if len(sys.argv) < 2:
        print("Usage: check_exif <folder_path>")
        sys.exit(1)

    folder = Path(sys.argv[1])
    if not folder.is_dir():
        print(f"{folder} is not a valid directory.")
        sys.exit(1)

    # Ask width filter
    apply_width_filter = input("Do you want to filter images by minimum width? (y/n): ").strip().lower()
    min_width = None
    if apply_width_filter == "y":
        try:
            min_width = int(input("Enter minimum width in pixels: ").strip())
            print(f"Filtering: only images with width >= {min_width}px will be included.\n")
        except ValueError:
            print("Invalid input. No width filter applied.\n")

    # Ask camera brand filter
    apply_brand_filter = input("Do you want to filter images by camera brand? (y/n): ").strip().lower()
    brands = None
    if apply_brand_filter == "y":
        brand_input = input("Enter camera brand(s), separated by commas (e.g., Canon,Nikon,Apple): ").strip()
        brands = [b.strip().lower() for b in brand_input.split(",") if b.strip()]
        if brands:
            print(f"Filtering: only images from {', '.join(brands)} will be included.\n")
        else:
            brands = None
            print("No valid brands entered. No brand filter applied.\n")

    output_file = Path.cwd() / "exif_output.txt"

    with open(output_file, "w", encoding="utf-8") as f:
        for file in folder.rglob("*"):
            if file.suffix.lower() in [".jpg", ".jpeg", ".png", ".heic"]:
                exif_data = extract_exif(file)
                if not exif_data:
                    continue  # skip images with no data at all

                # Apply width filter
                if min_width is not None:
                    width = exif_data.get("ImageWidth", 0)
                    if width < min_width:
                        continue

                # Apply camera brand filter
                if brands is not None:
                    make = str(exif_data.get("Make", "")).lower()
                    if not any(brand in make for brand in brands):
                        continue

                # Write results
                rel_path = file.relative_to(folder)
                f.write(f"\n[FILE] {rel_path}\n")
                for tag, val in exif_data.items():
                    f.write(f"   - {tag}: {val}\n")

    print(f"data written to {output_file}")

if __name__ == "__main__":
    main()
