"""Flask server for the emotion detection web application."""

from flask import Flask, jsonify, render_template, request
from requests.exceptions import RequestException

from EmotionDetection.emotion_detection import emotion_detector

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 16384


@app.after_request
def security_headers(response):
    """Keep results private and load resources from this origin."""
    response.headers["Cache-Control"] = "no-store"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Referrer-Policy"] = "no-referrer"
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; script-src 'self'; style-src 'self'; "
        "connect-src 'self'; img-src 'self'; base-uri 'none'; "
        "frame-ancestors 'none'; form-action 'self'"
    )
    return response


@app.errorhandler(413)
def too_large(_error):
    """Return a useful response when the transport limit is exceeded."""
    return jsonify(error="Request too large. Use up to 2,000 characters."), 413


@app.post("/api/emotions")
def analyze_emotions():
    """Validate bounded input and return verified provider scores."""
    origin = request.headers.get("Origin")
    if origin and origin != request.host_url.rstrip("/"):
        return jsonify(error="Request must come from this application."), 403
    if not request.is_json:
        return jsonify(error="Send a JSON request."), 415
    payload = request.get_json(silent=True)
    text = payload.get("text") if isinstance(payload, dict) else None
    if not isinstance(text, str) or not text.strip() or len(text) > 2000:
        return jsonify(error="Enter 1 to 2,000 characters of English text."), 400
    try:
        scores = emotion_detector(text.strip())
    except (RequestException, ValueError):
        return jsonify(error="The model is unavailable. Your text is still here; try again."), 503
    if scores["dominant_emotion"] is None:
        return jsonify(error="The model could not analyze this text. Try another example."), 422
    return jsonify(scores=scores, source="Watson NLP Skills Network")


@app.route("/")
def render_index_page():
    """Render the application home page."""
    return render_template("index.html")


@app.route("/emotionDetector")
def emotion_detector_route():
    """Analyze the supplied text and return a formatted result."""
    text_to_analyze = request.args.get("textToAnalyze", "")
    try:
        response = emotion_detector(text_to_analyze)
    except (RequestException, ValueError):
        return "Emotion detection service unavailable. Please try again later!", 503

    if response["dominant_emotion"] is None:
        return "Invalid text! Please try again!"

    result = (
        f"For the given statement, the system response is 'anger': "
        f"{response['anger']}, 'disgust': {response['disgust']}, "
        f"'fear': {response['fear']}, 'joy': {response['joy']} and "
        f"'sadness': {response['sadness']}. The dominant emotion is "
        f"{response['dominant_emotion']}."
    )
    return result, 200, {"Content-Type": "text/plain; charset=utf-8"}


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
