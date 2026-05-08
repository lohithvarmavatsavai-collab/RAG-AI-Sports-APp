# Building an AI Sports Performance Assistant with Retrieval-Augmented Generation: From Document Curation to Deployed Web Application

**Graduate Final Project Report**
San Jose State University | Spring 2026

---

## 1. Framing the Problem

When I began thinking about this project, I kept returning to a frustration that anyone who has used a general-purpose AI chatbot for fitness advice will recognize immediately: the answer sounds authoritative, cites nothing, and is almost always generic. Ask a chatbot how much protein a basketball player needs, and it will give you a number that seems plausible but traces to no organization, no study, and no sport-specific context whatsoever. Ask again for a soccer player at beginner level versus an advanced strength athlete, and the answer changes suspiciously little.

This is not simply a user experience problem. It is a technical one with identifiable roots. General-purpose language models encode knowledge in their parameters during training, which means their factual claims are statistical inferences — they reflect what appears most frequently in training data, not what the most authoritative sports science organizations actually publish. When protein recommendations from ISSN, ACSM, and NSCA all appear in training data with equal weight, the model learns to produce a blended average rather than the source-appropriate, sport-specific figure that a real practitioner would cite.

The motivating question for this project, therefore, became: what would happen if we forced the model to read the actual source material before answering? That is, in essence, what Retrieval-Augmented Generation offers — a mechanism for grounding generated text in a specific, curated, and verifiable document corpus rather than in model memory alone. Whether that grounding translates into meaningfully better guidance for athletes is the empirical question this project set out to answer.

The system I built supports four sports — Soccer, Tennis, Basketball, and Strength Training — across three guidance domains: Training, Nutrition, and Recovery. It is deployed as an interactive web application built with Streamlit, backed by a FAISS vector index of 123 document chunks derived from 36 curated source documents, and powered by Google Gemini 2.5 Flash for response generation.

**Why This Matters Societally:**
Access to professional sports science guidance is deeply stratified. Elite athletes train with full-time physiologists and registered sports dietitians. A recreational beginner in the same sport consults Reddit threads and generic YouTube content. The democratization of evidence-grounded athletic guidance — making available to any beginner what was previously reserved for elite programs — represents a genuine public good, particularly for communities where sports are socially significant but professional coaching resources are financially inaccessible.

The system is also designed with explicit acknowledgment of its limits: it will not diagnose injuries, prescribe supplements, or provide individualized medical nutrition therapy. These constraints are not just ethical guardrails — they reflect the boundaries of what an AI system, however well-designed, can responsibly do in a health-adjacent domain.

---

## 2. What I Set Out to Build

The project objectives, written in the technical language appropriate to a graduate engineering project, were as follows:

1. **Design and implement a complete RAG pipeline** covering all stages from source selection and document cleaning through chunking, embedding, vector storage, semantic retrieval, and structured LLM generation.
2. **Curate a corpus of 36 trusted source documents** drawn exclusively from internationally recognized sports science governing bodies, professional associations, and peer-reviewed journals — specifically, FIFA, ACSM, ISSN, NSCA, NIH, ITF, and FIBA.
3. **Construct an experimental comparison** between a RAG-augmented system and a baseline LLM-only configuration, using the same prompt structure in both cases to isolate the effect of retrieval on output quality.
4. **Deploy a polished, production-ready web application** incorporating athlete profile personalization, a novel 6-factor physiological readiness scoring model, and real-time response streaming with visible source attribution.
5. **Formally evaluate both system configurations** across 10 benchmark queries using five scoring dimensions: Relevance, Groundedness, Specificity, Structure, and Safety.
6. **Implement a dynamic readiness scoring system** combining experience level, training load relative to sport-specific optimal volume, primary goal type, body weight, sport metabolic intensity, and athlete age — producing an interpretable score displayed as a visual gauge with factor-level attribution.

---

## 3. Context from the Literature

### 3.1 How RAG Works and Why It Was the Right Choice Here

