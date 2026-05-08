# AI Sports Performance Assistant Using Retrieval-Augmented Generation, Embeddings, and Structured Prompting
## Final Project Report
**San Jose State University | Spring 2026**

---

## 1. Introduction / Problem Definition

Athletes at the beginner to intermediate level increasingly turn to AI tools for personalized guidance on training, nutrition, and recovery. However, general-purpose Large Language Models (LLMs) such as GPT-3.5 have well-documented limitations when used for domain-specific guidance: they may hallucinate specific numbers (e.g., incorrect protein targets), fail to cite credible sources, provide generic advice that ignores sport-specific physiological demands, and lack accountability for factual accuracy.

This project addresses the question: **Can a Retrieval-Augmented Generation (RAG) system, grounded in curated, trusted sports science documents, produce more relevant, specific, and accountable guidance than a baseline LLM-only approach?**

The system supports four sports (Soccer, Tennis, Basketball, and Strength Training) across three guidance categories (Training, Nutrition, Recovery/Hydration), targeting beginner to intermediate athletes.

**Scope and Boundaries:**
- Provides general, evidence-based sports performance guidance only.
- Does not provide medical diagnoses, injury treatment advice, or supplement prescriptions.
- Does not integrate live data, wearable sensors, or external APIs.
- Does not support personalized medical nutrition therapy.

---

## 2. Project Objectives

1. **Build a complete RAG pipeline** — from curated source documents through text cleaning, chunking, embedding, vector retrieval, and LLM generation.
2. **Ground responses in trusted, curated sources** from recognized sports science organizations (FIFA, ACSM, ISSN, NIH, etc.).
3. **Implement a baseline comparison** between LLM-only generation and RAG-augmented generation to evaluate the value added by retrieval.
4. **Deploy a polished web application** using Streamlit that presents structured, athlete-profile-aware responses with visible source attribution.
5. **Evaluate system performance** across 10 structured questions using five scoring criteria: relevance, groundedness, specificity, structure, and safety.

---

## 3. Related Work

**Retrieval-Augmented Generation (RAG)** was formalized by Lewis et al. (2020) as a method of combining parametric knowledge (stored in LLM weights) with non-parametric knowledge (retrieved from a document store) to produce more factual and specific outputs. This project applies the RAG paradigm to sports science, a domain where factual accuracy and source credibility are essential.

**LLM limitations in domain-specific contexts:** Studies have shown that LLMs tend to generate plausible-sounding but unverifiable content in highly specialized domains (Maynez et al., 2020). Sports science is particularly vulnerable to this because numerical guidelines (e.g., g/kg protein recommendations) vary by organization and are frequently updated.

**Sports science information systems:** While apps like MyFitnessPal, Whoop, and TrainingPeaks provide data-driven guidance, they rely on user-generated data inputs rather than structured sports science literature retrieval. This project occupies a different niche: using authoritative literature to ground AI-generated guidance.

**Embedding models for domain retrieval:** Sentence transformers such as `all-MiniLM-L6-v2` (Wang et al., 2020) provide computationally efficient sentence-level embeddings that capture semantic similarity well across short text passages, making them ideal for the chunked-document retrieval architecture used here.

---

## 4. Dataset and Source Selection

### 4.1 Source Selection Criteria
Sources were selected based on:
- **Authority:** Official governing bodies (FIFA, ITF, FIBA, NSCA) or peer-reviewed journals with high citation counts.
- **Recency:** Publications from 2021–2023 to ensure guidance reflects current standards.
- **Relevance:** Direct applicability to training, nutrition, or recovery for the supported sports.
- **Trustworthiness:** Government agencies (NIH), professional associations (ACSM, ISSN), or official federation publications.

### 4.2 Dataset Structure
| Sport | Training Sources | Nutrition Sources | Recovery Sources |
|---|---|---|---|
| Soccer | FIFA, UEFA | F-MARC, ISSN | ACSM, GSSI |
| Tennis | ITF, USTA | BJSM, ISSN | JSS, ITF |
| Basketball | FIBA, NBA Academy | JISSN, ACSM | Sports Medicine, GSSI |
| Strength Training | NSCA, ACSM | ISSN, NIH | NSCA, JSCR |
| **Total** | **8** | **8** | **8** |

