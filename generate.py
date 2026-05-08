import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
MODEL_NAME = "gemini-2.5-flash"

SYSTEM_PROMPT = (
    "You are an AI Sports Performance Assistant for beginner to intermediate athletes. "
    "Provide detailed, evidence-based guidance on training, nutrition, and recovery. "
    "Never diagnose injuries, prescribe supplements, or give medical advice. "
    "Always recommend consulting a qualified professional for medical needs. "
    "Be thorough, specific, and encouraging. Use numbers and specifics from the evidence."
)

RAG_STRUCTURE = """Respond using these exact sections. Be informative and specific, but concise — each section should be well-detailed yet easy to read (aim for quality over length):

**📋 Key Insight**
2-3 sentences explaining the core answer with the most important specific number or protocol (e.g. "1.6–2.2 g/kg protein", "70–80% max HR", "8 hours sleep"). Lead with the "why".

**🏋️ Recommendations**
4-5 bullet points. Each must include: a specific protocol with numbers (sets, reps, grams, minutes, %HR) AND a one-sentence explanation of why it matters for this athlete's sport and goal.

**🍽️ How to Implement**
3-4 clear, actionable steps showing exactly how to fit this into the athlete's weekly routine. Be practical and specific to their sport and experience level.

**📅 Sample Protocol**
One concrete, ready-to-use example: a sample workout day OR a daily meal plan with rough macros OR a weekly schedule. Keep it practical and directly applicable.

**📚 Evidence Base**
1-2 sentences naming the specific organizations and their key findings that support these recommendations.

**⚠️ Important Limits**
1 sentence: what this guidance does NOT cover and when to see a professional."""


def _call_gemini_stream(prompt: str):
    try:
        response = client.models.generate_content_stream(
            model=MODEL_NAME,
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                temperature=0.25,
                max_output_tokens=2000,  # balanced: rich detail without overwhelming the reader
            )
        )
        for chunk in response:
            if chunk.text:
                yield chunk.text
    except Exception as e:
        error_msg = str(e)
        if "503" in error_msg or "UNAVAILABLE" in error_msg:
            yield "\n\n> ⚠️ **API Overloaded:** The Google Gemini model is currently experiencing high demand. Please try again in a few moments."
        elif "429" in error_msg or "quota" in error_msg.lower():
            yield "\n\n> ⚠️ **Quota Exceeded:** API rate limit reached. Please wait a minute before trying again."
        else:
            yield f"\n\n> ⚠️ **Generation Error:** {error_msg}"


def get_rag_answer(question: str, retrieved_chunks: list, user_profile: dict) -> str:
    """RAG answer grounded in retrieved source chunks."""
    # Use up to 350 chars per chunk — enough for specific numbers and protocols
    context_parts = []
    for c in retrieved_chunks:
        snippet = c['text']  # send full chunk text — Gemini 2.5 Flash has 1M token context
        context_parts.append(f"[{c['organization']}, {c['sport']} {c['category']}]\n{snippet}")
    context = "\n\n".join(context_parts)

    profile_str = (
        f"Sport: {user_profile.get('sport')} | "
        f"Category Focus: {user_profile.get('category')} | "
        f"Primary Goal: {user_profile.get('goal')} | "
        f"Level: {user_profile.get('experience')} | "
        f"Training: {user_profile.get('training_days')} days/week | "
        f"Body weight: {user_profile.get('body_weight')} kg"
    )

    prompt = (
        f"Athlete Profile: {profile_str}\n"
        f"IMPORTANT DIRECTIVES:\n"
        f"1. Sport: The athlete plays {user_profile.get('sport')}. Do not recommend protocols from other sports.\n"
        f"2. Goal: Their primary goal is '{user_profile.get('goal')}'. Every piece of advice must actively serve this specific goal.\n"
        f"3. Category: This inquiry strictly falls under '{user_profile.get('category')}'. Frame the entire answer heavily through the lens of {user_profile.get('category')}.\n\n"
        f"Question: {question}\n\n"
        f"Retrieved Evidence from Trusted Sources:\n"
        f"{'='*50}\n"
        f"{context}\n"
        f"{'='*50}\n\n"
        f"{RAG_STRUCTURE}\n\n"
        "Use specific numbers and protocols from the evidence above. "
        f"Tailor every single recommendation to a {user_profile.get('experience')} {user_profile.get('sport')} athlete "
        f"focusing purely on {user_profile.get('category')} to achieve '{user_profile.get('goal')}'. Be complete — do not cut off mid-section."
    )
    return _call_gemini_stream(prompt)


def get_baseline_answer(question: str, user_profile: dict) -> str:
    """Baseline answer — no retrieved context."""
    profile_str = (
        f"Sport: {user_profile.get('sport')} | "
        f"Category Focus: {user_profile.get('category')} | "
        f"Primary Goal: {user_profile.get('goal')} | "
        f"Level: {user_profile.get('experience')} | "
        f"Training: {user_profile.get('training_days')} days/week | "
        f"Body weight: {user_profile.get('body_weight')} kg"
    )

    prompt = (
        f"Athlete Profile: {profile_str}\n"
        f"IMPORTANT DIRECTIVES:\n"
        f"1. Sport: The athlete plays {user_profile.get('sport')}. Do not recommend protocols from other sports.\n"
        f"2. Goal: Their primary goal is '{user_profile.get('goal')}'. Every piece of advice must actively serve this specific goal.\n"
        f"3. Category: This inquiry strictly falls under '{user_profile.get('category')}'. Frame the entire answer heavily through the lens of {user_profile.get('category')}.\n\n"
        f"Question: {question}\n\n"
        f"{RAG_STRUCTURE}\n\n"
        "Answer from general sports science knowledge. "
        "Be specific with numbers where possible. "
        f"Tailor every single recommendation to a {user_profile.get('experience')} {user_profile.get('sport')} athlete "
        f"focusing purely on {user_profile.get('category')} to achieve '{user_profile.get('goal')}'. Do not fabricate citations."
    )
    return _call_gemini_stream(prompt)
