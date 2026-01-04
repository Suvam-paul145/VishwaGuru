# ECWoC26 Issues for VishwaGuru

This document contains a curated list of issues for the Elite Coders Winter of Code 2026 (ECWoC26) event. These issues are categorized by difficulty and type to help contributors find tasks that match their skill level and interests.

## 🎯 How to Use This Document

1. Repository maintainers can create GitHub issues from the templates below
2. Each issue includes: Title, Description, Labels, Difficulty, Expected Outcome, and Technical Requirements
3. Copy the issue template and create it on GitHub with the `ECWoC26` label

---

## 🟢 Good First Issues (Beginner-Friendly)

### Issue 1: Add Contributing Guidelines
**Labels:** `documentation`, `good first issue`, `ECWoC26`  
**Difficulty:** Easy  
**Estimated Time:** 2-3 hours

**Description:**  
Create a comprehensive CONTRIBUTING.md file to help new contributors understand how to contribute to VishwaGuru. This should include setup instructions, coding standards, and the pull request process.

**Expected Outcome:**
- A well-structured CONTRIBUTING.md file in the repository root
- Clear sections on: Environment Setup, Code Style, Commit Messages, PR Process
- Links to relevant documentation and resources

**Technical Requirements:**
- Markdown formatting
- Understanding of Git workflow
- Familiarity with open source best practices

---

### Issue 2: Improve README with Badges and Better Formatting
**Labels:** `documentation`, `good first issue`, `ECWoC26`  
**Difficulty:** Easy  
**Estimated Time:** 1-2 hours

**Description:**  
Enhance the README.md file by adding status badges (build status, license, contributors), improving the structure, and adding a table of contents for better navigation.

**Expected Outcome:**
- Add shields.io badges for: License, GitHub stars, Issues, PRs
- Add a table of contents
- Improve visual hierarchy with better headings and sections
- Add screenshots or GIFs demonstrating the application

**Technical Requirements:**
- Markdown
- Basic understanding of CI/CD badges
- Design sense for documentation

---

### Issue 3: Create Issue Templates
**Labels:** `documentation`, `good first issue`, `ECWoC26`  
**Difficulty:** Easy  
**Estimated Time:** 2-3 hours

**Description:**  
Create GitHub issue templates for bug reports, feature requests, and general questions to standardize issue reporting and improve project management.

**Expected Outcome:**
- Create `.github/ISSUE_TEMPLATE/` directory
- Bug report template with sections for: Description, Steps to Reproduce, Expected Behavior, Actual Behavior, Screenshots, Environment
- Feature request template with sections for: Problem Statement, Proposed Solution, Alternatives Considered
- General question template

**Technical Requirements:**
- Markdown
- Understanding of GitHub issue templates
- YAML front matter

---

### Issue 4: Add Pull Request Template
**Labels:** `documentation`, `good first issue`, `ECWoC26`  
**Difficulty:** Easy  
**Estimated Time:** 1-2 hours

**Description:**  
Create a pull request template to ensure all PRs contain necessary information for review, including description of changes, related issues, type of change, and testing checklist.

**Expected Outcome:**
- Create `.github/PULL_REQUEST_TEMPLATE.md`
- Include sections for: Description, Related Issues, Type of Change, Checklist (tests, documentation, etc.)

**Technical Requirements:**
- Markdown
- Understanding of PR best practices

---

### Issue 5: Add Code of Conduct
**Labels:** `documentation`, `good first issue`, `ECWoC26`  
**Difficulty:** Easy  
**Estimated Time:** 1 hour

**Description:**  
Add a Code of Conduct to establish community standards and create a welcoming environment for all contributors. Use the Contributor Covenant as a base.

**Expected Outcome:**
- CODE_OF_CONDUCT.md file following the Contributor Covenant v2.1
- Clear sections on expected behavior, unacceptable behavior, and enforcement
- Contact information for reporting violations

**Technical Requirements:**
- Markdown
- Understanding of community management

**Reference:** This partially addresses the existing issue #57

---

## 🟡 Intermediate Issues

### Issue 6: Replace Print Statements with Structured Logging
**Labels:** `enhancement`, `code quality`, `ECWoC26`  
**Difficulty:** Medium  
**Estimated Time:** 4-6 hours

**Description:**  
Replace all `print()` statements throughout the backend codebase with proper logging using Python's `logging` module. This will improve production monitoring and debugging capabilities.

**Files to Update:**
- `backend/main.py` (lines 54, 66, 387, and others)
- `backend/bot.py`
- Other backend modules with print statements

