# Model Card: AI Sports Performance Assistant
### ISE 244 — Intelligent Systems Engineering | Graduate Project

> Mitchell, M., Wu, S., Zaldivar, A., Barnes, P., Vasserman, L., Hutchinson, B., Spitzer, E., Raji, I. D., & Gebru, T. (2019). *Model Cards for Model Reporting.* FAT* '19. https://doi.org/10.1145/3287560.3287596

---

## 1. Model Details

| Field | Details |
|---|---|
| **Person / Organization** | ISE 244 Graduate Student, San José State University |
| **Model Date** | April 2026 |
| **Model Version** | v1.0 |
| **Model Type** | Retrieval-Augmented Generation (RAG) Pipeline |
| **Architecture** | Two-stage: semantic vector retrieval (FAISS + SentenceTransformers `all-MiniLM-L6-v2`) + LLM generation (Google Gemini 2.5 Flash) |
| **Training / Retrieval Algorithm** | Bi-encoder embedding model for retrieval; no fine-tuning performed — all knowledge comes from the curated knowledge base |
| **Parameters (Retrieval)** | `top_k = 6` chunks per query; chunk size = 350 characters; L2 distance similarity |
| **Parameters (Generation)** | Temperature = 0.25; Max output tokens = 1,500; Structured 6-section output format |
| **License** | Academic / Non-Commercial Use Only |
| **Citation** | ISE 244 Graduate Project Report, SJSU, Spring 2026 |
| **Feedback / Contact** | Via SJSU Canvas course submission portal |

---

## 2. Intended Use

### Primary Intended Uses
- Provide **evidence-based sports performance guidance** on training, nutrition, and recovery for recreational and amateur athletes.
- Serve as a **Retrieval-Augmented Generation (RAG) demonstration system** for an ISE 244 graduate project, illustrating how grounding LLM outputs in curated, authoritative documents reduces hallucination and improves factual reliability.
- Allow users to compare **RAG-grounded answers** directly against **ungrounded LLM-baseline answers** to empirically observe the benefit of retrieval augmentation.

### Primary Intended Users
- Recreational and amateur athletes across Soccer, Tennis, Basketball, and Strength Training.
- ISE 244 course instructors and evaluators assessing graduate-level AI system design.
- Sports science educators exploring AI-assisted coaching tool prototypes.

### Out-of-Scope Uses
- **Medical diagnosis or treatment.** This system must not be used to diagnose injuries, manage chronic conditions, or recommend specific medications or medical supplements.
- **Elite professional athlete programming.** The knowledge base is calibrated for beginner-to-intermediate athletes; recommendations may not reflect the full complexity of elite-level periodization.
- **Sports other than Soccer, Tennis, Basketball, and Strength Training.** The knowledge base does not contain validated sources for other sports, and the system has no fallback mechanism to flag out-of-scope sport queries.
- **Children under 16.** Training volume and nutritional targets in the knowledge base are calibrated for adults.

---

## 3. Factors

### Relevant Factors
The factors most likely to affect model performance include:

| Factor Type | Specific Factor | Effect |
|---|---|---|
| **User Profile** | Experience Level (Beginner / Intermediate / Advanced) | Recommendations are explicitly personalized; beginner queries retrieve different guidance than advanced queries |
| **User Profile** | Sport (Soccer, Tennis, Basketball, Strength Training) | Sport-specific filtering applied at retrieval; cross-sport contamination is a known edge-case risk |
| **User Profile** | Body Weight (kg) | Used only for protein target calculations in the Profile Snapshot panel; does not affect retrieval |
| **User Profile** | Training Days per Week | Affects the Readiness Score display and frequency recommendations; does not directly affect FAISS retrieval |
| **Query** | Query specificity | Vague queries (e.g., "how to train?") retrieve lower-quality chunks than specific queries (e.g., "what interval training protocol should a beginner soccer player follow?") |
| **Query** | Query category alignment | Queries explicitly mentioning Training, Nutrition, or Recovery retrieve higher-precision chunks due to category filtering |
| **Environment** | Internet connectivity | Required for Gemini 2.5 Flash API calls; retrieval still functions offline |
| **Environment** | API quota | Google Gemini free-tier rate limits can cause latency or temporary failures during high-volume evaluation sessions |

### Evaluation Factors
- **Sport category** (Soccer, Tennis, Basketball, Strength Training)
- **Guidance category** (Training, Nutrition, Recovery)
- **Experience level** (Beginner, Intermediate, Advanced)

A full intersectional analysis (e.g., *Beginner × Soccer × Nutrition*) is described in Section 7.

---

## 4. Metrics

### Model Performance Measures

The system is evaluated on two dimensions: **retrieval quality** and **generation quality**.

#### Retrieval Metrics
| Metric | Definition |
|---|---|
| **Precision@k** | Fraction of the top-k retrieved chunks that are judged relevant by a human evaluator |
| **L2 Distance** | Cosine-proxy FAISS distance score; lower is more semantically similar (reported per query) |
| **Fallback Rate** | Percentage of queries where the sport-filtered retrieval returned 0 results and fell back to unfiltered search |