The foundational mechanism of RAG, as described by Lewis et al. (2020), involves retrieving a set of relevant passages from an external document store and presenting those passages as context within the prompt before the language model generates a response. The model is thereby constrained to produce output that is anchored to the retrieved material rather than to its parametric memory alone. This is architecturally distinct from standard prompting, where the model draws entirely on its training-time knowledge, and from fine-tuning, where the model's weights are modified to incorporate domain knowledge.

For a project grounded in sports science, RAG was a natural fit for several reasons. Sports science recommendations are numerically specific, organization-specific, and evolve over time. A fine-tuned model would embed whatever guidelines existed at training time and could not be updated without full retraining. A RAG system, by contrast, can be updated simply by adding or replacing documents in the corpus — making it both more maintainable and more epistemically honest about the provenance of its claims.

### 3.2 The Documented Problem with LLMs in Specialized Domains

Maynez et al. (2020), in their evaluation of abstractive summarization systems, demonstrated that even high-performing language models produce factually inconsistent outputs at substantial rates when operating in specialized domains. In sports nutrition, this manifests in a specific and practically consequential way: organizations do not agree on protein recommendations, and those disagreements track meaningful physiological distinctions. ISSN's position stand on protein and exercise (Jäger et al., 2017) recommends 1.6 to 2.2 grams per kilogram of body weight for strength athletes. ACSM's joint position statement with the Academy of Nutrition and Dietetics (Thomas et al., 2016) recommends 1.2 to 2.0 grams per kilogram for endurance athletes. A language model without retrieval will frequently conflate these two contexts, producing a hybrid answer that is neither correctly attributed nor sport-appropriate.

### 3.3 The Gap in Existing Sports Technology

Commercial products occupy the sports performance landscape with varying degrees of rigor. Platforms such as MyFitnessPal and Cronometer provide nutritional tracking but generate guidance based on user behavioral data and general dietary databases rather than sport-specific scientific literature. Wearable analytics platforms like Whoop and Oura produce physiological metrics from sensor data but do not interpret those metrics against published guidelines in a queryable format. This project occupies a different position entirely: it retrieves from authoritative publications and generates text that is directly traceable to those publications, making it more epistemically transparent than either category of existing tool.

### 3.4 Why `all-MiniLM-L6-v2` Was Selected as the Embedding Model

Several embedding models were considered during the design phase. The `all-MiniLM-L6-v2` model from the Sentence Transformers library, developed through a knowledge distillation process described by Wang et al. (2020), produces 384-dimensional dense vector representations that capture semantic similarity well at the sentence and short-passage level. I selected it over larger alternatives — including `text-embedding-ada-002` from OpenAI — for three reasons specific to this project: it runs entirely locally without API calls, which eliminates both cost and latency at retrieval time; it is sized at approximately 90 megabytes, making it deployable without GPU infrastructure; and its benchmark performance on short-passage similarity tasks is competitive with models of considerably larger size.

### 3.5 Tool Justification Summary

| Component | Selected Tool | Reasoning |
|---|---|---|
| Sentence Embedding | `all-MiniLM-L6-v2` | Local, fast, GPU-free, proven on short passages |
| Vector Index | FAISS `IndexFlatL2` | Exact search viable for 123-chunk corpus; no approximation error |
| Generation Model | Google Gemini 2.5 Flash | 1M-token context window; low latency; streaming support |
| Frontend | Streamlit | Rapid deployment; native Python integration; session state management |
| Data Management | Pandas / CSV | Reproducible, version-controllable, human-readable |

---

## 4. Building the Knowledge Base

### 4.1 How Sources Were Selected

The decision to limit the corpus to 36 carefully selected documents rather than scraping a larger but less curated dataset was deliberate and reflects a philosophical choice about the kind of system I wanted to build. The hypothesis underlying RAG is that retrieval improves generation quality — but this holds only if the retrieved content is itself high quality. A larger corpus of lower-quality sources would be worse for this application than a smaller corpus of authoritative ones.

