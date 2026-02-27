from collections import Counter

def extract_keywords(tokens_no_stop, top_n=6):
    return [word for word, _ in Counter(tokens_no_stop).most_common(top_n)]
