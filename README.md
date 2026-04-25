# DevBrain

A local web app that helps you learn developer tools by explaining commands in plain English, guiding you through workflows, and letting you paste any command for an instant breakdown.

Powered by Claude (Anthropic API).

## Features

**Command Lookup** — Describe what you want to do and get the exact command with a full explanation.
- Syntax-highlighted command with one-click copy
- Plain English breakdown of each part (click to expand)
- Real example with context
- Warning when a command is destructive or irreversible

**Workflow Guide** — Describe a task and get a step-by-step checklist.
- Checkable steps to follow along in real time
- Click any command to expand a breakdown of every part
- One-click copy on each step

**Command Analyzer** — Paste any command you've seen and get it explained.
- Auto-detected when you type a command instead of a question
- Summary of what the command does overall
- Full part-by-part breakdown, always open

**Cheat Sheets** — Quick reference cards for common command sequences.
- Syntax-highlighted commands (base command, subcommand, flags, arguments each in distinct colors)
- Click any command to reveal expected output
- Currently includes: Git start-to-push, Git branch & merge

**Smart Intent Detection** — No mode switching needed.
- Automatically detects whether you want a command, workflow, or analysis
- Shows a clarification pop-up when intent is ambiguous

**Caching** — Responses are saved locally so repeat lookups are instant and work offline.
- Seeded with common commands at launch
- Grows automatically with every new query
- Freshly generated responses get a "✦ freshly generated" badge

## Tools Covered

Git, Docker, VS Code / Cursor, Terminal / Bash, Python, Node / npm

## Setup

```bash
# 1. Go to the project
cd ~/projects/devbrain

# 2. Create a virtual environment
python3 -m venv .venv

# 3. Activate it
source .venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Set your Anthropic API key
export ANTHROPIC_API_KEY="your-key-here"

# 6. Run the app
python3 app.py
```

Then open http://127.0.0.1:5001 in your browser.

> Note: You'll need to re-run `export ANTHROPIC_API_KEY=...` and `source .venv/bin/activate` each time you open a new terminal session.

## Usage

| What you type | What you get |
|---|---|
| "how do I undo a commit" | Command card with breakdown |
| "set up a new Python project" | Workflow checklist |
| `git rebase -i HEAD~3` | Command analyzer breakdown |
| Click **Cheat Sheets** in sidebar | Reference cards |

## Project Structure

```
devbrain/
├── app.py                  # Flask backend + Claude API + intent detection
├── requirements.txt
├── cache/
│   ├── seed.json           # Pre-seeded common commands
│   └── responses.json      # Grows as you use the app (auto-created)
└── templates/
    └── index.html          # Frontend — all HTML, CSS, and JS in one file
```

## Stack

- **Backend**: Python + Flask
- **AI**: Anthropic Claude API (claude-opus-4-5)
- **Frontend**: Vanilla HTML, CSS, JavaScript — no frameworks
- **Fonts**: JetBrains Mono + DM Sans
