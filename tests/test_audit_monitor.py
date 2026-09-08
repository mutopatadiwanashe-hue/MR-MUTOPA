from reports.audit_monitor import get_audit_summary, get_recent_audit_logs


def test_audit_summary_structure():
    summary = get_audit_summary()

    assert isinstance(summary, dict)
    assert "total_transactions" in summary
    assert "low_risk" in summary
    assert "medium_risk" in summary
    assert "high_risk" in summary
    assert "allowed" in summary
    assert "review" in summary
    assert "blocked" in summary


def test_audit_summary_counts_are_valid():
    summary = get_audit_summary()

    assert summary["total_transactions"] >= 0
    assert summary["low_risk"] >= 0
    assert summary["medium_risk"] >= 0
    assert summary["high_risk"] >= 0
    assert summary["allowed"] >= 0
    assert summary["review"] >= 0
    assert summary["blocked"] >= 0

    assert (
        summary["low_risk"]
        + summary["medium_risk"]
        + summary["high_risk"]
        <= summary["total_transactions"]
    )

    assert (
        summary["allowed"]
        + summary["review"]
        + summary["blocked"]
        <= summary["total_transactions"]
    )


def test_recent_audit_logs_limit():
    logs = get_recent_audit_logs(3)

    assert isinstance(logs, list)
    assert len(logs) <= 3


def test_recent_audit_logs_zero_limit():
    logs = get_recent_audit_logs(0)

    assert logs == []


def test_recent_audit_logs_are_dictionaries():
    logs = get_recent_audit_logs(5)

    for log in logs:
        assert isinstance(log, dict)
        assert "transaction_id" in log
        assert "timestamp" in log
        assert "risk_level" in log
        assert "decision" in log


if __name__ == "__main__":
    test_audit_summary_structure()
    test_audit_summary_counts_are_valid()
    test_recent_audit_logs_limit()
    test_recent_audit_logs_zero_limit()
    test_recent_audit_logs_are_dictionaries()
    print("All audit monitor tests passed.")
