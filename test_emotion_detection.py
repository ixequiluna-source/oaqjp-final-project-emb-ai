"""Unit tests for the emotion detection package."""

import unittest

from EmotionDetection.emotion_detection import emotion_detector


class TestEmotionDetector(unittest.TestCase):
    """Validate the dominant emotion for representative statements."""

    def test_joy(self):
        """Test that a glad statement is classified as joy."""
        self.assertEqual(
            emotion_detector("I am glad this happened")["dominant_emotion"], "joy"
        )

    def test_anger(self):
        """Test that a mad statement is classified as anger."""
        self.assertEqual(
            emotion_detector("I am really mad about this")["dominant_emotion"], "anger"
        )

    def test_disgust(self):
        """Test that a disgusted statement is classified as disgust."""
        self.assertEqual(
            emotion_detector("I feel disgusted just hearing about this")[
                "dominant_emotion"
            ],
            "disgust",
        )

    def test_sadness(self):
        """Test that a sad statement is classified as sadness."""
        self.assertEqual(
            emotion_detector("I am so sad about this")["dominant_emotion"], "sadness"
        )

    def test_fear(self):
        """Test that an afraid statement is classified as fear."""
        self.assertEqual(
            emotion_detector("I am really afraid that this will happen")[
                "dominant_emotion"
            ],
            "fear",
        )


if __name__ == "__main__":
    unittest.main()
