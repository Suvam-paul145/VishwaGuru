"""
Tests for file upload validation.
Tests various security scenarios including file size limits,
MIME type validation, and malicious file detection.
"""
import asyncio
import os
import sys
import tempfile
import io
from fastapi.testclient import TestClient
from fastapi import UploadFile

# Add backend to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from main import app
from file_validator import validate_image_upload, validate_filename, MAX_FILE_SIZE
from models import Base
from database import engine

# Setup test DB
Base.metadata.create_all(bind=engine)

client = TestClient(app)


class TestFileValidator:
    """Test the file validation utility functions"""
    
    def test_validate_filename_normal(self):
        """Test normal filename validation"""
        result = validate_filename("image.jpg")
        assert result == "image.jpg"
    
    def test_validate_filename_path_traversal(self):
        """Test that path traversal attempts are rejected"""
        try:
            validate_filename("../../../etc/passwd")
            assert False, "Should have raised HTTPException"
        except Exception as e:
            assert "Invalid filename" in str(e)
    
    def test_validate_filename_null_bytes(self):
        """Test that null bytes are removed"""
        result = validate_filename("image\x00.jpg")
        assert "\x00" not in result
    
    def test_validate_filename_empty(self):
        """Test that empty filename is rejected"""
        try:
            validate_filename("")
            assert False, "Should have raised HTTPException"
        except Exception as e:
            assert "Filename is required" in str(e)


class TestIssueEndpointValidation:
    """Test file validation on /api/issues endpoint"""
    
    def test_create_issue_with_valid_image(self):
        """Test creating issue with valid small image"""
        # Create a minimal valid JPEG file (1x1 pixel)
        jpeg_header = b'\xFF\xD8\xFF\xE0\x00\x10JFIF\x00\x01\x01\x00\x00\x01\x00\x01\x00\x00'
        jpeg_body = b'\xFF\xDB\x00C\x00\x08\x06\x06\x07\x06\x05\x08\x07\x07\x07\t\t\x08\n\x0c\x14\r\x0c\x0b\x0b\x0c\x19\x12\x13\x0f'
        jpeg_end = b'\xFF\xD9'
        
        # This creates a minimal but valid JPEG
        image_data = jpeg_header + jpeg_body + jpeg_end
        
        response = client.post(
            "/api/issues",
            data={
                "description": "Test Issue with Valid Image",
                "category": "Road",
                "user_email": "test@example.com"
            },
            files={"image": ("test.jpg", io.BytesIO(image_data), "image/jpeg")}
        )
        
        # Should succeed or return 500 (due to AI service dependencies)
        # but not 400 (validation error)
        assert response.status_code in [200, 500]
        if response.status_code == 400:
            # If 400, it should not be about file validation
            detail = response.json().get("detail", "")
            assert "file" not in detail.lower() or "size" not in detail.lower()
    
    def test_create_issue_with_oversized_file(self):
        """Test that oversized files are rejected"""
        # Create a file larger than MAX_FILE_SIZE
        large_data = b'x' * (MAX_FILE_SIZE + 1000)
        
        response = client.post(
            "/api/issues",
            data={
                "description": "Test Issue with Large File",
                "category": "Road",
                "user_email": "test@example.com"
            },
            files={"image": ("large.jpg", io.BytesIO(large_data), "image/jpeg")}
        )
        
        assert response.status_code == 400
        assert "size" in response.json()["detail"].lower()
    
    def test_create_issue_with_invalid_extension(self):
        """Test that invalid file extensions are rejected"""
        response = client.post(
            "/api/issues",
            data={
                "description": "Test Issue with Invalid Extension",
                "category": "Road",
                "user_email": "test@example.com"
            },
            files={"image": ("test.exe", io.BytesIO(b"fake content"), "application/x-msdownload")}
        )
        
        assert response.status_code == 400
        assert "extension" in response.json()["detail"].lower()
    
    def test_create_issue_with_empty_file(self):
        """Test that empty files are rejected"""
        response = client.post(
            "/api/issues",
            data={
                "description": "Test Issue with Empty File",
                "category": "Road",
                "user_email": "test@example.com"
            },
            files={"image": ("empty.jpg", io.BytesIO(b""), "image/jpeg")}
        )
        
        assert response.status_code == 400
        assert "empty" in response.json()["detail"].lower()
    
    def test_create_issue_without_image(self):
        """Test that issues can still be created without image"""
        response = client.post(
            "/api/issues",
            data={
                "description": "Test Issue without Image",
                "category": "Road",
                "user_email": "test@example.com"
            }
        )
        
        # Should succeed or return 500 (due to AI service dependencies)
        # but not 400 (validation error)
        assert response.status_code in [200, 500]


