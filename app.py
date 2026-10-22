
# pyrefly: ignore [missing-import]

from module.work_coverage import save_json
import streamlit as st
from datetime import date, datetime
from module.auth import authenticate_user, create_user

from module.work_coverage import (
    load_employees,
    load_tasks,
    load_leave_requests,
    load_notifications,
    automate_work_coverage,
    mark_notification_as_read,
    create_notification,
)

from module.leave_management import (
    apply_leave,
    view_leave_requests,
    review_leave,
)


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="WorkMesh | Automation Workspace",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =========================================================
# AUTHENTICATION GATE
# =========================================================


# =========================================================
# AUTHENTICATION GATE
# =========================================================


# =========================================================
# AUTHENTICATION GATE - PROGRESSIVE LOGIN
# =========================================================

if "logged_in_user" not in st.session_state:
    st.session_state["logged_in_user"] = None

if "auth_step" not in st.session_state:
    st.session_state["auth_step"] = "username"

if "auth_username" not in st.session_state:
    st.session_state["auth_username"] = ""

if st.session_state["logged_in_user"] is None:
    st.markdown(
        """
        <style>

.stApp {
    background:
        radial-gradient(
            circle at 50% 35%,
            rgba(113, 67, 170, 0.18),
            transparent 42%
        ),
        linear-gradient(135deg, #080B17 0%, #050812 100%);
}

.block-container {
    max-width: 100% !important;
    padding-top: 8vh !important;
    padding-bottom: 3rem !important;
}

[data-testid="stVerticalBlockBorderWrapper"] {
    background: rgba(28, 22, 44, 0.58) !important;
    border: 1px solid rgba(197, 138, 249, 0.30) !important;
    border-radius: 24px !important;
    box-shadow:
        0 20px 65px rgba(0, 0, 0, 0.40),
        0 0 35px rgba(167, 121, 232, 0.08),
        inset 0 1px 0 rgba(255, 255, 255, 0.05) !important;
    backdrop-filter: blur(18px);
    -webkit-backdrop-filter: blur(18px);
}

.auth-brand {
    color: #F4F0FC;
    font-size: 32px;
    font-weight: 750;
    letter-spacing: -1.2px;
    text-align: center;
    margin-top: 4px;
}

.auth-subtitle {
    color: #AAA4BC;
    text-align: center;
    font-size: 14px;
    line-height: 1.6;
    margin-bottom: 28px;
}

.auth-footer {
    text-align: center;
    color: #8F89A5;
    font-size: 12px;
    margin-top: 24px;
}

div[data-testid="stForm"] {
    border: none !important;
    padding: 0 !important;
}

div.stButton > button,
div.stFormSubmitButton > button {
    background: linear-gradient(135deg, #C58AF9, #A779E8) !important;
    color: #160D23 !important;
    border: 1px solid rgba(255, 255, 255, 0.12) !important;
    border-radius: 12px !important;
    min-height: 46px;
    font-weight: 650 !important;
    transition: all 0.2s ease;
}

div.stButton > button:hover,
div.stFormSubmitButton > button:hover {
    box-shadow: 0 0 22px rgba(197, 138, 249, 0.28);
    border-color: #D9B8FF !important;
}

div[data-baseweb="input"] {
    background: #111321;
    border-radius: 10px;
}

div[data-baseweb="input"] input {
    color: #F4F0FC;
}

div[data-baseweb="select"] {
    border-radius: 10px;
}

h2 {
    color: #F4F0FC;
    letter-spacing: -0.5px;
}

@media (max-width: 640px) {
    .block-container {
        padding: 2rem 1rem !important;
    }

    [data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: 18px !important;
    }
}

/* ==========================================
   LeaveSync Glassmorphism Sidebar
   ========================================== */

section[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #0B1020 0%,
        #050A14 100%
    ) !important;
    border-right: 1px solid rgba(197, 138, 249, 0.20);
}

section[data-testid="stSidebar"] > div {
    background: transparent !important;
}

section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
    color: #AAA4BC;
}

section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: #F4F0FC;
}

section[data-testid="stSidebar"] hr {
    border-color: rgba(197, 138, 249, 0.18);
}

/* Navigation items */
section[data-testid="stSidebar"] [role="radiogroup"] label {
    background: transparent !important;
    border: 1px solid transparent !important;
    border-radius: 11px !important;
    padding: 8px 10px !important;
    transition: background 0.2s ease, border-color 0.2s ease;
}

section[data-testid="stSidebar"] [role="radiogroup"] label:hover {
    background: rgba(197, 138, 249, 0.09) !important;
    border-color: rgba(197, 138, 249, 0.18) !important;
}

/* Sidebar buttons */
section[data-testid="stSidebar"] div.stButton > button {
    background: rgba(24, 20, 39, 0.65) !important;
    color: #E7D9FA !important;
    border: 1px solid rgba(197, 138, 249, 0.24) !important;
    border-radius: 12px !important;
    min-height: 42px;
    transition: all 0.2s ease;
}

section[data-testid="stSidebar"] div.stButton > button:hover {
    background: rgba(65, 43, 91, 0.72) !important;
    border-color: rgba(197, 138, 249, 0.60) !important;
    box-shadow: 0 0 18px rgba(167, 121, 232, 0.14);
}

/* Sidebar captions */
section[data-testid="stSidebar"] [data-testid="stCaptionContainer"] {
    color: #8F89A5;
}

/* Mobile spacing */
@media (max-width: 640px) {
    section[data-testid="stSidebar"] {
        border-right: none;
    }
}


        </style>
        """,
        unsafe_allow_html=True,
    )

    
    left, center, right = st.columns([1, 1.1, 1])

    with center:
        with st.container(border=True):
            st.markdown(
                '<div class="auth-brand">LeaveSync</div>',
                unsafe_allow_html=True,
            )
            st.markdown(
                '<div class="auth-subtitle">'
                'Smarter leave management.<br>'
                'Better work coverage.'
                '</div>',
                unsafe_allow_html=True,
            )

            portal = st.selectbox(
                "Workspace",
                ["Employee", "Manager", "Admin"],
                key="auth_portal",
            )

            st.progress(
                0.5 if st.session_state["auth_step"] == "username" else 1.0
            )

            if st.session_state["auth_step"] == "username":
                st.subheader("Welcome back")
                st.caption("Enter your username to continue.")

                with st.form("username_step"):
                    username = st.text_input(
                        "Username",
                        value=st.session_state["auth_username"],
                        placeholder="Enter your username",
                    )
                    continue_clicked = st.form_submit_button(
                        "Continue",
                        type="primary",
                        use_container_width=True,
                    )

                if continue_clicked:
                    if not username.strip():
                        st.error("Please enter your username.")
                    else:
                        st.session_state["auth_username"] = username.strip()
                        st.session_state["auth_step"] = "password"
                        st.rerun()

                st.caption("New employee? Use the signup option below.")

                if portal == "Employee" and st.button(
                    "Create an employee account",
                    use_container_width=True,
                ):
                    st.session_state["auth_step"] = "signup"
                    st.rerun()

            elif st.session_state["auth_step"] == "password":
                st.subheader("Enter your password")
                st.caption(
                    f"Signing in as {st.session_state['auth_username']}"
                )

                with st.form("password_step"):
                    password = st.text_input(
                        "Password",
                        type="password",
                        placeholder="Enter your password",
                    )
                    login_clicked = st.form_submit_button(
                        "Log in",
                        type="primary",
                        use_container_width=True,
                    )

                if login_clicked:
                    user = authenticate_user(
                        st.session_state["auth_username"],
                        password,
                    )

                    if user is None:
                        st.error("Invalid username or password.")
                    elif user.get("role") != portal.lower():
                        st.error(
                            "This account cannot access that workspace."
                        )
                    else:
                        st.session_state["logged_in_user"] = user
                        st.session_state.pop("auth_username", None)
                        st.session_state.pop("auth_step", None)
                        st.rerun()

                if st.button("← Back", use_container_width=True):
                    st.session_state["auth_step"] = "username"
                    st.rerun()

            elif st.session_state["auth_step"] == "signup":
                st.subheader("Create employee account")
                st.info(
                    "Account registration needs secure employee "
                    "verification. Ask your administrator to "
                    "provision an account."
                )

                if st.button("← Back to login", use_container_width=True):
                    st.session_state["auth_step"] = "username"
                    st.rerun()

            st.markdown(
                '<div class="auth-footer">'
                'LeaveSync · Secure workforce workspace'
                '</div>',
                unsafe_allow_html=True,
            )

    st.stop()


