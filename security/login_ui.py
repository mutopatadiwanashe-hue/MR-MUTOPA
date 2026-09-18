import time
import streamlit as st

from security.password_auth import verify_password
from security.face_auth import verify_admin_face


# ============================================================
# THEME: LOGIN SCREEN (calm navy/blue)
# ============================================================

LOGIN_CSS = """
    :root {
        --navy-deep:#0A1128;
        --navy-panel:#101B3D;
        --blue:#3F8EFC;
        --cyan:#22E5FF;
        --ink:#F4F7FC;
        --ink-dim:#9AA9CC;
        --line: rgba(255,255,255,0.12);
    }
    .stApp { background: var(--navy-deep); }
    [data-testid="stHeader"] { background: transparent; }

    .login-card {
        max-width: 440px;
        margin: 6vh auto 0 auto;
        background: var(--navy-panel);
        border: 1px solid var(--line);
        border-radius: 16px;
        padding: 32px 34px 8px 34px;
        box-shadow: 0 30px 60px -30px rgba(0,0,0,0.7);
    }
    .login-mark {
        width: 44px; height: 44px; border-radius: 11px; margin-bottom: 16px;
        background: linear-gradient(135deg, var(--blue), var(--cyan));
        display: flex; align-items: center; justify-content: center;
        font-weight: 700; color: var(--navy-deep); font-size: 17px;
    }
    .login-card h1 { color: var(--ink); font-size: 22px; margin: 0 0 4px 0; }
    .login-card p.sub { color: var(--ink-dim); font-size: 14px; margin: 0 0 8px 0; }

    .stTextInput input {
        background: rgba(255,255,255,0.05) !important;
        color: var(--ink) !important;
        border: 1px solid var(--line) !important;
        border-radius: 8px !important;
    }
    .stTextInput label { color: var(--ink-dim) !important; }

    .stButton button, div[data-testid="stFormSubmitButton"] button {
        background: linear-gradient(135deg, var(--blue), var(--cyan)) !important;
        color: #04142B !important;
        border: none !important;
        border-radius: 9px !important;
        font-weight: 600 !important;
        width: 100%;
    }
    .login-divider { text-align:center; color: var(--ink-dim); font-size: 12px; margin: 4px 0 10px 0; }
"""

# ============================================================
# THEME: DASHBOARD (bright, once authenticated)
# ============================================================

DASHBOARD_CSS = """
    :root {
        --dash-bg:#160A2E;
        --dash-panel:#1F1140;
        --pink:#FF4FA3;
        --violet:#8B5CFF;
        --gold:#FFC93C;
        --dash-line: rgba(255,255,255,0.12);
        --dash-ink: #F4F0FF;
    }
    .stApp { background: var(--dash-bg); }
    h1, h2, h3 { color: var(--dash-ink) !important; }
    p, span, label { color: var(--dash-ink); }

    [data-testid="stMetric"] {
        background: var(--dash-panel);
        border: 1px solid var(--dash-line);
        border-radius: 14px;
        padding: 12px 16px;
    }
    [data-testid="stMetricValue"] { color: var(--pink) !important; }
    [data-testid="stMetricLabel"] { color: var(--dash-ink) !important; }

    .stButton button {
        background: linear-gradient(135deg, var(--pink), var(--violet)) !important;
        color: #160A2E !important;
        border: none !important;
        border-radius: 9px !important;
        font-weight: 600 !important;
    }
    hr { border-color: var(--dash-line) !important; }
"""


def _inject(css: str) -> None:
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


def require_admin_login() -> None:
    """
    Call this once, immediately after st.set_page_config(...) in app.py.

    Blocks the rest of the script (via st.stop()) until the admin
    verifies with either their real password (security.password_auth)
    or live face recognition (security.face_auth). Once authenticated,
    it switches the whole app to the bright dashboard theme and adds
    a Sign out control.
    """

    if "admin_authenticated" not in st.session_state:
        st.session_state.admin_authenticated = False

    if st.session_state.admin_authenticated:
        _inject(DASHBOARD_CSS)
        _render_signed_in_bar()
        return

    _inject(LOGIN_CSS)
    _render_login_screen()
    st.stop()


def _render_signed_in_bar() -> None:
    col1, col2 = st.columns([6, 1])
    with col2:
        if st.button("Sign out", key="admin_sign_out"):
            st.session_state.admin_authenticated = False
            st.rerun()


def _render_login_screen() -> None:
    st.markdown(
        """
        <div class="login-card">
            <div class="login-mark">BG</div>
            <h1>Administrator access</h1>
            <p class="sub">Sign in to open the BankGuard AI dashboard.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    _, center, _ = st.columns([1, 1.3, 1])

    with center:
        with st.form("admin_login_form"):
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Unlock dashboard")

        if submitted:
            if verify_password(password):
                st.session_state.admin_authenticated = True
                st.rerun()
            else:
                st.error("Incorrect administrator password.")

        st.markdown('<div class="login-divider">or</div>', unsafe_allow_html=True)

        if st.button("Verify with face recognition", key="face_login_button"):
            with st.spinner("Opening camera — look at the webcam..."):
                success, message = verify_admin_face()

            if success:
                st.session_state.admin_authenticated = True
                st.success(message)
                time.sleep(0.6)
                st.rerun()
            else:
                st.error(message)
