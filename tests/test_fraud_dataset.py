import pandas as pd

from data.generate_fraud_dataset import generate_fraud_dataset


def test_dataset_has_correct_number_of_records():
    dataset = generate_fraud_dataset(
        number_of_records=100,
        random_seed=42,
    )

    assert len(dataset) == 100


def test_dataset_has_required_columns():
    dataset = generate_fraud_dataset(
        number_of_records=100,
        random_seed=42,
    )

    required_columns = {
        "transaction_id",
        "amount",
        "sender_type",
        "receiver_type",
        "transaction_type",
        "sender_kyc_verified",
        "receiver_kyc_verified",
        "ecocash_connected",
        "transaction_frequency",
        "international",
        "fraud",
    }

    assert required_columns.issubset(dataset.columns)


def test_fraud_values_are_binary():
    dataset = generate_fraud_dataset(
        number_of_records=100,
        random_seed=42,
    )

    assert set(dataset["fraud"].unique()).issubset({0, 1})


def test_transaction_ids_are_unique():
    dataset = generate_fraud_dataset(
        number_of_records=100,
        random_seed=42,
    )

    assert dataset["transaction_id"].is_unique
