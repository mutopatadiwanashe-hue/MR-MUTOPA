from dataclasses import dataclass
import secrets


@dataclass
class PhoneConfirmation:
    confirmation_id: str
    receiver_number: str
    amount: float
    code: str
    confirmed: bool


def create_phone_confirmation(
    receiver_number: str,
    amount: float,
) -> PhoneConfirmation:

    return PhoneConfirmation(
        confirmation_id=secrets.token_hex(8),
        receiver_number=receiver_number,
        amount=amount,
        code=str(secrets.randbelow(900000) + 100000),
        confirmed=False,
    )


def confirm_phone_transaction(
    confirmation: PhoneConfirmation,
    entered_code: str,
) -> PhoneConfirmation:

    if secrets.compare_digest(
        confirmation.code,
        entered_code,
    ):
        return PhoneConfirmation(
            confirmation_id=confirmation.confirmation_id,
            receiver_number=confirmation.receiver_number,
            amount=confirmation.amount,
            code=confirmation.code,
            confirmed=True,
        )

    return confirmation
