#!/usr/bin/env python3
"""
Script to create GitHub Issues from ROADMAP.md

Usage:
    export GITHUB_TOKEN=your_token_here
    python scripts/create_github_issues.py

Or manually create issues by copying task descriptions from ROADMAP.md
"""

import os
import re
from typing import List, Dict
import requests

# Configuration
GITHUB_OWNER = "Kuba906"
GITHUB_REPO = "rag-docs-platform"
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
ROADMAP_FILE = "ROADMAP.md"

# Labels for different phases
PHASE_LABELS = {
    "Phase 1": ["frontend", "ui", "priority: medium"],
    "Phase 2": ["backend", "api", "priority: medium"],
    "Phase 3": ["monitoring", "observability", "priority: high"],
    "Phase 4": ["rag", "ai", "priority: high"],
    "Phase 5": ["ml-engineering", "evaluation", "priority: high"],
    "Phase 6": ["security", "compliance", "priority: medium"],
    "Phase 7": ["performance", "optimization", "priority: medium"],
    "Phase 8": ["documentation", "priority: low"],
}

def parse_roadmap(filepath: str) -> List[Dict]:
    """Parse ROADMAP.md and extract tasks."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    tasks = []
    current_phase = None
    current_epic = None

    # Find all tasks with pattern: - [ ] **#N** Task title
    pattern = r'- \[ \] \*\*#(\d+)\*\* (.+?)(?:\n(.+?))?(?=\n  -|\n\n|\Z)'

    lines = content.split('\n')
    for i, line in enumerate(lines):
        # Track current phase
        if line.startswith('## ') and 'Phase' in line:
            current_phase = re.search(r'Phase \d+', line).group()

        # Track current epic
        if line.startswith('### Epic:'):
            current_epic = line.replace('### Epic:', '').strip()

        # Find task
        if line.startswith('- [ ] **#'):
            match = re.match(r'- \[ \] \*\*#(\d+)\*\* (.+)', line)
            if match:
                task_num = match.group(1)
                title = match.group(2)

                # Collect description (next lines until "Est:")
                description_lines = []
                j = i + 1
                while j < len(lines):
                    next_line = lines[j]
                    if next_line.strip().startswith('Est:'):
                        estimate = next_line.strip().replace('Est:', '').strip()
                        break
                    if next_line.strip().startswith('- [ ]'):
                        break
                    if next_line.strip():
                        description_lines.append(next_line.strip().replace('- ', ''))
                    j += 1

                description = '\n'.join(description_lines)

                tasks.append({
                    'number': int(task_num),
                    'title': f"#{task_num}: {title}",
                    'description': description,
                    'estimate': estimate if 'estimate' in locals() else 'Unknown',
                    'phase': current_phase,
                    'epic': current_epic,
                    'labels': PHASE_LABELS.get(current_phase, ['enhancement'])
                })

    return sorted(tasks, key=lambda x: x['number'])


def create_github_issue(task: Dict) -> bool:
    """Create a GitHub issue for a task."""
    if not GITHUB_TOKEN:
        print(f"⚠️  No GITHUB_TOKEN found. Skipping issue creation.")
        print(f"   Would create: {task['title']}")
        return False

    url = f"https://api.github.com/repos/{GITHUB_OWNER}/{GITHUB_REPO}/issues"

    body = f"""## {task['epic']}

{task['description']}

**Estimate:** {task['estimate']}
**Phase:** {task['phase']}

---
*This issue was automatically generated from ROADMAP.md*
"""

    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }

    data = {
        "title": task['title'],
        "body": body,
        "labels": task['labels']
    }

    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 201:
        issue_url = response.json()['html_url']
        print(f"✅ Created: {task['title']}")
        print(f"   {issue_url}")
        return True
    else:
        print(f"❌ Failed to create: {task['title']}")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text}")
        return False


def main():
    print("🚀 Creating GitHub Issues from ROADMAP.md\n")

    # Parse roadmap
    tasks = parse_roadmap(ROADMAP_FILE)
    print(f"📋 Found {len(tasks)} tasks\n")

    # Check if GitHub token is available
    if not GITHUB_TOKEN:
        print("⚠️  GITHUB_TOKEN not set. Dry run mode.\n")
        print("To create issues, set your GitHub token:")
        print("  export GITHUB_TOKEN=your_token_here")
        print("\nTasks that would be created:\n")

        for task in tasks:
            print(f"  #{task['number']}: {task['title'].replace(f\"#{task['number']}: \", '')}")

        print(f"\n💡 Alternatively, manually create issues using ROADMAP.md")
        return

    # Create issues
    created = 0
    for task in tasks:
        if create_github_issue(task):
            created += 1

    print(f"\n✨ Created {created}/{len(tasks)} issues")
    print(f"\n🔗 View issues: https://github.com/{GITHUB_OWNER}/{GITHUB_REPO}/issues")


if __name__ == "__main__":
    main()
