# Emotion Detector Final Project

Final project for the IBM/Coursera Python Project for AI & Application Development course.

This project implements an AI-powered emotion detector using the Watson NLP Skills Network endpoint, packages the functionality as `EmotionDetection`, validates it with unit tests, deploys it with Flask, handles blank-input errors, and includes static code analysis.

## Files

- `EmotionDetection/emotion_detection.py`
- `EmotionDetection/__init__.py`
- `test_emotion_detection.py`
- `server.py`
- `templates/index.html`
- `static/mywebscript.js`

## Run

```bash
pip install flask requests pylint
python server.py
```

## Test

```bash
python -m unittest test_emotion_detection.py
pylint server.py EmotionDetection/emotion_detection.py
```