Sources were admitted into the corpus only if they satisfied all four of the following criteria: (1) the originating organization is internationally recognized in sports science or athletic development — governing bodies such as FIFA and FIBA, professional associations such as ACSM and NSCA, or federal health agencies such as NIH qualify; (2) the document was published or updated between 2016 and 2023, ensuring currency; (3) the content directly addresses training, nutrition, or recovery in the context of one of the four supported sports; and (4) the document is written in a format that produces coherent, embeddable chunks — narrative or guideline documents with specific numerical content were preferred over tabular databases.

### 4.2 Corpus Structure

| Sport | Training | Nutrition | Recovery | Total |
|---|---|---|---|---|
| Soccer | FIFA F-MARC, UEFA | F-MARC Nutrition, ISSN | ACSM, GSSI | 9 |
| Tennis | ITF, USTA | BJSM, ISSN | JSS, ITF Recovery | 9 |
| Basketball | FIBA, NBA Academy | JISSN, ACSM | Sports Medicine, GSSI | 9 |
| Strength Training | NSCA, ACSM | ISSN, NIH ODS | NSCA, JSCR | 9 |
| **Total** | **12** | **12** | **12** | **36** |

### 4.3 Chunking Design and Its Rationale

I chose a sliding window of 150 words with a 30-word overlap after manually testing several configurations. Windows shorter than 100 words frequently split mid-recommendation — for example, severing a specific protocol description from its associated numerical target. Windows longer than 200 words tended to aggregate multiple distinct recommendations into a single chunk, which degraded retrieval precision by forcing the embedding to represent too many distinct ideas simultaneously.

The 30-word overlap was chosen to ensure that a recommendation spanning a chunk boundary — a sentence that begins at the end of one chunk and concludes at the beginning of the next — would be captured in at least one chunk in its complete form.

The final corpus of 123 chunks retains the following metadata per chunk: `source_id`, `sport`, `category`, `organization`, `title`, and `text`. This metadata is used at retrieval time for pre-filtering and at generation time for source attribution in the response.

**Key modeling assumptions made:**
- A 150-word window is sufficient to capture one complete, self-contained recommendation from a guideline document. This was validated by manually inspecting 20 randomly sampled chunks and confirming that 18 of the 20 contained at least one complete, attributable recommendation.
- Overlapping chunks introduce redundancy in the retrieval pool but improve the probability of capturing cross-boundary content. The benefit of completeness outweighs the cost of duplicate retrieval.
- The MiniLM embedding model represents 150-word passages with sufficient fidelity to discriminate between sport- and category-specific content when queried. This assumption is supported by the model's published performance on semantic similarity benchmarks involving passages of this length.

---

## 5. System Design and Methodology

### 5.1 End-to-End Architecture

The full pipeline from user input to displayed response operates through seven sequential stages:

```
[Athlete Profile: Sport · Goal · Category · Experience · Weight · Age · Query]
                              │
                              ▼
            [Query Embedding — all-MiniLM-L6-v2 → 384-dim vector]
                              │
                              ▼
         [Pre-filter on Sport × Category from FAISS candidate pool ×10]
                              │
                              ▼
            [FAISS IndexFlatL2 → Top-K nearest chunks by L2 distance]
                              │
                              ▼
            [Prompt Assembly: Directives + Profile + Chunks + Structure]
                              │
                              ▼
        [Gemini 2.5 Flash → Streaming generation (temp=0.25, max=2000 tok)]
                              │
                              ▼
        [Streamlit: st.write_stream() → real-time character-by-character display]
```

The baseline path runs identically except that the retrieved chunks block is omitted from the prompt — the model receives only the athlete profile, the directives, and the question.

### 5.2 Retrieval Strategy

The retrieval module implements a two-stage design. In the first stage, a hard metadata filter removes any chunks whose sport or category field does not match the user's current profile. This filtering is applied to a candidate pool of `top_k × 10` chunks, which ensures that the filter has enough candidates to draw from even when the corpus is sparse for a particular sport-category combination. In the second stage, FAISS `IndexFlatL2` ranks the surviving candidates by L2 distance to the embedded query and returns the closest `top_k` results.

A fallback path handles the edge case where no chunks survive the metadata filter — in that scenario, the filter is released and global similarity search is used across the entire corpus. This ensures the system degrades gracefully rather than returning an empty context.

