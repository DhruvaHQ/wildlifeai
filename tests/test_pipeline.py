"""
Tests for wildlifeai.pipeline module
"""
import pytest
from pathlib import Path
from PIL import Image
from wildlifeai.pipeline import run_pipeline


class TestRunPipeline:
    """Tests for run_pipeline function"""
    
    @pytest.fixture
    def temp_image_folder(self, tmp_path):
        """Create a temporary folder with test images"""
        image_dir = tmp_path / "test_images"
        image_dir.mkdir()
        
        # Create test images
        img = Image.new('RGB', (100, 100), color='blue')
        img.save(image_dir / "test1.jpg")
        
        return image_dir
    
    def test_pipeline_basic(self, temp_image_folder, tmp_path):
        """Test basic pipeline execution"""
        json_out = tmp_path / "output.json"
        csv_out = tmp_path / "output.csv"
        
        results = run_pipeline(
            image_folder=str(temp_image_folder),
            json_output=str(json_out),
            csv_output=str(csv_out)
        )
        
        assert len(results) == 1
        assert "species_prediction" in results[0]
        assert json_out.exists()
        assert csv_out.exists()
    
    def test_pipeline_with_predictions(self, temp_image_folder, tmp_path):
        """Test that species predictions are included in results"""
        json_out = tmp_path / "output.json"
        csv_out = tmp_path / "output.csv"
        
        results = run_pipeline(
            image_folder=str(temp_image_folder),
            json_output=str(json_out),
            csv_output=str(csv_out)
        )
        
        # Verify predictions are in the results
        for item in results:
            assert "species_prediction" in item
            assert isinstance(item["species_prediction"], dict)
    
    def test_pipeline_nonexistent_folder(self):
        """Test error handling for nonexistent folder"""
        with pytest.raises(FileNotFoundError):
            run_pipeline(image_folder="/nonexistent/path")


# TODO: Add integration tests with custom models
# TODO: Test different configuration options
# TODO: Test error recovery
