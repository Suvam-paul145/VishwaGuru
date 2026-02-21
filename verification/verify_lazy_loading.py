import sys
import os
from unittest.mock import MagicMock

# Adjust path to include repo root
repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

# Mock heavy dependencies
sys.modules['ultralytics'] = MagicMock()
sys.modules['ultralyticsplus'] = MagicMock()
sys.modules['torch'] = MagicMock()
# Mock torch.Tensor as a class to satisfy issubclass checks if any
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
sys.modules['sklearn'] = MagicMock() # Often imported as sklearn
sys.modules['numpy'] = MagicMock() # Often imported as numpy

# Now import verify_lazy_loading
def verify_lazy_loading():
    print("Checking initial state...")

    # We must import backend.ai_interfaces before calling get_ai_services
    import backend.ai_interfaces

    # Verify _ai_services is initially None
    if backend.ai_interfaces._ai_services is not None:
        print("FAIL: AI services were already initialized! This implies eager loading somewhere.")
        sys.exit(1)
    else:
        print("PASS: AI services are initially None.")

    print("Calling get_ai_services() to trigger lazy load...")
    try:
        container = backend.ai_interfaces.get_ai_services()
    except Exception as e:
        print(f"FAIL: get_ai_services() raised an exception: {e}")
        # Print full traceback
        import traceback
        traceback.print_exc()
        sys.exit(1)

    if container is None:
        print("FAIL: get_ai_services() returned None!")
        sys.exit(1)

    if backend.ai_interfaces._ai_services is None:
         print("FAIL: Global variable _ai_services was not updated after call!")
         sys.exit(1)

    print("PASS: AI services lazy loaded successfully.")

    # Check if services are operational
    if not hasattr(container, 'action_plan_service'):
         print("FAIL: Service container missing action_plan_service")
         sys.exit(1)

    print("All checks passed.")

if __name__ == "__main__":
    verify_lazy_loading()
