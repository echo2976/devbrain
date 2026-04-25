from flask import Flask, request, jsonify, render_template
import anthropic
import json
import os
import hashlib
import re
from pathlib import Path
from config import load_config, get_api_credentials, save_credentials

app = Flask(__name__)

# Paths
CACHE_FILE = Path(__file__).parent / "cache" / "responses.json"
SEED_FILE = Path(__file__).parent / "cache" / "seed.json"
CACHE_FILE.parent.mkdir(exist_ok=True)

# Load cache
def load_cache():
    if CACHE_FILE.exists():
        with open(CACHE_FILE) as f:
            return json.load(f)
    # Start with seed data
    if SEED_FILE.exists():
        with open(SEED_FILE) as f:
            return json.load(f)
    return {}

def save_cache(cache):
    with open(CACHE_FILE, "w") as f:
        json.dump(cache, f, indent=2)

def cache_key(query):
    return hashlib.md5(query.lower().strip().encode()).hexdigest()

# Intent detection
WORKFLOW_SIGNALS = [
    "set up", "setup", "install", "create a", "start a", "initialize",
    "configure", "walk me through", "how do i start", "get started",
    "new project", "first time", "beginning", "from scratch", "workflow"
]

AMBIGUOUS_SIGNALS = {
    "git": ["branch", "remote", "merge", "push", "pull"],
    "docker": ["container", "image", "compose"],
    "python": ["package", "environment", "venv"],
}

def detect_intent(query):
    q = query.lower()
    for signal in WORKFLOW_SIGNALS:
        if signal in q:
            return "workflow"
    return "command"

def is_command_input(query):
    """Detect if the user typed an actual command rather than a question."""
    q = query.strip()
    command_starters = [
        "git ", "docker ", "python3 ", "python ", "pip ", "npm ", "npx ",
        "node ", "ssh ", "chmod ", "grep ", "find ", "ls ", "cd ", "mkdir ",
        "rm ", "mv ", "cp ", "cat ", "echo ", "curl ", "wget ", "brew ",
        "source ", "export ", "code "
    ]
    question_words = ["how", "what", "why", "when", "where", "can", "should", "do", "does", "is"]
    has_question = any(q.lower().startswith(w) for w in question_words) or q.endswith("?")
    starts_with_command = any(q.startswith(c) for c in command_starters)
    return starts_with_command and not has_question

def detect_tool(query):
    q = query.lower()
    tools = {
        "git": ["git", "commit", "branch", "merge", "push", "pull", "rebase", "clone", "repo"],
        "docker": ["docker", "container", "image", "dockerfile", "compose", "registry"],
        "vscode": ["vscode", "vs code", "cursor", "editor", "extension", "debug", "breakpoint"],
        "terminal": ["bash", "terminal", "shell", "chmod", "grep", "find", "pipe", "redirect", "ssh"],
        "python": ["python", "pip", "venv", "virtualenv", "poetry", "pytest", "pyproject"],
        "node": ["node", "npm", "npx", "package.json", "yarn", "pnpm", "nvm"],
    }
    for tool, keywords in tools.items():
        if any(k in q for k in keywords):
            return tool
    return "general"

# Claude API
SYSTEM_PROMPT = """You are DevBrain, an expert developer tools assistant helping a beginner learn common development tools.

You respond in strict JSON format only. No markdown, no preamble, just the JSON object.

For COMMAND queries, respond with:
{
  "type": "command",
  "tool": "git|docker|vscode|terminal|python|node",
  "title": "Short descriptive title",
  "command": "the exact command",
  "breakdown": [
    {"part": "git", "explanation": "the git program"},
    {"part": "commit", "explanation": "saves a snapshot of your changes"},
    {"part": "-m", "explanation": "flag to provide a message inline"},
    {"part": "\"your message\"", "explanation": "a short description of what you changed"}
  ],
  "example": {
    "command": "git commit -m \"Add login form\"",
    "context": "After staging your files with git add, this saves them with a description"
  },
  "warning": "optional warning string or null"
}

For WORKFLOW queries, respond with:
{
  "type": "workflow",
  "tool": "git|docker|vscode|terminal|python|node",
  "title": "Short workflow title",
  "description": "One sentence describing what this workflow accomplishes",
  "steps": [
    {
      "id": 1,
      "title": "Step title",
      "command": "exact command",
      "explanation": "plain English explanation of this step",
      "breakdown": [
        {"part": "python", "explanation": "runs the Python interpreter"},
        {"part": "-m", "explanation": "runs a built-in module as a script"},
        {"part": "venv", "explanation": "the virtual environment module"},
        {"part": ".venv", "explanation": "the folder name to create (.venv is the convention)"}
      ],
      "warning": null
    }
  ]
}

Be accurate, beginner-friendly, and practical. Real examples over abstract ones.

For ANALYZE queries (user pasted an actual command), respond with:
{
  "type": "analyze",
  "tool": "git|docker|vscode|terminal|python|node",
  "title": "Short descriptive title of what this command does",
  "command": "the exact command as provided",
  "summary": "One plain English sentence describing what this command does overall",
  "breakdown": [
    {"part": "git", "explanation": "the git program"},
    {"part": "rebase", "explanation": "replays commits on top of another branch"},
    {"-i", "explanation": "interactive mode — opens an editor so you can choose what to do with each commit"},
    {"HEAD~3", "explanation": "the last 3 commits from your current position"}
  ],
  "warning": "optional warning string or null"
}"""