**Expected Outcome:**
- All print() calls replaced with appropriate logging levels (info, warning, error, debug)
- Consistent log format across the application
- Log configuration that works for both development and production

**Technical Requirements:**
- Python logging module
- Understanding of log levels and when to use each
- Experience with FastAPI

**Reference:** This addresses the existing issue #67

---

### Issue 7: Add Input Validation for File Uploads
**Labels:** `security`, `enhancement`, `ECWoC26`  
**Difficulty:** Medium  
**Estimated Time:** 6-8 hours

**Description:**  
Implement comprehensive input validation for all file upload endpoints to prevent security vulnerabilities and improve reliability.

**Validation Requirements:**
- File type validation (check MIME type using `python-magic`)
- File size limits (max 10MB for images)
- Image format validation (PNG, JPG, JPEG only)
- File content inspection for malicious content

**Files to Update:**
- `backend/main.py` (upload endpoints like `/api/issues`, `/api/detect-*`)

**Expected Outcome:**
- Secure file upload handling with proper validation
- Clear error messages for invalid uploads
- Updated requirements.txt with any new dependencies
- Unit tests for validation logic

**Technical Requirements:**
- Python
- FastAPI
- python-magic library
- Security best practices

**Reference:** This addresses the existing issue #65

---

### Issue 8: Improve Error Handling in AI Service Calls
**Labels:** `enhancement`, `reliability`, `ECWoC26`  
**Difficulty:** Medium  
**Estimated Time:** 6-8 hours

**Description:**  
Implement robust error handling for AI service API calls with retry logic, exponential backoff, and graceful degradation when services are unavailable.

**Expected Outcome:**
- Retry logic with exponential backoff for transient failures
- Circuit breaker pattern to prevent cascading failures
- Fallback responses when AI services are unavailable
- Proper error logging and monitoring
- Unit tests for error scenarios

**Files to Update:**
- `backend/ai_service.py`
- `backend/hf_service.py`
- `backend/gemini_summary.py`

**Technical Requirements:**
- Python
- Error handling patterns (retry, circuit breaker)
- Understanding of rate limits and API failures
- pytest for testing

**Reference:** This addresses the existing issue #70

---

### Issue 9: Add Frontend Unit Tests with React Testing Library
**Labels:** `testing`, `frontend`, `ECWoC26`  
**Difficulty:** Medium  
**Estimated Time:** 8-10 hours

**Description:**  
Set up a testing framework for the React frontend and add comprehensive unit tests for key components.

**Expected Outcome:**
- Install and configure React Testing Library and Jest/Vitest
- Add tests for at least 5 key components
- Achieve >70% code coverage for tested components
- Add test scripts to package.json
- Document testing approach in README

**Technical Requirements:**
- React
- React Testing Library
- Vitest or Jest
- JavaScript/TypeScript testing patterns

---

### Issue 10: Add Dark Mode Toggle with Persistence
**Labels:** `enhancement`, `frontend`, `UI/UX`, `ECWoC26`  
**Difficulty:** Medium  
**Estimated Time:** 4-6 hours

**Description:**  
Implement a dark mode toggle in the frontend that persists user preference across sessions using localStorage.

**Expected Outcome:**
- Dark mode toggle button in the header/navbar
- Smooth transition between light and dark modes
- User preference persisted in localStorage
- All components properly styled for both modes
- WCAG contrast compliance for both themes

**Technical Requirements:**
- React
- Tailwind CSS (dark mode utilities)
- localStorage API
- CSS/design skills

**Reference:** This is part of the issue #60

---

### Issue 11: Add API Response Caching
**Labels:** `performance`, `backend`, `ECWoC26`  
**Difficulty:** Medium  
**Estimated Time:** 6-8 hours

**Description:**  
Implement caching for frequently accessed API endpoints to improve performance and reduce database load.

**Expected Outcome:**
- Redis or in-memory caching for read-heavy endpoints
- Cache invalidation strategy
- Configurable TTL for different endpoint types
- Performance benchmarks showing improvement
- Documentation on cache configuration

**Technical Requirements:**
- Python
- FastAPI
- Redis or Python caching libraries (functools.lru_cache, async-lru)
- Understanding of cache invalidation patterns

---

### Issue 12: Create API Documentation with Swagger/OpenAPI
**Labels:** `documentation`, `backend`, `ECWoC26`  
**Difficulty:** Medium  
**Estimated Time:** 4-6 hours

