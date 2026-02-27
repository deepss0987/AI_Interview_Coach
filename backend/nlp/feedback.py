from math import fabs

def generate_feedback(sentiment, grammar, preprocess, keywords, fillers):
    suggestions = []
    score = 0.0 
    weights = {}

    word_count = preprocess.get("word_count", 0)
    if word_count < 10:
        suggestions.append("Your answer is too short. Please elaborate on your experience and provide more details.")
        score -= 0.8 
        weights["length_penalty"] = -0.8
    else:
        weights["length_penalty"] = 0.0

    combined = float(sentiment.get("combined", 0.0))
    conf = float(sentiment.get("confidence", 0.25))
   
    sentiment_score = (combined + 1) / 2  
    score += 0.4 * sentiment_score * conf
    weights["sentiment"] = round(0.4 * sentiment_score * conf, 3)

    neg_patterns = preprocess.get("negative_patterns", [])
    if neg_patterns:
        suggestions.append("Your answer contains evasive phrases (e.g. 'I don't know', 'not sure'). Try to answer directly and confidently.")
        score -= 0.6 
        weights["negative_patterns"] = -0.6
    else:
        weights["negative_patterns"] = 0.0

    if preprocess.get("apologetic"):
        suggestions.append("Avoid leading with apologies (e.g. 'sorry') — it weakens your response.")
        score -= 0.2
        weights["apologetic"] = -0.2
    else:
        weights["apologetic"] = 0.0

    hedges = preprocess.get("hedging_count", 0)
    if hedges >= 2:
        suggestions.append(f"I noticed {hedges} hedging words (maybe/possibly/etc.). Reduce hedging to sound more decisive.")
        score -= 0.2
        weights["hedging"] = -0.2
    else:
        weights["hedging"] = 0.0

    grammar_sugg = grammar.get("suggestions") if grammar else []
    if grammar_sugg:
        suggestions.append("There are grammar/spelling suggestions — review the corrected text.")
        score -= 0.15
        weights["grammar"] = -0.15
    else:
        weights["grammar"] = 0.0

    filler_count = sum(f.get("count", 0) for f in fillers or [])
    if filler_count >= 2:
        suggestions.append(f"Detected {filler_count} filler words (um/uh/like). Practice removing them to sound more fluent.")
        score -= 0.15
        weights["fillers"] = -0.15
    else:
        weights["fillers"] = 0.0

    avg_len = preprocess.get("avg_sentence_length", 0)
    if avg_len > 30:
        suggestions.append("Sentences are long — try breaking them into shorter sentences for clarity.")
        score -= 0.1
        weights["avg_len"] = -0.1
    else:
        weights["avg_len"] = 0.0

    if not keywords or len(keywords) < 2:
        suggestions.append("Your answer lacks strong keywords (skills, tech names, achievements). Add specific examples and results.")
        score -= 0.1
        weights["keywords"] = -0.1
    else:
        score += 0.1
        weights["keywords"] = 0.1

    if combined < -0.35:
        suggestions.append("Your answer sounds negative or demotivated. Reframe negative language into positive/constructive phrasing.")
        score -= 0.4
        weights["strong_negative"] = -0.4
    else:
        weights["strong_negative"] = 0.0

    raw = 0.5 + score
    normalized = max(0.0, min(1.0, raw))

    if normalized >= 0.70:
        verdict = "good"
    elif normalized >= 0.50:
        verdict = "needs_improvement"
    else:
        verdict = "poor"

    overall_confidence = max(0.2, min(0.99, 0.5 * conf + 0.5 * normalized))  # combine sentiment conf + normalized

    feedback = {
        "verdict": verdict,
        "score": round(normalized, 3),
        "confidence": round(overall_confidence, 3),
        "suggestions": suggestions,
        "weights": weights,
        "summary": _build_summary(verdict, normalized, sentiment)
    }

    return feedback

def _build_summary(verdict, score, sentiment):
    """
    Short human-friendly summary.
    """
    s = ""
    if verdict == "good":
        s = "Overall this answer is good — clear and confident."
    elif verdict == "needs_improvement":
        s = "This answer is OK but could be improved — see suggestions."
    else:
        s = "This answer needs work — consider the suggestions to improve clarity and tone."

    combined = sentiment.get("combined", 0.0)
    if combined < -0.2:
        s += " The tone is negative."
    elif combined > 0.3:
        s += " The tone is positive."
    else:
        s += " Tone is neutral."

    return s
