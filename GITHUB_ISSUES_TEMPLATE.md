# GitHub Issues - Quick Copy Template

Use this file to quickly copy-paste issues into GitHub manually.

Go to: https://github.com/Kuba906/rag-docs-platform/issues/new

---

## Phase 1: Frontend & User Experience

### Issue #1: Setup React + TypeScript project with Vite

**Labels:** `frontend`, `ui`, `priority: medium`

**Description:**
Initialize frontend directory
Configure TypeScript, ESLint, Prettier
Setup Tailwind CSS
Configure API client (axios/fetch)

**Estimate:** 2h

---

### Issue #2: Create document upload component

**Labels:** `frontend`, `ui`, `priority: medium`

**Description:**
Drag & drop file upload
File type validation (PDF, DOCX, TXT)
Upload progress indicator
Success/error notifications

**Estimate:** 3h

---

### Issue #3: Build search interface

**Labels:** `frontend`, `ui`, `priority: medium`

**Description:**
Search input with auto-focus
Submit on Enter key
Loading state with spinner
Empty state message

**Estimate:** 2h

---

### Issue #4: Create answer display component

**Labels:** `frontend`, `ui`, `priority: medium`

**Description:**
Formatted answer text (markdown support)
Copy to clipboard button
Timestamp
Confidence score badge (if available)

**Estimate:** 3h

---

### Issue #5: Build sources/citations list

**Labels:** `frontend`, `ui`, `priority: medium`

**Description:**
Source cards with snippet preview
Click to expand full text
Link to original document
Relevance score indicator

**Estimate:** 3h

---

### Issue #6: Add document library sidebar

**Labels:** `frontend`, `ui`, `priority: medium`

**Description:**
List all uploaded documents
Show metadata (filename, size, chunks)
Delete document button with confirmation
Filter/search documents

**Estimate:** 4h

---

### Issue #7: Create metrics dashboard page

**Labels:** `frontend`, `ui`, `monitoring`, `priority: medium`

**Description:**
Total queries counter
Average latency chart
Cost tracker
Document count stats

**Estimate:** 4h

---

### Issue #8: Add dark mode toggle

**Labels:** `frontend`, `ui`, `priority: low`

**Description:**
Theme switcher component
LocalStorage persistence
Tailwind dark: classes

**Estimate:** 2h

---

### Issue #9: Setup Docker build for frontend

**Labels:** `frontend`, `devops`, `priority: medium`

**Description:**
Create Dockerfile for React app
Nginx configuration for SPA
Environment variable injection
Multi-stage build optimization

**Estimate:** 2h

---

### Issue #10: Deploy frontend to Azure Container Apps

**Labels:** `frontend`, `devops`, `azure`, `priority: high`

**Description:**
Create Terraform config for frontend Container App
Setup CI/CD pipeline for frontend
Configure CORS on backend
Test production deployment

**Estimate:** 3h

---

## Quick Instructions:

1. Go to https://github.com/Kuba906/rag-docs-platform/issues/new
2. Copy title from above (e.g., "Setup React + TypeScript project with Vite")
3. Paste description
4. Add labels
5. Click "Submit new issue"
6. Repeat for all 60 tasks!

---

## OR Use the Script:

```bash
# Install dependencies
pip install requests

# Set GitHub token (get from https://github.com/settings/tokens)
export GITHUB_TOKEN=your_token_here

# Run script
python scripts/create_github_issues.py
```

This will create all 60 issues automatically! 🚀

---

## Recommended Labels to Create First:

Go to: https://github.com/Kuba906/rag-docs-platform/labels

Create these labels:
- `frontend` (color: #0366d6)
- `backend` (color: #d73a4a)
- `api` (color: #a2eeef)
- `rag` (color: #7057ff)
- `ai` (color: #7057ff)
- `ml-engineering` (color: #7057ff)
- `evaluation` (color: #e99695)
- `monitoring` (color: #f9d0c4)
- `observability` (color: #f9d0c4)
- `security` (color: #d93f0b)
- `compliance` (color: #d93f0b)
- `performance` (color: #fbca04)
- `optimization` (color: #fbca04)
- `documentation` (color: #0075ca)
- `priority: high` (color: #d73a4a)
- `priority: medium` (color: #fbca04)
- `priority: low` (color: #0e8a16)
- `ui` (color: #1d76db)
- `devops` (color: #5319e7)
- `azure` (color: #0078d4)

Then issues will be properly categorized! 🏷️
