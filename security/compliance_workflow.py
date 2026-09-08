from dataclasses import dataclass

from security.admin_auth import AdminAuthorization
from security.compliance_review import (
    ComplianceReview,
    approve_compliance_review,
    create_compliance_review,
    reject_compliance_review,
)


@dataclass
class ComplianceWorkflowResult:
    review: ComplianceReview
    authorization: AdminAuthorization | None


def create_review_for_transaction(
    transaction_id: str,
    risk_level: str,
    reason: str,
) -> ComplianceWorkflowResult:

    review = create_compliance_review(
        transaction_id=transaction_id,
        risk_level=risk_level,
        reason=reason,
    )

    return ComplianceWorkflowResult(
        review=review,
        authorization=None,
    )


def approve_review(
    review: ComplianceReview,
    authorization: AdminAuthorization,
    reviewer: str,
) -> ComplianceWorkflowResult:

    if not authorization.authorized:
        return ComplianceWorkflowResult(
            review=review,
            authorization=authorization,
        )

    updated_review = approve_compliance_review(
        review,
        reviewer=reviewer,
    )

    return ComplianceWorkflowResult(
        review=updated_review,
        authorization=authorization,
    )


def reject_review(
    review: ComplianceReview,
    authorization: AdminAuthorization,
    reviewer: str,
) -> ComplianceWorkflowResult:

    if not authorization.authorized:
        return ComplianceWorkflowResult(
            review=review,
            authorization=authorization,
        )

    updated_review = reject_compliance_review(
        review,
        reviewer=reviewer,
    )

    return ComplianceWorkflowResult(
        review=updated_review,
        authorization=authorization,
    )


if __name__ == "__main__":
    from security.admin_auth import authorize_admin

    workflow = create_review_for_transaction(
        transaction_id="TX_HUMAN_REVIEW_TEST",
        risk_level="MEDIUM",
        reason="Transaction requires compliance review.",
    )

    print("BANKGUARD AI HUMAN COMPLIANCE WORKFLOW")
    print("--------------------------------------")
    print(f"Transaction ID: {workflow.review.transaction_id}")
    print(f"Risk Level: {workflow.review.risk_level}")
    print(f"Initial Status: {workflow.review.status}")

    authorization = authorize_admin(
        password_valid=True,
    )

    approved = approve_review(
        workflow.review,
        authorization=authorization,
        reviewer="COMPLIANCE_ADMIN",
    )

    print(f"Authorization: {approved.authorization.authorized}")
    print(f"Final Status: {approved.review.status}")
    print(f"Reviewer: {approved.review.reviewer}")
