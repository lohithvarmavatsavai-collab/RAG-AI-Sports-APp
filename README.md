# ⚡ AI Sports Performance Assistant
### Retrieval-Augmented Generation for Evidence-Based Athletic Guidance
**San Jose State University | Graduate Final Project | Spring 2026**

> 🖥️ **Local App URL:** `http://localhost:8502`
> Run: `python3 -m streamlit run app.py --server.port 8502`

---

## 📌 Project Overview
This project builds a **Retrieval-Augmented Generation (RAG)** system that provides sport-specific training, nutrition, and recovery guidance for beginner-to-intermediate athletes. It retrieves evidence from a curated corpus of **36 trusted source documents** (FIFA, ACSM, ISSN, NSCA, NIH, ITF, FIBA, and more) before generating structured, grounded answers — and compares them against a baseline LLM-only approach in a side-by-side interface.

**Supported Sports:** Soccer · Tennis · Basketball · Strength Training
**Guidance Categories:** Training · Nutrition · Recovery
**LLM Backend:** Google Gemini 2.5 Flash
**Embedding Model:** `all-MiniLM-L6-v2` (SentenceTransformers)
**Vector Store:** FAISS `IndexFlatL2`

---

## 🗂️ Project Structure
```
sports_rag_project/
├── app.py                    # Streamlit web application (main entry point)
├── retrieve.py               # FAISS semantic retrieval module
├── generate.py               # RAG + baseline LLM generation module
├── clean_data.py             # Text cleaning pipeline
├── chunk_data.py             # 150-word sliding window chunking
├── embed_and_index.py        # Embedding + FAISS index builder
├── metadata.csv              # 36 source metadata records
├── chunks.csv                # 123 text chunks with full metadata
├── evaluation_questions.csv  # 10 benchmark evaluation questions
├── evaluation_results.csv    # RAG vs Baseline comparison scores
├── model_card.md             # Model card (system documentation)
├── model_card.html           # Model card (HTML version)
├── requirements.txt          # Python dependencies
├── .env.example              # API key template (safe to share)
├── data_raw/                 # Original source text files (36 docs)
├── data_clean/               # Cleaned versions of source files
├── faiss_index/              # FAISS vector index
├── results/                  # Output logs / evaluation JSON
├── screenshots/              # App screenshots
├── report/                   # Final project report (Markdown)
└── presentation/             # Slides / presentation materials
```

---

## ⚙️ Setup Instructions

### Step 1 — Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/ai-sports-rag.git
cd ai-sports-rag
```

### Step 2 — Install Dependencies
```bash
pip3 install -r requirements.txt
```

### Step 3 — Add Your Google Gemini API Key
```bash
cp .env.example .env
# Open .env and add your key:
# GOOGLE_API_KEY=your_key_here
```
Get a free key at: https://aistudio.google.com/app/apikey

### Step 4 — The Data Pipeline (Pre-built — Skip if files exist)
The FAISS index and chunks are already included. Only run these if you need to rebuild from scratch:
```bash
python3 clean_data.py        # Clean raw source files
python3 chunk_data.py        # Chunk into 150-word windows
python3 embed_and_index.py   # Build FAISS vector index
```

### Step 5 — Launch the App
```bash
python3 -m streamlit run app.py --server.port 8502
```
Open in browser: **http://localhost:8502**

---

## 🔬 How the RAG Pipeline Works

```
[User: Sport + Goal + Category + Experience + Weight + Age + Question]
                          │
                          ▼
    [Query Embedding — all-MiniLM-L6-v2 → 384-dim vector]
                          │
                          ▼
    [Pre-filter on Sport × Category from FAISS candidate pool]
                          │
                          ▼
    [FAISS IndexFlatL2 → Top-K nearest chunks by L2 distance]
                          │
                          ▼
    [Prompt Assembly: Profile Directives + Chunks + Structure]
                          │
                          ▼
    [Gemini 2.5 Flash → Real-time streaming response]
                          │
                          ▼
    [Streamlit: Side-by-side RAG vs Baseline comparison display]
```

---

## 📊 Evaluation Results Summary

| Criterion | RAG (avg/5) | Baseline (avg/5) | RAG Advantage |
|---|---|---|---|
| Relevance | 4.5 | 3.8 | +0.7 |
| Groundedness | 4.6 | 2.1 | **+2.5** |
| Specificity | 4.3 | 3.2 | +1.1 |
| Structure | 4.7 | 4.5 | +0.2 |
| Safety | 4.9 | 4.7 | +0.2 |
| **Overall** | **4.6** | **3.7** | **+0.9** |

Full per-question scores: `evaluation_results.csv`

---

## 📚 Trusted Sources Used
| Organization | Type | Sports |
|---|---|---|
| FIFA / UEFA / F-MARC | Governing Bodies | Soccer |
| ITF / USTA | Governing Bodies | Tennis |
| FIBA / NBA Academy | Governing Bodies | Basketball |
| NSCA / ACSM | Professional Associations | Strength Training |
| ISSN | Position Stands | All Sports |
| NIH Office of Dietary Supplements | Government Agency | Strength Training |
| GSSI (Gatorade Sports Science Institute) | Applied Research | Soccer / Basketball |
| BJSM / JSS / JSCR / JISSN | Peer-Reviewed Journals | All Sports |

---

## 🧠 Key Features
- **RAG vs Baseline Comparison** — Side-by-side display isolates the impact of retrieval
- **6-Factor Readiness Score** — Physiological readiness gauge (Experience, Load, Goal, Weight, Sport Intensity, Age)
- **Profile-Aware Prompting** — Three hard directives lock generation to sport + goal + category
- **Graceful Error Handling** — 503/429 API errors display friendly messages, never crash the app
- **Real-time Streaming** — `st.write_stream()` for live response display

---

## ⚠️ Limitations & Ethical Scope
- Does **not** diagnose injuries or prescribe medical treatment
- Does **not** recommend supplements or provide medical nutrition therapy
- Sources are curated summaries — always verify recommendations with primary literature
- LLM outputs may contain errors; human expert review is recommended

---

## 👨‍🎓 Academic Context
- **Institution:** San Jose State University
- **Project Type:** Graduate Final Project — Spring 2026
- **Methodology:** RAG · SentenceTransformers · FAISS · Google Gemini 2.5 Flash · Streamlit
- **Full Report:** `report/project_report_final.md`