The choice to use exact L2 search rather than approximate nearest-neighbor methods was made because the corpus of 123 chunks is small enough that exact search completes in under 0.5 seconds. There is no practical performance advantage to approximation at this scale, and exact search eliminates the small but non-zero error rate associated with approximate methods.

### 5.3 Prompt Architecture

The prompt structure evolved through several iterations during testing, and the version that produced the best results follows a three-block architecture:

**Block 1 — Profile and Directives:**
Three hard constraints are presented as numbered directives before the question is even shown to the model. These state explicitly: which sport the athlete plays and that cross-sport recommendations are prohibited; what the athlete's primary goal is and that all advice must serve that goal; and which guidance category the query falls under, with the instruction to frame the entire answer through that lens. Testing demonstrated that adding this directive block eliminated the pattern where Gemini would produce generic, multi-sport answers in response to ambiguous queries.

**Block 2 — Retrieved Evidence:**
All retrieved chunks are presented with their source organization and category as headers. The model is instructed to use the specific numbers and protocols from this evidence block, grounding its numerical claims in the retrieved material.

**Block 3 — Output Structure:**
The model is given a bounded six-section output format with explicit length guidance for each section. Temperature is set to 0.25, near the minimum, to maximize factual consistency and reduce the variability that higher temperatures introduce into numerically sensitive domains.

### 5.4 The 6-Factor Readiness Score

One feature of the application that I was particularly interested in developing was a physiologically grounded readiness score — a single number that communicates the athlete's current training readiness given their full profile. The score is computed as a sum of six factors, each representing a distinct physiological dimension:

| Factor | Description | Score Contribution |
|---|---|---|
| F1: Experience Level | Baseline capacity — beginners carry higher injury risk at equivalent loads | Beginner=68, Intermediate=75, Advanced=82 |
| F2: Training Load vs. Optimal | Deviation from the evidence-based optimal volume for the athlete's experience level | +5 if optimal; −7 per day above; −2 per day below |
| F3: Goal Type | Recovery-focused goals signal existing fatigue; performance goals signal readiness | −6 (recovery) to +4 (performance) |
| F4: Body Weight | Heavier athletes have higher recovery demand per session at equivalent relative intensity | +3 (<65 kg) to −4 (>95 kg) |
| F5: Sport Metabolic Intensity | High-impact intermittent sports (soccer, basketball) carry higher cumulative fatigue than lower-intensity ones | 0 to +2 |
| F6: Age | Physiological recovery capacity declines measurably after approximately age 30 | +4 (<22 years) to −6 (50+ years) |

The score is clamped to the range [10, 100] and displayed as a circular gauge with a color-coded status label (Peak / Moderate / High Load). Below the gauge, a Whoop-style breakdown panel displays the individual contribution of each factor as a signed mini-bar, making the scoring logic transparent and interpretable to the user.

---

## 6. Results

### 6.1 Evaluation Framework

I evaluated both system configurations — RAG and Baseline LLM — against 10 benchmark questions designed to span all four sports and all three guidance categories, with a mix of beginner and intermediate athlete profiles. The questions were specifically chosen to have objectively verifiable answers from published literature, which enables meaningful scoring on the groundedness dimension.

Each response was scored on a 1–5 scale across five dimensions:
- **Relevance:** Does the answer address what was actually asked, or does it drift toward related but distinct topics?
- **Groundedness:** Does the response cite specific organizations, numbers, or guidelines that can be traced to the source documents?
- **Specificity:** Are the protocols concrete and actionable — specific quantities, durations, frequencies, or intensities — rather than vague and qualitative?
- **Structure:** Is the response organized and readable — does it follow the prescribed format consistently?
- **Safety:** Does the response stay within appropriate scope, avoiding medical diagnoses, drug recommendations, or other out-of-scope claims?

### 6.2 Quantitative Findings

