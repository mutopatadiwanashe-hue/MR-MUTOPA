# BankGuard-Al

## Intelligent Banking Fraud, AML, KYC and Security Monitoring System

BankGuard-Al is an intelligent financial-security application designed to assist banking and financial operations teams in identifying suspicious transactions, fraud indicators, Anti-Money Laundering (AML) risks and Know Your Customer (KYC) compliance issues.

The system combines transaction analysis, rule-based security controls, explainable risk assessment, audit logging and administrator authentication into a single Streamlit application.

## Key Features

- Suspicious transaction detection
- Fraud and security threat detection
- AML risk flagging
- KYC compliance support
- Explainable risk assessment
- Human-in-the-loop decision making
- Administrator authentication
- Real face-recognition authentication
- Security threat warning and alarm
- Automatic system locking
- Security and audit reporting
- Automated testing
- RAG-based knowledge support

## Security Controls

BankGuard-Al includes a protected administrator access workflow.

When a serious security threat is detected, the system can:

1. Display a prominent security warning.
2. Trigger the security response.
3. Automatically lock the system.
4. Require administrator authentication.
5. Allow authorized unlocking through password or face recognition.

Biometric authentication data is intentionally excluded from the Git repository.

## Technology Stack

- Python 3.12
- Streamlit
- OpenCV
- NumPy
- Pandas
- Scikit-learn
- Plotly
- Pytest
- ONNX-based face detection and recognition models

## Project Structure

BankGuard-Al/
|
+-- app.py
+-- requirements.txt
+-- README.md
+-- .gitignore
|
+-- agents/
+-- graph/
+-- rules/
+-- models/
+-- data/
+-- database/
+-- security/
+-- rag/
+-- tests/
+-- reports/
+-- docs/

## Face Authentication

The administrator face-authentication system uses computer-vision models for face detection and face recognition.

The biometric template is stored locally and is excluded from version control for security and privacy.

Do not commit or publish biometric templates, passwords, API keys, secrets or other sensitive credentials.

## Installation

Clone the repository and enter the project directory:

    git clone https://github.com/mutopatadiwanashe-hue/MR-MUTOPA.git
    cd MR-MUTOPA

Create a virtual environment:

    python -m venv .venv

Activate it on Windows PowerShell:

    .venv\Scripts\Activate.ps1

Install dependencies:

    pip install -r requirements.txt

## Running the Application

Start BankGuard-Al with:

    streamlit run app.py

The Streamlit application will open in your browser.

## Testing

Run the automated test suite with:

    pytest

## Security Notice

BankGuard-Al is a security and decision-support application. It should be properly tested, configured and reviewed before being used in a production financial environment.

Never publish:

- Administrator passwords
- API keys
- Authentication tokens
- Biometric templates
- Private credentials
- Confidential banking or customer data

## Development Status

BankGuard-Al is under active development.

Current development areas include:

- Fraud detection
- AML and KYC risk analysis
- Security monitoring
- Administrator authentication
- Face-recognition authentication
- Audit and reporting
- Deployment preparation

## Author

Tadiwanashe Able Mutopa

BankGuard-Al - Intelligent Security for Financial Operations
