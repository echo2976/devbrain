"""
config.py — owns all credential read/write for DevBrain.
No other file touches credentials directly.

Instance directory: instance/
  - secret.key   — Fernet key, auto-generated on first run, chmod 600
  - config.json  — encrypted sensitive values, plain non-sensitive values

Two-tier read API:
  load_config()         — non-sensitive fields + boolean flags only for secrets
                          (e.g. anthropic_api_key_saved: True)
  get_api_credentials() — all fields fully decrypted (service clients only)
"""

import json
import os
import stat
from datetime import datetime
from pathlib import Path
from cryptography.fernet import Fernet

# ── Paths ──
BASE_DIR = Path(__file__).parent
INSTANCE_DIR = BASE_DIR / "instance"
KEY_FILE = INSTANCE_DIR / "secret.key"
CONFIG_FILE = INSTANCE_DIR / "config.json"

INSTANCE_DIR.mkdir(exist_ok=True)

# ── Fernet helpers ──
def _get_fernet() -> Fernet:
    """Load existing key or generate a new one."""
    if KEY_FILE.exists():
        key = KEY_FILE.read_bytes()
    else:
        key = Fernet.generate_key()
        KEY_FILE.write_bytes(key)
        KEY_FILE.chmod(0o600)
    return Fernet(key)

def _encrypt(value: str) -> str:
    if not value:
        return ""
    return _get_fernet().encrypt(value.encode()).decode()

def _decrypt(token: str) -> str:
    if not token:
        return ""
    return _get_fernet().decrypt(token.encode()).decode()

# ── Default config structure ──
DEFAULT_CONFIG = {
    "anthropic_api_key": "",       # encrypted
    "openai_api_key": "",          # encrypted
    "tokens_input_total": 0,
    "tokens_output_total": 0,
    "tokens_tracking_since": "",
}

def _read_raw() -> dict:
    """Read raw config from disk, merging with defaults."""
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE) as f:
            data = json.load(f)
        # Merge any new default keys
        for k, v in DEFAULT_CONFIG.items():
            if k not in data:
                data[k] = v
        return data
    return dict(DEFAULT_CONFIG)

def _write_raw(data: dict):
    """Write config to disk with restricted permissions."""
    with open(CONFIG_FILE, "w") as f:
        json.dump(data, f, indent=2)
    CONFIG_FILE.chmod(0o600)

# ── SENSITIVE FIELDS ──
SENSITIVE_FIELDS = {"anthropic_api_key", "openai_api_key"}

# ── Public API ──
def load_config() -> dict:
    """
    Returns non-sensitive config values plus boolean *_saved flags for secrets.
    Templates and routes use this — they never see actual key values.
    """
    raw = _read_raw()
    result = {}
    for key, value in raw.items():
        if key in SENSITIVE_FIELDS:
            result[f"{key}_saved"] = bool(value)
        else:
            result[key] = value
    return result

def get_api_credentials() -> dict:
    """
    Returns all fields fully decrypted.
    Only service clients (e.g. query_claude) call this at request time.
    """
    raw = _read_raw()
    result = {}
    for key, value in raw.items():
        if key in SENSITIVE_FIELDS:
            try:
                result[key] = _decrypt(value) if value else ""
            except Exception:
                result[key] = ""
        else:
            result[key] = value
    return result

def save_credentials(updates: dict):
    """
    Save credential updates.
    - Sensitive fields are encrypted before storage
    - Blank submission preserves existing saved value
    - Non-sensitive fields stored as plain text
    """
    raw = _read_raw()
    for key, value in updates.items():
        if key in SENSITIVE_FIELDS:
            if value and value.strip():
                raw[key] = _encrypt(value.strip())
                if key == "anthropic_api_key":
                    raw["tokens_input_total"] = 0
                    raw["tokens_output_total"] = 0
                    raw["tokens_tracking_since"] = datetime.now().isoformat()
        else:
            raw[key] = value
    _write_raw(raw)


def add_token_usage(input_tokens: int, output_tokens: int):
    raw = _read_raw()
    raw["tokens_input_total"] = raw.get("tokens_input_total", 0) + input_tokens
    raw["tokens_output_total"] = raw.get("tokens_output_total", 0) + output_tokens
    if not raw.get("tokens_tracking_since"):
        raw["tokens_tracking_since"] = datetime.now().isoformat()
    _write_raw(raw)
