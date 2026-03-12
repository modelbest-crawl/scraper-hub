#!/usr/bin/env python3
"""扫描所有项目 README.md 的 frontmatter，生成项目清单"""

from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
OUTPUT = REPO_ROOT / "docs" / "project_registry.md"


def parse_frontmatter(readme_path: Path) -> dict | None:
    content = readme_path.read_text(encoding="utf-8")
    if not content.startswith("---"):
        return None

    parts = content.split("---", 2)
    if len(parts) < 3:
        return None

    meta = {}
    for line in parts[1].strip().split("\n"):
        if ":" in line:
            key, val = line.split(":", 1)
            meta[key.strip()] = val.strip().strip('"').strip("'")
    return meta


def scan_projects() -> list[dict]:
    projects = []
    for readme in sorted(REPO_ROOT.glob("projects/*/*/README.md")):
        if "_template" in str(readme):
            continue
        meta = parse_frontmatter(readme)
        if meta:
            meta["_path"] = str(readme.parent.relative_to(REPO_ROOT))
            projects.append(meta)
    return projects


def generate_markdown(projects: list[dict]) -> str:
    lines = [
        "# 项目清单",
        "",
        "> 自动生成，请勿手动编辑。运行 `make registry` 更新。",
        "",
        "| 负责人 | 项目 | 目标 | 状态 | 调度 | 路径 |",
        "|--------|------|------|------|------|------|",
    ]

    for p in projects:
        owner = p.get("owner", "")
        target = p.get("target", "")
        status = p.get("status", "")
        schedule = p.get("schedule", "")
        path = p.get("_path", "")
        name = path.split("/")[-1] if "/" in path else ""

        status_icon = {"running": "🟢", "paused": "🟡", "deprecated": "🔴", "pending": "⚪"}.get(
            status, "⚪"
        )

        lines.append(
            f"| {owner} | {name} | {target} | {status_icon} {status} | {schedule} | `{path}` |"
        )

    lines.append("")
    lines.append(f"共 {len(projects)} 个项目")
    lines.append("")
    return "\n".join(lines)


def main():
    projects = scan_projects()
    md = generate_markdown(projects)

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(md, encoding="utf-8")
    print(f"已生成项目清单: {OUTPUT} ({len(projects)} 个项目)")


if __name__ == "__main__":
    main()
