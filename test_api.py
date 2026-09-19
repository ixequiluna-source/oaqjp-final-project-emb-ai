"""Regression tests for provider validation and the browser's POST contract."""
import unittest
from unittest.mock import Mock, patch
from requests.exceptions import Timeout
from server import app
from EmotionDetection.emotion_detection import emotion_detector

SCORES = dict(anger=.01, disgust=.02, fear=.03, joy=.9, sadness=.04)


class ApiTests(unittest.TestCase):
    """Exercise failures without sending any external requests."""

    def setUp(self):
        self.client = app.test_client()

    def test_success_and_headers(self):
        with patch('server.emotion_detector', return_value={**SCORES, 'dominant_emotion': 'joy'}) as model:
            response = self.client.post('/api/emotions', json={'text': '  fictional example  '})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['scores']['joy'], .9)
        model.assert_called_once_with('fictional example')
        self.assertEqual(response.headers['Cache-Control'], 'no-store')
        self.assertNotIn('unsafe-inline', response.headers['Content-Security-Policy'])

    def test_invalid_inputs_never_call_provider(self):
        with patch('server.emotion_detector') as model:
            for payload in [{}, {'text': ''}, {'text': '   '}, {'text': 7}, {'text': 'x'*2001}, []]:
                with self.subTest(payload_type=type(payload)):
                    self.assertEqual(self.client.post('/api/emotions', json=payload).status_code, 400)
            model.assert_not_called()

    def test_malformed_json(self):
        self.assertEqual(self.client.post('/api/emotions', data='{', content_type='application/json').status_code, 400)

    def test_media_type_and_size(self):
        self.assertEqual(self.client.post('/api/emotions', data='hello').status_code, 415)
        self.assertEqual(self.client.post('/api/emotions', data='x'*17000, content_type='application/json').status_code, 413)

    def test_cross_origin_rejected(self):
        self.assertEqual(self.client.post('/api/emotions', json={'text':'demo'}, headers={'Origin':'https://other.example'}).status_code, 403)

    def test_provider_failures_are_recoverable(self):
        for error in [Timeout('private provider details'), ValueError('private payload')]:
            with patch('server.emotion_detector', side_effect=error):
                response = self.client.post('/api/emotions', json={'text':'demo'})
            self.assertEqual(response.status_code, 503)
            self.assertNotIn('private', response.get_data(as_text=True))

    def test_unanalyzable_text(self):
        with patch('server.emotion_detector', return_value={'dominant_emotion':None}):
            self.assertEqual(self.client.post('/api/emotions', json={'text':'demo'}).status_code, 422)

    def test_legacy_contract(self):
        with patch('server.emotion_detector', return_value={**SCORES, 'dominant_emotion':'joy'}):
            result = self.client.get('/emotionDetector?textToAnalyze=demo')
        self.assertEqual(result.status_code, 200)
        self.assertTrue(result.content_type.startswith('text/plain'))

    def test_empty_input_skips_network(self):
        with patch('EmotionDetection.emotion_detection.requests.post') as post:
            self.assertIsNone(emotion_detector('  ')['dominant_emotion'])
            post.assert_not_called()

    def test_provider_schema_and_ranges(self):
        for payload in [{}, {'emotionPredictions':[]}, {'emotionPredictions':[{'emotion':{}}]}] + [
            {'emotionPredictions':[{'emotion':{**SCORES,'joy':bad}}]} for bad in [None,'0.9',True,-1,2,float('nan'),float('inf')]
        ]:
            response=Mock(status_code=200);response.json.return_value=payload
            with patch('EmotionDetection.emotion_detection.requests.post',return_value=response):
                with self.assertRaises(ValueError): emotion_detector('demo')


if __name__ == '__main__':
    unittest.main()
