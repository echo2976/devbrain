# DevBrain

Type what you want to do. Get the command, the explanation, or a full walkthrough. Paste a command you don't recognize and it breaks down every part. Built for learning dev tools without the context-switching.

Requires an Anthropic API key.

## Features

Command lookup — describe what you want in plain English, get the exact command. Each result includes a syntax-highlighted command you can copy, a breakdown of every part (click to expand), a real example, and a warning if the command is destructive.

Workflow guide — describe a task and get a step-by-step checklist you can follow in real time. Click any command in the list to see what each part does.

Command analyzer — paste any command and get it explained. Auto-detected when you type a command instead of a question.

Cheat sheets — quick reference cards for common command sequences, syntax-highlighted with expected output on click. Includes GitHub and GitLab variants for Git workflows.

Claude Code tips — curated tips organized by category: setup, workflow, prompting, context, and Git integration.

Smart intent detection — the app figures out whether you want a command, workflow, or analysis. If it's ambiguous, it asks.

Caching — responses save locally so repeat lookups are instant. New responses show a "✦ freshly generated" badge.

## Tools covered

Git (GitHub + GitLab), Docker, VS Code / Cursor, Terminal / Bash, Python, Node / npm

## Setup

### Mac / Linux

```bash
cd ~/projects/devbrain
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export ANTHROPIC_API_KEY="your-key-here"
python3 app.py
```

### Windows

```cmd
cd %USERPROFILE%\projects\devbrain
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
set ANTHROPIC_API_KEY=your-key-here
python app.py
```

Open http://127.0.0.1:5001 in your browser.

Each new terminal session needs `source .venv/bin/activate` (Mac/Linux) or `.venv\Scripts\activate` (Windows) and the API key export before running the app.

## Usage

| What you type | What you get |
|---|---|
| "how do I undo a commit" | Command card with breakdown |
| "set up a new Python project" | Workflow checklist |
| `git rebase -i HEAD~3` | Command analyzer breakdown |
| Click Cheat Sheets in sidebar | Reference cards |
| Click Claude Code Tips in sidebar | Tips by category |

## Project structure

```
devbrain/
├── app.py                  # Flask backend + Claude API + intent detection
├── requirements.txt
├── cache/
│   ├── seed.json           # Pre-seeded common commands
│   └── responses.json      # Auto-created on first use
└── templates/
    └── index.html          # All HTML, CSS, and JS in one file
```

## Stack

Backend: Python + Flask  
AI: Anthropic Claude API (claude-opus-4-5)  
Frontend: Vanilla HTML, CSS, JavaScript  
Fonts: JetBrains Mono + DM Sans