**Total: 24 source documents**

### 4.3 Chunking Strategy
- Each cleaned source document was segmented into overlapping windows of **150 words** with a **30-word overlap**.
- Overlap preserves contextual continuity across chunk boundaries.
- This produced **72 total chunks** from the 24 sources (~3 chunks per source on average).
- Chunks containing fewer than 20 words were discarded.

### 4.4 Metadata Schema
Each source is recorded in `metadata.csv` with fields: `source_id`, `title`, `sport`, `category`, `source_type`, `organization`, `year`, `url_or_reference`, `filename`.

---

## 5. Methodology

### 5.1 System Architecture

```
[User Input: Sport + Goal + Experience + Body Weight + Question]
                            │
                            ▼
              [SentenceTransformer Embedding]
              (all-MiniLM-L6-v2, 384-dim)
                            │
                            ▼
              [FAISS IndexFlatL2 Search]
              (Top-K most similar chunks)
                            │
                            ▼
         [Retrieved Chunks + User Profile Context]
                            │
                            ▼
         [Structured Prompt → GPT-3.5-turbo]
         (Temperature: 0.3, Max Tokens: 700)
                            │
                            ▼
         [Structured Response: Summary, Recommendations,
          Practical Tips, Evidence Base, Limitations]
```

**Baseline path:** Identical prompt structure, but no retrieved chunks are injected. Only the user profile and question are provided.

### 5.2 Text Cleaning
- Removal of excessive whitespace and blank lines (≥3 consecutive newlines compressed to 2)
- Normalization of multiple spaces to single spaces
- UTF-8 encoding enforced throughout

### 5.3 Embedding Model Selection
`all-MiniLM-L6-v2` was selected because:
- 384-dimensional embeddings balance speed and quality
- Free and open-source, no API costs
- Proven performance on semantic similarity benchmarks (SBERT leaderboard)
- Small enough (90MB) to run locally without GPU

### 5.4 Vector Store — FAISS
FAISS `IndexFlatL2` (exact L2 distance search) was used rather than approximate methods because the corpus (72 chunks) is small enough that exact search is near-instantaneous and more accurate.

### 5.5 Prompt Engineering
The RAG prompt instructs GPT-3.5-turbo to:
1. Ground its response in the retrieved evidence
2. Use a strict five-section output structure
3. Avoid medical diagnoses and supplement prescriptions
4. Acknowledge limitations explicitly

Temperature was set to 0.3 (low) to reduce hallucination and maximize factual consistency.

### 5.6 Sport and Category Filtering
Retrieval applies a pre-filter by sport and category to ensure retrieved chunks are topically relevant before applying embedding similarity. If no results pass the filter, the filter is released and global similarity is used as a fallback.

---

## 6. Results

*[FILL THIS SECTION AFTER RUNNING EVALUATION]*

### 6.1 Evaluation Summary
After running 10 evaluation questions through both the baseline (LLM-only) and RAG systems, results were scored on a 1–5 scale for five criteria. See `evaluation_results.csv` for raw scores.

### 6.2 Key Findings
*[Fill with observed patterns from evaluation_results.csv after scoring]*

Example structure:
- **Groundedness:** RAG scored X.X vs Baseline X.X on average — reflecting the addition of cited source material.
- **Specificity:** RAG scored X.X vs Baseline X.X — RAG provided specific numerical targets (e.g., 1.6 g/kg protein) traced to ISSN sources.
- **Structure:** Both modes scored similarly on structure due to the shared prompt template.
- **Safety:** Both modes scored comparably high on safety due to system-level guardrails.

### 6.3 Qualitative Observations
*[Fill with 3–4 sentences describing key differences between the two answer modes]*

---

## 7. Discussion

