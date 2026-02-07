from wildlifeai.utils import extract_exif
from wildlifeai.models import SpeciesClassifier
import logging
import json
import csv
from pathlib import Path
from typing import List, Dict, Any
from PIL import Image, UnidentifiedImageError

logger = logging.getLogger(__name__)


def run_pipeline(
    image_folder: str,
    json_output: str = "image_metadata.json",
    csv_output: str = "image_metadata.csv",
    model_path: str | None = None,
) -> List[Dict[str, Any]]:
    """
    High-level WildlifeAI pipeline with ML hook.
    
    Args:
        image_folder: Path to folder containing images
        json_output: Path for JSON output file
        csv_output: Path for CSV output file
        model_path: Optional path to ML model weights
        
    Returns:
        List of dictionaries containing image metadata and predictions
        
    Raises:
        FileNotFoundError: If image_folder does not exist
    """
    logger.info("WildlifeAI pipeline started")

    classifier = SpeciesClassifier(model_path=model_path)
    results = []
    folder = Path(image_folder)

    if not folder.exists():
        logger.error(f"Folder not found: {image_folder}")
        raise FileNotFoundError(f"{image_folder} does not exist")

    if not folder.is_dir():
        logger.error(f"Path is not a directory: {image_folder}")
        raise NotADirectoryError(f"{image_folder} is not a directory")

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

                # Add ML prediction BEFORE saving (critical fix)
                info["species_prediction"] = classifier.predict(str(filepath))
                
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
    logger.info(f"Saved JSON output to: {json_output}")

    # ---- Save CSV ----
    if results:
        output_csv = Path(csv_output)
        with output_csv.open("w", newline="", encoding="utf-8") as f:
            # Flatten species_prediction dict for CSV
            csv_results = []
            for item in results:
                row = {k: v for k, v in item.items() if k != "species_prediction"}
                # Add prediction as a simple string
                row["species_prediction"] = json.dumps(item.get("species_prediction", {}))
                csv_results.append(row)
            
            if csv_results:
                writer = csv.DictWriter(f, fieldnames=csv_results[0].keys())
                writer.writeheader()
                writer.writerows(csv_results)
        logger.info(f"Saved CSV output to: {csv_output}")

    logger.info(f"WildlifeAI pipeline completed - processed {len(results)} images")
    print(f"[OK] Saved {len(results)} images with predictions to {json_output} and {csv_output}")
    
    return results
