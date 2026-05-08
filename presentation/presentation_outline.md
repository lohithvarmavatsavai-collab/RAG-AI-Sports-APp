# Presentation Outline
## AI Sports Performance Assistant Using RAG
### San Jose State University | Spring 2026 | 10–15 Minute Presentation

---

## SLIDE 1 — Title
- **Title:** AI Sports Performance Assistant Using Retrieval-Augmented Generation, Embeddings, and Structured Prompting
- **Subtitle:** SJSU Graduate Final Project | Spring 2026
- **Your Name | Course | Date**
- *Suggested visual: Dark background, sport icons (⚽🎾🏀🏋️), glowing neural network graphic*

---

## SLIDE 2 — The Problem (30 seconds)
**Headline:** "Athletes can't trust generic AI advice."
- LLMs hallucinate specific numbers (protein targets, carb intake)
- Answers are not grounded in trusted sources
- Advice ignores sport-specific physiological demands
- No source accountability = no way to verify

**Visual:** Side-by-side: vague chatbot answer vs. source-cited answer

---

## SLIDE 3 — The Solution (30 seconds)
**Headline:** "RAG: Evidence Before Generation"
- Curate trusted sources → Chunk → Embed → Retrieve → Generate
- Answers grounded in FIFA, ACSM, ISSN, NIH, and more
- Structured output: Summary + Recommendations + Evidence + Limitations
- Direct comparison: RAG vs. Baseline LLM

**Visual:** Simple pipeline diagram (boxes with arrows)

---

## SLIDE 4 — Prior Work (1 minute)
- **Lewis et al. (2020):** Original RAG paper — combining parametric + non-parametric knowledge
- **SentenceTransformers (Wang, 2020):** Semantic embedding for document retrieval
- **LLM limitations in specialized domains:** Maynez et al. (2020) on hallucination
- **Gap:** No RAG system exists specifically for curated sports science guidance

---

## SLIDE 5 — Dataset & Sources (1 minute)
**Headline:** "24 Trusted Sources. 4 Sports. 3 Categories."

| Sport | Training | Nutrition | Recovery |
|---|---|---|---|
| Soccer | FIFA, UEFA | F-MARC, ISSN | ACSM, GSSI |
| Tennis | ITF, USTA | BJSM, ISSN | JSS, ITF |
| Basketball | FIBA, NBA | JISSN, ACSM | Sports Med, GSSI |
| Strength | NSCA, ACSM | ISSN, NIH | NSCA, JSCR |

- 72 text chunks after cleaning and windowed chunking (150 words, 30 overlap)

---

## SLIDE 6 — System Architecture (1.5 minutes)
**Headline:** "How It Works"

```
User Question + Athlete Profile
        ↓
SentenceTransformer Embedding (all-MiniLM-L6-v2)
        ↓
FAISS Vector Search → Top-K Relevant Chunks
        ↓
Structured Prompt (with chunks + profile)
        ↓
GPT-3.5-turbo → Structured Answer
        ↓
Streamlit App: Answer + Sources + Comparison
```

Key choices:
- FAISS (fast, no cloud dependency)
- all-MiniLM-L6-v2 (free, 384-dim, proven quality)
- Temperature 0.3 (reduces hallucination)
- 5-section structured output format

---

## SLIDE 7 — Live Demo (3–4 minutes)
**Headline:** "Let's see it in action"

Demo flow:
1. Open the app at localhost:8501
2. Set profile: Soccer | Beginner | 70kg | 3 days/week | Nutrition
3. Ask: "How many carbohydrates should I eat on match day?"
4. Show: RAG answer with source chips visible
5. Toggle: Show baseline comparison
6. Point out: Specificity difference (g/kg in RAG, vague advice in baseline)
7. Show: Retrieved source chunks (FIFA F-MARC, ISSN)
8. Show: Limitations section at the bottom

*Tip: Take 5 screenshots in advance in case of connection issues.*

---

## SLIDE 8 — Evaluation Results (2 minutes)
**Headline:** "RAG vs. Baseline: What the Numbers Show"

Table or bar chart showing:
- Average scores across 10 questions, 5 criteria
- Highlight: Groundedness and Specificity where RAG wins
- Note: Structure and Safety are similar (both use same prompt format)

Key finding: *"RAG improves groundedness and specificity significantly while maintaining safety guardrails"*

---

## SLIDE 9 — Discussion (1 minute)
**Headline:** "When does RAG help most?"
- Nutrition questions with specific numerical targets (g/kg protein, mL fluids)
- Sport-specific protocols where generic advice fails
- When source attribution is required for trust

**When both modes are similar:**
- High-level conceptual answers (e.g., "what is active recovery?")
- Safety guardrails (built into the system prompt, not the retrieval)

---

## SLIDE 10 — What I Learned (1 minute)
**Headline:** "Lessons Learned"
- RAG architecture is not magic — source quality is everything
- Chunking strategy matters: too large = noise, too small = loss of context
- Structured prompting is as important as retrieval
- Evaluation design should be built before the system, not after
- Small corpus (72 chunks) limits retrieval diversity

---

## SLIDE 11 — Future Work (30 seconds)
- Expand to 100+ sources and more sports
- Cross-encoder re-ranking for improved precision
- Fine-tuned domain embedding model
- User feedback loop to improve retrieval over time
- Integration with nutritional databases (USDA)

---

## SLIDE 12 — Conclusion
**Headline:** "Summary"
- Built a complete RAG pipeline grounded in 24 trusted sports science sources
- Demonstrated measurable improvement in groundedness and specificity vs. baseline
- Deployed as a polished, interactive Streamlit application
- Established evaluation framework for evidence-based AI guidance systems

**Thank you.**
*Questions?*

---

## PRESENTER NOTES

### Timing Guide
| Slide | Time |
|---|---|
| 1–3 | 2 min |
| 4–5 | 2 min |
| 6 | 1.5 min |
| 7 Demo | 3–4 min |
| 8–9 | 3 min |
| 10–12 | 2 min |
| **Total** | **~15 min** |

### Key Points to Emphasize
1. The baseline comparison is what makes this academically rigorous — not just an app
2. Source selection from governing bodies is the credibility anchor
3. The limitations section in the app shows you understand the boundaries of AI