current_user = st.session_state["logged_in_user"]
current_role = current_user["role"]


# =========================================================
# CUSTOM DESIGN
# =========================================================

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
    }

    .stApp {
        background:
            radial-gradient(ellipse at 15% 0%, #29203d 0%, transparent 35%),
            radial-gradient(ellipse at 90% 30%, #111d38 0%, transparent 35%),
            #070b14;
        color: #e8e5f0;
    }

    [data-testid="stHeader"] {
        background: transparent;
    }

    
/* LeaveSync glassmorphism sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #0B1020 0%,
        #050A14 100%
    ) !important;
    border-right: 1px solid rgba(197, 138, 249, 0.22) !important;
    box-shadow: 8px 0 35px rgba(0, 0, 0, 0.18);
}

[data-testid="stSidebar"] > div:first-child {
    background: transparent !important;
    padding-top: 1.4rem;
}


    [data-testid="stSidebar"] > div:first-child {
        padding-top: 1.4rem;
    }

    .block-container {
        padding-top: 1.8rem;
        padding-bottom: 3rem;
        max-width: 1500px;
    }

    h1, h2, h3 {
        color: #f4efff !important;
        letter-spacing: -0.6px;
    }

    p, label, .stMarkdown {
        color: #c5bfd5;
    }

    .wm-brand {
        font-size: 25px;
        font-weight: 700;
        letter-spacing: -1px;
        color: #f6efff;
        margin-bottom: 0;
    }

    .wm-brand span {
        color: #c18af2;
    }

    .wm-subtitle {
        color: #8c879e;
        font-size: 12px;
        margin-top: 3px;
    }

    .wm-eyebrow {
        color: #b89be8;
        font-size: 11px;
        letter-spacing: 2px;
        font-weight: 700;
        text-transform: uppercase;
    }

    .wm-panel {
        background: linear-gradient(
            135deg,
            rgba(62, 45, 79, 0.72),
            rgba(15, 20, 34, 0.96) 65%
        );
        border: 1px solid #3a3049;
        border-radius: 17px;
        padding: 21px;
        margin-bottom: 16px;
    }

    .wm-panel-dark {
        background: linear-gradient(
            145deg,
            #141323,
            #0c111d 70%
        );
        border: 1px solid #302a40;
        border-radius: 17px;
        padding: 20px;
        margin-bottom: 16px;
    }

    .wm-card-label {
        color: #aaa2bf;
        font-size: 12px;
        margin-bottom: 15px;
    }

    .wm-card-number {
        font-size: 34px;
        line-height: 1.15;
        color: #eee5ff;
        font-weight: 600;
        letter-spacing: -1.3px;
    }

    .wm-card-note {
        font-size: 11px;
        color: #8d87a2;
        margin-top: 9px;
    }

    .wm-pill {
        display: inline-block;
        background: #262039;
        color: #d5b5ff;
        border: 1px solid #4c3967;
        padding: 5px 10px;
        border-radius: 30px;
        font-size: 11px;
    }

    .wm-dot {
        display: inline-block;
        width: 7px;
        height: 7px;
        border-radius: 50%;
        background: #a8e4bd;
        margin-right: 7px;
    }

    .wm-divider {
        height: 1px;
        background: #292538;
        margin: 18px 0;
    }

    div[data-testid="stMetric"] {
        background: linear-gradient(
            145deg,
            rgba(65, 47, 83, 0.75),
            rgba(15, 19, 32, 0.98)
        );
        border: 1px solid #3b304b;
        border-radius: 15px;
        padding: 19px 20px;
        min-height: 115px;
    }

    [data-testid="stMetricLabel"] {
        color: #b8afca !important;
        font-size: 12px !important;
    }

    [data-testid="stMetricValue"] {
        color: #eee4ff !important;
        font-size: 31px !important;
        font-weight: 600;
    }

    [data-testid="stMetricDelta"] {
        font-size: 11px !important;
    }

    div.stButton > button {
        border: 1px solid #494057;
        background: #151323;
        color: #e9e1f6;
        border-radius: 10px;
        min-height: 39px;
        transition: all 0.2s ease;
    }

    div.stButton > button:hover {
        border-color: #c18af2;
        color: white;
        background: #29203b;
    }

    div.stButton > button[kind="primary"] {
        background: linear-gradient(110deg, #8e5bc5, #b77be6);
        color: white;
        border: 1px solid #c89cf0;
        font-weight: 600;
    }

    div.stButton > button[kind="primary"]:hover {
        background: linear-gradient(110deg, #a16bd7, #c78bf1);
        border-color: #dec1ff;
    }

    div[data-baseweb="select"] > div,
    div[data-baseweb="input"] > div {
        background: #111321;
        border-color: #383148;
        border-radius: 9px;
    }

    textarea {
        background: #111321 !important;
    }

    [data-testid="stDataFrame"] {
        border: 1px solid #332b43;
        border-radius: 12px;
        overflow: hidden;
    }

    [data-testid="stTabs"] button {
        color: #aaa1bd;
    }

    [data-testid="stTabs"] button[aria-selected="true"] {
        color: #d6adff;
    }

    hr {
        border-color: #292538;
    }

    #MainMenu, footer {
        visibility: hidden;
    }

    @media (max-width: 768px) {
        .block-container {
            padding-top: 1rem;
        }

        .wm-card-number {
            font-size: 27px;
        }
    }
    
/* Navigation styling */
[data-testid="stSidebar"] [role="radiogroup"] label {
    border-radius: 11px !important;
    border: 1px solid transparent !important;
    padding: 7px 10px !important;
    transition: all 0.2s ease;
}

[data-testid="stSidebar"] [role="radiogroup"] label:hover {
    background: rgba(197, 138, 249, 0.10) !important;
    border-color: rgba(197, 138, 249, 0.25) !important;
}

/* Sidebar action buttons */
[data-testid="stSidebar"] .stButton > button {
    background: rgba(24, 20, 39, 0.75) !important;
    color: #F4F0FC !important;
    border: 1px solid rgba(197, 138, 249, 0.28) !important;
    border-radius: 12px !important;
}

[data-testid="stSidebar"] .stButton > button:hover {
    background: rgba(65, 43, 91, 0.80) !important;
    border-color: #C58AF9 !important;
    box-shadow: 0 0 16px rgba(167, 121, 232, 0.18);
}
    /* ===== Clean dashboard system ===== */
    :root {
        --space-1: 0.5rem;
        --space-2: 1rem;
        --space-3: 1.5rem;
        --space-4: 2.5rem;
        --radius: 16px;
        --card-bg: rgba(24, 20, 39, 0.75);
        --card-border: rgba(197, 138, 249, 0.22);
        --text-main: #F4F0FC;
        --text-muted: #B9B0CF;
    }

    html { -webkit-text-size-adjust: 100%; }

    /* Page: centred, equal left and right margins */
    .block-container {
        max-width: 1200px;
        margin: 0 auto;
        padding: 2rem 2rem 4rem 2rem;
    }

    /* One gap between all blocks */
    [data-testid="stVerticalBlock"] { gap: var(--space-2); }
    [data-testid="stHorizontalBlock"] {
        gap: var(--space-2);
        align-items: flex-start;
    }

    /* Clutter removal */
    [data-testid="stHeaderActionElements"] { display: none !important; }
    .stDeployButton, [data-testid="stAppDeployButton"] { display: none !important; }

    /* Text: one scale, always left aligned */
    h1, h2, h3, h4, p, label, li {
        text-align: left;
        overflow-wrap: anywhere;
    }
    h1 {
        font-size: clamp(1.9rem, 6vw, 3rem);
        line-height: 1.1;
        margin: 0 0 var(--space-1) 0;
    }
    h2 {
        font-size: clamp(1.4rem, 4.5vw, 1.9rem);
        line-height: 1.2;
        margin: var(--space-2) 0 var(--space-1) 0;
        padding: 0;
    }
    h3 {
        font-size: 1.15rem;
        line-height: 1.3;
        margin: var(--space-1) 0;
        padding: 0;
    }
    p, li { font-size: 1rem; line-height: 1.5; }
    [data-testid="stCaptionContainer"] { color: var(--text-muted) !important; }

    /* Small section labels (your wm-eyebrow class) */
    .wm-eyebrow {
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 0.16em;
        text-transform: uppercase;
        margin: var(--space-3) 0 var(--space-1) 0;
    }
    .wm-divider { margin: var(--space-3) 0; }

    /* Buttons: same size everywhere, white readable label */
    .stButton > button,
    .stFormSubmitButton > button {
        width: 100%;
        min-height: 48px;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.5rem;
    }
    .stButton > button p,
    .stFormSubmitButton > button p {
        color: #ffffff !important;
        font-size: 1rem;
        font-weight: 600;
        margin: 0;
    }
    button[data-testid="stBaseButton-primary"],
    button[data-testid="stBaseButton-primaryFormSubmit"] {
        background: linear-gradient(135deg, #7c3aed, #9333ea) !important;
        border: none !important;
    }

    /* Number cards (st.metric): same padding, label, and number style */
    [data-testid="stMetric"] {
        background: var(--card-bg);
        border: 1px solid var(--card-border);
        border-radius: var(--radius);
        padding: 1.25rem 1.5rem;
    }
    [data-testid="stMetricLabel"] p {
        font-size: 0.8rem;
        font-weight: 600;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        color: var(--text-muted);
    }
    [data-testid="stMetricValue"] {
        font-size: clamp(1.8rem, 5vw, 2.4rem);
        font-weight: 700;
        line-height: 1.1;
        color: var(--text-main);
    }

    /* Tables and charts: rounded, never wider than the screen */
    [data-testid="stDataFrame"],
    [data-testid="stTable"] {
        border: 1px solid var(--card-border);
        border-radius: var(--radius);
        overflow: hidden;
        max-width: 100%;
    }
    [data-testid="stVegaLiteChart"],
    [data-testid="stArrowVegaLiteChart"] { width: 100%; }

    /* Inputs: 16px stops phones from zooming in */
    input, textarea, select,
    div[data-baseweb="select"] > div {
        font-size: 16px;
        min-height: 44px;
    }

    /* Phones and small tablets */
    @media (max-width: 768px) {
        .block-container { padding: 1rem 0.9rem 4rem 0.9rem; }
        [data-testid="stHorizontalBlock"] { flex-wrap: wrap; }
        [data-testid="stColumn"],
        [data-testid="column"] {
            min-width: 100% !important;
            flex: 1 1 100% !important;
            width: 100% !important;
        }
    }
        /* ===== Sidebar navigation (pill style) ===== */

    /* Hide the "Navigation" title above the menu */
    [data-testid="stSidebar"] [data-testid="stRadio"] [data-testid="stWidgetLabel"] {
        display: none !important;
    }

    /* Menu list: one full-width column */
    [data-testid="stSidebar"] [data-testid="stRadio"] [role="radiogroup"] {
        display: flex !important;
        flex-direction: column !important;
        gap: 0.25rem !important;
        width: 100% !important;
    }
    [data-testid="stSidebar"] [data-testid="stRadio"] [role="radiogroup"] > * {
        width: 100% !important;
    }

    /* Each menu item */
    [data-testid="stSidebar"] label[data-baseweb="radio"] {
        display: flex !important;
        align-items: center !important;
        gap: 0.75rem !important;
        width: 100% !important;
        padding: 0.7rem 0.9rem !important;
        margin: 0 !important;
        border-radius: 12px !important;
        border: 1px solid transparent !important;
        background: transparent !important;
        cursor: pointer;
    }

    /* Hide the round dot (the part that has no text inside it) */
    [data-testid="stSidebar"] label[data-baseweb="radio"] > span,
    [data-testid="stSidebar"] label[data-baseweb="radio"] > div:not(:has(p)) {
        display: none !important;
    }

    /* Hover */
    [data-testid="stSidebar"] label[data-baseweb="radio"]:hover {
        background: rgba(167, 121, 232, 0.10) !important;
    }

    /* Active item */
    [data-testid="stSidebar"] label[data-baseweb="radio"]:has(input:checked) {
        background: rgba(167, 121, 232, 0.18) !important;
        border-color: rgba(197, 138, 249, 0.35) !important;
    }

    /* Text */
    [data-testid="stSidebar"] label[data-baseweb="radio"] p {
        margin: 0 !important;
        font-size: 0.95rem !important;
        font-weight: 500 !important;
        color: #B9B0CF !important;
    }
    [data-testid="stSidebar"] label[data-baseweb="radio"]:has(input:checked) p {
        color: #FFFFFF !important;
        font-weight: 600 !important;
    }

    /* Icon slot: same width for every item, so the text lines up */
    [data-testid="stSidebar"] label[data-baseweb="radio"]::before {
        display: inline-block;
        width: 1.5rem;
        text-align: center;
        font-size: 1.05rem;
        filter: grayscale(1) brightness(1.5);
    }
    [data-testid="stSidebar"] [role="radiogroup"] > :nth-child(1) label[data-baseweb="radio"]::before { content: "🏠"; }
    [data-testid="stSidebar"] [role="radiogroup"] > :nth-child(2) label[data-baseweb="radio"]::before { content: "👥"; }
    [data-testid="stSidebar"] [role="radiogroup"] > :nth-child(3) label[data-baseweb="radio"]::before { content: "📅"; }
    [data-testid="stSidebar"] [role="radiogroup"] > :nth-child(4) label[data-baseweb="radio"]::before { content: "🔁"; }
    [data-testid="stSidebar"] [role="radiogroup"] > :nth-child(5) label[data-baseweb="radio"]::before { content: "🔔"; }
    [data-testid="stSidebar"] [role="radiogroup"] > :nth-child(6) label[data-baseweb="radio"]::before { content: "📈"; }

    /* ===== Sidebar text alignment (LeaveSync, vivek, Workspace...) ===== */
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] > div {
        padding-left: 0 !important;
        margin-left: 0 !important;
        text-indent: 0 !important;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# SESSION STATE AND HELPERS
# =========================================================

if "activity_log" not in st.session_state:
    st.session_state.activity_log = []

if "coverage_results" not in st.session_state:
    st.session_state.coverage_results = []


def log_activity(message):
    st.session_state.activity_log.insert(
        0,
        {
            "Time": datetime.now().strftime("%d %b %Y, %H:%M:%S"),
            "Activity": message,
        },
    )
    st.session_state.activity_log = st.session_state.activity_log[:100]


def load_records(loader, label):
    try:
        result = loader()
        if isinstance(result, list):
            return result
        st.error(f"{label} did not return a list.")
        return []
    except Exception as error:
        st.error(f"Could not load {label}: {error}")
        return []


def status_text(value):
    return str(value or "unknown").replace("_", " ").title()


def show_table(rows, message="No records found."):
    if rows:
        st.dataframe(
            rows,
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.info(message)


def employee_label(employee):
    return f"{employee.get('name', 'Unknown')} · #{employee.get('id')}"


def card(label, value, note, icon="✦"):
    st.markdown(
        f"""
        <div class="wm-panel-dark">
            <div style="display:flex;justify-content:space-between;align-items:center;">
                <div class="wm-card-label">{label}</div>
                <span style="color:#c18af2;font-size:17px;">{icon}</span>
            </div>
            <div class="wm-card-number">{value}</div>
            <div class="wm-card-note">{note}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# =========================================================
# LOAD DATA
# =========================================================

employees = load_records(load_employees, "employees")
tasks = load_records(load_tasks, "tasks")
leaves = load_records(load_leave_requests, "leave requests")
notifications = load_records(load_notifications, "notifications")


# Restrict employee sessions to their own records.
if current_role == "employee":
    employee_id = current_user.get("employee_id")

    employees = [
        item for item in employees
        if str(item.get("id")) == str(employee_id)
    ]

    leaves = [
        item for item in leaves
        if str(item.get("employee_id")) == str(employee_id)
    ]

    notifications = [
        item for item in notifications
        if str(item.get("employee_id")) == str(employee_id)
    ]


employee_names = {
    employee.get("id"): employee.get("name", "Unknown")
    for employee in employees
}

approved_leaves = [
    item for item in leaves
    if str(item.get("status", "")).lower() == "approved"
]

pending_leaves = [
    item for item in leaves
    if str(item.get("status", "")).lower() == "pending"
]

pending_tasks = [
    item for item in tasks
    if str(item.get("status", "")).lower() == "pending"
]

unread_notifications = [
    item for item in notifications
    if str(item.get("status", "")).lower() == "unread"
]



# =========================================================
# SIDEBAR — ROLE-BASED ACCESS
# =========================================================

role_pages = {
    "employee": [
        "Dashboard",
        "Leave Management",
        "Notifications",
    ],
    "manager": [
        "Dashboard",
        "Leave Management",
        "Work Coverage",
        "Notifications",
    ],
    "admin": [
        "Dashboard",
        "Employees",
        "Leave Management",
        "Work Coverage",
        "Notifications",
        "Activity",
    ],
}

allowed_pages = role_pages.get(current_role, ["Dashboard"])

with st.sidebar:
    st.markdown(
        """
        <div style="padding:0 8px 18px 8px;">
            <div class="wm-brand">◉ <span>Leave</span>Sync</div>
            <div class="wm-subtitle">WORKFLOW AUTOMATION</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"**{current_user.get('username', 'User')}**"
    )
    st.caption(f"Signed in as: {current_role.title()}")

    st.markdown(
        '<div class="wm-eyebrow">Workspace</div>',
        unsafe_allow_html=True,
    )

    page = st.radio(
        "Navigation",
        allowed_pages,
        label_visibility="collapsed",
        key="role_navigation",
    )

    st.markdown(
        "<div class='wm-divider'></div>",
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="wm-subtitle">
            <span class="wm-dot"></span>LOCAL SYSTEM
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.caption("Python · JSON · Streamlit")

    if st.button("↻ Refresh workspace", use_container_width=True):
        st.rerun()

    if st.button("Log out", use_container_width=True):
        st.session_state["logged_in_user"] = None
        st.session_state.pop("role_navigation", None)
        st.rerun()

    st.markdown("<div style='height:30px'></div>", unsafe_allow_html=True)
    st.markdown("<div class='wm-divider'></div>", unsafe_allow_html=True)
    st.caption("LeaveSync · Workforce workspace")


# =========================================================
# ROLE-BASED PAGE ACCESS GUARD
# =========================================================

if page not in allowed_pages:
    st.error("You do not have permission to access this page.")
    st.stop()
# =========================================================
# HEADER
# =========================================================

page_info = {
    "Dashboard": (
        "OVERVIEW / WORKSPACE",
        "Your workforce, at a glance.",
    ),
    "Employees": (
        "WORKSPACE / PEOPLE",
        "Manage your employee directory.",
    ),
    "Leave Management": (
        "WORKSPACE / LEAVE",
        "Review leave requests and manage applications.",
    ),
    "Work Coverage": (
        "AUTOMATION / EXECUTIONS",
        "Run and review automated task coverage.",
    ),
    "Notifications": (
        "WORKSPACE / INBOX",
        "Keep track of task assignment updates.",
    ),
    "Activity": (
        "SYSTEM / ACTIVITY",
        "Recent actions in this app session.",
    ),
}

eyebrow, subtitle = page_info[page]

st.markdown(
    f"<div class='wm-eyebrow'>{eyebrow}</div>",
    unsafe_allow_html=True,
)

header_left, header_right = st.columns([4, 1])

with header_left:
    st.title(page)
    st.caption(subtitle)

with header_right:
    st.markdown(
        """
        <div style="text-align:right;padding-top:15px;">
            <span class="wm-pill">● SYSTEM READY</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("<div class='wm-divider'></div>", unsafe_allow_html=True)


# =========================================================
# DASHBOARD
# =========================================================

# =========================================================
# EMPLOYEE PERSONAL DASHBOARD
# =========================================================

if page == "Dashboard" and current_role == "employee":
    employee_id = current_user.get("employee_id")

    my_employee = next(
        (
            emp for emp in employees
            if str(emp.get("id")) == str(employee_id)
        ),
        None,
    )

    if my_employee is None:
        st.error(
            "Your account is not linked to a valid employee record. "
            "Please contact your Admin."
        )
    else:
        my_leaves = sorted(
            leaves,
            key=lambda item: str(item.get("from_date", "")),
            reverse=True,
        )

        pending_count = sum(
            str(item.get("status", "")).lower() == "pending"
            for item in my_leaves
        )
        approved_count = sum(
            str(item.get("status", "")).lower() == "approved"
            for item in my_leaves
        )

        st.subheader(f"Welcome, {my_employee.get('name', 'Employee')}!")
        st.caption("Your personal LeaveSync workspace.")

        c1, c2, c3 = st.columns(3)

        c1.metric(
            "Leave Balance",
            my_employee.get("leave_balance", "N/A"),
        )
        c2.metric("Pending Requests", pending_count)
        c3.metric("Approved Requests", approved_count)

        st.markdown("---")
        st.subheader("My Leave Status")

        show_table(
            [
                {
                    "Request ID": item.get("id"),
                    "From": item.get("from_date"),
                    "To": item.get("to_date"),
                    "Reason": item.get("reason", ""),
                    "Status": status_text(item.get("status")),
                }
                for item in my_leaves
            ],
            "You haven't submitted any leave requests yet.",
        )

        st.markdown("---")
        st.subheader("My Recent Notifications")

        recent_notifications = notifications[-5:][::-1]

        show_table(
            [
                {
                    "Message": item.get("message", ""),
                    "Status": status_text(item.get("status")),
                }
                for item in recent_notifications
            ],
            "You have no notifications yet.",
        )

        
if st.button(
    "Apply for Leave",
    type="primary",
    use_container_width=True,
):
    st.session_state["pending_navigation"] = "Leave Management"
    st.rerun()


if page == "Dashboard" and current_role != "employee":

    st.markdown('<div class="wm-eyebrow">WORKFORCE OVERVIEW</div>', unsafe_allow_html=True)
    st.write("Your workspace is connected to your existing local JSON data.")

    m1, m2, m3 = st.columns(3)
    with m1:
        card("TOTAL EMPLOYEES", len(employees), "Employee records", "♙")
    with m2:
        card("ACTIVE TASKS", len(pending_tasks), "Tasks marked pending", "⌘")
    with m3:
        card("PENDING LEAVES", len(pending_leaves), "Awaiting review", "◷")

    st.markdown("<div style='height:5px'></div>", unsafe_allow_html=True)

    left, right = st.columns([1.7, 1])

    with left:
        st.markdown(
            "<div class='wm-eyebrow'>TASK EXECUTIONS</div>",
            unsafe_allow_html=True,
        )
        st.subheader("Task status overview")

        status_counts = {}
        for task in tasks:
            current_status = status_text(task.get("status"))
            status_counts[current_status] = status_counts.get(current_status, 0) + 1

        if status_counts:
            st.bar_chart(status_counts, color="#b98aeF", height=260)
        else:
            st.info("No task records are available.")

        st.markdown(
            f"""
            <div class="wm-panel">
                <div class="wm-card-label">AUTOMATION QUEUE</div>
                <div class="wm-card-number">{len(approved_leaves)}</div>
                <div class="wm-card-note">
                    Approved leave requests available for coverage processing
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if current_role in {"manager", "admin"} and st.button(
            "▶  Run automatic work coverage",
            type="primary",
            use_container_width=True,
            disabled=not approved_leaves,
        ):
            results = []

            with st.spinner("Running work coverage..."):
                for leave in approved_leaves:
                    try:
                        result = automate_work_coverage(leave.get("employee_id"))
                        results.append(result)
                    except Exception as error:
                        st.error(
                            f"Coverage failed for employee "
                            f"{leave.get('employee_id')}: {error}"
                        )

            st.session_state.coverage_results = results
            log_activity("Ran automatic work coverage from Dashboard")

            if results:
                st.success("Coverage execution finished.")
                st.rerun()

    with right:
        st.markdown(
            "<div class='wm-eyebrow'>SYSTEM SNAPSHOT</div>",
            unsafe_allow_html=True,
        )

        card(
            "NOTIFICATIONS",
            len(notifications),
            f"{len(unread_notifications)} unread",
            "♧",
        )
        card(
            "APPROVED LEAVES",
            len(approved_leaves),
            "Approved requests",
            "✓",
        )

        st.markdown("<div class='wm-eyebrow'>RECENT LEAVE REQUESTS</div>", unsafe_allow_html=True)

        recent = sorted(
            leaves,
            key=lambda item: str(item.get("from_date", "")),
            reverse=True,
        )[:5]

        show_table(
            [
                {
                    "Employee": item.get(
                        "employee_name",
                        employee_names.get(item.get("employee_id"), "Unknown"),
                    ),
                    "Start": item.get("from_date", "—"),
                    "Status": status_text(item.get("status")),
                }
                for item in recent
            ],
            "No leave requests yet.",
        )

    if st.session_state.coverage_results:
        st.markdown("<div class='wm-divider'></div>", unsafe_allow_html=True)
        st.subheader("Latest execution results")

        for result in st.session_state.coverage_results:
            employee_id = result.get("employee_id")
            st.markdown(
                f"**{employee_names.get(employee_id, 'Unknown')} · Employee #{employee_id}**"
            )

            c1, c2 = st.columns(2)
            c1.metric("Reassigned", len(result.get("reassigned", [])))
            c2.metric("Unassigned", len(result.get("unassigned", [])))

            if result.get("reassigned"):
                show_table(result["reassigned"])

            if result.get("unassigned"):
                st.warning(f"Tasks without a replacement: {result['unassigned']}")


# =========================================================
# EMPLOYEES
# =========================================================


# =========================================================
# EMPLOYEES
# =========================================================

elif page == "Employees":

    st.markdown(
        '<div class="wm-eyebrow">PEOPLE DIRECTORY</div>',
        unsafe_allow_html=True,
    )

    # ADD EMPLOYEE
    with st.expander("＋ Add new employee", expanded=False):
        with st.form("add_employee_form"):
            new_name = st.text_input("Full name")
            new_domain = st.text_input("Domain", placeholder="Backend")
            new_skills = st.text_input(
                "Skills (comma-separated)",
                placeholder="Python, SQL, FastAPI",
            )
            new_workload = st.number_input(
                "Current workload (%)",
                min_value=0,
                max_value=100,
                value=0,
                step=5,
            )
            new_available = st.checkbox(
                "Employee is available",
                value=True,
            )
            new_leave_balance = st.number_input(
                "Leave balance (days)",
                min_value=0,
                value=20,
                step=1,
            )

            add_submitted = st.form_submit_button(
                "Add employee",
                type="primary",
                use_container_width=True,
            )

        if add_submitted:
            name = new_name.strip()
            domain = new_domain.strip()
            skills = list(dict.fromkeys(
                skill.strip()
                for skill in new_skills.split(",")
                if skill.strip()
            ))

            if not name or not domain:
                st.error("Name and domain are required.")
            elif any(
                str(employee.get("name", "")).strip().lower() == name.lower()
                for employee in employees
            ):
                st.error("An employee with this name already exists.")
            else:
                next_id = max(
                    (int(employee.get("id", 0)) for employee in employees),
                    default=0,
                ) + 1

                new_employee = {
                    "id": next_id,
                    "name": name,
                    "domain": domain,
                    "skills": skills,
                    "workload": int(new_workload),
                    "available": new_available,
                    "leave_balance": int(new_leave_balance),
                }

                updated_employees = employees + [new_employee]

                if save_json("employees.json", updated_employees):
                    st.success(
                        f"Employee {name} added successfully (ID {next_id})."
                    )
                    st.rerun()
                else:
                    st.error("Could not save employee data. Check file access.")

    st.markdown("<div class='wm-divider'></div>", unsafe_allow_html=True)

    # EMPLOYEE DIRECTORY
    search = st.text_input(
        "Search employees",
        placeholder="Search name, domain, or skills...",
    )

    availability = st.selectbox(
        "Availability filter",
        ["All", "Available", "Unavailable"],
    )

    employee_rows = []

    for employee in employees:
        skills = employee.get("skills", [])
        skills_text = ", ".join(map(str, skills))
        searchable = (
            f"{employee.get('name', '')} "
            f"{employee.get('domain', '')} {skills_text}"
        ).lower()

        is_available = employee.get("available") is True

        if search and search.lower() not in searchable:
            continue
        if availability == "Available" and not is_available:
            continue
        if availability == "Unavailable" and is_available:
            continue

        employee_rows.append({
            "ID": employee.get("id"),
            "Employee": employee.get("name"),
            "Domain": employee.get("domain"),
            "Skills": skills_text,
            "Workload": employee.get("workload", 0),
            "Availability": "Available" if is_available else "Unavailable",
            "Leave Balance": employee.get("leave_balance", "—"),
        })

    st.caption(f"{len(employee_rows)} employee records")
    show_table(employee_rows, "No matching employees.")

    # EMPLOYEE PROFILE AND EDITING
    st.markdown("<div class='wm-divider'></div>", unsafe_allow_html=True)
    st.subheader("Employee profile and editing")

    if employees:
        selected = st.selectbox(
            "Select employee to view or edit",
            employees,
            format_func=employee_label,
            key="employee_profile_select",
        )

        if selected:
            a, b, c = st.columns(3)
            a.metric("Employee ID", selected.get("id", "—"))
            b.metric("Workload", selected.get("workload", 0))
            c.metric(
                "Availability",
                "Available" if selected.get("available") else "Unavailable",
            )

            st.markdown(
                f"""
                <div class="wm-panel">
                    <div class="wm-card-label">EMPLOYEE PROFILE</div>
                    <h3>{selected.get('name', 'Unknown')}</h3>
                    <p>Domain: {selected.get('domain', '—')}</p>
                    <p>Skills: {', '.join(map(str, selected.get('skills', [])))}</p>
                    <p>Leave balance: {selected.get('leave_balance', '—')}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

            with st.expander("Edit employee details"):
                with st.form("edit_employee_form"):
                    edit_name = st.text_input(
                        "Full name",
                        value=selected.get("name", ""),
                    )
                    edit_domain = st.text_input(
                        "Domain",
                        value=selected.get("domain", ""),
                    )
                    edit_skills = st.text_input(
                        "Skills (comma-separated)",
                        value=", ".join(selected.get("skills", [])),
                    )
                    edit_workload = st.number_input(
                        "Current workload (%)",
                        min_value=0,
                        max_value=100,
                        value=max(
                            0,
                            min(100, int(selected.get("workload", 0))),
                        ),
                        step=5,
                    )
                    edit_available = st.checkbox(
                        "Employee is available",
                        value=bool(selected.get("available", False)),
                    )
                    edit_leave_balance = st.number_input(
                        "Leave balance (days)",
                        min_value=0,
                        value=max(
                            0,
                            int(selected.get("leave_balance", 20)),
                        ),
                        step=1,
                    )

                    edit_submitted = st.form_submit_button(
                        "Save changes",
                        type="primary",
                        use_container_width=True,
                    )

                if edit_submitted:
                    name = edit_name.strip()
                    domain = edit_domain.strip()
                    skills = list(dict.fromkeys(
                        skill.strip()
                        for skill in edit_skills.split(",")
                        if skill.strip()
                    ))

                    duplicate_name = any(
                        str(employee.get("name", "")).strip().lower()
                        == name.lower()
                        and employee.get("id") != selected.get("id")
                        for employee in employees
                    )

                    if not name or not domain:
                        st.error("Name and domain are required.")
                    elif duplicate_name:
                        st.error("Another employee already uses this name.")
                    else:
                        updated_employees = []

                        for employee in employees:
                            updated = employee.copy()

                            if updated.get("id") == selected.get("id"):
                                updated.update({
                                    "name": name,
                                    "domain": domain,
                                    "skills": skills,
                                    "workload": int(edit_workload),
                                    "available": edit_available,
                                    "leave_balance": int(edit_leave_balance),
                                })

                            updated_employees.append(updated)

                        if save_json("employees.json", updated_employees):
                            st.success("Employee details updated successfully.")
                            st.rerun()
                        else:
                            st.error(
                                "Could not save changes. Check file access."
                            )
    else:
        st.info("No employees found. Add your first employee above.")



# =========================================================
# LEAVE MANAGEMENT
# =========================================================

elif page == "Leave Management":

    tab1, tab2 = st.tabs(["Leave requests", "New application"])

    with tab1:
        st.subheader("Leave request queue")

        filter_status = st.selectbox(
            "Request status",
            ["All", "Pending", "Approved", "Rejected"],
        )

        filtered = [
            item for item in leaves
            if filter_status == "All"
            or str(item.get("status", "")).lower() == filter_status.lower()
        ]

        show_table(
            [
                {
                    "Request ID": item.get("id"),
                    "Employee": item.get(
                        "employee_name",
                        employee_names.get(item.get("employee_id"), "Unknown"),
                    ),
                    "From": item.get("from_date"),
                    "To": item.get("to_date"),
                    "Days": item.get("days", "—"),
                    "Reason": item.get("reason", ""),
                    "Status": status_text(item.get("status")),
                }
                for item in filtered
            ],
            "No leave requests found.",
        )

        pending = (
             []
         if current_role == "employee"
    else [
        item for item in leaves
        if str(item.get("status", "")).lower() == "pending"
    ]
)


        st.markdown("<div class='wm-divider'></div>", unsafe_allow_html=True)
        if current_role != "employee":
            st.subheader("Review pending request")

        if pending:
            request = st.selectbox(
                "Choose a request",
                pending,
                format_func=lambda item: (
                    f"#{item.get('id')} · "
                    f"{item.get('employee_name', 'Unknown')} · "
                    f"{item.get('from_date')} to {item.get('to_date')}"
                ),
            )

            a, b = st.columns(2)

            with a:
                if st.button("✓ Approve", type="primary", use_container_width=True):
                    result = review_leave(request["id"], "approved", current_role)
                    if result.get("success"):
                        log_activity(f"Approved leave request #{request['id']}")
                        st.success(result.get("message", "Approved"))
                        st.rerun()
                    else:
                        st.error(result.get("message", "Could not approve request."))

            with b:
                if st.button("✕ Reject", use_container_width=True):
                    result = review_leave(request["id"], "rejected", current_role)

                    if result.get("success"):
                        log_activity(f"Rejected leave request #{request['id']}")
                        st.success(result.get("message", "Rejected"))
                        st.rerun()
                    else:
                        st.error(result.get("message", "Could not reject request."))
        else:
            st.info("There are no pending requests.")

    
    with tab2:
        st.subheader("Submit leave application")

        if not employees:
            st.warning("No employees are available.")
        else:
            employee = None

            if current_role == "employee":
                employee_id = current_user.get("employee_id")

                employee = next(
                    (
                        emp for emp in employees
                        if str(emp.get("id")) == str(employee_id)
                    ),
                    None,
                )

                if employee is None:
                    st.error(
                        "Your account is not linked to an employee record. "
                        "Please contact your Manager/Admin."
                    )
            else:
                employee = st.selectbox(
                    "Employee",
                    employees,
                    format_func=employee_label,
                    key="leave_employee_select",
                )

            if employee is not None:
                if current_role == "employee":
                    st.info(
                        f"Applying for leave as: {employee.get('name', 'Employee')}"
                    )

                with st.form("leave_application", clear_on_submit=True):
                    start = st.date_input(
                        "Start date",
                        value=date.today(),
                        min_value=date.today(),
                    )

                    end = st.date_input(
                        "End date",
                        value=date.today(),
                        min_value=date.today(),
                    )

                    reason = st.text_area(
                        "Reason",
                        placeholder="Enter your leave reason...",
                    )

                    submitted = st.form_submit_button(
                        "Submit application",
                        type="primary",
                        use_container_width=True,
                    )

                    if submitted:
                        if end < start:
                            st.error("End date cannot be before start date.")
                        elif not reason.strip():
                            st.error("Please enter a reason.")
                        else:
                            result = apply_leave(
                                employee["id"],
                                start.isoformat(),
                                end.isoformat(),
                                reason.strip(),
                            )

                            if result.get("success"):
                                log_activity(
                                    f"Submitted leave application for "
                                    f"{employee['name']}"
                                )
                                st.success(
                                    result.get(
                                        "message",
                                        "Application submitted.",
                                    )
                                )
                                st.rerun()
                            else:
                                st.error(
                                    result.get(
                                        "message",
                                        "Application failed.",
                                    )
                                )


    # -----------------------------------------------------
    # TASK MANAGEMENT
    # -----------------------------------------------------
    st.subheader("Task Management")

    with st.expander("➕ Create a new task", expanded=False):
        with st.form("create_task_form", clear_on_submit=True):
            new_title = st.text_input("Task title")
            new_domain = st.text_input("Domain", placeholder="e.g. Backend")
            new_skills = st.text_input(
                "Required skills",
                placeholder="Python, SQL, FastAPI",
            )

            available_employees = [
                employee for employee in employees
                if employee.get("available", True)
            ]

            employee_options = {
                employee["id"]: employee
                for employee in available_employees
            }

            new_assignee = st.selectbox(
                "Assign employee",
                options=[None] + list(employee_options.keys()),
                format_func=lambda employee_id: (
                    "Unassigned"
                    if employee_id is None
                    else (
                        f"{employee_options[employee_id].get('name', 'Employee')} "
                        f"· #{employee_id}"
                    )
                ),
            )

            create_task = st.form_submit_button(
                "Create task",
                type="primary",
            )

            if create_task:
                if not new_title.strip() or not new_domain.strip():
                    st.error("Task title and domain are required.")
                else:
                    current_tasks = load_tasks()
                    next_task_id = max(
                        [int(task.get("id", 0)) for task in current_tasks],
                        default=100,
                    ) + 1

                    task = {
                        "id": next_task_id,
                        "title": new_title.strip(),
                        "assigned_to": new_assignee,
                        "domain": new_domain.strip(),
                        "required_skills": [
                            skill.strip()
                            for skill in new_skills.split(",")
                            if skill.strip()
                        ],
                        "status": "pending",
                    }

                    current_tasks.append(task)

                    if save_json("tasks.json", current_tasks):
                        log_activity(f"Created task #{next_task_id}")
                        st.success(f"Task #{next_task_id} created successfully.")
                        st.rerun()
                    else:
                        st.error("Could not save the task. Check tasks.json.")

    current_tasks = load_tasks()

    if current_tasks:
        task_options = {
            task["id"]: task for task in current_tasks
        }

        with st.expander("✏️ Edit task / assignment / status", expanded=False):
            selected_task_id = st.selectbox(
                "Select task",
                options=list(task_options.keys()),
                format_func=lambda task_id: (
                    f"#{task_id} — {task_options[task_id].get('title', 'Untitled')}"
                ),
                key="manage_task_id",
            )

            selected_task = task_options[selected_task_id]

            with st.form("edit_task_form"):
                edit_title = st.text_input(
                    "Task title",
                    value=selected_task.get("title", ""),
                )
                edit_domain = st.text_input(
                    "Domain",
                    value=selected_task.get("domain", ""),
                )
                edit_skills = st.text_input(
                    "Required skills (comma-separated)",
                    value=", ".join(selected_task.get("required_skills", [])),
                )

                all_employee_options = {
                    employee["id"]: employee
                    for employee in employees
                }

                current_assignee = selected_task.get("assigned_to")
                assignment_options = [None] + list(all_employee_options.keys())

                if current_assignee not in assignment_options:
                    current_assignee = None

                edit_assignee = st.selectbox(
                    "Assigned employee",
                    options=assignment_options,
                    index=assignment_options.index(current_assignee),
                    format_func=lambda employee_id: (
                        "Unassigned"
                        if employee_id is None
                        else (
                            f"{all_employee_options[employee_id].get('name', 'Employee')} "
                            f"· #{employee_id}"
                        )
                    ),
                )

                status_options = [
                    "pending",
                    "in_progress",
                    "completed",
                    "blocked",
                    "reassigned",
                ]

                current_status = selected_task.get("status", "pending")
                if current_status not in status_options:
                    status_options.append(current_status)

                edit_status = st.selectbox(
                    "Task status",
                    options=status_options,
                    index=status_options.index(current_status),
                )

                save_task_changes = st.form_submit_button(
                    "Save changes",
                    type="primary",
                )

                if save_task_changes:
                    if not edit_title.strip() or not edit_domain.strip():
                        st.error("Task title and domain are required.")
                    else:
                        updated_tasks = load_tasks()

                        for task in updated_tasks:
                            if task.get("id") == selected_task_id:
                                previous_assignee = task.get("assigned_to")

                                task["title"] = edit_title.strip()
                                task["domain"] = edit_domain.strip()
                                task["required_skills"] = [
                                    skill.strip()
                                    for skill in edit_skills.split(",")
                                    if skill.strip()
                                ]
                                task["assigned_to"] = edit_assignee
                                task["status"] = edit_status

                                if previous_assignee != edit_assignee:
                                    task["previous_assignee"] = previous_assignee

                                break

                       
                        if save_json("tasks.json", updated_tasks):
                            # Notify the newly assigned employee only
                            # when the assignment actually changes.
                            if (
                                previous_assignee != edit_assignee
                                and edit_assignee is not None
                            ):
                                updated_task = next(
                                    (
                                        task for task in updated_tasks
                                        if task.get("id") == selected_task_id
                                    ),
                                    None,
                                )

                                if updated_task:
                                    notification = create_notification(
                                        edit_assignee,
                                        updated_task,
                                    )

                                    if notification is None:
                                        st.warning(
                                            "Task saved, but the assignment "
                                            "notification could not be saved."
                                        )

                            log_activity(f"Updated task #{selected_task_id}")
                            st.success("Task updated successfully.")
                            st.rerun()
                        else:
                            st.error("Could not save changes to tasks.json.")


    st.markdown("<div class='wm-divider'></div>", unsafe_allow_html=True)
    st.subheader("Task assignments")

    show_table(
        [
            {
                "Task ID": task.get("id"),
                "Task": task.get("title", "Untitled"),
                "Assignee": employee_names.get(
                    task.get("assigned_to"), "Unassigned"
                ),
                "Domain": task.get("domain", "—"),
                "Status": status_text(task.get("status")),
                "Previous assignee": employee_names.get(
                    task.get("previous_assignee"),
                    task.get("previous_assignee", "—"),
                ),
            }
            for task in tasks
        ],
        "No tasks available.",
    )

    st.markdown("<div class='wm-divider'></div>", unsafe_allow_html=True)

    st.markdown(
        """
        <div class="wm-panel">
            <div class="wm-eyebrow">EXECUTION CONTROL</div>
            <h3>Automatic work coverage</h3>
            <p>
                Find pending tasks for employees with approved leave,
                select suitable replacements, and create assignment notifications.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if not approved_leaves:
        st.info("No approved leave requests are available.")
    else:
        mode = st.radio(
            "Execution scope",
            ["All approved leave requests", "Choose an employee"],
        )

        employee_ids = list(
            dict.fromkeys(
                item.get("employee_id")
                for item in approved_leaves
                if item.get("employee_id") is not None
            )
        )

        if mode == "Choose an employee":
            selected_id = st.selectbox(
                "Employee on leave",
                employee_ids,
                format_func=lambda employee_id: (
                    f"{employee_names.get(employee_id, 'Unknown')} · #{employee_id}"
                ),
            )
            ids_to_process = [selected_id]
        else:
            ids_to_process = employee_ids

        st.warning(
            "Executing coverage can modify tasks.json and notifications.json. "
            "Run it only when you intend to process approved leave."
        )

        if current_role in {"manager", "admin"} and st.button(
            "Execute work coverage",
            type="primary",
            use_container_width=True,
        ):
            results = []

            with st.spinner("Executing automation..."):
                for employee_id in ids_to_process:
                    try:
                        results.append(automate_work_coverage(employee_id))
                    except Exception as error:
                        st.error(f"Employee #{employee_id}: {error}")

            st.session_state.coverage_results = results
            log_activity("Executed work coverage")

            st.success("Execution finished.")
            st.rerun()

    if st.session_state.coverage_results:
        st.subheader("Execution results")

        for result in st.session_state.coverage_results:
            employee_id = result.get("employee_id")

            st.markdown(
                f"**{employee_names.get(employee_id, 'Unknown')} · #{employee_id}**"
            )

            a, b = st.columns(2)
            a.metric("Reassigned", len(result.get("reassigned", [])))
            b.metric("Unassigned", len(result.get("unassigned", [])))

            if result.get("reassigned"):
                show_table(result["reassigned"])

            if result.get("unassigned"):
                st.warning(
                    f"Tasks without a replacement: {result['unassigned']}"
                )


# =========================================================
# NOTIFICATIONS
# =========================================================

elif page == "Notifications":

    st.markdown('<div class="wm-eyebrow">NOTIFICATION CENTRE</div>', unsafe_allow_html=True)

    a, b = st.columns(2)
    a.metric("Total notifications", len(notifications))
    b.metric("Unread notifications", len(unread_notifications))

    filter_value = st.selectbox(
        "Filter",
        ["All", "Unread", "Read"],
    )

    filtered = [
        item for item in notifications
        if filter_value == "All"
        or str(item.get("status", "")).lower() == filter_value.lower()
    ]

    show_table(
        [
            {
                "ID": item.get("id"),
                "Employee": employee_names.get(
                    item.get("employee_id"), "Unknown"
                ),
                "Message": item.get("message", ""),
                "Task ID": item.get("task_id", "—"),
                "Status": status_text(item.get("status")),
            }
            for item in filtered
        ],
        "No notifications match this filter.",
    )

    st.markdown("<div class='wm-divider'></div>", unsafe_allow_html=True)
    st.subheader("Notification actions")

    unread = [
        item for item in notifications
        if str(item.get("status", "")).lower() == "unread"
    ]

    if unread:
        notification = st.selectbox(
            "Choose unread notification",
            unread,
            format_func=lambda item: (
                f"#{item.get('id')} · {item.get('message', '')}"
            ),
        )

        if st.button("Mark as read", type="primary"):
            success = mark_notification_as_read(
    notification["id"],
    employee_id=(
        current_user.get("employee_id")
        if current_role == "employee"
        else None
    ),
)
            if success:
                log_activity(
                    f"Marked notification #{notification['id']} as read"
                )
                st.success("Notification marked as read.")
                st.rerun()
            else:
                st.error("Could not mark notification as read.")
    else:
        st.info("All notifications are read.")


# =========================================================
# ACTIVITY
# =========================================================

elif page == "Activity":

    st.markdown('<div class="wm-eyebrow">RECENT EVENTS</div>', unsafe_allow_html=True)
    st.subheader("Activity history")

    st.caption(
        "Actions shown here are held in the current Streamlit session. "
        "This is not a permanent audit log."
    )

    activity = st.session_state.activity_log

    show_table(
        activity,
        "No actions recorded yet. Perform an action to populate this list.",
    )

    st.markdown("<div class='wm-divider'></div>", unsafe_allow_html=True)
    st.subheader("System snapshot")

    show_table(
        [
            {"Metric": "Employees", "Value": len(employees)},
            {"Metric": "Tasks", "Value": len(tasks)},
            {"Metric": "Pending tasks", "Value": len(pending_tasks)},
            {"Metric": "Leave requests", "Value": len(leaves)},
            {"Metric": "Pending leaves", "Value": len(pending_leaves)},
            {"Metric": "Notifications", "Value": len(notifications)},
        ]
    )
