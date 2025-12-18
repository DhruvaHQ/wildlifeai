from typing import Dict


class SpeciesClassifier:
    """
    Placeholder species classification model.

    This class defines the interface for future ML models.
    """

    def __init__(self, model_path: str | None = None):
        self.model_path = model_path

    def predict(self, image_path: str) -> Dict[str, float]:
        """
        Predict species probabilities for a given image.

        NOTE:
        This is a placeholder. Replace with a real ML model later.
        """

        # Fake prediction (stub)
        return {
            "unknown": 1.0
        }
