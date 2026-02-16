# 🏷️ Issue Labels Guide
## VishwaGuru Label System

This document describes the labeling system used in VishwaGuru for organizing issues and pull requests.

---

## 📋 Label Categories

### **Type Labels** (What kind of change?)

| Label | Color | Description | Use When |
|-------|-------|-------------|----------|
| `bug` | 🔴 Red | Something isn't working | Reporting broken functionality |
| `enhancement` | 🟢 Green | New feature or request | Suggesting improvements |
| `documentation` | 🔵 Blue | Documentation improvements | Adding/updating docs |
| `security` | 🟣 Purple | Security-related issues | Reporting vulnerabilities |
| `performance` | 🟡 Yellow | Performance improvements | Optimizing speed/efficiency |
| `refactor` | 🟠 Orange | Code refactoring | Restructuring without changing behavior |
|`chore` | ⚪ Gray | Maintenance tasks | Dependencies, configs, etc. |

### **Priority Labels** (How urgent?)

| Label | Description |
|-------|-------------|
| `priority: critical` | Blocking issue, needs immediate attention |
| `priority: high` | Important, should be addressed soon |
| `priority: medium` | Normal priority |
| `priority: low` | Nice to have, not urgent |

### **Status Labels** (What's the state?)

| Label | Description |
|-------|-------------|
| `status: needs-triage` | Needs review and prioritization |
| `status: blocked` | Blocked by dependencies or other issues |
| `status: in-progress` | Currently being worked on |
| `status: needs-review` | Waiting for code review |
| `status: ready-to-merge` | Approved and ready to merge |

### **Difficulty Labels** (Good for contributors!)

| Label | Description |
|-------|-------------|
| `good first issue` | Easy for newcomers |
| `help wanted` | Community help needed |
| `advanced` | Requires significant experience |

### **Component Labels** (Which part?)

| Label | Description |
|-------|-------------|
| `frontend` | React/Vite UI changes |
| `backend` | FastAPI server changes |
| `database` | Database schema/queries |
| `telegram-bot` | Telegram bot integration |
| `ai/ml` | AI/ML models and prompts |
| `deployment` | CI/CD, hosting, infrastructure |

---

## 🎯 How to Use Labels

### **For Issue Reporters:**
1. Add a **type label** (bug, enhancement, etc.)
2. Add **component labels** if you know which part is affected
3. Leave priority/status labels for maintainers

### **For Maintainers:**
1. Add **type** and **component** labels
2. Set **priority** based on impact
3. Add **difficulty** if suitable for new contributors
4. Update **status** as issue progresses

### **For Pull Request Authors:**
1. Add **type** label matching your changes
2. Add affected **component** labels
3. Reference related issues

---

## 📝 Examples

### **Example 1: Bug Report**
```
Title: Telegram bot fails to send images
Labels: bug, telegram-bot, priority: high
```

### **Example 2: Feature Request**
```
Title: Add dark mode to frontend
Labels: enhancement, frontend, good first issue
```

### **Example 3: Documentation**
```
Title: Update API documentation for /issues endpoint
Labels: documentation, backend, priority: medium
```

### **Example 4: Security Issue**
```
Title: API keys exposed in logs
Labels: security, backend, priority: critical
```

---

## 🔄 Label Lifecycle

```
1. Issue Created
   ↓
2. needs-triage (maintainer reviews)
   ↓
3. priority set, difficulty assigned (if applicable)
   ↓
4. in-progress (someone starts working)
   ↓
5. needs-review (PR created)
   ↓
6. ready-to-merge (approved)
   ↓
7. Merged & Closed
```

---

## 🎨 Label Colors

We use consistent colors for easy visual scanning:
- 🔴 **Red**: Problems (bugs, critical)
- 🟢 **Green**: Additions (enhancements, features)
- 🔵 **Blue**: Information (documentation)
- 🟣 **Purple**: Security
- 🟡 **Yellow**: Performance
- 🟠 **Orange**: Code quality (refactor)
- ⚪ **Gray**: Maintenance (chore)

---

## 💡 Tips for Contributors

- **Look for `good first issue`** if you're new
- **`help wanted`** means maintainers welcome contributions
- **Priority labels** help you focus on important work
- **Multiple labels** are okay (e.g., `bug` + `frontend` + `priority: high`)

---

## 🤝 Need Help?

If you're unsure which labels to use:
1. Start with just the type (bug/enhancement/docs)
2. Maintainers will add other labels
3. Ask in the issue comments if confused

---

**Happy Contributing! 🚀**
