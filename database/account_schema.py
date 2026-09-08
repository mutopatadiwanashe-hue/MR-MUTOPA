from dataclasses import dataclass


@dataclass
class Account:
    account_id: str
    account_type: str
    owner_name: str
    ecocash_connected: bool
    kyc_verified: bool
    active: bool
