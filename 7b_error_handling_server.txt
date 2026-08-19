"""Flask server for the emotion detection web application."""

from flask import Flask, render_template, request
from requests.exceptions import RequestException

from EmotionDetection.emotion_detection import emotion_detector

app = Flask(__name__)


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
    except RequestException:
        return "Emotion detection service unavailable. Please try again later!", 503

    if response["dominant_emotion"] is None:
        return "Invalid text! Please try again!"

    return (
        f"For the given statement, the system response is 'anger': "
        f"{response['anger']}, 'disgust': {response['disgust']}, "
        f"'fear': {response['fear']}, 'joy': {response['joy']} and "
        f"'sadness': {response['sadness']}. The dominant emotion is "
        f"{response['dominant_emotion']}."
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
