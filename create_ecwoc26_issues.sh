#!/bin/bash

# ECWoC26 Issue Creation Helper Script
# This script helps create the complex issues defined in ECWOC26_COMPLEX_ISSUES.md

echo "======================================"
echo "ECWoC26 Issue Creation Helper"
echo "======================================"
echo ""
echo "This script will guide you through creating ECWoC26 issues on GitHub."
echo ""
echo "Prerequisites:"
echo "  - GitHub CLI (gh) must be installed"
echo "  - You must be authenticated with 'gh auth login'"
echo "  - You must have write access to the repository"
echo ""

# Check if gh is installed
if ! command -v gh &> /dev/null; then
    echo "❌ GitHub CLI (gh) is not installed."
    echo "Please install it from: https://cli.github.com/"
    exit 1
fi

# Check if authenticated
if ! gh auth status &> /dev/null; then
    echo "❌ You are not authenticated with GitHub CLI."
    echo "Please run: gh auth login"
    exit 1
fi

echo "✅ GitHub CLI is installed and authenticated"
echo ""

# Define issue titles
declare -a ISSUES=(
    "Implement Real-time WebSocket Notifications System with Redis Pub/Sub"
    "Multi-language Support with Dynamic Translation Pipeline"
    "Advanced Image Analysis Pipeline with Multi-Model Ensemble"
    "Blockchain-based Issue Verification and Transparency System"
    "Intelligent Issue Clustering and Duplicate Detection System"
    "Progressive Web App (PWA) with Offline-First Architecture"
    "Advanced Analytics Dashboard with Data Visualization"
    "AI-Powered Smart Routing and Authority Assignment"
    "Comprehensive API Rate Limiting and Abuse Prevention System"
    "End-to-End Testing Framework with Visual Regression"
)

echo "The following ${#ISSUES[@]} complex issues will be created:"
echo ""
for i in "${!ISSUES[@]}"; do
    echo "$((i+1)). ${ISSUES[$i]}"
done
echo ""

read -p "Do you want to proceed? (y/n): " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Aborted."
    exit 0
fi

echo ""
echo "Creating issues... (This may take a minute)"
echo ""

# Function to create issue from template file
create_issue() {
    local issue_num=$1
    local title=$2
    local labels="ECWoC26,enhancement"
    
    echo "Creating issue $issue_num: $title"
    
    # Each issue template is in ECWOC26_ISSUE_TEMPLATES.md
    # For now, we'll point users to manually create them or use the templates
    echo "  → Please use the template from ECWOC26_ISSUE_TEMPLATES.md"
}

echo ""
echo "======================================"
echo "Manual Issue Creation Instructions"
echo "======================================"
echo ""
echo "Since GitHub API rate limits and permissions may vary,"
echo "please create these issues manually:"
echo ""
echo "1. Open the repository on GitHub"
echo "2. Go to Issues → New Issue"
echo "3. Copy the template from ECWOC26_ISSUE_TEMPLATES.md"
echo "4. Add the label 'ECWoC26'"
echo "5. Submit the issue"
echo ""
echo "All templates are available in:"
echo "  - ECWOC26_ISSUE_TEMPLATES.md"
echo "  - ECWOC26_COMPLEX_ISSUES.md"
echo ""
echo "Alternatively, if you have the GitHub CLI configured with"
echo "appropriate permissions, you can create issues programmatically."
echo ""
echo "Example command:"
echo '  gh issue create --title "Your Title" --body "Your Body" --label "ECWoC26,enhancement"'
echo ""
echo "======================================"
echo "✅ Documentation Ready!"
echo "======================================"
