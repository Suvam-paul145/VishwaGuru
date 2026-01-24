import sys
import os
import asyncio
from fastapi.testclient import TestClient
# Ensure backend modules are found
sys.path.append(os.getcwd())
from backend.main import app

def test_recent_issues_optimization():
    print("Testing /api/issues/recent optimization...")

    # Mock environment variables if needed
    os.environ["FRONTEND_URL"] = "http://localhost:5173"

    with TestClient(app) as client:
        # Create a dummy issue first to ensure we have data
        # We don't upload an image to keep it simple
        print("Creating a test issue...")
        create_response = client.post(
            "/api/issues",
            data={
                "description": "Verification Issue for Optimization",
                "category": "Road",
                "user_email": "verify@example.com"
            }
        )
        if create_response.status_code != 201:
             print(f"Failed to create issue: {create_response.text}")
             # Don't exit, maybe there are existing issues

        print("Fetching recent issues...")
        response = client.get("/api/issues/recent")
        if response.status_code != 200:
            print(f"Failed to fetch recent issues: {response.text}")
            sys.exit(1)

        issues = response.json()

        if not issues:
            print("Warning: No issues found, cannot verify structure fully.")
            return

        first_issue = issues[0]
        print(f"Issue keys: {list(first_issue.keys())}")

        if "action_plan" in first_issue:
            print("FAILED: 'action_plan' should NOT be in the response.")
            sys.exit(1)
        else:
            print("SUCCESS: 'action_plan' correctly excluded from response.")

if __name__ == "__main__":
    test_recent_issues_optimization()