| Evaluation Criterion | RAG Average (out of 5) | Baseline Average (out of 5) | Difference |
|---|---|---|---|
| Relevance | 4.5 | 3.8 | +0.7 |
| Groundedness | 4.6 | 2.1 | **+2.5** |
| Specificity | 4.3 | 3.2 | +1.1 |
| Structure | 4.7 | 4.5 | +0.2 |
| Safety | 4.9 | 4.7 | +0.2 |
| **Combined Average** | **4.6** | **3.7** | **+0.9** |

> Full per-question scores are recorded in `evaluation_results.csv`.

### 6.3 Retrieval Precision (Precision@6)

| Sport | Category | Precision@6 |
|---|---|---|
| Soccer | Training | 5/6 = 83% |
| Soccer | Nutrition | 4/6 = 67% |
| Soccer | Recovery | 4/6 = 67% |
| Tennis | Training | 5/6 = 83% |
| Tennis | Recovery | 5/6 = 83% |
| Basketball | Training | 5/6 = 83% |
| Basketball | Nutrition | 4/6 = 67% |
| Strength Training | Training | 6/6 = 100% |
| Strength Training | Nutrition | 5/6 = 83% |
| Strength Training | Recovery | 4/6 = 67% |
| **Overall** | | **77%** |

Precision was lowest for nutrition categories in soccer and basketball — both sports where the curated sources tend to be qualitative rather than numerically precise in their dietary guidelines. Strength Training retrieval performed best, consistent with the more technical, quantitative nature of ISSN and NSCA source texts.

### 6.4 Qualitative Patterns

The most consistent pattern in the evaluation was that RAG responses included attributable, sport-specific numerical targets whereas baseline responses offered statistically plausible but organizationally unattributed figures. For example, on the soccer match-day carbohydrate question, the RAG system returned "FIFA recommends 6 to 8 grams of carbohydrate per kilogram of body weight in the 24 hours before competition" while the baseline returned a similar figure with no attribution and without distinguishing pre-competition from general training day intake. This distinction matters: a user who can trace a recommendation to FIFA rather than an unnamed source has a basis for evaluating that recommendation's credibility.

---

## 7. Discussion

### 7.1 What the Groundedness Gap Tells Us

The +2.5 average advantage on groundedness is the most practically significant result in this evaluation, and understanding where it comes from clarifies both what the system does well and where its limits lie. The RAG system's groundedness advantage is not primarily a function of the language model producing more accurate paraphrases — it is a function of the prompt containing specific, citable content that the model incorporates into its response. When the retrieved chunk states "ISSN recommends 1.6 to 2.2 grams of protein per kilogram of body weight for individuals engaged in resistance training," the model has material to work with. The baseline model, receiving no such material, must produce a figure from its parametric memory — and while the figure may be numerically similar, it carries no organizational traceability.

This distinction has direct implications for trust calibration. A beginner athlete who receives a recommendation attributed to the International Society of Sports Nutrition has more basis for evaluating and acting on that recommendation than one who receives the same number from an anonymous AI.

### 7.2 Where Retrieval Does Not Add Value

The near-equal scores on Structure (RAG 4.7 vs. Baseline 4.5) and Safety (RAG 4.9 vs. Baseline 4.7) confirm that the prompt engineering layer, not retrieval, carries responsibility for those dimensions. Both configurations use the same structured output format and the same safety constraints. This is an intended property of the design — it would be unacceptable for the baseline mode to produce unsafe outputs simply because it lacks retrieved context.

The implication is that prompt engineering and retrieval are complementary, not interchangeable. Prompt engineering controls format, tone, and safety; retrieval controls factual grounding and specificity.

### 7.3 What the Retrieval Precision Results Indicate

The 77% average Precision@6 across the evaluation set is acceptable for a corpus of this size, but the variation by sport and category reveals a systematic pattern. Categories with higher precision — Strength Training Training and Tennis Training — correspond to source documents that are written in structured, guideline format with clear numerical targets. Categories with lower precision — Soccer Nutrition, Basketball Nutrition — correspond to sources where the relevant content is embedded in longer narrative paragraphs alongside non-nutritional content, which diffuses the embedding signal and reduces retrieval precision.

This finding has a direct implication for future corpus expansion: adding more sources with explicit nutritional guidelines for soccer and basketball would likely raise retrieval precision in those categories more effectively than adding sources of any other type.

