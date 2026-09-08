import json
from dataclasses import asdict
from datetime import datetime
from pathlib import Path

from database.audit_log import AuditLog


AUDIT_FILE = Path("database/audit_logs.json")


def save_audit_log(audit_log: AuditLog) -> None:
    AUDIT_FILE.parent.mkdir(parents=True, exist_ok=True)

    logs = []

    if AUDIT_FILE.exists():
        with open(AUDIT_FILE, "r", encoding="utf-8") as file:
            try:
                logs = json.load(file)
            except json.JSONDecodeError:
                logs = []

    log_data = asdict(audit_log)
    log_data["timestamp"] = audit_log.timestamp.isoformat()

    logs.append(log_data)

    with open(AUDIT_FILE, "w", encoding="utf-8") as file:
        json.dump(logs, file, indent=4)


def load_audit_logs() -> list[dict]:
    if not AUDIT_FILE.exists():
        return []

    with open(AUDIT_FILE, "r", encoding="utf-8") as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            return []