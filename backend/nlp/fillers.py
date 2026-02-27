FILLERS = {"um", "uh", "like", "actually", "basically", "you know", "i mean"}

def detect_fillers(tokens):
    lower = " ".join(tokens).lower()
    found = []

    for f in FILLERS:
        if f in lower:
            found.append({
                "filler": f,
                "count": lower.count(f)
            })

    return found