**Description:**  
Enhance the existing FastAPI auto-generated documentation with better descriptions, examples, and response schemas.

**Expected Outcome:**
- Comprehensive docstrings for all API endpoints
- Request/response examples for each endpoint
- Proper schema descriptions with field explanations
- Tags and grouping for better organization
- Published Swagger UI accessible at `/docs`

**Technical Requirements:**
- FastAPI
- OpenAPI/Swagger specifications
- Python docstrings
- API documentation best practices

---

## 🔴 Advanced Issues

### Issue 13: Implement Rate Limiting for API Endpoints
**Labels:** `security`, `backend`, `ECWoC26`  
**Difficulty:** Hard  
**Estimated Time:** 8-10 hours

**Description:**  
Add rate limiting to protect the API from abuse and ensure fair resource allocation. Implement different rate limits for different endpoint types.

**Expected Outcome:**
- Rate limiting middleware using `slowapi` or similar
- Different limits for: public endpoints (10/min), authenticated endpoints (100/min), ML inference endpoints (5/min)
- Proper HTTP 429 responses with Retry-After headers
- Redis-based rate limit storage for distributed deployment
- Configuration via environment variables
- Unit and integration tests

**Technical Requirements:**
- FastAPI middleware
- Redis
- Rate limiting algorithms (token bucket, sliding window)
- HTTP standards

---

### Issue 14: Add Comprehensive Backend Test Suite
**Labels:** `testing`, `backend`, `ECWoC26`  
**Difficulty:** Hard  
**Estimated Time:** 12-16 hours

**Description:**  
Create a comprehensive test suite for the backend covering unit tests, integration tests, and API endpoint tests.

**Expected Outcome:**
- Unit tests for all service modules (AI service, database operations, etc.)
- Integration tests for API endpoints
- Test fixtures for database and external services
- >80% code coverage for backend
- CI/CD integration with GitHub Actions
- Documentation on running tests

**Files to Test:**
- All modules in `backend/` directory
- Expand existing tests in `tests/` directory

**Technical Requirements:**
- Python
- pytest
- pytest-asyncio
- httpx (for API testing)
- Coverage.py
- Mocking and fixtures

---

### Issue 15: Create Interactive Dashboard with Analytics
**Labels:** `feature`, `frontend`, `ECWoC26`  
**Difficulty:** Hard  
**Estimated Time:** 16-20 hours

**Description:**  
Build an interactive analytics dashboard showing issue statistics, trends, and geographic distribution of reported problems.

**Features:**
- Issue count by type and status
- Time-series graphs showing reporting trends
- Geographic heatmap of issue locations
- Top issue categories
- Response time metrics

**Expected Outcome:**
- New `/dashboard` route in frontend
- Interactive charts using Chart.js or Recharts
- Real-time data updates
- Responsive design
- Export functionality for reports

**Technical Requirements:**
- React
- Chart.js or Recharts
- Data visualization best practices
- API integration
- Responsive design

---

### Issue 16: Implement User Authentication System
**Labels:** `feature`, `backend`, `frontend`, `security`, `ECWoC26`  
**Difficulty:** Hard  
**Estimated Time:** 20-24 hours

**Description:**  
Add a complete user authentication system with registration, login, and role-based access control.

**Expected Outcome:**
- User registration and login endpoints
- JWT-based authentication
- Password hashing with bcrypt
- Role-based permissions (admin, user)
- Protected routes in frontend
- Session management
- Password reset functionality
- Security best practices (rate limiting on auth endpoints, password strength requirements)

**Technical Requirements:**
- FastAPI security utilities
- JWT (PyJWT)
- bcrypt
- React Context API or state management
- RESTful API design
- Security best practices

---

### Issue 17: Add Multi-Language Support (i18n)
**Labels:** `feature`, `frontend`, `ECWoC26`  
**Difficulty:** Hard  
**Estimated Time:** 12-16 hours

**Description:**  
Implement internationalization to support multiple Indian languages, starting with Hindi, English, and Marathi.

**Expected Outcome:**
- i18n setup using react-i18next
- Translation files for Hindi, English, Marathi
- Language switcher component
- RTL support if needed
- Persistent language preference
- All user-facing text externalized

**Technical Requirements:**
- React
- react-i18next or similar i18n library
- Understanding of internationalization best practices
- Knowledge of Indian languages (or ability to work with translators)

---

### Issue 18: Create Mobile App with React Native
**Labels:** `feature`, `mobile`, `ECWoC26`  
**Difficulty:** Hard  
**Estimated Time:** 40+ hours

