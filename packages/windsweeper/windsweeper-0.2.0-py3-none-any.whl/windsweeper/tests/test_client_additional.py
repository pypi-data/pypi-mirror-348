"""
Additional test cases for the WindsweeperClient class.
"""
import json
import unittest
from unittest.mock import MagicMock, patch, ANY
import requests
from requests.exceptions import HTTPError, Timeout, JSONDecodeError

from windsweeper.client import WindsweeperClient, ValidationResult


class TestWindsweeperClientAdditional(unittest.TestCase):
    """Additional test cases for the WindsweeperClient class."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.server_url = 'http://test-server:8080'
        self.api_key = 'test-api-key'
        self.client = WindsweeperClient(
            server_url=self.server_url,
            api_key=self.api_key,
            timeout=30
        )

    def _create_mock_response(self, status_code=200, json_data=None, text=None, raise_for_status=None):
        """Helper to create a mock response."""
        mock_resp = MagicMock()
        mock_resp.status_code = status_code
        
        if json_data is not None:
            mock_resp.json.return_value = json_data
            
        if text is not None:
            mock_resp.text = text
            
        if raise_for_status is not None:
            mock_resp.raise_for_status.side_effect = raise_for_status
            
        return mock_resp
    
    def _create_http_error(self, status_code, message, response_data=None):
        """Helper to create an HTTPError with a response."""
        response = MagicMock()
        response.status_code = status_code
        if response_data:
            response.json.return_value = response_data
            response.text = json.dumps(response_data)
        
        http_error = HTTPError(message)
        http_error.response = response
        return http_error

    @patch('windsweeper.client.requests.request')
    def test_check_health_success(self, mock_request):
        """Test successful health check."""
        # Setup mock response
        mock_response = self._create_mock_response(
            json_data={'status': 'ok'}
        )
        mock_request.return_value = mock_response
        
        # Test health check
        result = self.client.check_health()
        
        # Verify result
        self.assertTrue(result)
        
        # Verify request
        mock_request.assert_called_once()
        call_args = mock_request.call_args.kwargs
        self.assertEqual(call_args['method'], 'GET')
        self.assertEqual(call_args['url'], f"{self.server_url}/health")

    @patch('windsweeper.client.requests.request')
    def test_check_health_failure(self, mock_request):
        """Test failed health check."""
        # Setup mock to raise HTTPError
        http_error = self._create_http_error(
            500,
            'Internal Server Error',
            {'error': 'Something went wrong'}
        )
        mock_request.side_effect = http_error
        
        # Test health check
        result = self.client.check_health()
        
        # Verify result
        self.assertFalse(result)

    @patch('windsweeper.client.requests.request')
    def test_get_resource_success(self, mock_request):
        """Test successful resource retrieval."""
        # Setup mock response
        resource = {
            'id': 'res1',
            'name': 'Test Resource',
            'type': 'test',
            'description': 'A test resource',
            'metadata': {'key': 'value'}
        }
        mock_response = self._create_mock_response(
            json_data=resource
        )
        mock_request.return_value = mock_response
        
        # Test get resource
        result = self.client.get_resource('test-server', 'res1')
        
        # Verify result
        self.assertEqual(result, resource)
        
        # Verify request
        mock_request.assert_called_once()
        call_args = mock_request.call_args.kwargs
        self.assertEqual(call_args['method'], 'GET')
        self.assertEqual(call_args['url'], f"{self.server_url}/resources/res1")
        self.assertEqual(call_args['params'], {'serverName': 'test-server'})

    @patch('windsweeper.client.requests.request')
    def test_validate_code_success(self, mock_request):
        """Test successful code validation."""
        # Setup mock response
        validation_result = {
            'valid': True,
            'issues': [],
            'message': 'Validation successful',
            'metadata': {}
        }
        mock_response = self._create_mock_response(
            json_data=validation_result
        )
        mock_request.return_value = mock_response
        
        # Test validate code
        code = 'print("Hello, World!"'
        rule_ids = ['rule1', 'rule2']
        language_id = 'python'
        
        result = self.client.validate_code(code, rule_ids, language_id)
        
        # Verify result
        self.assertEqual(result, validation_result)
        
        # Verify request
        mock_request.assert_called_once()
        call_args = mock_request.call_args.kwargs
        self.assertEqual(call_args['method'], 'POST')
        self.assertEqual(call_args['url'], f"{self.server_url}/validate/code")
        self.assertEqual(call_args['json'], {
            'code': code,
            'ruleIds': rule_ids,
            'languageId': language_id
        })

    @patch('windsweeper.client.requests.request')
    def test_apply_template_success(self, mock_request):
        """Test successful template application."""
        # Setup mock response
        template_result = 'Hello, John! Welcome to our platform.'
        mock_response = self._create_mock_response(
            json_data={'result': template_result}
        )
        mock_request.return_value = mock_response
        
        # Test apply template
        template_id = 'welcome-email'
        variables = {'name': 'John', 'platform': 'our platform'}
        
        result = self.client.apply_template(template_id, variables)
        
        # Verify result
        self.assertEqual(result, template_result)
        
        # Verify request
        mock_request.assert_called_once()
        call_args = mock_request.call_args.kwargs
        self.assertEqual(call_args['method'], 'POST')
        self.assertEqual(call_args['url'], f"{self.server_url}/templates/apply")
        self.assertEqual(call_args['json'], {
            'templateId': template_id,
            'variables': variables
        })

    @patch('windsweeper.client.requests.request')
    def test_generate_success(self, mock_request):
        """Test successful content generation."""
        # Setup mock response
        generated_text = 'This is a generated response.'
        mock_response = self._create_mock_response(
            json_data={'result': generated_text}
        )
        mock_request.return_value = mock_response
        
        # Test generate
        prompt = 'Tell me a joke'
        options = {
            'max_tokens': 50,
            'temperature': 0.7
        }
        
        result = self.client.generate(prompt, options)
        
        # Verify result
        self.assertEqual(result, generated_text)
        
        # Verify request
        mock_request.assert_called_once()
        call_args = mock_request.call_args.kwargs
        self.assertEqual(call_args['method'], 'POST')
        self.assertEqual(call_args['url'], f"{self.server_url}/generate")
        self.assertEqual(call_args['json'], {
            'prompt': prompt,
            'max_tokens': 50,
            'temperature': 0.7
        })


if __name__ == '__main__':
    unittest.main()