def query_claude(query, intent, platform='github'):
    creds = get_api_credentials()
    api_key = creds.get("anthropic_api_key") or os.environ.get("ANTHROPIC_API_KEY", "")
    if not api_key:
        raise ValueError("No Anthropic API key configured. Add it in Settings → Configure API Access.")
    client = anthropic.Anthropic(api_key=api_key)
    
    platform_context = ""
    if platform == 'gitlab':
        platform_context = "\nPlatform context: The user is using GitLab. Use GitLab terminology (Merge Request instead of Pull Request, GitLab CI/CD instead of GitHub Actions, gitlab.com instead of github.com, etc.) and reference GitLab documentation and conventions in your explanations."
    else:
        platform_context = "\nPlatform context: The user is using GitHub. Use GitHub terminology (Pull Request, GitHub Actions, github.com, etc.) and reference GitHub documentation and conventions in your explanations."

    prompt = f"Intent: {intent}\nQuery: {query}{platform_context}"
    
    message = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=2000,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": prompt}]
    )
    
    raw = message.content[0].text.strip()
    raw = re.sub(r'^```json\s*', '', raw)
    raw = re.sub(r'\s*```$', '', raw)
    return json.loads(raw)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/query", methods=["POST"])
def handle_query():
    data = request.json
    query = data.get("query", "").strip()
    intent_override = data.get("intent")
    platform = data.get("platform", "github")
    
    if not query:
        return jsonify({"error": "No query provided"}), 400
    
    # Detect if user typed an actual command vs a question
    if not intent_override and is_command_input(query):
        intent = "analyze"
    else:
        intent = intent_override or detect_intent(query)
    
    tool = detect_tool(query)
    key = cache_key(f"{intent}:{platform}:{query}")
    
    cache = load_cache()
    
    if key in cache:
        result = cache[key]
        result["from_cache"] = True
        return jsonify(result)
    
    # Generate fresh
    try:
        result = query_claude(query, intent, platform)
        result["from_cache"] = False
        cache[key] = result
        save_cache(cache)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/clarify", methods=["POST"])
def clarify():
    """Check if a query needs clarification before responding."""
    data = request.json
    query = data.get("query", "").strip()
    q = query.lower()
    
    # Check for ambiguous queries that could be command or workflow
    ambiguous_keywords = ["branch", "remote", "container", "image", "environment", "package"]
    is_ambiguous = (
        not any(s in q for s in WORKFLOW_SIGNALS) and
        any(k in q for k in ambiguous_keywords) and
        len(query.split()) <= 3  # Short queries are more ambiguous
    )
    
    if is_ambiguous:
        return jsonify({
            "needs_clarification": True,
            "options": [
                {"label": "Show me the command", "intent": "command", "icon": ">_"},
                {"label": "Walk me through it", "intent": "workflow", "icon": "☑"}
            ]
        })
    
    return jsonify({"needs_clarification": False, "intent": detect_intent(query)})

@app.route("/api/workflows", methods=["GET"])
def get_workflows():
    """Return the pre-built workflow library."""
    workflows = {
        "git": [
            "Initialize a new repo and make your first commit",
            "Clone a project and set it up locally",
            "Undo a mistake (revert or reset)",
            "Resolve a merge conflict"
        ],
        "docker": [
            "Run your first container",
            "Build and run a custom image",
            "Set up docker-compose for a project"
        ],
        "vscode": [
            "Set up VS Code for Python development",
            "Configure debugging for a Python project",
            "Install and manage extensions"
        ],
        "terminal": [
            "Navigate and manage files from the terminal",
            "Find files and search file contents",
            "Set up SSH key authentication"
        ],
        "python": [
            "Set up a new Python project with venv",
            "Install and manage packages with pip",
            "Run and debug a Python script"
        ],
        "node": [
            "Initialize a new Node.js project",
            "Install and manage npm packages",
            "Run scripts with npm"
        ]
    }
    return jsonify(workflows)

@app.route("/api/config", methods=["GET"])
def get_config():
    """Return config with boolean flags for saved secrets — never actual values."""
    return jsonify(load_config())

@app.route("/api/config", methods=["POST"])
def update_config():
    """Save credential updates."""
    data = request.json
    try:
        save_credentials(data)
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5001)
