import streamlit as st
import streamlit.components.v1 as components

from reports.audit_monitor import get_audit_summary
from security.unified_security_controller import process_transaction_security
from security.alarm_engine import start_alarm, stop_alarm
from security.unlock_controller import (
    attempt_system_unlock_with_password,
    attempt_system_unlock,
)
from security.face_auth import verify_admin_face
from security.admin_auth import authorize_admin_with_face

def play_browser_alarm():
    components.html(
        """
        <script>
        const AudioContext = window.AudioContext || window.webkitAudioContext;
        const ctx = new AudioContext();

        function beep(frequency, duration) {
            const oscillator = ctx.createOscillator();
            const gain = ctx.createGain();

            oscillator.type = "square";
            oscillator.frequency.value = frequency;
            gain.gain.value = 0.25;

            oscillator.connect(gain);
            gain.connect(ctx.destination);

            oscillator.start();
            setTimeout(() => {
                oscillator.stop();
            }, duration);
        }

        if (ctx.state === "suspended") {
            ctx.resume();
        }

        beep(1200, 500);

        setTimeout(() => {
            beep(800, 500);
        }, 700);

        setTimeout(() => {
            beep(1200, 500);
        }, 1400);
        </script>
        """,
        height=0,
    )



def show_security_warning():
    st.markdown(
        """
        <style>
        .warning-overlay {
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            background: rgba(120, 0, 0, 0.97);
            z-index: 999999;
            display: flex;
            justify-content: center;
            align-items: center;
            animation: warningHide 2s forwards;
        }

        .warning-triangle {
            font-size: 260px;
            line-height: 1;
            color: #ff0000;
            text-shadow:
                0 0 20px #ffffff,
                0 0 40px #ff0000,
                0 0 80px #ff0000;
            animation: warningPulse 0.4s infinite alternate;
        }

        @keyframes warningPulse {
            from {
                transform: scale(1);
            }
            to {
                transform: scale(1.12);
            }
        }

        @keyframes warningHide {
            0% {
                opacity: 1;
                visibility: visible;
                pointer-events: auto;
            }
            99% {
                opacity: 1;
                visibility: visible;
                pointer-events: auto;
            }
            100% {
                opacity: 0;
                visibility: hidden;
                pointer-events: none;
            }
        }
        </style>

        <div class="warning-overlay">
            <div class="warning-triangle">&#9888;</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="BankGuard AI",
    page_icon="🛡️",
    layout="wide",
)


# ============================================================
# SESSION STATE
# ============================================================

if "system_unlocked" not in st.session_state:
    st.session_state.system_unlocked = False

if "security_response" not in st.session_state:
    st.session_state.security_response = None


# ============================================================
# HEADER
# ============================================================

st.title("🛡️ BankGuard AI")

st.subheader(
    "AI-Powered Banking Security and Compliance System"
)

st.markdown(
    """
    BankGuard AI combines Fraud Detection, KYC, AML, Transaction
    Monitoring, Security Controls and Human Compliance Review.
    """
)


# ============================================================
# SECURITY MONITORING
# ============================================================

summary = get_audit_summary()

st.divider()

st.header("Security Monitoring Dashboard")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Transactions",
        summary["total_transactions"],
    )

with col2:
    st.metric(
        "Allowed",
        summary["allowed"],
    )

with col3:
    st.metric(
        "Under Review",
        summary["review"],
    )

with col4:
    st.metric(
        "Blocked",
        summary["blocked"],
    )


# ============================================================
# RISK DISTRIBUTION
# ============================================================

st.divider()

st.subheader("Risk Distribution")

risk_col1, risk_col2, risk_col3 = st.columns(3)

with risk_col1:
    st.metric(
        "Low Risk",
        summary["low_risk"],
    )

with risk_col2:
    st.metric(
        "Medium Risk",
        summary["medium_risk"],
    )

with risk_col3:
    st.metric(
        "High Risk",
        summary["high_risk"],
    )


# ============================================================
# TRANSACTION SECURITY CHECK
# ============================================================

st.divider()

st.header("Transaction Security Check")

st.write(
    "Enter transaction details below to test BankGuard AI security controls."
)


transaction_id = st.text_input(
    "Transaction ID",
    value="TX_STREAMLIT_TEST",
)

amount = st.number_input(
    "Transaction Amount",
    min_value=0.0,
    value=5000.0,
    step=500.0,
)

sender_type = st.selectbox(
    "Sender Account Type",
    ["personal", "business"],
)

receiver_type = st.selectbox(
    "Receiver Account Type",
    ["personal", "business"],
)

transaction_frequency = st.number_input(
    "Transaction Frequency",
    min_value=0,
    value=5,
    step=1,
)

international = st.checkbox(
    "International Transaction",
)

sender_kyc_verified = st.checkbox(
    "Sender KYC Verified",
    value=True,
)

receiver_kyc_verified = st.checkbox(
    "Receiver KYC Verified",
    value=True,
)

ecocash_connected = st.checkbox(
    "EcoCash Connected",
    value=True,
)


# ============================================================
# RUN SECURITY CHECK
# ============================================================

if st.button(
    "Run Security Check",
    type="primary",
    key="run_security_check",
):

    transaction = {
        "transaction_id": transaction_id,
        "amount": amount,
        "sender_type": sender_type,
        "receiver_type": receiver_type,
        "transaction_type": "transfer",
        "sender_kyc_verified": sender_kyc_verified,
        "receiver_kyc_verified": receiver_kyc_verified,
        "ecocash_connected": ecocash_connected,
        "transaction_frequency": transaction_frequency,
        "international": international,
    }

    response = process_transaction_security(
        transaction
    )

    st.session_state.security_response = response
    st.session_state.system_unlocked = False

    if response.security_lock.locked:
        show_security_warning()
        start_alarm()
        play_browser_alarm()
    else:
        stop_alarm()

# DISPLAY SECURITY RESPONSE
# ============================================================

response = st.session_state.security_response

if response is not None:

    st.divider()

    st.header("Security Decision")

    decision = response.decision_result

    # --------------------------------------------------------
    # FINAL DECISION
    # --------------------------------------------------------

    if decision.final_decision == "ALLOW":

        st.success(
            "✅ TRANSACTION ALLOWED"
        )

    elif decision.final_decision == "REVIEW":

        st.warning(
            "⚠️ TRANSACTION REQUIRES COMPLIANCE REVIEW"
        )

    elif decision.final_decision == "BLOCK":

        st.error(
            "🚨 CRITICAL: TRANSACTION BLOCKED"
        )

    st.write(
        f"Final Risk Level: "
        f"**{decision.final_risk_level}**"
    )

    st.write(
        f"Final Decision: "
        f"**{decision.final_decision}**"
    )


    # ========================================================
    # AGENT RISK ASSESSMENT
    # ========================================================

    st.subheader(
        "Agent Risk Assessment"
    )

    agent_col1, agent_col2, agent_col3 = st.columns(3)

    with agent_col1:

        st.metric(
            "Fraud Risk",
            decision.fraud_risk,
        )

    with agent_col2:

        st.metric(
            "KYC Risk",
            decision.kyc_risk,
        )

    with agent_col3:

        st.metric(
            "AML Risk",
            decision.aml_risk,
        )


    # ========================================================
    # SECURITY ALERT
    # ========================================================

    if response.alert is not None:

        st.subheader(
            "Security Alert"
        )

        if response.alert.level == "CRITICAL":

            st.error(
                "🚨 CRITICAL SECURITY ALERT\n\n"
                + response.alert.message
            )

        else:

            st.warning(
                "⚠️ SECURITY WARNING\n\n"
                + response.alert.message
            )


    # ========================================================
    # COMPLIANCE REVIEW
    # ========================================================

    if response.compliance_review is not None:

        st.subheader(
            "Compliance Review"
        )

        review = response.compliance_review.review

        st.warning(
            f"Review Status: {review.status}"
        )

        st.write(
            f"Transaction ID: "
            f"**{review.transaction_id}**"
        )

        st.write(
            f"Risk Level: "
            f"**{review.risk_level}**"
        )

        st.write(
            f"Reason: "
            f"**{review.reason}**"
        )


    # ========================================================
    # SECURITY REASONS
    # ========================================================

    st.subheader(
        "Security Reasons"
    )

    for reason in decision.reasons:

        st.write(
            "- " + reason
        )


    # ========================================================
    # AUDIT LOG
    # ========================================================

    if response.audit_log is not None:

        st.subheader(
            "Audit Log"
        )

        st.write(
            f"Transaction ID: "
            f"**{response.audit_log.transaction_id}**"
        )

        st.write(
            f"Risk Level: "
            f"**{response.audit_log.risk_level}**"
        )

        st.write(
            f"Decision: "
            f"**{response.audit_log.decision}**"
        )

        st.write(
            f"Timestamp: "
            f"**{response.audit_log.timestamp}**"
        )


    # ========================================================
    # AUTOMATIC SYSTEM LOCK
    # ========================================================

    if response.security_lock is not None:

        if (
            response.security_lock.locked
            and not st.session_state.system_unlocked
        ):

            # Start the Windows alarm.
            start_alarm()

            st.error(
                "🔒 SYSTEM LOCKED"
            )

            st.warning(
                "🚨 SECURITY ALARM ACTIVE"
            )

            st.write(
                "Administrator authorization is required."
            )

            st.write(
                f"Lock Reason: "
                f"**{response.security_lock.reason}**"
            )


            # ------------------------------------------------
            # ADMINISTRATOR UNLOCK METHOD
            # ------------------------------------------------

            unlock_method = st.radio(
                "Choose Administrator Unlock Method",
                ["Password", "Face Recognition"],
                horizontal=True,
                key="admin_unlock_method",
            )

            # ------------------------------------------------
            # PASSWORD UNLOCK
            # ------------------------------------------------

            if unlock_method == "Password":

                admin_password = st.text_input(
                    "Administrator Password",
                    type="password",
                    key="admin_unlock_password",
                )

                if st.button(
                    "Unlock with Password",
                    type="primary",
                    key="unlock_system_password",
                ):

                    unlock_result = (
                        attempt_system_unlock_with_password(
                            lock=response.security_lock,
                            password=admin_password,
                        )
                    )

                    if unlock_result.unlocked:

                        stop_alarm()

                        st.session_state.security_response.security_lock = (
                            unlock_result.lock
                        )

                        st.session_state.system_unlocked = True

                        st.success(
                            "SYSTEM UNLOCKED"
                        )

                        st.rerun()

                    else:

                        st.error(
                            "Invalid administrator password."
                        )

            # ------------------------------------------------
            # REAL FACE RECOGNITION UNLOCK
            # ------------------------------------------------

            else:

                st.info(
                    "Look directly at the camera for face verification."
                )

                if st.button(
                    "Verify Administrator Face",
                    type="primary",
                    key="unlock_system_face",
                ):

                    with st.spinner(
                        "Verifying administrator face..."
                    ):

                        face_valid, face_message = (
                            verify_admin_face()
                        )

                    if face_valid:

                        authorization = (
                            authorize_admin_with_face(
                                face_valid=True
                            )
                        )

                        unlock_result = attempt_system_unlock(
                            lock=response.security_lock,
                            authorization=authorization,
                        )

                        if unlock_result.unlocked:

                            stop_alarm()

                            st.session_state.security_response.security_lock = (
                                unlock_result.lock
                            )

                            st.session_state.system_unlocked = True

                            st.success(
                                "SYSTEM UNLOCKED BY FACE"
                            )

                            st.rerun()

                        else:

                            st.error(
                                "Face recognized, but administrator authorization failed."
                            )

                    else:

                        st.error(
                            face_message
                        )

# ============================================================
# SYSTEM STATUS
# ============================================================

st.divider






