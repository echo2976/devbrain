# DevBrain

Type what you want to do. Get the command, the explanation, or a full walkthrough. Paste a command you don't recognize and it breaks down every part. Built for learning dev tools without the context-switching.

Requires an Anthropic API key (entered once via the app — no environment variables needed).

## Features

Command lookup — describe what you want in plain English, get the exact command. Each result includes a syntax-highlighted command you can copy, a breakdown of every part (click to expand), a real example, and a warning if the command is destructive.

Workflow guide — describe a task and get a step-by-step checklist you can follow in real time. Click any command in the list to see what each part does.

Command analyzer — paste any command and get it explained. Auto-detected when you type a command instead of a question.

Cheat sheets — quick reference cards for common command sequences, syntax-highlighted with expected output on click. Includes GitHub and GitLab variants for Git workflows, plus a terminal reference card.

Claude Code tips — curated tips organized by category: setup, workflow, prompting, context, and Git integration.

Smart intent detection — the app figures out whether you want a command, workflow, or analysis. If it's ambiguous, it asks.

Caching — responses save locally so repeat lookups are instant. New responses show a "✦ freshly generated" badge.

Color themes — 5 dark and 5 light themes, picked from the ⚙ settings page. Your choice persists across restarts.

Credential management — API keys are entered once through Settings → Configure API Access. They're encrypted with Fernet and stored in `instance/config.json`, which is never committed to git. The browser never sees the actual key value — only the Flask backend decrypts it at request time.

## Tools covered

Git (GitHub + GitLab), Docker, VS Code / Cursor, Terminal / Bash, Python, Node / npm

## Setup

### Mac / Linux

```bash
cd ~/projects/devbrain
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
python3 app.py
```

### Windows

```cmd
cd %USERPROFILE%\projects\devbrain
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:5001 in your browser.

On first run, go to ⚙ Settings → Configure API Access and enter your Anthropic API key. It gets encrypted and stored locally — you won't need to set it again.

Each new terminal session still needs `source .venv/bin/activate` (Mac/Linux) or `.venv\Scripts\activate` (Windows) before running the app.

## Usage

| What you type | What you get |
|---|---|
| "how do I undo a commit" | Command card with breakdown |
| "set up a new Python project" | Workflow checklist |
| `git rebase -i HEAD~3` | Command analyzer breakdown |
| Click Cheat Sheets in sidebar | Reference cards |
| Click Claude Code Tips in sidebar | Tips by category |
| Click ⚙ in top right | Settings (themes + API keys) |

## Project structure

```
devbrain/
├── app.py                  # Flask backend + Claude API + intent detection
├── config.py               # Credential read/write — only file that touches keys
├── requirements.txt
├── instance/               # Auto-created, never committed
│   ├── secret.key          # Fernet encryption key
│   └── config.json         # Encrypted API keys + settings
├── cache/
│   ├── seed.json           # Pre-seeded common commands
│   └── responses.json      # Auto-created on first use
└── templates/
    └── index.html          # All HTML, CSS, and JS in one file
```

## Stack

Backend: Python + Flask  
AI: Anthropic Claude API (claude-opus-4-5)  
Encryption: Python cryptography (Fernet)  
Frontend: Vanilla HTML, CSS, JavaScript  
Fonts: JetBrains Mono + DM Sans