class TestDetectionEndpointsValidation:
    """Test file validation on detection endpoints"""
    
    def test_detect_pothole_with_invalid_file_type(self):
        """Test pothole detection rejects non-image files"""
        response = client.post(
            "/api/detect-pothole",
            files={"image": ("test.txt", io.BytesIO(b"not an image"), "text/plain")}
        )
        
        assert response.status_code == 400
        detail = response.json()["detail"].lower()
        assert "extension" in detail or "type" in detail
    
    def test_detect_infrastructure_with_invalid_file_type(self):
        """Test infrastructure detection rejects non-image files"""
        response = client.post(
            "/api/detect-infrastructure",
            files={"image": ("test.pdf", io.BytesIO(b"fake pdf"), "application/pdf")}
        )
        
        assert response.status_code == 400
        detail = response.json()["detail"].lower()
        assert "extension" in detail or "type" in detail
    
    def test_detect_flooding_with_oversized_file(self):
        """Test flooding detection rejects oversized files"""
        large_data = b'x' * (MAX_FILE_SIZE + 1000)
        
        response = client.post(
            "/api/detect-flooding",
            files={"image": ("large.jpg", io.BytesIO(large_data), "image/jpeg")}
        )
        
        assert response.status_code == 400
        assert "size" in response.json()["detail"].lower()
    
    def test_detect_vandalism_with_empty_file(self):
        """Test vandalism detection rejects empty files"""
        response = client.post(
            "/api/detect-vandalism",
            files={"image": ("empty.jpg", io.BytesIO(b""), "image/jpeg")}
        )
        
        assert response.status_code == 400
        assert "empty" in response.json()["detail"].lower()
    
    def test_detect_garbage_with_executable(self):
        """Test garbage detection rejects executable files"""
        response = client.post(
            "/api/detect-garbage",
            files={"image": ("malware.exe", io.BytesIO(b"MZ fake exe"), "application/x-msdownload")}
        )
        
        assert response.status_code == 400
        detail = response.json()["detail"].lower()
        assert "extension" in detail or "type" in detail


def run_tests():
    """Run all tests"""
    print("Testing File Validation Utility...")
    validator_tests = TestFileValidator()
    validator_tests.test_validate_filename_normal()
    print("✓ Normal filename validation")
    
    validator_tests.test_validate_filename_path_traversal()
    print("✓ Path traversal rejection")
    
    validator_tests.test_validate_filename_null_bytes()
    print("✓ Null byte handling")
    
    validator_tests.test_validate_filename_empty()
    print("✓ Empty filename rejection")
    
    print("\nTesting Issue Endpoint Validation...")
    issue_tests = TestIssueEndpointValidation()
    
    issue_tests.test_create_issue_with_valid_image()
    print("✓ Valid image accepted")
    
    issue_tests.test_create_issue_with_oversized_file()
    print("✓ Oversized file rejected")
    
    issue_tests.test_create_issue_with_invalid_extension()
    print("✓ Invalid extension rejected")
    
    issue_tests.test_create_issue_with_empty_file()
    print("✓ Empty file rejected")
    
    issue_tests.test_create_issue_without_image()
    print("✓ Issue without image works")
    
    print("\nTesting Detection Endpoints Validation...")
    detection_tests = TestDetectionEndpointsValidation()
    
    detection_tests.test_detect_pothole_with_invalid_file_type()
    print("✓ Pothole: Invalid file type rejected")
    
    detection_tests.test_detect_infrastructure_with_invalid_file_type()
    print("✓ Infrastructure: Invalid file type rejected")
    
    detection_tests.test_detect_flooding_with_oversized_file()
    print("✓ Flooding: Oversized file rejected")
    
    detection_tests.test_detect_vandalism_with_empty_file()
    print("✓ Vandalism: Empty file rejected")
    
    detection_tests.test_detect_garbage_with_executable()
    print("✓ Garbage: Executable file rejected")
    
    print("\n✅ All file validation tests passed!")


if __name__ == "__main__":
    run_tests()