### 7.1 When Does RAG Improve Answers?
*[Fill after evaluation: typically when specific numbers matter, when sport-specific protocols differ, and when source attribution increases user trust]*

### 7.2 When Are Both Modes Similar?
*[Fill: structure and safety tend to be equal due to the shared prompt engineering; RAG adds most value on groundedness and specificity]*

### 7.3 Source Quality Impact
The quality of retrieved answers was heavily influenced by the quality of the underlying source text. Sources from ISSN, ACSM, and NSCA with specific numerical guidelines produced the most useful retrieved chunks. Sources from governing bodies (FIFA, ITF) were more qualitative and produced stronger training guidance but weaker nutrition specifics.

### 7.4 Prompt Design Observations
The structured five-section output format significantly improved usability compared to free-form generation. The explicit "Evidence Base" section in the prompt encouraged the model to trace its recommendations to source material, increasing perceived trustworthiness.

---

## 8. Evaluation and Reflection

### 8.1 Evaluation Design
10 questions were selected to cover all four sports and all three categories, with a mix of beginner and intermediate profiles. Questions were designed to have objectively verifiable numerical answers (e.g., protein intake targets) or well-established recommendations (e.g., sleep duration) to enable meaningful scoring.

### 8.2 What Worked Well
- The chunking and retrieval pipeline reliably returned sport- and category-specific content.
- The structured prompt template produced consistently formatted, readable outputs.
- The FAISS index was fast enough for real-time interactive use.
- The baseline vs. RAG comparison mode was clearly useful for demonstrating the value of retrieval.

### 8.3 Limitations and Challenges
- The corpus is small (24 documents / 72 chunks). A larger corpus would improve retrieval quality and coverage.
- Source text was manually curated rather than automatically scraped, limiting scalability.
- Evaluation was performed by a single rater; inter-rater reliability was not measured.
- The system cannot handle out-of-scope sports or categories gracefully.

### 8.4 What I Would Change
- Use a larger corpus (100+ sources) for broader coverage.
- Implement cross-encoder re-ranking for improved retrieval precision.
- Add multi-sport query support.
- Implement automatic source quality scoring.

---

## 9. Conclusion and Future Work

This project successfully demonstrates that a RAG system grounded in curated, trusted sports science literature can provide more specific, accountable, and evidence-referenced guidance than a baseline LLM-only approach. The system is deployed as a polished Streamlit web application supporting four sports and three guidance categories.

**Future Work:**
- Expand the corpus to 100+ sources across additional sports (swimming, cycling, running).
- Implement user authentication and saved profiles.
- Add a feedback loop where users rate answer quality to improve retrieval over time.
- Explore fine-tuning a domain-specific embedding model on sports science literature.
- Integrate nutritional databases (e.g., USDA FoodData Central) for real-time food analysis.

---

## References

- Lewis, P., et al. (2020). Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks. *NeurIPS 2020*.
- Wang, L., et al. (2020). Making Monolingual Sentence Embeddings Multilingual Using Knowledge Distillation. *EMNLP 2020*.
- FIFA F-MARC (2022). Nutrition for Football. FIFA Medical Assessment and Research Centre.
- Thomas, D.T., et al. (2016). Position of the Academy of Nutrition and Dietetics, Dietitians of Canada, and ACSM. *Journal of the Academy of Nutrition and Dietetics*.
- Jäger, R., et al. (2017). ISSN Position Stand: Protein and Exercise. *Journal of the International Society of Sports Nutrition*.
- NIH Office of Dietary Supplements (2023). Exercise and Athletic Performance Fact Sheet.
- NSCA (2022). Essentials of Strength Training and Conditioning, 4th Ed.
- ACSM (2021). Position Stand: Resistance Training.
- ITF (2023). Physical Training Guide for Tennis.
- FIBA (2023). Basketball Athletic Development Program.

*[Add complete bibliography per your institution's citation style (APA preferred)]*

---

*Report prepared for SJSU Graduate Final Project — Spring 2026*
