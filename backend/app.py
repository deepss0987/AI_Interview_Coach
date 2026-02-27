from flask import Flask, request, jsonify
from flask_cors import CORS

from utils.logger import logger
from utils.nltk_setup import ensure_nltk_data

from nlp.preprocess import preprocess_text
from nlp.sentiment import analyze_sentiment
from nlp.grammar import grammar_check
from nlp.keywords import extract_keywords
from nlp.fillers import detect_fillers
from nlp.feedback import generate_feedback

ensure_nltk_data()  

app = Flask(__name__)
CORS(app)


from database.db import init_db, save_interview, get_history
init_db()

QUESTIONS = [
    "Tell me about yourself.",
    "What are your greatest strengths?",
    "What is your biggest weakness?",
    "Why do you want to work here?",
    "Where do you see yourself in 5 years?",
    "Describe a challenging situation you faced and how you handled it.",
    "How do you handle stress and pressure?",
    "What is your preferred work style?",
    "Tell me about a time you worked in a team.",
    "Do you have any questions for us?"
]

@app.route("/questions", methods=["GET"])
def get_questions_route():
    return jsonify(QUESTIONS)

@app.route("/history", methods=["GET"])
def get_history_route():
    try:
        history = get_history()
        return jsonify(history)
    except Exception as e:
        logger.error(f"History error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/history", methods=["POST"])
def save_history_route():
    try:
        data = request.json
        save_interview(data)
        return jsonify({"success": True})
    except Exception as e:
        logger.error(f"Save history error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/process_answer", methods=["POST"])
def process_answer():
    try:
        data = request.json
        answer = data.get("answer", "")

        prep = preprocess_text(answer)
        sentiment = analyze_sentiment(answer)
        grammar = grammar_check(answer)
        keywords = extract_keywords(prep["tokens_no_stop"])
        fillers = detect_fillers(prep["tokens"])

        feedback = generate_feedback(
            sentiment=sentiment,
            grammar=grammar,
            preprocess=prep,
            keywords=keywords,
            fillers=fillers,
        )

        return jsonify({
            "success": True,
            "sentiment": sentiment,
            "grammar": grammar,
            "keywords": keywords,
            "fillers": fillers,
            "analysis": prep,
            "feedback": feedback
        })

    except Exception as e:
        logger.error(f"Processing error: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