**Description:**  
Develop a mobile application for VishwaGuru using React Native, sharing code with the web frontend where possible.

**Expected Outcome:**
- React Native application for iOS and Android
- Core features: Issue reporting, photo upload, location services
- Push notifications for issue updates
- Offline support with local storage
- Native camera integration
- Published to Google Play Store (optional: App Store)

**Technical Requirements:**
- React Native
- Expo or vanilla React Native
- Native modules for camera and location
- Mobile UI/UX best practices
- App store deployment knowledge

---

### Issue 19: Implement CI/CD Pipeline
**Labels:** `devops`, `ECWoC26`  
**Difficulty:** Hard  
**Estimated Time:** 8-12 hours

**Description:**  
Set up a complete CI/CD pipeline using GitHub Actions for automated testing, linting, and deployment.

**Expected Outcome:**
- GitHub Actions workflows for:
  - Running tests on PR
  - Code quality checks (linting, formatting)
  - Security scanning
  - Automated deployment to staging/production
- Branch protection rules
- Status checks required for merging
- Documentation on CI/CD process

**Technical Requirements:**
- GitHub Actions
- Docker (optional)
- Understanding of CI/CD concepts
- YAML configuration

---

### Issue 20: Add WebSocket Support for Real-Time Updates
**Labels:** `feature`, `backend`, `frontend`, `ECWoC26`  
**Difficulty:** Hard  
**Estimated Time:** 12-16 hours

**Description:**  
Implement WebSocket support to enable real-time notifications and live updates when new issues are reported or existing issues are updated.

**Expected Outcome:**
- WebSocket endpoint in FastAPI
- Real-time issue updates pushed to connected clients
- Frontend components that subscribe to WebSocket updates
- Connection management and reconnection logic
- Scalable architecture (consider Redis for pub/sub)

**Technical Requirements:**
- FastAPI WebSockets
- React WebSocket integration
- Redis (for multi-instance support)
- Real-time communication patterns

---

## 🔵 Feature Enhancements

### Issue 21: Add Export Functionality for Issue Reports
**Labels:** `feature`, `enhancement`, `ECWoC26`  
**Difficulty:** Medium  
**Estimated Time:** 6-8 hours

**Description:**  
Allow users to export issue data in multiple formats (CSV, PDF, JSON) for reporting and analysis purposes.

**Expected Outcome:**
- Export buttons in the UI
- CSV export for spreadsheet analysis
- PDF export with formatted report
- JSON export for developers
- Filtering options before export
- Backend API endpoints to generate exports

**Technical Requirements:**
- Python (reportlab for PDF, csv module)
- FastAPI
- React
- File download handling

---

### Issue 22: Implement Issue Search and Filtering
**Labels:** `feature`, `frontend`, `ECWoC26`  
**Difficulty:** Medium  
**Estimated Time:** 8-10 hours

**Description:**  
Add comprehensive search and filtering capabilities to help users find relevant issues quickly.

**Expected Outcome:**
- Search bar with autocomplete
- Filters: by type, status, location, date range
- Sort options: newest, oldest, most reported
- URL parameters for shareable filtered views
- Performance optimization for large datasets

**Technical Requirements:**
- React
- API integration
- URL state management
- UI/UX for search interfaces

---

### Issue 23: Add Email Notifications
**Labels:** `feature`, `backend`, `ECWoC26`  
**Difficulty:** Medium  
**Estimated Time:** 8-10 hours

**Description:**  
Implement email notifications for issue updates, acknowledgments, and resolution notifications.

**Expected Outcome:**
- Email service integration (SendGrid, AWS SES, or SMTP)
- Email templates for: Issue received, Status update, Issue resolved
- User preferences for email notifications
- Queue system for sending emails asynchronously
- Unsubscribe functionality

**Technical Requirements:**
- Python email libraries
- Email service provider (SendGrid, etc.)
- HTML email templates
- Celery or background task queue (optional)

---

### Issue 24: Create Impact Map Dashboard
**Labels:** `feature`, `frontend`, `visualization`, `ECWoC26`  
**Difficulty:** Hard  
**Estimated Time:** 16-20 hours

**Description:**  
Build an interactive map showing civic issues reported across India with heatmap visualization and pin markers for individual issues.

**Expected Outcome:**
- Interactive map using React-Leaflet or Mapbox
- Issue markers on map with popup details
- Heatmap layer showing issue density
- Clustering for performance with many markers
- Filters to show/hide different issue types
- Mobile-responsive map interface

