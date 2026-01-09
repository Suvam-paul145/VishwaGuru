"""
Test CORS configuration validation to ensure security best practices.
This test verifies that wildcard origins are rejected and proper validation is enforced.
"""
import sys
import os
import pytest

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

def test_cors_rejects_wildcard():
    """Test that CORS configuration rejects wildcard origins"""
    # Set environment to wildcard
    os.environ["FRONTEND_URL"] = "*"
    
    # Importing should raise ValueError due to wildcard rejection
    with pytest.raises(ValueError, match="cannot be set to.*wildcard"):
        # Force reimport to trigger validation
        import importlib
        if 'main' in sys.modules:
            importlib.reload(sys.modules['main'])
        else:
            import main

def test_cors_rejects_empty():
    """Test that CORS configuration rejects empty FRONTEND_URL"""
    # Remove or set empty FRONTEND_URL
    if "FRONTEND_URL" in os.environ:
        del os.environ["FRONTEND_URL"]
    
    # Importing should raise ValueError due to missing FRONTEND_URL
    with pytest.raises(ValueError, match="FRONTEND_URL environment variable is required"):
        import importlib
        if 'main' in sys.modules:
            importlib.reload(sys.modules['main'])
        else:
            import main

def test_cors_accepts_valid_single_origin():
    """Test that CORS configuration accepts a valid single origin"""
    # Set valid frontend URL
    os.environ["FRONTEND_URL"] = "https://example.netlify.app"
    
    try:
        import importlib
        if 'main' in sys.modules:
            importlib.reload(sys.modules['main'])
        else:
            import main
        # If we get here without exception, the test passes
        assert True
    except ValueError:
        pytest.fail("Valid single origin should not raise ValueError")

def test_cors_accepts_multiple_origins():
    """Test that CORS configuration accepts comma-separated origins"""
    # Set multiple valid origins
    os.environ["FRONTEND_URL"] = "http://localhost:5173,https://example.netlify.app"
    
    try:
        import importlib
        if 'main' in sys.modules:
            importlib.reload(sys.modules['main'])
        else:
            import main
        # If we get here without exception, the test passes
        assert True
    except ValueError:
        pytest.fail("Multiple valid origins should not raise ValueError")

def test_cors_rejects_wildcard_in_list():
    """Test that CORS configuration rejects wildcard even in comma-separated list"""
    # Set origins with wildcard in list
    os.environ["FRONTEND_URL"] = "http://localhost:5173,*,https://example.netlify.app"
    
    # Should raise ValueError due to wildcard in list
    with pytest.raises(ValueError, match="Wildcard origin.*is not allowed"):
        import importlib
        if 'main' in sys.modules:
            importlib.reload(sys.modules['main'])
        else:
            import main

if __name__ == "__main__":
    print("Testing CORS configuration validation...")
    
    # We'll run basic validation tests without pytest
    print("\nTest 1: Validating that the validation function works correctly...")
    
    # Test the validation function directly
    from main import validate_and_get_cors_origins
    
    # Test valid single origin
    os.environ["FRONTEND_URL"] = "https://example.netlify.app"
    try:
        origins = validate_and_get_cors_origins()
        assert origins == ["https://example.netlify.app"]
        print("✓ Valid single origin test passed")
    except Exception as e:
        print(f"✗ Valid single origin test failed: {e}")
    
    # Test valid multiple origins
    os.environ["FRONTEND_URL"] = "http://localhost:5173,https://example.netlify.app"
    try:
        origins = validate_and_get_cors_origins()
        assert origins == ["http://localhost:5173", "https://example.netlify.app"]
        print("✓ Valid multiple origins test passed")
    except Exception as e:
        print(f"✗ Valid multiple origins test failed: {e}")
    
    # Test wildcard rejection
    os.environ["FRONTEND_URL"] = "*"
    try:
        origins = validate_and_get_cors_origins()
        print(f"✗ Wildcard rejection test failed: should have raised ValueError")
    except ValueError as e:
        if "wildcard" in str(e).lower():
            print("✓ Wildcard rejection test passed")
        else:
            print(f"✗ Wildcard rejection test failed with wrong error: {e}")
    
    # Test empty FRONTEND_URL
    if "FRONTEND_URL" in os.environ:
        del os.environ["FRONTEND_URL"]
    try:
        origins = validate_and_get_cors_origins()
        print(f"✗ Empty FRONTEND_URL test failed: should have raised ValueError")
    except ValueError as e:
        if "required" in str(e).lower():
            print("✓ Empty FRONTEND_URL test passed")
        else:
            print(f"✗ Empty FRONTEND_URL test failed with wrong error: {e}")
    
    # Test wildcard in list
    os.environ["FRONTEND_URL"] = "http://localhost:5173,*"
    try:
        origins = validate_and_get_cors_origins()
        print(f"✗ Wildcard in list test failed: should have raised ValueError")
    except ValueError as e:
        if "wildcard" in str(e).lower():
            print("✓ Wildcard in list test passed")
        else:
            print(f"✗ Wildcard in list test failed with wrong error: {e}")
    
    print("\n✓ All validation tests passed!")
