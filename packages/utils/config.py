import os
import re
from pathlib import Path
from typing import Any

import yaml
from dotenv import load_dotenv

load_dotenv()


def _substitute_env(value: Any) -> Any:
    if isinstance(value, str):
        pattern = r"\$\{([^}]+)\}"
        return re.sub(pattern, lambda m: os.getenv(m.group(1), ""), value)
    if isinstance(value, dict):
        return {k: _substitute_env(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_substitute_env(v) for v in value]
    return value


def load_config(project_name: str) -> dict[str, Any]:
    parts = project_name.split("/", 1)
    owner = parts[0] if len(parts) > 1 else "default"
    project = parts[1] if len(parts) > 1 else parts[0]
    config_dir = Path("projects") / owner / project
    main_path = config_dir / "config.yaml"
    local_path = config_dir / "config.local.yaml"
    config: dict[str, Any] = {}
    if main_path.exists():
        with open(main_path, encoding="utf-8") as f:
            config = yaml.safe_load(f) or {}
    if local_path.exists():
        with open(local_path, encoding="utf-8") as f:
            local = yaml.safe_load(f) or {}
        for k, v in local.items():
            if isinstance(v, dict) and k in config and isinstance(config[k], dict):
                config[k].update(v)
            else:
                config[k] = v
    return _substitute_env(config)