### 7.4 The Effect of Prompt Directives on Output Quality

One of the more instructive findings from the testing phase was how significantly the three-directive block in the prompt affected output quality. In early testing without the sport-specificity, goal-alignment, and category-framing directives, Gemini produced responses that were technically coherent but generically applicable — the recommendations for a beginner soccer player were barely distinguishable from those for a beginner basketball player. Adding the directive block caused a marked shift toward sport-specific language and sport-specific protocols, which is consistent with the interpretation that the model has sport-specific knowledge in its parameters but requires explicit instruction to activate it in preference to generic patterns.

---

## 8. Evaluation and Reflection

### 8.1 Reflecting on What This System Actually Does

Building this system required me to think carefully about the difference between what a language model knows, what it can retrieve, and what it should be allowed to claim. These are not the same thing. The sports science domain sits in a particularly interesting position: it is specialized enough that generic AI guidance can be misleading, but not so specialized that a well-curated corpus of 36 sources cannot cover the most common and consequential questions a recreational athlete would ask.

The decision to show users both the RAG answer and the baseline answer side by side was motivated by exactly this tension. A user who sees both responses can observe, concretely, what retrieval adds — and can make their own judgment about whether the added specificity and attribution changes how they interpret the guidance. That kind of epistemic transparency feels important in a domain where the stakes of misinformation, while not life-threatening, are real.

### 8.2 Assumptions and Their Implications

The three most consequential modeling assumptions in this project were: that 150-word chunks carry sufficient self-contained meaning for embedding-based retrieval; that 36 sources constitute an adequate representation of current sports science consensus across four sports; and that a single evaluator's scores are a valid basis for the quantitative comparison reported in Section 6.

The first assumption held well in practice — manual inspection confirmed that most chunks contained complete, actionable information. The second assumption holds for the most common questions in the domain but would break down for highly specialized queries involving, for example, altitude training adaptations or sport-specific periodization models not represented in the corpus. The third assumption is the weakest: single-rater evaluation introduces potential bias, and the scores reported here should be interpreted as directional rather than precisely calibrated.

### 8.3 What I Would Change

If I were to redesign this system with additional time and resources, three changes would have the largest impact on output quality.

First, I would add a cross-encoder re-ranking stage between the FAISS retrieval and the prompt assembly. A bi-encoder like MiniLM is efficient but less precise than a cross-encoder at ranking retrieved passages by query relevance. Re-ranking the top-20 retrieved chunks with a cross-encoder before selecting the top-6 for the prompt would likely raise Precision@6 from 77% toward 85% or higher.

Second, I would expand the corpus to at least 100 sources, prioritizing soccer and basketball nutrition guidelines to address the retrieval precision gaps identified in Section 6.3. The corpus expansion would not require architectural changes — FAISS scales efficiently to corpora of thousands of documents, and the chunking and embedding pipeline is already modular.

Third, I would implement session-level conversation history, allowing follow-up questions to reference context from earlier in the conversation. The current architecture treats each query as independent, which is appropriate for a first version but limits the usefulness of the system for progressive learning.

### 8.4 Broader Impact and Ethical Considerations

The access gap in sports science is a concrete, documented phenomenon — professional athletes receive continuous, individualized expert guidance while recreational athletes navigate a largely unregulated landscape of social media content, supplement marketing, and anecdotal advice. This system does not close that gap entirely, but it demonstrates that it is technically feasible to close it meaningfully, at minimal cost, using publicly available tools and curated open-access literature.

The ethical design choices embedded in the system — the explicit limitations section in every response, the prohibition on medical advice and supplement recommendations, the visible source attribution — reflect a conviction that responsible deployment in health-adjacent domains requires building appropriate epistemic humility directly into the system's output, not relying on users to supply it themselves. An AI system that claims more certainty than its evidence warrants is not helpful; it is harmful. These design choices represent a deliberate counter to that tendency.

Soccer alone has over 250 million registered players globally, the vast majority of whom have no access to professional sports science support (FIFA, 2022). The system's architecture is language-agnostic at the retrieval and generation level, suggesting a practical path to extending its reach beyond English-speaking populations through localized corpus curation and multilingual embedding models.

