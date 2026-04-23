# 🔍 KenyaRAG — Civic AI for Kenya

> Retrieval-augmented generation over Kenya's civic datasets. Ask questions about parliament records, county budgets, SACCO data, and constitutional rights — and get grounded, cited answers.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://python.org)
[![Built on LlamaIndex](https://img.shields.io/badge/Built%20on-LlamaIndex-purple)](https://llamaindex.ai)

## What it does

KenyaRAG turns Kenya's public civic datasets into a queryable knowledge base. Built on [LlamaIndex](https://github.com/run-llama/llama_index) with Kenya-specific document loaders, retrievers, and citation formatting.

**Ask questions like:**
- *"Which counties had the lowest development fund absorption in FY 2022/23?"*
- *"What is the CDF allocation for Westlands constituency?"*
- *"Which MPs have voted against the Finance Bill the most times?"*
- *"What does the Constitution say about riparian land rights?"*

## Data sources

All data from our published civic dataset:

| Dataset | Source | DOI |
|---------|--------|-----|
| Parliamentary bills | Parliament of Kenya | [Kaggle](https://doi.org/10.34740/kaggle/dsv/15473045) |
| County budgets FY22/23 | Controller of Budget | [HuggingFace](https://doi.org/10.57967/hf/8223) |
| MP records | Parliament / Mzalendo | [Zenodo](https://zenodo.org) |
| SACCO registry | SASRA | [Kaggle](https://doi.org/10.34740/kaggle/dsv/15473045) |
| CDF utilisation | Controller of Budget | [HuggingFace](https://doi.org/10.57967/hf/8223) |

## Architecture

```
civic_data/          ← Kenya civic CSVs (from Kaggle/HuggingFace datasets)
    ├── mps_seed.csv
    ├── county_budgets_fy2223.csv
    ├── bills_seed.csv
    ├── cdf_seed.csv
    └── saccos_seed.csv
    
kenya_rag/
    ├── loaders/     ← Custom LlamaIndex document loaders per dataset
    ├── indices/     ← Vector + keyword index builders
    ├── query/       ← Query engines with Kenya-specific prompts
    └── app.py       ← Streamlit interface
```

Built on [LlamaIndex](https://github.com/run-llama/llama_index) — the leading open-source RAG framework (30k+ GitHub stars).

## Quickstart

```bash
pip install kenya-rag
# or from source:
git clone https://github.com/gabrielmahia/kenya-rag
cd kenya-rag
pip install -r requirements.txt

export OPENAI_API_KEY=your_key   # or ANTHROPIC_API_KEY
streamlit run app.py
```

## Why this exists

Kenya's public data is published but not accessible. A Controller of Budget PDF exists. 350-page Hansard records exist. SASRA SACCO registries exist. None of them are queryable in plain language — especially not in Kiswahili.

KenyaRAG closes that gap using retrieval-augmented generation: the LLM answers from the actual documents, not from its training data. Every answer cites its source row.

## Related tools

Part of the [gabrielmahia civic portfolio](https://gabrielmahia.github.io):

- [Hesabu](https://hesabu.streamlit.app) — County budget execution dashboard
- [Macho ya Wananchi](https://macho-ya-wananchi.streamlit.app) — MP accountability tracker
- [Jibu](https://jibuyangu.streamlit.app) — AI civic rights assistant
- [mpesa-mcp](https://pypi.org/project/mpesa-mcp/) — M-Pesa MCP server

## Citation

If you use KenyaRAG or the underlying datasets in research or tools, please cite:

```bibtex
@misc{mahia2026kenyarag,
  author    = {Gabriel Mahia},
  title     = {KenyaRAG: Retrieval-Augmented Generation over Kenya Civic Datasets},
  year      = {2026},
  url       = {https://github.com/gabrielmahia/kenya-rag}
}
```

Dataset DOI: `10.34740/kaggle/dsv/15473045` / `10.57967/hf/8223`

## IP & Collaboration

© 2026 Gabriel Mahia · [contact@aikungfu.dev](mailto:contact@aikungfu.dev)
License: MIT — share with attribution, no commercial use, no derivatives.
Not affiliated with Parliament of Kenya, Controller of Budget, or SASRA.
