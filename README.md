# Final Project - Emotion Detector

Final Project for the IBM/Coursera Python Project for AI & Application Development course.

This project implements an AI-powered emotion detector using the Watson NLP Skills Network endpoint, packages the functionality as `EmotionDetection`, validates it with unit tests, deploys it with Flask, handles blank-input errors, and includes static code analysis.

## Files

- `EmotionDetection/emotion_detection.py`
- `EmotionDetection/__init__.py`
- `test_emotion_detection.py`
- `server.py`
- `templates/index.html`
- `static/mywebscript.js`

## Setup

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
```

## Run

```bash
.venv/bin/python server.py
```

## Test

```bash
.venv/bin/python -m unittest test_emotion_detection.py
PYLINTHOME=.pylint.d .venv/bin/pylint server.py
```

The project depends on the public Watson NLP Skills Network endpoint. If that
endpoint is unavailable, live emotion-score tests and the deployed Flask result
for non-empty text will fail with a network error rather than fabricated scores.
