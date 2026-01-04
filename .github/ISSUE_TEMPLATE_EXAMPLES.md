# Issue Template Examples for ECWoC26

This directory would contain issue templates for GitHub. Since we can't directly create GitHub issues, here are the templates that maintainers can use.

## Instructions

1. Go to the repository settings
2. Navigate to "Issues" section
3. Click "Set up templates"
4. Or manually create files in `.github/ISSUE_TEMPLATE/` directory

## Quick Issue Templates

Below are ready-to-use templates for creating ECWoC26 issues:

---

### Template 1: Good First Issue

```markdown
---
name: 🟢 Good First Issue - [TITLE]
about: Beginner-friendly task for ECWoC26
title: '[ECWoC26] [TITLE]'
labels: 'ECWoC26, good first issue'
assignees: ''
---

## 📝 Description
[Brief description of what needs to be done]

## 🎯 Expected Outcome
- [ ] Item 1
- [ ] Item 2
- [ ] Item 3

## 🛠️ Technical Requirements
- Technology 1
- Technology 2

## 📚 Resources
- Link to relevant documentation
- Related issues: #XX

## ⏱️ Estimated Time
X-Y hours

## 💡 Tips for Contributors
[Any helpful hints or starting points]
```

---

### Template 2: Enhancement Issue

```markdown
---
name: ✨ Enhancement - [TITLE]
about: Feature enhancement for ECWoC26
title: '[ECWoC26] [TITLE]'
labels: 'ECWoC26, enhancement'
assignees: ''
---

## 🎯 Goal
[What we want to achieve]

## 📋 Current Behavior
[What currently happens]

## 🚀 Desired Behavior
[What should happen after the enhancement]

## 📁 Files to Modify
- `path/to/file1.py`
- `path/to/file2.js`

## ✅ Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Tests added
- [ ] Documentation updated

## 🛠️ Technical Stack
- Technology 1
- Technology 2

## ⏱️ Estimated Time
X-Y hours

## 🔗 Related Issues
Closes #XX
See also #YY
```

---

### Template 3: Security Issue

```markdown
---
name: 🔒 Security Enhancement - [TITLE]
about: Security improvement for ECWoC26
title: '[ECWoC26] [TITLE]'
labels: 'ECWoC26, security'
assignees: ''
---

## ⚠️ Security Concern
[Description of the security issue or improvement]

## 📍 Location
- File: `path/to/file.py`
- Lines: XX-YY

## 🎯 Proposed Solution
[How to fix or improve the security]

## ✅ Expected Outcome
- [ ] Security vulnerability fixed
- [ ] Tests added to prevent regression
- [ ] Documentation updated

## 🛠️ Technical Requirements
- Security best practice knowledge
- Technology/library knowledge

## 📚 References
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- Related security guidelines

## ⏱️ Estimated Time
X-Y hours

## 🔗 Related Issues
Addresses #XX
```

---

### Template 4: ML/AI Issue

```markdown
---
name: 🤖 ML/AI Enhancement - [TITLE]
about: Machine learning improvement for ECWoC26
title: '[ECWoC26] [TITLE]'
labels: 'ECWoC26, machine learning'
assignees: ''
---

## 🎯 Objective
[What ML improvement is needed]

## 📊 Current Model Performance
- Accuracy: XX%
- Inference time: XX ms

## 🚀 Target Performance
- Accuracy: YY%
- Inference time: YY ms

## 📋 Implementation Steps
1. Step 1
2. Step 2
3. Step 3

## 📁 Files Involved
- `backend/ml_model.py`
- `backend/inference.py`

## ✅ Acceptance Criteria
- [ ] Model accuracy improved
- [ ] Performance benchmarks included
- [ ] Model documentation updated
- [ ] Tests added

## 🛠️ Technical Stack
- TensorFlow/PyTorch
- Python
- Computer Vision libraries

## ⏱️ Estimated Time
XX-YY hours

## 📚 Resources
- Paper/article reference
- Related work
```

---

## General Guidelines for Issue Creation

1. **Title Format:** `[ECWoC26] Brief descriptive title`
2. **Always Include:**
   - Clear description
   - Expected outcome
   - Technical requirements
   - Estimated time
   - Labels: Always include `ECWoC26` + relevant type labels

3. **Labels to Use:**
   - `ECWoC26` (required for all)
   - `good first issue` (for beginners)
   - `enhancement`, `bug`, `documentation`
   - `frontend`, `backend`, `testing`
   - `security`, `performance`
   - `machine learning`, `devops`

4. **Difficulty Indicators:**
   - 🟢 Good First Issue (Easy)
   - 🟡 Intermediate
   - 🔴 Advanced

5. **Link Related Issues:**
   - Use "Closes #XX" if this issue will resolve another
   - Use "See also #YY" for related context
   - Use "Addresses #ZZ" for partial solutions

---

## Batch Issue Creation Script

For maintainers who want to create multiple issues at once, here's a sample script concept:

```bash
# Install GitHub CLI if not already installed
# gh auth login

# Example: Create an issue from the command line
gh issue create \
  --title "[ECWoC26] Add Contributing Guidelines" \
  --body "$(cat issue_descriptions/contributing.md)" \
  --label "ECWoC26,documentation,good first issue"
```

---

## Issue Assignment Process

1. Contributor comments "I'd like to work on this"
2. Maintainer reviews contributor's profile/experience
3. Maintainer assigns issue or asks clarifying questions
4. Contributor creates PR referencing the issue
5. Review and merge

---

## Tracking Progress

Create a GitHub Project board with columns:
- 📋 To Do
- 🏗️ In Progress
- 👀 In Review
- ✅ Done

Add all ECWoC26 issues to this board for easy tracking.

---

Remember: The goal is to provide clear, actionable, and well-scoped issues that help contributors learn and contribute effectively! 🚀
