from dataclasses import dataclass
from datetime import datetime


@dataclass
class Transaction:
    transaction_id: str
    sender_account: str
    receiver_account: str
    amount: float
    currency: str
    transaction_type: str
    timestamp: datetime
    sender_account_type: str
    receiver_account_type: str
    sender_kyc_verified: bool
    receiver_kyc_verified: bool