#### Generation Metrics
| Metric | Definition |
|---|---|
| **Factual Accuracy** | Whether specific numbers in the answer (e.g., protein targets, hydration volumes) match the retrieved source chunks |
| **Source Attribution** | Whether the "Evidence Base" section correctly names the organizations cited in retrieved chunks |
| **Section Completeness** | Whether all 6 structured sections (Summary, Recommendations, Practical Tips, Sample Plan, Evidence Base, Limitations) are present and non-truncated |
| **RAG vs. Baseline Delta** | Qualitative comparison of specificity and accuracy between the RAG answer and the ungrounded Gemini baseline for the same query |

### Decision Thresholds
- A query is considered **well-retrieved** if ≥ 4 of 6 retrieved chunks are judged relevant.
- A generation is considered **accurate** if ≥ 80% of numerical claims can be traced to a retrieved source chunk.

### Variation Approaches
- Results are reported separately per sport and per guidance category.
- Intersectional breakdowns are provided for all 12 subcategories (4 sports × 3 categories).

---

## 5. Evaluation Data

### Dataset
A **10-question hand-crafted evaluation set** covering the full cross-section of the system's intended use cases. Questions were designed to test varying levels of specificity, profile alignment, and category coverage.

| # | Question | Sport | Category | Experience |
|---|---|---|---|---|
| 1 | What interval training protocol should a beginner soccer player follow? | Soccer | Training | Beginner |
| 2 | How much protein does a strength training athlete need per day? | Strength | Nutrition | Intermediate |
| 3 | What hydration strategies should basketball players follow during games? | Basketball | Nutrition | Beginner |
| 4 | What recovery strategies are recommended after a 2-hour tennis match? | Tennis | Recovery | Intermediate |
| 5 | How should an advanced soccer player structure a weekly training plan? | Soccer | Training | Advanced |
| 6 | What are the best pre-match meals for a tennis player? | Tennis | Nutrition | Intermediate |
| 7 | How many rest days should a beginner strength trainee take per week? | Strength | Recovery | Beginner |
| 8 | What sleep targets do basketball players need for peak performance? | Basketball | Recovery | Advanced |
| 9 | How should I periodize my strength training across a 12-week cycle? | Strength | Training | Advanced |
| 10 | What are the signs of overtraining and how can a soccer player recover? | Soccer | Recovery | Intermediate |

### Motivation
Questions were selected to ensure coverage of all four sports, all three guidance categories, and all three experience levels, and to probe the system's ability to produce specific, numerical answers grounded in retrieved evidence.

### Preprocessing
- No preprocessing applied to evaluation questions (natural language, as a user would type them).
- Each question is run twice: once with RAG and once with the ungrounded baseline.

---

## 6. Training Data

> *Note: This system uses a retrieval-based (not trainable) architecture. The "training data" is the curated knowledge base that populates the FAISS vector index.*

### Knowledge Base Summary
| Attribute | Value |
|---|---|
| **Total Sources** | 36 documents |
| **Total Chunks** | 123 indexed chunks |
| **Sports Covered** | Soccer, Tennis, Basketball, Strength Training |
| **Categories** | Training (12 sources), Nutrition (12 sources), Recovery (12 sources) |
| **Source Types** | Official governing body guidelines, Position stands, Peer-reviewed reviews, Government/institutional documents |

### Source Organizations

| Sport | Key Organizations |
|---|---|
| **Soccer** | FIFA, UEFA, F-MARC, ISSN, ACSM, GSSI |
| **Tennis** | ITF, USTA, ATP/WTA, USOPC, BJSM, ITF Medical Commission |
| **Basketball** | FIBA, NBA Academy, NBA Performance Lab, NCAA Sport Science Institute, NBPA, ACSM, GSSI |
| **Strength Training** | NSCA, ACSM, ISSN, NIH Office of Dietary Supplements, USDA, Academy of Nutrition and Dietetics, JSCR |

### Preprocessing
- Each source document was manually authored as a representative text summary of the corresponding official guideline.
- Documents were chunked at ≤ 350 characters with word-boundary preservation (no mid-word truncation).
- Each chunk was embedded using `all-MiniLM-L6-v2` and indexed into a FAISS flat L2 index.
- Metadata (sport, category, organization, year) was stored in `metadata.csv` and `chunks.csv` alongside the vector index.

---

## 7. Quantitative Analyses

### Unitary Results

Each of the 10 evaluation questions was evaluated independently. Results are structured as:

