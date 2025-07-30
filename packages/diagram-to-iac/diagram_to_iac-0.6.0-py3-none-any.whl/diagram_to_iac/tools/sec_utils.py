# src/diagram_to_iac/tools/secrets.py

"""
Decode /run/secrets.yaml (Base64‑encoded values) into real env vars.

Mount it into the container with:
  docker run … -v "$PWD/config/secrets.yaml":/run/secrets.yaml:ro …

If the file is missing (e.g. CI injects GitHub Secrets directly),
load_yaml_secrets() is a no‑op.
"""

import os
import base64
import yaml
import pathlib
import binascii

# Path inside container where the encoded YAML is mounted
_YAML_PATH = pathlib.Path("/run/secrets.yaml")


def _decode_b64(enc: str) -> str:
    """Robust Base64 decode: fixes padding, falls back if invalid."""
    enc = enc.strip()
    if not enc:
        return ""
    # Fix missing padding
    enc += "=" * (-len(enc) % 4)
    try:
        return base64.b64decode(enc).decode("utf-8").strip()
    except (binascii.Error, UnicodeDecodeError):
        # If it isn’t valid Base64, return the raw string
        return enc


def load_yaml_secrets() -> None:
    """
    Read /run/secrets.yaml, decode each *_ENCODED value, and export
    as environment variables. Special‑case REPO_TOKEN → GITHUB_TOKEN.
    Safe to call when the file does not exist.
    """
    if not _YAML_PATH.exists():
        return

    data: dict[str, str] = yaml.safe_load(_YAML_PATH.read_text()) or {}
    for key, encoded in data.items():
        if not encoded:
            continue

        # Strip the "_ENCODED" suffix
        # base_name = key.removesuffix("_ENCODED")

        # GitHub Actions requires the env var "GITHUB_TOKEN"
        # not "REPO_TOKEN", so map accordingly
        if key == "REPO_API_KEY":
            env_name = "GITHUB_TOKEN"
        else:
            env_name = key

        # Decode and export
        plain_value = _decode_b64(str(encoded))
        os.environ[env_name] = plain_value
        # print(f"Decoded {env_name}={plain_value}")
