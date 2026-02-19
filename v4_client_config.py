"""Per-client config loading with base competitor merge.

Usage:
    from v4_client_config import load_client_config, list_clients

    config = load_client_config("1453")   # returns merged config dict
    clients = list_clients()               # returns ["1453", ...]
"""
from __future__ import annotations

from pathlib import Path

import yaml

_ROOT = Path(__file__).parent
_CONFIGS = _ROOT / "configs"
_BASE_PATH = _CONFIGS / "base_competitors.yaml"
_CLIENTS_DIR = _CONFIGS / "clients"


def load_base() -> dict:
    """Load the shared base config (competitors, financial_services, payroll, etc.)."""
    if not _BASE_PATH.exists():
        raise FileNotFoundError(f"Base config not found: {_BASE_PATH}")
    with open(_BASE_PATH, encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def load_client_config(client_id: str) -> dict:
    """Load a client config merged with the base.

    Merge rules:
    - competitors: client patterns are APPENDED to base (per category, per tier)
    - false_positives: client list appended to base list
    - financial_services, payroll: base values used unless client overrides
    - All other client fields (paths, params) come from client file only

    Returns a dict ready to pass to run_pipeline().
    """
    base = load_base()

    client_path = _CLIENTS_DIR / f"{client_id}.yaml"
    if not client_path.exists():
        raise FileNotFoundError(
            f"No client config for '{client_id}'. "
            f"Create {client_path} to configure this client."
        )
    with open(client_path, encoding="utf-8") as f:
        client = yaml.safe_load(f) or {}

    # Merge competitors: client patterns extend base patterns
    base_comp = base.get("competitors", {})
    client_comp = client.pop("competitors", {})
    merged_comp = _merge_competitors(base_comp, client_comp)

    # Merge false positives (deduplicated, order preserved)
    base_fp = base.get("false_positives", [])
    client_fp = client.pop("false_positives", [])
    merged_fp = list(dict.fromkeys(base_fp + client_fp))

    # Start with client fields, then layer in merged/base values
    config = dict(client)
    config["competitors"] = merged_comp
    config["false_positives"] = merged_fp

    # Carry over base sections the client doesn't override
    for key in ("financial_services", "payroll"):
        if key not in config and key in base:
            config[key] = base[key]

    return config


def _merge_competitors(base: dict, client: dict) -> dict:
    """Deep-merge competitor dicts. Client patterns extend base patterns."""
    merged = {}
    all_categories = set(base) | set(client)

    for cat in all_categories:
        base_rules = base.get(cat, {})
        client_rules = client.get(cat, {})

        # Skip empty base categories with no client override
        if not base_rules and not client_rules:
            continue

        merged[cat] = {}
        for tier in ("exact", "starts_with", "contains"):
            base_list = base_rules.get(tier, []) if isinstance(base_rules, dict) else []
            client_list = client_rules.get(tier, []) if isinstance(client_rules, dict) else []
            # Deduplicate while preserving order
            combined = list(dict.fromkeys(base_list + client_list))
            if combined:
                merged[cat][tier] = combined

    return merged


def list_clients() -> list[str]:
    """Return sorted list of configured client IDs."""
    if not _CLIENTS_DIR.exists():
        return []
    return sorted(p.stem for p in _CLIENTS_DIR.glob("*.yaml"))
