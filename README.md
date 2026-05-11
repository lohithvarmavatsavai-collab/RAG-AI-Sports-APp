# RAG-Based AI Sports Performance Assistant

This is my final project for my graduate course at San Jose State University (Spring 2026). I built a sports performance assistant that uses Retrieval-Augmented Generation to give athletes better, more evidence-backed advice than a regular chatbot would.

The basic idea: instead of letting the AI make up answers from memory, I force it to read actual sports science documents first (from FIFA, ACSM, ISSN, etc.) and then generate answers based on that evidence. I also built a comparison mode so you can see the difference between a RAG answer and a plain LLM answer side by side.

## What it does

- Covers 4 sports: Soccer, Tennis, Basketball, Strength Training
- 3 guidance categories: Training, Nutrition, Recovery
- You fill in your athlete profile (sport, goal, experience level, weight, age, training days/week)
- It retrieves relevant chunks from 36 curated source documents using FAISS
- Then Gemini 2.5 Flash generates a structured answer grounded in that evidence
- There's also a readiness score based on 6 factors (experience, training load, goal type, weight, sport intensity, age)

## How to run it locally

You'll need Python 3.9+ and a Google Gemini API key (free from https://aistudio.google.com/app/apikey).

```bash
# install dependencies
pip install -r requirements.txt

# create your .env file
cp .env.example .env
# then open .env and paste your GOOGLE_API_KEY

# run the app
python3 -m streamlit run app.py --server.port 8502
```

App opens at http://localhost:8502

## Running on Google Colab

If you don't want to set things up locally, there's a Colab notebook included (`AI_Sports_RAG_Pipeline.ipynb`). It walks through the full pipeline — retrieval, generation, evaluation — without needing to install anything on your machine.

You'll need to upload a few data files when Colab prompts you: `chunks.csv`, `metadata.csv`, `sports_rag.index`, and `evaluation_questions.csv`.

## Project structure

```
├── app.py                    # main Streamlit app
├── retrieve.py               # FAISS retrieval logic
├── generate.py               # Gemini prompt construction + generation
├── clean_data.py             # text cleaning script
├── chunk_data.py             # splits documents into 150-word chunks
├── embed_and_index.py        # builds the FAISS vector index
├── chunks.csv                # the 123 text chunks with metadata
├── metadata.csv              # info about all 36 source documents
├── faiss_index/              # the FAISS index file
├── data_raw/                 # original source texts
├── data_clean/               # cleaned versions
├── evaluation_questions.csv  # 10 benchmark questions I used for testing
├── evaluation_results.csv    # scores from my RAG vs baseline comparison
├── model_card.md             # model documentation
├── report/                   # my final written report
├── AI_Sports_RAG_Pipeline.ipynb  # Colab notebook version
└── requirements.txt
```

## How the RAG pipeline works

1. User submits a question along with their athlete profile
2. The question gets embedded using `all-MiniLM-L6-v2` (sentence transformer, 384 dimensions)
3. FAISS searches for the most similar chunks, filtered by sport and category
4. Those chunks get injected into a structured prompt alongside the user's profile
5. Gemini 2.5 Flash generates the answer, constrained to follow a specific section format
6. The baseline mode runs the same prompt but without any retrieved chunks, so you can compare

## Sources I used

I curated 36 documents from organizations like FIFA, ACSM, ISSN, NSCA, NIH, ITF, FIBA, and others. Full list is in `metadata.csv`. I specifically picked sources that had concrete numerical guidelines (like protein g/kg recommendations or heart rate zone targets) since those are the hardest things for an LLM to get right without retrieval.

## Evaluation

I tested 10 questions across all 4 sports and scored both the RAG and baseline answers on relevance, groundedness, specificity, structure, and safety (each on a 1-5 scale). The biggest gap was in groundedness — the RAG system averaged 4.6 vs 2.1 for baseline, which makes sense because the baseline has no source material to cite.

## Limitations

- This doesn't give medical advice — it says so explicitly in every response
- The knowledge base is intentionally small (36 docs). A production system would need way more
- I only tested with one evaluator (me), so there's potential scoring bias
- The Streamlit app runs locally only unless you deploy it somewhere

## Built with

- Python, Streamlit
- Google Gemini 2.5 Flash
- FAISS (Facebook AI Similarity Search)
- SentenceTransformers (`all-MiniLM-L6-v2`)
- Pandas, NumPy, Matplotlib
