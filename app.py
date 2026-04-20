"""
KenyaRAG — Streamlit app for querying Kenya civic datasets via RAG.
Built on LlamaIndex with Claude/GPT as the LLM backend.
"""
import os
import streamlit as st
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="KenyaRAG — Civic AI",
    page_icon="🔍",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.markdown("""
    <style>
    .main > div { padding: 1rem 1rem 2rem; }
    .stTextInput > div > div > input { font-size: 1rem; }
    </style>
""", unsafe_allow_html=True)

st.title("🔍 KenyaRAG")
st.caption("Civic AI — query Kenya's public datasets in plain language")

DATA_DIR = Path(__file__).parent / "civic_data"

@st.cache_resource
def build_index():
    """Build LlamaIndex over Kenya civic CSVs."""
    from llama_index.core import VectorStoreIndex, Document, Settings
    from llama_index.llms.anthropic import Anthropic
    from llama_index.llms.openai import OpenAI

    # Choose LLM
    if os.getenv("ANTHROPIC_API_KEY"):
        Settings.llm = Anthropic(model="claude-haiku-4-5-20251001")
    elif os.getenv("OPENAI_API_KEY"):
        Settings.llm = OpenAI(model="gpt-4o-mini")
    else:
        st.error("Set ANTHROPIC_API_KEY or OPENAI_API_KEY")
        st.stop()

    documents = []
    datasets = {
        "county_budgets_fy2223.csv": "Kenya county budget execution FY 2022/23. Source: Controller of Budget.",
        "mps_seed.csv": "Kenya Member of Parliament records, 13th Parliament. Source: Parliament of Kenya / Mzalendo.",
        "bills_seed.csv": "Parliamentary bills, 13th Parliament. Status, sponsor, reading, votes. Source: Parliament of Kenya.",
        "cdf_seed.csv": "Constituency Development Fund utilisation. Source: Controller of Budget.",
        "saccos_seed.csv": "Registered SACCOs from SASRA registry. Data vintage 2023.",
    }

    for filename, context in datasets.items():
        fpath = DATA_DIR / filename
        if fpath.exists():
            df = pd.read_csv(fpath)
            for _, row in df.iterrows():
                text = f"{context}\n\n" + "\n".join(f"{k}: {v}" for k, v in row.items() if pd.notna(v))
                documents.append(Document(text=text, metadata={"source": filename, "context": context}))

    if not documents:
        st.warning("No civic data found. Place CSV files in the civic_data/ directory.")
        st.stop()

    index = VectorStoreIndex.from_documents(documents, show_progress=True)
    return index.as_query_engine(
        similarity_top_k=8,
        response_mode="compact",
    )

# ── UI ────────────────────────────────────────────────────────
EXAMPLES = [
    "Which counties had the lowest development fund absorption in FY 2022/23?",
    "How many MPs are from the UDA party?",
    "What is the status of the Finance Bill 2024?",
    "Which SACCOs are registered in Nairobi?",
    "What are the CDF allocations for Westlands?",
]

col1, col2 = st.columns([3, 1])
with col1:
    question = st.text_input("Ask a question about Kenya's civic data:", placeholder=EXAMPLES[0])
with col2:
    st.markdown("<br>", unsafe_allow_html=True)
    ask = st.button("Ask", type="primary", use_container_width=True)

st.caption("**Examples:** " + " · ".join(f"*{e}*" for e in EXAMPLES[:3]))

if ask and question:
    with st.spinner("Searching civic data..."):
        engine = build_index()
        response = engine.query(question)

    st.markdown("### Answer")
    st.write(str(response))

    if hasattr(response, "source_nodes") and response.source_nodes:
        with st.expander("📄 Sources", expanded=False):
            for node in response.source_nodes[:5]:
                meta = node.metadata
                st.markdown(f"**{meta.get('source','?')}** — {meta.get('context','')[:80]}")
                st.caption(node.get_content()[:300] + "...")
                st.divider()

# ── Footer ────────────────────────────────────────────────────
st.divider()
st.caption(
    "Data: [Kenya Civic Datasets](https://kaggle.com/datasets/gmahia/kenya-civic-data-parliament-budget-saccos) "
    "· Built on [LlamaIndex](https://llamaindex.ai) "
    "· [GitHub](https://github.com/gabrielmahia/kenya-rag) "
    "· © 2026 Gabriel Mahia"
)
