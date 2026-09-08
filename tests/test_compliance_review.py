from security.compliance_review import (
    create_compliance_review,
    approve_compliance_review,
    reject_compliance_review,
)


def test_create_pending_review():
    review = create_compliance_review(
        transaction_id="TX_REVIEW_001",
        risk_level="MEDIUM",
        reason="Transaction requires compliance review.",
    )

    assert review.status == "PENDING"
    assert review.reviewer is None


def test_approve_review():
    review = create_compliance_review(
        transaction_id="TX_REVIEW_002",
        risk_level="MEDIUM",
        reason="Transaction requires compliance review.",
    )

    approved = approve_compliance_review(
        review,
        reviewer="COMPLIANCE_ADMIN",
    )

    assert approved.status == "APPROVED"
    assert approved.reviewer == "COMPLIANCE_ADMIN"


def test_reject_review():
    review = create_compliance_review(
        transaction_id="TX_REVIEW_003",
        risk_level="HIGH",
        reason="High-risk transaction requires human review.",
    )

    rejected = reject_compliance_review(
        review,
        reviewer="COMPLIANCE_ADMIN",
    )

    assert rejected.status == "REJECTED"
    assert rejected.reviewer == "COMPLIANCE_ADMIN"


if __name__ == "__main__":
    test_create_pending_review()
    test_approve_review()
    test_reject_review()

    print("BANKGUARD AI COMPLIANCE REVIEW TESTS")
    print("------------------------------------")
    print("All 3 tests passed.")
