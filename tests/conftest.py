import os
import pytest

# Set environment variable for security check in main.py
os.environ["FRONTEND_URL"] = "http://localhost:5173"

# Configure pytest-asyncio
# This allows using @pytest.mark.asyncio without strict mode warnings if configured via ini,
# but since we don't have pytest.ini here, we just rely on the plugin being installed.
# We can also set the default loop scope if needed.
