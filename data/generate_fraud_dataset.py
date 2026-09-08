import random
from pathlib import Path

import pandas as pd


OUTPUT_FILE = Path("data/fraud_transactions.csv")


def generate_fraud_dataset(
    number_of_records: int = 1000,
    random_seed: int = 42,
) -> pd.DataFrame:

    random.seed(random_seed)

    records = []

    for i in range(number_of_records):

        amount = round(random.uniform(10, 25000), 2)

        sender_type = random.choice(
            ["business", "personal"]
        )

        receiver_type = random.choice(
            ["business", "personal"]
        )

        transaction_type = random.choice(
            ["transfer", "payment", "withdrawal"]
        )

        sender_kyc = random.choice(
            [True, True, True, False]
        )

        receiver_kyc = random.choice(
            [True, True, True, False]
        )

        ecocash_connected = random.choice(
            [True, True, False]
        )

        transaction_frequency = random.randint(1, 30)

        international = random.choice(
            [False, False, False, True]
        )

        risk_score = 0

        if amount > 10000:
            risk_score += 2

        if sender_type == "business" and receiver_type == "personal":
            risk_score += 2

        if not sender_kyc or not receiver_kyc:
            risk_score += 2

        if transaction_frequency > 20:
            risk_score += 1

        if international:
            risk_score += 1

        if not ecocash_connected:
            risk_score += 1

        fraud = 1 if risk_score >= 4 else 0

        records.append(
            {
"amount": amount,
                "sender_type": sender_type,
                "receiver_type": receiver_type,
                "transaction_type": transaction_type,
                "sender_kyc_verified": sender_kyc,
                "receiver_kyc_verified": receiver_kyc,
                "ecocash_connected": ecocash_connected,
                "transaction_frequency": transaction_frequency,
                "international": international,
                "fraud": fraud,
            }
        )

    dataset = pd.DataFrame(records)
    dataset.insert(
    0,
    "transaction_id",
    [f"TX{i + 1:05d}" for i in range(len(dataset))]
)

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    dataset.to_csv(
        OUTPUT_FILE,
        index=False,
    )

    return dataset


if __name__ == "__main__":
    dataset = generate_fraud_dataset()

    print("Fraud dataset generated successfully.")
    print(f"Records: {len(dataset)}")
    print(f"Fraud cases: {dataset['fraud'].sum()}")
    print(
        f"Legitimate cases: "
        f"{(dataset['fraud'] == 0).sum()}"
    )
    print(f"Saved to: {OUTPUT_FILE}")