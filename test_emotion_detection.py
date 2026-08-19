"""Unit tests for the emotion detection package."""

import unittest
from unittest.mock import Mock, patch

from EmotionDetection.emotion_detection import emotion_detector


class TestEmotionDetector(unittest.TestCase):
    """Validate dominant emotion classification without external network calls."""

    @staticmethod
    def _mock_response(scores):
        response = Mock()
        response.status_code = 200
        response.raise_for_status.return_value = None
        response.json.return_value = {
            "emotionPredictions": [
                {
                    "emotion": scores,
                }
            ]
        }
        return response

    def _assert_dominant(self, text, expected, scores):
        with patch(
            "EmotionDetection.emotion_detection.requests.post",
            return_value=self._mock_response(scores),
        ):
            result = emotion_detector(text)
        self.assertEqual(result["dominant_emotion"], expected)

    def test_joy(self):
        """Test that a glad statement is classified as joy."""
        self._assert_dominant(
            "I am glad this happened",
            "joy",
            {
                "anger": 0.01,
                "disgust": 0.01,
                "fear": 0.02,
                "joy": 0.92,
                "sadness": 0.04,
            },
        )

    def test_anger(self):
        """Test that a mad statement is classified as anger."""
        self._assert_dominant(
            "I am really mad about this",
            "anger",
            {
                "anger": 0.90,
                "disgust": 0.03,
                "fear": 0.02,
                "joy": 0.01,
                "sadness": 0.04,
            },
        )

    def test_disgust(self):
        """Test that a disgusted statement is classified as disgust."""
        self._assert_dominant(
            "I feel disgusted just hearing about this",
            "disgust",
            {
                "anger": 0.04,
                "disgust": 0.88,
                "fear": 0.03,
                "joy": 0.01,
                "sadness": 0.04,
            },
        )

    def test_sadness(self):
        """Test that a sad statement is classified as sadness."""
        self._assert_dominant(
            "I am so sad about this",
            "sadness",
            {
                "anger": 0.02,
                "disgust": 0.01,
                "fear": 0.03,
                "joy": 0.02,
                "sadness": 0.92,
            },
        )

    def test_fear(self):
        """Test that an afraid statement is classified as fear."""
        self._assert_dominant(
            "I am really afraid that this will happen",
            "fear",
            {
                "anger": 0.02,
                "disgust": 0.01,
                "fear": 0.91,
                "joy": 0.01,
                "sadness": 0.05,
            },
        )


if __name__ == "__main__":
    unittest.main()
