"""
Tests for wildlifeai.utils module
"""
import pytest
from pathlib import Path
from PIL import Image
from wildlifeai.utils import extract_exif, say_hello


class TestSayHello:
    """Tests for say_hello function"""
    
    def test_say_hello_basic(self):
        """Test basic hello functionality"""
        result = say_hello("World")
        assert "Hello, World!" in result
        assert "WildlifeAI" in result


class TestExtractExif:
    """Tests for extract_exif function"""
    
    def test_extract_exif_with_no_exif(self):
        """Test EXIF extraction from image without EXIF data"""
        # Create a simple test image
        img = Image.new('RGB', (100, 100), color='red')
        exif = extract_exif(img)
        
        # Should return empty dict or handle gracefully
        assert isinstance(exif, dict)
    
    def test_extract_exif_handles_errors(self):
        """Test that extract_exif handles errors gracefully"""
        img = Image.new('RGB', (100, 100))
        result = extract_exif(img)
        assert isinstance(result, dict)


class TestProcessImages:
    """Tests for process_images function"""
    
    @pytest.fixture
    def temp_image_folder(self, tmp_path):
        """Create a temporary folder with test images"""
        image_dir = tmp_path / "test_images"
        image_dir.mkdir()
        
        # Create a simple test image
        img = Image.new('RGB', (100, 100), color='blue')
        img.save(image_dir / "test1.jpg")
        
        img2 = Image.new('RGB', (200, 150), color='green')
        img2.save(image_dir / "test2.png")
        
        return image_dir
    
    def test_process_images_basic(self, temp_image_folder, tmp_path):
        """Test basic image processing"""
        from wildlifeai.utils import process_images
        
        json_out = tmp_path / "output.json"
        csv_out = tmp_path / "output.csv"
        
        results = process_images(
            folder_path=str(temp_image_folder),
            json_output=str(json_out),
            csv_output=str(csv_out)
        )
        
        assert len(results) == 2
        assert json_out.exists()
        assert csv_out.exists()
    
    def test_process_images_nonexistent_folder(self):
        """Test error handling for nonexistent folder"""
        from wildlifeai.utils import process_images
        
        with pytest.raises(FileNotFoundError):
            process_images(
                folder_path="/nonexistent/path/to/images"
            )


# TODO: Add more comprehensive tests
# - Test with actual EXIF data
# - Test error handling for corrupted images
# - Test different image formats
# - Integration tests with pipeline
