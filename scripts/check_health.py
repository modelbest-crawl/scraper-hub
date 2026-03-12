#!/usr/bin/env python3
"""检查所有爬虫项目的运行健康状态"""

import json
import sys
from datetime import datetime, timedelta
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
HEARTBEAT_DIR = REPO_ROOT / "data" / ".heartbeats"
ALERT_THRESHOLD_HOURS = 24
FAIL_THRESHOLD = 3


def load_heartbeats() -> dict[str, list[dict]]:
    results: dict[str, list[dict]] = {}
    if not HEARTBEAT_DIR.exists():
        return results

    for f in HEARTBEAT_DIR.glob("*.jsonl"):
        project = f.stem
        records = []
        for line in f.read_text().strip().split("\n"):
            if line.strip():
                records.append(json.loads(line))
        results[project] = records
    return results


def get_registered_projects() -> list[dict]:
    projects = []
    for readme in REPO_ROOT.glob("projects/*/*/README.md"):
        content = readme.read_text()
        if content.startswith("---"):
            parts = content.split("---", 2)
            if len(parts) >= 3:
                meta = {}
                for line in parts[1].strip().split("\n"):
                    if ":" in line:
                        key, val = line.split(":", 1)
                        meta[key.strip()] = val.strip().strip('"')
                if meta.get("status") == "running":
                    meta["path"] = str(readme.parent.relative_to(REPO_ROOT))
                    projects.append(meta)
    return projects


def check() -> list[str]:
    alerts = []
    heartbeats = load_heartbeats()
    projects = get_registered_projects()
    now = datetime.now()

    for proj in projects:
        proj_key = proj["path"].replace("projects/", "").replace("/", "_")
        records = heartbeats.get(proj_key, [])

        if not records:
            alerts.append(f"[无心跳] {proj['path']} 从未上报过运行状态")
            continue

        last = records[-1]
        last_time = datetime.fromisoformat(last.get("timestamp", "2000-01-01"))

        if now - last_time > timedelta(hours=ALERT_THRESHOLD_HOURS):
            hours = int((now - last_time).total_seconds() / 3600)
            alerts.append(f"[超时] {proj['path']} 已 {hours} 小时未上报")

        recent = records[-FAIL_THRESHOLD:]
        if len(recent) >= FAIL_THRESHOLD and all(
            r.get("status") == "failed" for r in recent
        ):
            alerts.append(f"[连续失败] {proj['path']} 连续 {FAIL_THRESHOLD} 次失败")

        if len(records) >= 2:
            prev_count = records[-2].get("count", 0)
            curr_count = last.get("count", 0)
            if prev_count > 0 and curr_count < prev_count * 0.5:
                alerts.append(
                    f"[数据骤降] {proj['path']} 抓取量从 {prev_count} 降到 {curr_count}"
                )

    return alerts


def main():
    alerts = check()

    print(f"=== 爬虫健康检查 ({datetime.now().strftime('%Y-%m-%d %H:%M')}) ===\n")

    if not alerts:
        print("所有项目运行正常")
    else:
        print(f"发现 {len(alerts)} 个告警:\n")
        for alert in alerts:
            print(f"  {alert}")

    print()
    projects = get_registered_projects()
    print(f"已注册 running 状态项目: {len(projects)} 个")

    if alerts:
        sys.exit(1)


if __name__ == "__main__":
    main()
