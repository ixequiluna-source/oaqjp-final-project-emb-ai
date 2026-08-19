"""Compatibility module for the course's Task 2 import path.

The graded activity imports ``emotion_detector`` directly from a top-level
``emotion_detection`` module before the application is packaged.  The actual
implementation lives in ``EmotionDetection.emotion_detection`` so this module
re-exports the same function without duplicating logic.
"""

from EmotionDetection.emotion_detection import emotion_detector

__all__ = ["emotion_detector"]
