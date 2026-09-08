from datetime import datetime

from database.audit_log import AuditLog
from database.audit_repository import save_audit_log, load_audit_logs


def test_save_and_load_audit_log(tmp_path, monkeypatch):
    test_file = tmp_path / "audit_logs.json"

    monkeypatch.setattr(
        "database.audit_repository.AUDIT_FILE",
        test_file,
    )

    audit_log = AuditLog(
        transaction_id="TX019",
        timestamp=datetime.now(),
        risk_level="HIGH",
        decision="BLOCK",
        reason="Transaction triggered multiple high-risk indicators.",
        flags=["HIGH_RISK_TRANSACTION"],
    )

    save_audit_log(audit_log)

    logs = load_audit_logs()

    assert len(logs) == 1
    assert logs[0]["transaction_id"] == "TX019"
    assert logs[0]["risk_level"] == "HIGH"
    assert logs[0]["decision"] == "BLOCK"
    assert logs[0]["flags"] == ["HIGH_RISK_TRANSACTION"]


def test_load_empty_audit_repository(tmp_path, monkeypatch):
    test_file = tmp_path / "empty_audit_logs.json"

    monkeypatch.setattr(
        "database.audit_repository.AUDIT_FILE",
        test_file,
    )

    logs = load_audit_logs()

    assert logs == []