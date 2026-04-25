# DevBrain

A local web app for looking up developer tool commands and workflows in plain English.

## Setup

```bash
# 1. Go to the project
cd ~/projects/devbrain

# 2. Create a virtual environment
python -m venv .venv

# 3. Activate it
source .venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Set your Anthropic API key
export ANTHROPIC_API_KEY="your-key-here"

# 6. Run the app
python app.py
```

Then open http://127.0.0.1:5001 in your browser.

## Usage

- **Command lookup**: Type what you want to do — "how do I undo a commit"
- **Workflow**: Type a task — "set up a new Python project"
- **Click any command** to see a breakdown of each part
- **Sidebar**: Filter by tool or click a pre-built workflow to load it

## Project Structure

```
devbrain/
├── app.py              # Flask backend + Claude API
├── requirements.txt
├── cache/
│   ├── seed.json       # Pre-seeded common commands
│   └── responses.json  # Grows as you use the app
└── templates/
    └── index.html      # Frontend (all-in-one)
```
