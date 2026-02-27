import nltk
import re
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords

STOPWORDS = set(stopwords.words("english"))

NEGATIVE_PATTERNS = [
    r"\bi don't know\b",
    r"\bi'm not sure\b",
    r"\bno idea\b",
    r"\bsorry\b",
    r"\bcan't\b",
    r"\bi don't have\b",
    r"\bnot relevant\b",
    r"\bnot really\b",
]

HEDGING_WORDS = {"maybe", "perhaps", "possibly", "might", "could", "probably", "sort of", "kind of"}

def preprocess_text(text):
    if not isinstance(text, str):
        text = str(text or "")

    sentences = sent_tokenize(text)
    words = word_tokenize(text)

    tokens_clean = [w.lower() for w in words if re.match(r"[A-Za-z0-9']+", w)]
    tokens_no_stop = [t for t in tokens_clean if t not in STOPWORDS]

    word_count = len(tokens_clean)
    sentence_count = max(1, len(sentences))
    avg_sentence_len = round(word_count / sentence_count, 2)

    lowered = text.lower()
    negative_matches = []
    for patt in NEGATIVE_PATTERNS:
        if re.search(patt, lowered):
            negative_matches.append(patt)

    hedges = [w for w in tokens_clean if w in HEDGING_WORDS]
    hedging_count = len(hedges)

    apologetic = any(word in lowered for word in ["sorry", "apologize", "apologies"])

    return {
        "sentences": sentences,
        "words": words,
        "tokens": tokens_clean,
        "tokens_no_stop": tokens_no_stop,
        "word_count": word_count,
        "sentence_count": sentence_count,
        "avg_sentence_length": avg_sentence_len,
        "negative_patterns": negative_matches,
        "hedging_count": hedging_count,
        "apologetic": apologetic,
    }
