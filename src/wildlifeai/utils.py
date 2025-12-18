from PIL import Image, ExifTags
import os
import json
import csv
import logging


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


def extract_exif(img: Image.Image) -> dict:
    """
    Extract EXIF metadata from an image if available.
    """
    exif_data = {}

    try:
        raw_exif = img._getexif()
        if raw_exif is not None:
            for tag_id, value in raw_exif.items():
                tag = ExifTags.TAGS.get(tag_id, tag_id)
                exif_data[tag] = value
    except Exception as e:
        logger.warning(f"EXIF extraction failed: {e}")

    return exif_data


def process_images(
    folder_path: str,
    json_output: str = "image_metadata.json",
    csv_output: str = "image_metadata.csv",
):
    """
    Load images, extract metadata + EXIF,
    and save results to JSON and CSV.
    """
    logger.info(f"Pipeline started for folder: {folder_path}")

    results = []

    if not os.path.exists(folder_path):
        logger.error(f"Folder not found: {folder_path}")
        raise FileNotFoundError(f"{folder_path} does not exist")

    for filename in os.listdir(folder_path):
        if filename.lower().endswith((".jpg", ".jpeg", ".png")):
            filepath = os.path.join(folder_path, filename)

            try:
                with Image.open(filepath) as img:
                    exif = extract_exif(img)

                    info = {
                        "filename": filename,
                        "format": img.format,
                        "width": img.size[0],
                        "height": img.size[1],
                        "mode": img.mode,
                        "datetime": exif.get("DateTime"),
                        "camera_make": exif.get("Make"),
                        "camera_model": exif.get("Model"),
                    }

                    results.append(info)
                    logger.info(f"Processed image: {filename}")

            except Exception as e:
                logger.error(f"Failed to process {filename}: {e}")

    # ---- Save JSON ----
    with open(json_output, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4)

    # ---- Save CSV ----
    if results:
        with open(csv_output, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=results[0].keys())
            writer.writeheader()
            writer.writerows(results)

    logger.info(
        f"Pipeline finished. Images processed: {len(results)} | "
        f"JSON: {json_output} | CSV: {csv_output}"
    )

    print(
        f"Saved metadata for {len(results)} images to "
        f"{json_output} and {csv_output}"
    )

    return results
