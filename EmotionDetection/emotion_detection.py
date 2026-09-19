"""Emotion detection using the Watson NLP service."""

import math
import requests

EMOTION_ENDPOINT = (
    "https://sn-watson-emotion.labs.skills.network/"
    "v1/watson.runtime.nlp.v1/NlpService/EmotionPredict"
)
EMOTION_HEADERS = {
    "grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"
}
EMOTION_KEYS = ("anger", "disgust", "fear", "joy", "sadness")
REQUEST_TIMEOUT = 30


def _empty_emotion_response():
    """Return the expected response structure for invalid input."""
    return {
        "anger": None,
        "disgust": None,
        "fear": None,
        "joy": None,
        "sadness": None,
        "dominant_emotion": None,
    }


def emotion_detector(text_to_analyze):
    """Analyze text and return emotion scores plus the dominant emotion."""
    if not text_to_analyze or not text_to_analyze.strip():
        return _empty_emotion_response()

    payload = {"raw_document": {"text": text_to_analyze}}

    response = requests.post(
        EMOTION_ENDPOINT,
        json=payload,
        headers=EMOTION_HEADERS,
        timeout=REQUEST_TIMEOUT,
    )

    if response.status_code == 400:
        return _empty_emotion_response()

    response.raise_for_status()
    try:
        emotions = response.json()["emotionPredictions"][0]["emotion"]
        emotion_scores = {emotion: emotions[emotion] for emotion in EMOTION_KEYS}
    except (ValueError, KeyError, IndexError, TypeError) as exc:
        raise ValueError("Invalid provider response") from exc
    for value in emotion_scores.values():
        if (isinstance(value, bool) or not isinstance(value, (int, float))
                or not math.isfinite(value) or not 0 <= value <= 1):
            raise ValueError("Invalid provider score")
    emotion_scores["dominant_emotion"] = max(emotion_scores, key=emotion_scores.get)
    return emotion_scores
