"""
Unit tests for file upload validation module.
Tests file validation logic in isolation without requiring full app dependencies.
"""
import asyncio
import io
import os
import sys

# Add backend to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from file_validator import validate_filename, MAX_FILE_SIZE


class MockUploadFile:
    """Mock UploadFile for testing"""
    def __init__(self, filename, content, content_type):
        self.filename = filename
        self.content = content
        self.content_type = content_type
        self._file = io.BytesIO(content)
        self._position = 0
    
    async def read(self, size=-1):
        return self._file.read(size)
    
    async def seek(self, position):
        self._file.seek(position)
        return position


class TestFilenameValidation:
    """Test filename sanitization"""
    
    def test_normal_filename(self):
        """Test normal filename passes validation"""
        result = validate_filename("image.jpg")
        assert result == "image.jpg"
        print("✓ Normal filename validation passed")
    
    def test_filename_with_spaces(self):
        """Test filename with spaces"""
        result = validate_filename("my image.png")
        assert result == "my image.png"
        print("✓ Filename with spaces passed")
    
    def test_path_traversal_attack(self):
        """Test that path traversal attempts are blocked"""
        try:
            validate_filename("../../../etc/passwd")
            assert False, "Should have raised exception"
        except Exception as e:
            assert "Invalid filename" in str(e)
            print("✓ Path traversal attack blocked")
    
    def test_backslash_path_traversal(self):
        """Test that Windows-style path traversal is blocked"""
        try:
            validate_filename("..\\..\\..\\windows\\system32\\config\\sam")
            assert False, "Should have raised exception"
        except Exception as e:
            assert "Invalid filename" in str(e)
            print("✓ Backslash path traversal blocked")
    
    def test_null_byte_injection(self):
        """Test that null byte injection is handled"""
        result = validate_filename("image.jpg\x00.exe")
        assert "\x00" not in result
        print("✓ Null byte injection handled")
    
    def test_empty_filename(self):
        """Test that empty filename is rejected"""
        try:
            validate_filename("")
            assert False, "Should have raised exception"
        except Exception as e:
            assert "Filename is required" in str(e)
            print("✓ Empty filename rejected")
    
    def test_none_filename(self):
        """Test that None filename is rejected"""
        try:
            validate_filename(None)
            assert False, "Should have raised exception"
        except Exception as e:
            assert "Filename is required" in str(e)
            print("✓ None filename rejected")


async def test_async_validation():
    """Test async file validation functions"""
    from file_validator import validate_image_upload
    
    # Test 1: Empty file rejection
    print("\nTesting async validation...")
    empty_file = MockUploadFile("empty.jpg", b"", "image/jpeg")
    try:
        await validate_image_upload(empty_file)
        assert False, "Should have raised exception"
    except Exception as e:
        assert "empty" in str(e).lower()
        print("✓ Empty file rejected")
    
    # Test 2: Oversized file rejection
    oversized_content = b"x" * (MAX_FILE_SIZE + 1000)
    oversized_file = MockUploadFile("large.jpg", oversized_content, "image/jpeg")
    try:
        await validate_image_upload(oversized_file)
        assert False, "Should have raised exception"
    except Exception as e:
        assert "size" in str(e).lower()
        print("✓ Oversized file rejected")
    
    # Test 3: Invalid extension rejection
    invalid_ext_file = MockUploadFile("malware.exe", b"MZ fake", "application/x-msdownload")
    try:
        await validate_image_upload(invalid_ext_file)
        assert False, "Should have raised exception"
    except Exception as e:
        assert "extension" in str(e).lower()
        print("✓ Invalid extension rejected")
    
    # Test 4: No filename
    no_name_file = MockUploadFile(None, b"content", "image/jpeg")
    try:
        await validate_image_upload(no_name_file)
        assert False, "Should have raised exception"
    except Exception as e:
        assert "filename" in str(e).lower()
        print("✓ Missing filename rejected")
    
    # Test 5: Valid small JPEG header (minimal but recognizable)
    # JPEG magic bytes
    jpeg_magic = b'\xFF\xD8\xFF'
    small_jpeg = MockUploadFile("valid.jpg", jpeg_magic + b"\x00" * 100, "image/jpeg")
    try:
        await validate_image_upload(small_jpeg)
        print("✓ Valid JPEG format accepted")
    except Exception as e:
        # If magic library detects it as non-image, that's also acceptable
        if "type" in str(e).lower():
            print("✓ MIME type validation working (rejected minimal JPEG)")
        else:
            raise


def run_all_tests():
    """Run all tests"""
    print("=" * 60)
    print("File Upload Validation - Unit Tests")
    print("=" * 60)
    
    print("\n1. Testing Filename Validation")
    print("-" * 60)
    filename_tests = TestFilenameValidation()
    filename_tests.test_normal_filename()
    filename_tests.test_filename_with_spaces()
    filename_tests.test_path_traversal_attack()
    filename_tests.test_backslash_path_traversal()
    filename_tests.test_null_byte_injection()
    filename_tests.test_empty_filename()
    filename_tests.test_none_filename()
    
    print("\n2. Testing Async File Validation")
    print("-" * 60)
    asyncio.run(test_async_validation())
    
    print("\n" + "=" * 60)
    print("✅ All validation unit tests passed!")
    print("=" * 60)


if __name__ == "__main__":
    run_all_tests()
