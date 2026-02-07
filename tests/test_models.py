"""
Tests for wildlifeai.models module
"""
import pytest
from wildlifeai.models import SpeciesClassifier


class TestSpeciesClassifier:
    """Tests for SpeciesClassifier"""
    
    def test_classifier_init_no_model(self):
        """Test initialization without model path"""
        classifier = SpeciesClassifier()
        assert classifier.model_path is None
        assert classifier.model is None
    
    def test_classifier_init_with_model_path(self):
        """Test initialization with model path"""
        model_path = "path/to/model.pth"
        classifier = SpeciesClassifier(model_path=model_path)
        assert classifier.model_path == model_path
    
    def test_predict_returns_dict(self):
        """Test that predict returns a dictionary"""
        classifier = SpeciesClassifier()
        result = classifier.predict("dummy_image.jpg")
        
        assert isinstance(result, dict)
        assert "unknown" in result
        assert result["unknown"] == 1.0
    
    def test_predict_batch(self):
        """Test batch prediction"""
        classifier = SpeciesClassifier()
        paths = ["image1.jpg", "image2.jpg", "image3.jpg"]
        results = classifier.predict_batch(paths)
        
        assert len(results) == 3
        assert all(isinstance(r, dict) for r in results)


# TODO: Add tests for custom classifier implementations
# TODO: Test model loading when actual models are integrated
