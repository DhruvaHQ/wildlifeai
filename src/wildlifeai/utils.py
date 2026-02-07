from PIL import Image, ExifTags, UnidentifiedImageError
import os
import json
import csv
import logging
from pathlib import Path
from typing import List, Dict, Any


# ---------------- Logging Setup ----------------
logging.basicConfig(
    filename="wildlifeai.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger(__name__)
# ------------------------------------------------


def say_hello(name: str) -> str:
    """
    Simple helper to confirm the package works.
    """
    logger.info(f"say_hello called with name={name}")
    return f"Hello, {name}! WildlifeAI is ready."


def extract_exif(img: Image.Image) -> Dict[str, Any]:
    """
    Extract EXIF metadata from an image if available.
    
    Args:
        img: PIL Image object
        
    Returns:
        Dictionary containing EXIF metadata. Common keys include:
        - DateTime: Image capture timestamp
        - Make: Camera manufacturer
        - Model: Camera model
        - GPSInfo: GPS coordinates (if available)
        
    Note:
        Returns empty dict if no EXIF data is present or extraction fails.
    """
    exif_data = {}

    try:
        raw_exif = img._getexif()
        if raw_exif is not None:
            for tag_id, value in raw_exif.items():
                tag = ExifTags.TAGS.get(tag_id, tag_id)
                # Convert bytes to string if needed
                if isinstance(value, bytes):
                    try:
                        value = value.decode('utf-8', errors='ignore')
                    except (UnicodeDecodeError, AttributeError):
                        value = str(value)
                exif_data[tag] = value
    except AttributeError:
        # Image format doesn't support EXIF (e.g., PNG)
        logger.debug("Image format does not support EXIF metadata")
    except Exception as e:
        logger.warning(f"EXIF extraction failed: {e}")

    return exif_data


def process_images(
    folder_path: str,
    json_output: str = "image_metadata.json",
    csv_output: str = "image_metadata.csv",
) -> List[Dict[str, Any]]:
    """
    Load images, extract metadata + EXIF,
    and save results to JSON and CSV.
    
    Args:
        folder_path: Path to folder containing images
        json_output: Path for JSON output file
        csv_output: Path for CSV output file
        
    Returns:
        List of dictionaries containing image metadata
        
    Raises:
        FileNotFoundError: If folder_path does not exist
    """
    logger.info(f"Pipeline started for folder: {folder_path}")

    results = []
    folder = Path(folder_path)

    if not folder.exists():
        logger.error(f"Folder not found: {folder_path}")
        raise FileNotFoundError(f"{folder_path} does not exist")

    if not folder.is_dir():
        logger.error(f"Path is not a directory: {folder_path}")
        raise NotADirectoryError(f"{folder_path} is not a directory")

    # Process all image files
    image_files = [
        f for f in folder.iterdir() 
        if f.is_file() and f.suffix.lower() in {".jpg", ".jpeg", ".png", ".gif", ".bmp"}
    ]
    
    logger.info(f"Found {len(image_files)} image files")

    for filepath in image_files:
        filename = filepath.name
        
        try:
            with Image.open(filepath) as img:
                exif = extract_exif(img)

                info = {
                    "filename": filename,
                    "format": img.format,
                    "width": img.size[0],
                    "height": img.size[1],
                    "mode": img.mode,
                    "file_size_bytes": filepath.stat().st_size,
                    "datetime": exif.get("DateTime"),
                    "camera_make": exif.get("Make"),
                    "camera_model": exif.get("Model"),
                }

                results.append(info)
                logger.info(f"Processed image: {filename}")

        except FileNotFoundError:
            logger.error(f"Image file not found: {filename}")
        except UnidentifiedImageError:
            logger.error(f"Invalid or corrupted image format: {filename}")
        except PermissionError:
            logger.error(f"Permission denied accessing: {filename}")
        except Exception as e:
            logger.error(f"Unexpected error processing {filename}: {e}", exc_info=True)

    # ---- Save JSON ----
    output_json = Path(json_output)
    with output_json.open("w", encoding="utf-8") as f:
        json.dump(results, f, indent=4)

    # ---- Save CSV ----
    if results:
        output_csv = Path(csv_output)
        with output_csv.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=results[0].keys())
            writer.writeheader()
            writer.writerows(results)

    logger.info(
        f"Pipeline finished. Images processed: {len(results)} | "
        f"JSON: {json_output} | CSV: {csv_output}"
    )

    print(
        f"[OK] Saved metadata for {len(results)} images to "
        f"{json_output} and {csv_output}"
    )

    return results
