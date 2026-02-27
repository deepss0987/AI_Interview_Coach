from textblob import TextBlob
import difflib

def grammar_check(text):
    if not text:
        return {"corrected_text": "", "suggestions": []}

    blob = TextBlob(text)
    corrected = str(blob.correct())

    diff = list(difflib.ndiff(text.split(), corrected.split()))
    suggestions = []

    for d in diff:
        if d.startswith("- "):
            suggestions.append({"remove": d[2:]})
        elif d.startswith("+ "):
            suggestions.append({"add": d[2:]})

    return {
        "corrected_text": corrected,
        "suggestions": suggestions[:20]
    }
