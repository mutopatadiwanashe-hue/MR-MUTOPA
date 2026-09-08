from collections import Counter

from database.audit_repository import load_audit_logs


def get_audit_summary() -> dict:
    logs = load_audit_logs()

    risk_counts = Counter(
        log.get("risk_level", "UNKNOWN")
        for log in logs
    )

    decision_counts = Counter(
        log.get("decision", "UNKNOWN")
        for log in logs
    )

    return {
        "total_transactions": len(logs),
        "low_risk": risk_counts.get("LOW", 0),
        "medium_risk": risk_counts.get("MEDIUM", 0),
        "high_risk": risk_counts.get("HIGH", 0),
        "allowed": decision_counts.get("ALLOW", 0),
        "review": decision_counts.get("REVIEW", 0),
        "blocked": decision_counts.get("BLOCK", 0),
    }


def get_recent_audit_logs(limit: int = 10) -> list[dict]:
    logs = load_audit_logs()

    if limit <= 0:
        return []

    return logs[-limit:][::-1]


if __name__ == "__main__":
    summary = get_audit_summary()

    print("BANKGUARD AI AUDIT MONITOR")
    print("--------------------------")
    print(f"Total Transactions: {summary['total_transactions']}")
    print(f"Low Risk: {summary['low_risk']}")
    print(f"Medium Risk: {summary['medium_risk']}")
    print(f"High Risk: {summary['high_risk']}")
    print(f"Allowed: {summary['allowed']}")
    print(f"Review: {summary['review']}")
    print(f"Blocked: {summary['blocked']}")

    print("\nRECENT AUDIT LOGS")
    print("-----------------")

    for log in get_recent_audit_logs():
        print(
            log.get("transaction_id"),
            "|",
            log.get("risk_level"),
            "|",
            log.get("decision"),
        )
