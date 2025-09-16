from django.test import TestCase, override_settings
from unittest.mock import patch, Mock
from .services import get_jwt_token, fetch_telemetry


class MetricsServiceTests(TestCase):
	@override_settings(API_CALLS_ENABLED=False)
	def test_get_jwt_token_disabled(self):
		token = get_jwt_token('u', 'p', 'r')
		self.assertIsNone(token)

	@override_settings(API_CALLS_ENABLED=False)
	def test_fetch_telemetry_disabled(self):
		data = fetch_telemetry('abc')
		self.assertEqual(data, [])

	@override_settings(API_CALLS_ENABLED=True, API_BASE_URL='http://api.example.com')
	@patch('metrics.services.requests.post')
	def test_get_jwt_token_success(self, mock_post):
		mock_resp = Mock()
		mock_resp.ok = True
		mock_resp.json.return_value = {'access_token': 'xyz'}
		mock_post.return_value = mock_resp
		token = get_jwt_token('user', 'pass', 'role')
		self.assertEqual(token, 'xyz')
		mock_post.assert_called()

	@override_settings(API_CALLS_ENABLED=True, API_BASE_URL='http://api.example.com')
	@patch('metrics.services.requests.get')
	def test_fetch_telemetry_success(self, mock_get):
		mock_resp = Mock()
		mock_resp.ok = True
		mock_resp.json.return_value = [{'v': 1}]
		mock_get.return_value = mock_resp
		out = fetch_telemetry('tkn')
		self.assertEqual(out, [{'v': 1}])
		mock_get.assert_called()
