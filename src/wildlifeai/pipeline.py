from wildlifeai.utils import process_images
from wildlifeai.models import SpeciesClassifier
import logging

logger = logging.getLogger(__name__)


def run_pipeline(
    image_folder: str,
    json_output: str = "image_metadata.json",
    csv_output: str = "image_metadata.csv",
    model_path: str | None = None,
):
    """
    High-level WildlifeAI pipeline with ML hook.
    """
    logger.info("WildlifeAI pipeline started")

    classifier = SpeciesClassifier(model_path=model_path)

    results = process_images(
        folder_path=image_folder,
        json_output=json_output,
        csv_output=csv_output,
    )

    # Attach ML predictions (placeholder)
    for item in results:
        image_path = f"{image_folder}/{item['filename']}"
        item["species_prediction"] = classifier.predict(image_path)

    logger.info("WildlifeAI pipeline completed")
    return results
