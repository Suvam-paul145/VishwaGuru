# VishwaGuru Tests

This directory contains tests for the VishwaGuru backend API.

## Running Tests

Before running any tests that import the FastAPI app, you must set the `FRONTEND_URL` environment variable:

```bash
# For local testing
export FRONTEND_URL=http://localhost:5173

# Or set it inline
FRONTEND_URL=http://localhost:5173 python tests/test_startup.py
```

### Why is FRONTEND_URL Required?

As of the security fix for CORS configuration, the app requires `FRONTEND_URL` to be explicitly set to prevent wildcard origin vulnerabilities. The app will not start without this environment variable.

## Test Files

- `test_cors_configuration.py` - Tests CORS validation logic
- `test_startup.py` - Tests app startup and health endpoints
- `test_issue_creation.py` - Tests issue creation functionality
- `test_mh_endpoint.py` - Tests Maharashtra-specific endpoints
- `test_infrastructure_endpoint.py` - Tests infrastructure detection endpoints
- `test_vandalism.py` - Tests vandalism detection

## Security Note

The CORS configuration now enforces strict origin validation:
- Wildcard (`*`) origins are rejected
- `FRONTEND_URL` must be explicitly set
- Multiple origins can be specified with comma separation: `http://localhost:5173,https://your-app.netlify.app`