---

## 9. Conclusions and Future Directions

This project demonstrates, across a structured evaluation of 10 benchmark queries, that a RAG system grounded in a carefully curated corpus of authoritative sports science literature produces meaningfully better guidance than a baseline LLM-only configuration — most substantially on the dimensions of groundedness (+2.5 average points on a 5-point scale) and specificity (+1.1), with comparable performance on structure and safety.

The deployed application represents a complete, production-ready implementation of the RAG paradigm in the sports science domain: a modular pipeline with reproducible data artifacts, a novel athlete readiness scoring model with transparent factor attribution, real-time response streaming with graceful error handling, and an explicit side-by-side comparison mode that makes the value of retrieval directly observable to users.

The most important contribution of this project may not be the performance numbers but the demonstration that the toolchain required to build this kind of system — sentence transformers, FAISS, a modern frontier LLM, and a lightweight web framework — is now accessible enough that a single graduate student can implement, evaluate, and deploy it in a single semester.

Future directions I would prioritize are corpus expansion (particularly for soccer and basketball nutrition categories), cross-encoder re-ranking for improved retrieval precision, LLM-as-judge automated evaluation to enable scalable benchmarking, and session-level memory to support multi-turn athletic consultations.

---

## 10. References

Jäger, R., Kerksick, C. M., Campbell, B. I., Cribb, P. J., Wells, S. D., Skwiat, T. M., ... & Antonio, J. (2017). International Society of Sports Nutrition position stand: Protein and exercise. *Journal of the International Society of Sports Nutrition*, *14*(20), 1–25. https://doi.org/10.1186/s12970-017-0177-8

Lewis, P., Perez, E., Piktus, A., Petroni, F., Karpukhin, V., Laguardia, N., ... & Kiela, P. (2020). Retrieval-augmented generation for knowledge-intensive NLP tasks. *Advances in Neural Information Processing Systems*, *33*, 9459–9474.

Maynez, J., Narayan, S., Bohnet, B., & McDonald, R. (2020). On faithfulness and factuality in abstractive summarization. In *Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics* (pp. 1906–1919). https://doi.org/10.18653/v1/2020.acl-main.173

Wang, L., Yang, N., Huang, X., Jiao, B., Yang, L., Jiang, D., ... & Wei, F. (2020). Text embeddings by weakly-supervised contrastive pre-training. *arXiv preprint arXiv:2212.03533*.

Thomas, D. T., Erdman, K. A., & Burke, L. M. (2016). Position of the Academy of Nutrition and Dietetics, Dietitians of Canada, and the American College of Sports Medicine: Nutrition and athletic performance. *Journal of the Academy of Nutrition and Dietetics*, *116*(3), 501–528. https://doi.org/10.1016/j.jand.2015.12.006

FIFA Medical Assessment and Research Centre. (2022). *Nutrition for football: A practical guide to eating and drinking for health and performance*. Fédération Internationale de Football Association.

National Strength and Conditioning Association. (2022). *Essentials of strength training and conditioning* (4th ed.). Human Kinetics.

American College of Sports Medicine. (2021). Resistance training for health and fitness: ACSM position stand. *Medicine & Science in Sports & Exercise*, *53*(8). https://doi.org/10.1249/MSS.0000000000002660

International Tennis Federation. (2023). *Physical training guide for tennis: A resource for coaches and players*. ITF Player Development Programme.

Fédération Internationale de Basketball. (2023). *FIBA basketball athletic development program: Strength and conditioning guidelines*. FIBA.

NIH Office of Dietary Supplements. (2023). *Dietary supplements for exercise and athletic performance: Fact sheet for health professionals*. National Institutes of Health.

FIFA. (2022). *FIFA big count: How many people play football?* FIFA Communications Division Information Services.

Grand View Research. (2024). *Sports performance market size, share & trends analysis report, 2024–2030*. Grand View Research.

---

*Submitted in partial fulfillment of the requirements for the Graduate Final Project*
*San Jose State University — Spring 2026*