**Technical Requirements:**
- React-Leaflet or Mapbox
- Geospatial data handling
- Map performance optimization
- API integration for issue data

**Reference:** This addresses the existing issue #59

---

### Issue 25: Add Progressive Web App (PWA) Support
**Labels:** `feature`, `frontend`, `ECWoC26`  
**Difficulty:** Medium  
**Estimated Time:** 6-8 hours

**Description:**  
Convert the web application to a Progressive Web App for offline support and mobile installation.

**Expected Outcome:**
- Service worker for caching
- Web app manifest
- Offline fallback page
- Install prompts for mobile users
- Background sync for offline issue reporting
- Push notification capability

**Technical Requirements:**
- Service Workers
- Web App Manifest
- PWA best practices
- Background Sync API
- Push API

---

## 🟣 Machine Learning Enhancements

### Issue 26: Develop Local ML Model for Image Classification
**Labels:** `machine learning`, `feature`, `ECWoC26`  
**Difficulty:** Hard  
**Estimated Time:** 20-30 hours

**Description:**  
Create a local machine learning model for civic issue classification (pothole, garbage, flooding, etc.) to reduce dependency on external APIs.

**Expected Outcome:**
- Trained model using TensorFlow/PyTorch
- Model serves predictions locally
- >85% accuracy on test dataset
- Model versioning and update strategy
- Documentation on model architecture and training
- Reduced inference latency compared to external APIs

**Technical Requirements:**
- Python
- TensorFlow or PyTorch
- Computer Vision knowledge
- Model optimization
- ML deployment patterns

**Reference:** This addresses the existing issue #76

---

### Issue 27: Improve ML Model Accuracy with Data Augmentation
**Labels:** `machine learning`, `enhancement`, `ECWoC26`  
**Difficulty:** Hard  
**Estimated Time:** 12-16 hours

**Description:**  
Enhance the existing detection models by implementing data augmentation techniques and fine-tuning strategies.

**Expected Outcome:**
- Data augmentation pipeline
- Improved model accuracy (>5% improvement)
- A/B testing framework for model comparison
- Documentation on training process
- Model performance benchmarks

**Technical Requirements:**
- Python
- Computer Vision libraries (OpenCV, Pillow)
- ML frameworks (TensorFlow/PyTorch)
- Understanding of data augmentation techniques

---

### Issue 28: Add ML Model Monitoring and Drift Detection
**Labels:** `machine learning`, `monitoring`, `ECWoC26`  
**Difficulty:** Hard  
**Estimated Time:** 12-16 hours

**Description:**  
Implement monitoring for ML models to track performance metrics and detect model drift over time.

**Expected Outcome:**
- Logging of prediction confidence scores
- Dashboard showing model performance over time
- Alerts for prediction accuracy drops
- Data drift detection
- Retraining triggers based on performance

**Technical Requirements:**
- Python
- ML monitoring tools (MLflow, Weights & Biases)
- Time-series analysis
- Statistical methods for drift detection

---

## 📊 Summary

- **Total Issues:** 28
- **Easy (Good First Issues):** 5
- **Medium:** 11
- **Hard:** 12

These issues cover a wide range of skills and technologies:
- **Documentation:** 5 issues
- **Frontend:** 8 issues
- **Backend:** 10 issues
- **Testing:** 3 issues
- **Security:** 4 issues
- **Machine Learning:** 3 issues
- **DevOps:** 1 issue
- **Mobile:** 1 issue

---

## 🚀 Getting Started

For maintainers creating these issues:

1. Copy the issue template
2. Create a new GitHub issue
3. Add the `ECWoC26` label
4. Add other relevant labels (difficulty, type)
5. Link related existing issues if applicable
6. Consider adding a "help wanted" label for community contributions

For contributors:

1. Browse the issues labeled with `ECWoC26`
2. Comment on the issue you'd like to work on
3. Wait for assignment from maintainers
4. Follow the CONTRIBUTING.md guidelines (once created)
5. Submit a PR referencing the issue number

---

## 📝 Notes

- Some issues reference existing open issues in the repository
- Issues are designed to be relatively independent to avoid merge conflicts
- Estimated times are approximate and may vary based on contributor experience
- Issues can be split into smaller sub-tasks if needed
- New issues can be added to this list as the project evolves

---

**Happy Coding! 🎉**  
ECWoC26 - Elite Coders Winter of Code 2026
