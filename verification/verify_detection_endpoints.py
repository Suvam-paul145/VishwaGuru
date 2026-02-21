import sys
import os
import inspect
from unittest.mock import MagicMock

# Adjust path to include repo root
repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

# Mock heavy dependencies
sys.modules['ultralytics'] = MagicMock()
sys.modules['ultralyticsplus'] = MagicMock()
sys.modules['torch'] = MagicMock()
sys.modules['torch'].Tensor = type('Tensor', (), {})
sys.modules['transformers'] = MagicMock()
sys.modules['google'] = MagicMock()
sys.modules['google.generativeai'] = MagicMock()
sys.modules['telegram'] = MagicMock()
sys.modules['telegram.ext'] = MagicMock()
sys.modules['telegram.error'] = MagicMock()
sys.modules['pywebpush'] = MagicMock()
sys.modules['firebase_admin'] = MagicMock()
sys.modules['scikit-learn'] = MagicMock()
sys.modules['sklearn'] = MagicMock()
sys.modules['numpy'] = MagicMock()

def verify_detection_endpoints():
    print("Importing backend.routers.detection...")
    try:
        import backend.routers.detection as detection
    except ImportError as e:
        print(f"FAIL: ImportError: {e}")
        sys.exit(1)

    # Verify cached wrappers exist
    print("Checking for cached wrappers...")
    if not hasattr(detection, '_cached_detect_traffic_sign'):
        print("FAIL: _cached_detect_traffic_sign missing")
        sys.exit(1)
    if not hasattr(detection, '_cached_detect_abandoned_vehicle'):
        print("FAIL: _cached_detect_abandoned_vehicle missing")
        sys.exit(1)

    print("PASS: Cached wrappers found.")

    # Inspect the endpoint functions source code to ensure they call process_uploaded_image
    print("Inspecting endpoint source code...")

    try:
        traffic_source = inspect.getsource(detection.detect_traffic_sign_endpoint)
        if 'process_uploaded_image' not in traffic_source:
            print("FAIL: detect_traffic_sign_endpoint does not seem to use process_uploaded_image")
            print("Source:\n", traffic_source)
            sys.exit(1)
        if '_cached_detect_traffic_sign' not in traffic_source:
            print("FAIL: detect_traffic_sign_endpoint does not seem to use the cached wrapper")
            sys.exit(1)

        abandoned_source = inspect.getsource(detection.detect_abandoned_vehicle_endpoint)
        if 'process_uploaded_image' not in abandoned_source:
            print("FAIL: detect_abandoned_vehicle_endpoint does not seem to use process_uploaded_image")
            sys.exit(1)
        if '_cached_detect_abandoned_vehicle' not in abandoned_source:
            print("FAIL: detect_abandoned_vehicle_endpoint does not seem to use the cached wrapper")
            sys.exit(1)

    except OSError:
        print("WARN: Could not retrieve source code (maybe compiled?). Skipping source check.")

    print("PASS: Endpoints seem to use optimization and caching.")
    print("All checks passed.")

if __name__ == "__main__":
    verify_detection_endpoints()
