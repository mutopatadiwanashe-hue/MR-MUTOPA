from dataclasses import dataclass


@dataclass
class ComplianceReview:
    transaction_id: str
    risk_level: str
    reason: str
    status: str
    reviewer: str | None


def create_compliance_review(
    transaction_id: str,
    risk_level: str,
    reason: str,
) -> ComplianceReview:

    return ComplianceReview(
        transaction_id=transaction_id,
        risk_level=risk_level,
        reason=reason,
        status="PENDING",
        reviewer=None,
    )


def approve_compliance_review(
    review: ComplianceReview,
    reviewer: str,
) -> ComplianceReview:

    return ComplianceReview(
        transaction_id=review.transaction_id,
        risk_level=review.risk_level,
        reason=review.reason,
        status="APPROVED",
        reviewer=reviewer,
    )


def reject_compliance_review(
    review: ComplianceReview,
    reviewer: str,
) -> ComplianceReview:

    return ComplianceReview(
        transaction_id=review.transaction_id,
        risk_level=review.risk_level,
        reason=review.reason,
        status="REJECTED",
        reviewer=reviewer,
    )


if __name__ == "__main__":
    review = create_compliance_review(
        transaction_id="TX_COMPLIANCE_TEST",
        risk_level="MEDIUM",
        reason="Transaction requires compliance review.",
    )

    print("BANKGUARD AI COMPLIANCE REVIEW")
    print("------------------------------")
    print(f"Transaction ID: {review.transaction_id}")
    print(f"Risk Level: {review.risk_level}")
    print(f"Reason: {review.reason}")
    print(f"Status: {review.status}")
    print(f"Reviewer: {review.reviewer}")

    approved = approve_compliance_review(
        review,
        reviewer="COMPLIANCE_ADMIN",
    )

    print("\nAfter Human Review")
    print("------------------")
    print(f"Status: {approved.status}")
    print(f"Reviewer: {approved.reviewer}")
