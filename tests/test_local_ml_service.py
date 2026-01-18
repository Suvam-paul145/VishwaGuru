"""
Tests for the Local ML Service.

This test file covers:
- Image classification functionality (via YOLO)
- Detection functions for vandalism, infrastructure, and flooding
"""

import pytest
import sys
import os
from unittest.mock import Mock, patch, MagicMock
from PIL import Image

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from local_ml_service import detect_vandalism_local, detect_infrastructure_local, detect_flooding_local

class TestLocalMLService:
    """Tests for the local_ml_service module."""
    
    @pytest.fixture
    def sample_image(self):
        """Create a sample test image."""
        return Image.new("RGB", (224, 224), color="red")
    
    @patch("local_ml_service.get_general_model")
    @patch("local_ml_service.run_in_threadpool")
    @pytest.mark.asyncio
    async def test_detect_vandalism_local_empty(self, mock_run, mock_get_model, sample_image):
        """Test vandalism detection with no detections."""
        mock_model = MagicMock()
        mock_get_model.return_value = mock_model
        
        mock_result = MagicMock()
        mock_result.boxes = []
        mock_run.return_value = [mock_result]
        
        detections = await detect_vandalism_local(sample_image)
        assert isinstance(detections, list)
        assert len(detections) == 0

    @patch("local_ml_service.get_general_model")
    @patch("local_ml_service.run_in_threadpool")
    @pytest.mark.asyncio
    async def test_detect_vandalism_local_positive(self, mock_run, mock_get_model, sample_image):
        """Test vandalism detection with positive detection."""
        mock_model = MagicMock()
        mock_get_model.return_value = mock_model
        
        # Construct a mock result that looks like a YOLO result
        mock_box = MagicMock()
        mock_box.xyxy = [MagicMock()]
        mock_box.xyxy[0].cpu().numpy().tolist.return_value = [0, 0, 100, 100]
        mock_box.conf = [MagicMock()]
        mock_box.conf[0].cpu().numpy.return_value = 0.8
        mock_box.cls = [MagicMock()]
        mock_box.cls[0].cpu().numpy.return_value = 0 # person
        
        mock_result = MagicMock()
        mock_result.boxes = [mock_box]
        mock_result.names = {0: 'person'}
        
        mock_run.return_value = [mock_result]
        
        detections = await detect_vandalism_local(sample_image)
        assert isinstance(detections, list)
        assert len(detections) == 1
        assert detections[0]['label'] == "vandalism activity"

    @patch("local_ml_service.get_general_model")
    @patch("local_ml_service.run_in_threadpool")
    @pytest.mark.asyncio
    async def test_detect_infrastructure_local(self, mock_run, mock_get_model, sample_image):
        """Test infrastructure detection."""
        mock_model = MagicMock()
        mock_get_model.return_value = mock_model
        
        mock_box = MagicMock()
        mock_box.xyxy = [MagicMock()]
        mock_box.xyxy[0].cpu().numpy().tolist.return_value = [0, 0, 100, 100]
        mock_box.conf = [MagicMock()]
        mock_box.conf[0].cpu().numpy.return_value = 0.9
        mock_box.cls = [MagicMock()]
        mock_box.cls[0].cpu().numpy.return_value = 0 # traffic light
        
        mock_result = MagicMock()
        mock_result.boxes = [mock_box]
        mock_result.names = {0: 'traffic light'}
        
        mock_run.return_value = [mock_result]
        
        detections = await detect_infrastructure_local(sample_image)
        assert isinstance(detections, list)
        assert len(detections) == 1
        assert detections[0]['label'] == "damaged sign" # traffic light maps to damaged sign in logic

    @patch("local_ml_service.get_general_model")
    @patch("local_ml_service.run_in_threadpool")
    @pytest.mark.asyncio
    async def test_detect_flooding_local(self, mock_run, mock_get_model, sample_image):
        """Test flooding detection."""
        mock_model = MagicMock()
        mock_get_model.return_value = mock_model
        
        mock_box = MagicMock()
        mock_box.xyxy = [MagicMock()]
        # y2 is 200, image height default 480, 200 < 480*0.6, so it might NOT be flooding?
        # Logic: if box_bottom > image_height * 0.6
        # 480 * 0.6 = 288.
        # Let's set y2 to 300.
        mock_box.xyxy[0].cpu().numpy().tolist.return_value = [0, 250, 50, 300]
        mock_box.conf = [MagicMock()]
        mock_box.conf[0].cpu().numpy.return_value = 0.9
        mock_box.cls = [MagicMock()]
        mock_box.cls[0].cpu().numpy.return_value = 0 # car
        
        mock_result = MagicMock()
        mock_result.boxes = [mock_box]
        mock_result.names = {0: 'car'}
        
        mock_run.return_value = [mock_result]
        
        detections = await detect_flooding_local(sample_image)
        assert isinstance(detections, list)
        assert len(detections) == 1
        assert detections[0]['label'] == "potential flooding"
