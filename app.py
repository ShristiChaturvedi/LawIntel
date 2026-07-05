import streamlit as st

from rag.chatbot import ask_question
from rag.mcq_generator import generate_mcqs
# ============================================================
# Page Configuration
# ============================================================

st.set_page_config(
    page_title="LawIntel",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# Custom CSS
# ============================================================

st.markdown("""
<style>

/* =========================================================
   Hide Streamlit Elements
========================================================= */

#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}


/* =========================================================
   App Background
========================================================= */

.stApp{
    background:#0F172A;
    color:#F8FAFC;
}


/* =========================================================
   Main Content
========================================================= */

.block-container{
    padding-top:2rem;
    padding-left:3rem;
    padding-right:3rem;
    max-width:100%;
}


/* =========================================================
   Sidebar
========================================================= */

section[data-testid="stSidebar"]{
    background:#111827;
    border-right:1px solid #374151;
}

section[data-testid="stSidebar"] .block-container{
    padding-top:2rem;
}

/* Sidebar Title */

section[data-testid="stSidebar"] h1{
    color:#FFFFFF !important;
    font-size:34px !important;
    font-weight:800 !important;
}

/* Sidebar Text */

section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] span,
section[data-testid="stSidebar"] label{
    color:#F8FAFC !important;
    font-size:17px !important;
    font-weight:600 !important;
}

/* Radio labels */

section[data-testid="stSidebar"] div[role="radiogroup"] label{
    color:#F8FAFC !important;
}

/* Divider */

section[data-testid="stSidebar"] hr{
    border-color:#374151;
}


/* =========================================================
   Headings
========================================================= */

h1{
    color:#FFFFFF !important;
    font-size:52px !important;
    font-weight:800 !important;
}

h2,h3{
    color:#FFFFFF !important;
}


/* =========================================================
   Caption
========================================================= */

[data-testid="stCaptionContainer"]{
    color:#CBD5E1 !important;
}


/* =========================================================
   Text Area
========================================================= */

div[data-testid="stTextArea"] textarea{

    background:#1E293B !important;
    color:#FFFFFF !important;

    caret-color:#FFFFFF !important;

    border-radius:12px !important;
    border:1px solid #475569 !important;

    font-size:20px !important;
    line-height:1.6 !important;

    padding:18px !important;
}


/* =========================================================
   Button
========================================================= */

.stButton>button{

    background:#2563EB !important;
    color:white !important;

    border:none;
    border-radius:12px;

    width:180px;
    height:56px;

    font-size:20px;
    font-weight:700;

    transition:0.25s;
}

.stButton>button:hover{

    background:#1D4ED8 !important;

    transform:translateY(-2px);
}


/* =========================================================
   Metrics
========================================================= */

div[data-testid="stMetric"]{
    background:#1E293B;
    border:1px solid #334155;
    border-radius:14px;
    padding:18px;
}

/* Metric label */
div[data-testid="stMetric"] label,
div[data-testid="stMetric"] p,
div[data-testid="stMetric"] span{
    color:#F8FAFC !important;
    opacity:1 !important;
    font-size:17px !important;
    font-weight:600 !important;
}

/* Metric value */
div[data-testid="stMetric"] [data-testid="stMetricValue"]{
    color:#FFFFFF !important;
    font-size:34px !important;
    font-weight:700 !important;
}

/* =========================================================
   Horizontal Rule
========================================================= */

hr{
    border-color:#334155;
}

</style>
""", unsafe_allow_html=True)

# ============================================================
# Header
# ============================================================

st.title("⚖️ LawIntel")
st.caption("AI Powered Legal Learning Assistant")

# ============================================================
# Sidebar
# ============================================================

with st.sidebar:

    st.title("⚖️ LawIntel")

    st.markdown("---")

    feature = st.radio(
    "Choose Feature",
    [
        "🔍 Legal Search",
        "📄 Legal Summary",
        "❓ MCQ Generator"
    ],
    key="feature_selector"
)

    st.markdown("---")

    st.success("Prototype Version 1.0")

# ============================================================
# Input
# ============================================================

question = st.text_area(
    "Ask your legal question",
    placeholder="Example: What is Article 21?",
    height=120
)


search = st.button("🚀 Generate")

# ============================================================
# Default Values
# ============================================================

answer = ""
docs = []

domain = "-"
documents = 0
sources_count = 0

# ============================================================
# Generate Response
# ============================================================

if search and question:

    print("=" * 80)
    print("SEARCH STARTED")
    print("Feature:", feature)
    print("Question:", question)
    print("=" * 80)

    if feature == "🔍 Legal Search":

        print("Running Legal Search...")

        with st.spinner("Searching legal documents..."):

            answer, docs = ask_question(
                question,
                mode="search"
            )

    elif feature == "📄 Legal Summary":

        print("Running Legal Summary...")

        with st.spinner("Generating legal summary..."):

            answer, docs = ask_question(
                question,
                mode="summary"
            )

    elif feature == "❓ MCQ Generator":

        print("Running MCQ Generator...")

        with st.spinner("Generating MCQs..."):

            answer, docs = generate_mcqs(question)

    print("Returned Documents:", len(docs))

    documents = len(docs)

    unique_sources = {
        doc.metadata.get("source")
        for doc in docs
        if doc.metadata.get("source")
    }

    sources_count = len(unique_sources)

    if docs:
        domain = docs[0].metadata.get("document", "Unknown")
    else:
        domain = "-"

    print("Domain:", domain)
    print("Sources:", sources_count)

# ============================================================
# Metrics
# ============================================================

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("⚖️ Domain", domain)

with col2:
    st.metric("📄 Documents", documents)

with col3:
    st.metric("📚 Sources", sources_count)

# ============================================================
# Output
# ============================================================

if answer:

    st.divider()

    if feature == "🔍 Legal Search":
        st.subheader("📖 Legal Search")

    elif feature == "📄 Legal Summary":
        st.subheader("📄 Legal Summary")

    elif feature == "❓ MCQ Generator":
        st.subheader("❓ MCQ Generator")

    st.markdown(answer)

    # -----------------------------
    # Sources
    # -----------------------------
    if docs:

        st.divider()
        st.subheader("📚 Sources")

        shown = set()

        for doc in docs:

            source = doc.metadata.get("source")

            if source and source not in shown:

                st.success(source)
                shown.add(source)

elif search:

    st.warning("No answer generated.")

    st.markdown(answer)

    st.divider()

    st.subheader("📚 Sources")

    shown = set()

    for doc in docs:

        source = doc.metadata.get("source")

        if source and source not in shown:

            st.success(source)

            shown.add(source)