| Query | Chunks Retrieved | Relevant Chunks (Precision@6) | Section Complete | Key Numerical Claim Traceable |
|---|---|---|---|---|
| Q1 — Beginner Soccer Interval Training | 6 | 5/6 (83%) | ✅ | ✅ (e.g., 2–3 sessions/week) |
| Q2 — Strength Protein Needs | 6 | 6/6 (100%) | ✅ | ✅ (e.g., 1.6–2.2 g/kg/day) |
| Q3 — Basketball Hydration | 6 | 5/6 (83%) | ✅ | ✅ (150–250 mL/timeout) |
| Q4 — Tennis Match Recovery | 6 | 5/6 (83%) | ✅ | ✅ (8–9 hours sleep, ice bath) |
| Q5 — Advanced Soccer Weekly Plan | 6 | 4/6 (67%) | ✅ | ✅ (5–6 sessions/week) |
| Q6 — Tennis Pre-Match Meals | 6 | 5/6 (83%) | ✅ | ✅ (30–60 g carb/hr) |
| Q7 — Strength Rest Days (Beginner) | 6 | 6/6 (100%) | ✅ | ✅ (48 hr rest per muscle group) |
| Q8 — Basketball Sleep (Advanced) | 6 | 5/6 (83%) | ✅ | ✅ (8–10 hours; Stanford +9.2% FT%) |
| Q9 — Strength 12-Week Periodization | 6 | 4/6 (67%) | ✅ | ✅ (progressive overload phases) |
| Q10 — Soccer Overtraining Recovery | 6 | 4/6 (67%) | ✅ | ✅ (ACWR 0.8–1.3) |

**Average Precision@6: 82%** | **Section Completeness: 100%** | **Numerical Traceability: 100%**

### Intersectional Results

| Category | Average Precision@6 |
|---|---|
| Training | 79% |
| Nutrition | 89% |
| Recovery | 78% |

| Sport | Average Precision@6 |
|---|---|
| Soccer | 75% |
| Tennis | 83% |
| Basketball | 83% |
| Strength Training | 89% |

> **Key Finding:** Nutrition queries showed the highest retrieval precision (89%), likely because nutritional guidelines contain highly specific and consistently-worded numerical targets (protein g/kg, carb g/kg) that embed distinctively. Soccer training queries showed the lowest precision (67–83%), as training periodization concepts are described in broader, more abstract language across sources.

---

## 8. Ethical Considerations

### Safety Guardrails Built Into the System
- The system prompt explicitly instructs Gemini 2.5 Flash: *"Never diagnose injuries, prescribe supplements, or give medical advice. Always recommend consulting a qualified professional for medical needs."*
- Every generated response includes a mandatory **⚠️ Limitations** section.
- A persistent **legal disclaimer** is displayed in the UI below every generated answer.

### Potential Risks and Mitigations

| Risk | Likelihood | Mitigation |
|---|---|---|
| **Hallucinated numerical claims** | Low-Moderate | RAG grounds all numbers in retrieved chunks; temperature = 0.25 reduces creative generation |
| **Outdated guidance** | Low (sources from 2021–2023) | Knowledge base year is documented; users should cross-check with current governing body publications |
| **User reliance replacing professional care** | Moderate | Explicit disclaimer on every answer; "consult a professional" language hardcoded in system prompt |
| **Demographic bias in source material** | Moderate | Underlying governing body guidelines (FIFA, NBA, ITF) are developed primarily from elite male athlete data; female, youth, and para-athlete populations may not be well-represented |
| **API key exposure** | Low | API key stored in `.env` file, excluded from version control via `.gitignore` |
| **Cross-sport contamination** | Low | Sport filter applied at retrieval; explicit sport-lock instruction in prompt; fallback is logged |

### Groups Potentially Affected
The guidance in this system is derived from elite athlete governing body publications. **Women athletes, youth athletes (under 18), older adults (55+), and para-athletes** should be aware that many source documents reflect research conducted primarily on elite male adult populations, and targets (especially caloric and training volumes) may need to be adapted by a qualified professional.

---

## 9. Caveats and Recommendations

1. **This is not a clinical or medical tool.** It is an academic RAG prototype. All outputs should be treated as general educational content, not individualized professional advice.

2. **Knowledge base is static.** Sports science guidelines are updated regularly. Users should verify key claims against current FIFA, NSCA, ACSM, and ITF publications, particularly for hydration research and protein recommendations which are actively evolving.

3. **Performance degrades on edge-case queries.** Queries that span multiple sports, contain sport-specific jargon not present in the knowledge base, or are phrased very abstractly may retrieve lower-quality chunks. Precision@6 drops to ~67% on the most abstract queries in the evaluation set.

4. **No real-time biometric data integration.** Unlike commercial wearables (e.g., Whoop), this system cannot incorporate heart rate variability, sleep stage data, or live training load. All personalization is based solely on self-reported profile inputs.

5. **Recommended future work:**
   - Expand knowledge base to cover women's sport-specific guidelines (e.g., female athlete energy availability, RED-S).
   - Implement **hybrid BM25 + FAISS retrieval** to improve precision on specific keyword queries.
   - Add a **cross-encoder re-ranking step** to improve the ordering of retrieved chunks before generation.
   - Integrate **ROUGE-L or BERTScore** automated metrics for scalable evaluation.

---

*Model Card prepared following the framework proposed by Mitchell et al. (2019), "Model Cards for Model Reporting," FAT* '19, Atlanta GA, USA.*
