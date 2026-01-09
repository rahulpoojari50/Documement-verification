import unittest
import os
import sys
import tempfile
import numpy as np
from PIL import Image

# Add the scripts directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'scripts'))

class TestDataPreparation(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
        pass

    def tearDown(self):
        """Clean up after each test method."""
        pass

    def test_directory_creation(self):
        """Test that required directories are created."""
        # This would test the create_directories function
        # For now, we'll just check that the function exists
        try:
            from scripts.data_prep import create_directories
            self.assertTrue(callable(create_directories))
        except ImportError:
            self.skipTest("data_prep module not available")

    def test_image_corruption_check(self):
        """Test image corruption detection."""
        try:
            from scripts.data_prep import is_image_corrupted
            
            # Create a valid image
            valid_img = Image.new('RGB', (100, 100), color='red')
            with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as tmp:
                valid_img.save(tmp.name, 'JPEG')
                tmp_path = tmp.name
            
            # Test with valid image
            self.assertFalse(is_image_corrupted(tmp_path))
            
            # Clean up
            os.unlink(tmp_path)
            
            # Test with non-existent file
            self.assertTrue(is_image_corrupted('/non/existent/file.jpg'))
            
        except ImportError:
            self.skipTest("data_prep module not available")

class TestModelComponents(unittest.TestCase):
    def test_model_imports(self):
        """Test that model components can be imported."""
        try:
            from scripts.train import DocumentClassifier, DocumentDataset
            self.assertTrue(callable(DocumentClassifier))
            self.assertTrue(callable(DocumentDataset))
        except ImportError:
            self.skipTest("train module not available")

    def test_evaluation_imports(self):
        """Test that evaluation components can be imported."""
        try:
            from scripts.evaluate import evaluate_model
            self.assertTrue(callable(evaluate_model))
        except ImportError:
            self.skipTest("evaluate module not available")

class TestAPIComponents(unittest.TestCase):
    def test_api_imports(self):
        """Test that API components can be imported."""
        try:
            # Try importing the main FastAPI app
            from app.main import app
            self.assertIsNotNone(app)
        except ImportError:
            self.skipTest("API module not available")

if __name__ == '__main__':
    unittest.main()