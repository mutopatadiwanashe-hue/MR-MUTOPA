from pathlib import Path

import joblib
import pandas as pd


MODEL_FILE = Path("models/fraud_detection_model.pkl")
DATA_FILE = Path("data/fraud_transactions.csv")


def test_model_file_exists():
    assert MODEL_FILE.exists()


def test_model_can_be_loaded():
    model = joblib.load(MODEL_FILE)
    assert model is not None


def test_model_can_make_prediction():
    model = joblib.load(MODEL_FILE)

    dataset = pd.read_csv(DATA_FILE)

    sample = dataset.drop(columns=["fraud"]).iloc[[0]]

    prediction = model.predict(sample)

    assert prediction[0] in [0, 1]


def test_model_probability_is_valid():
    model = joblib.load(MODEL_FILE)

    dataset = pd.read_csv(DATA_FILE)

    sample = dataset.drop(columns=["fraud"]).iloc[[0]]

    probability = model.predict_proba(sample)[0][1]

    assert 0.0 <= probability <= 1.0
