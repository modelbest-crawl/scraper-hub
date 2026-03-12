import sys
from pathlib import Path

from loguru import logger

_initialized = False
_configured_projects: set[str] = set()


def get_logger(project_name: str):
    global _initialized
    fmt = (
        "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{extra[project]}</cyan> | "
        "<level>{message}</level>"
    )
    if not _initialized:
        _initialized = True
        logger.remove()
        logger.add(sys.stderr, format=fmt, level="INFO")
    if project_name not in _configured_projects:
        _configured_projects.add(project_name)
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        logger.add(
            log_dir / f"{project_name}.log",
            rotation="10 MB",
            retention="7 days",
            format=fmt,
            level="DEBUG",
            filter=lambda r: r["extra"].get("project") == project_name,
        )
    return logger.bind(project=project_name)
