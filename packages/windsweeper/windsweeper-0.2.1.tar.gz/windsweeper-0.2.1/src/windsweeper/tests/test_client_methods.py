"""
Test cases for the WindsweeperClient class.
"""
import json
import unittest
from unittest.mock import MagicMock, patch, ANY
import requests
from requests.exceptions import HTTPError, Timeout, JSONDecodeError, ConnectionError

from windsweeper.client import WindsweeperClient


class TestWindsweeperClientMethods(unittest.TestCase):
    """Test cases for the WindsweeperClient class."""

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
    def test_list_resources_error_handling(self, mock_request):
        """Test error handling in list_resources."""
        # Test HTTP error
        http_error = self._create_http_error(
            500,
            'Internal Server Error',
            {'error': 'Something went wrong'}
        )
        mock_request.return_value = self._create_mock_response(
            status_code=500,
            raise_for_status=http_error
        )
        
        with self.assertRaises(HTTPError) as context:
            self.client.list_resources('test-server')
        self.assertEqual(context.exception.response.status_code, 500)
        
        # Test network timeout
        mock_request.side_effect = Timeout('Request timed out')
        with self.assertRaises(Timeout):
            self.client.list_resources('test-server')
            
        # Test invalid JSON response
        mock_request.side_effect = None
        mock_response = self._create_mock_response(
            text='invalid json',
            json_data=None
        )
        # Make json() raise JSONDecodeError
        mock_response.json.side_effect = json.JSONDecodeError("Expecting value", "<string>", 0)
        mock_request.return_value = mock_response
        
        # The client will raise a JSONDecodeError when trying to parse the response
        with self.assertRaises(json.JSONDecodeError):
            self.client.list_resources('test-server')

    @patch('windsweeper.client.requests.request')
    def test_list_resources_large_result_set(self, mock_request):
        """Test list_resources with a large result set (pagination)."""
        # Create a large list of resources
        resources = [{'id': f'res{i}', 'name': f'Resource {i}'} for i in range(1, 101)]
        
        # Setup mock response with first 50 resources
        response_data = {
            'resources': resources[:50],
            'next_cursor': 'cursor-123',
            'has_more': True
        }
        
        # Setup mock to return the response
        mock_request.return_value = self._create_mock_response(json_data=response_data)
        
        # Test listing resources
        result = self.client.list_resources('test-server')
        
        # Verify we got the first page of resources
        self.assertEqual(len(result['resources']), 50)
        self.assertEqual(result['next_cursor'], 'cursor-123')
        self.assertTrue(result['has_more'])
        
        # Verify the request was made correctly
        mock_request.assert_called_once()
        call_args = mock_request.call_args.kwargs
        self.assertEqual(call_args['method'], 'GET')
        self.assertEqual(call_args['url'], f"{self.server_url}/resources")
        self.assertEqual(call_args['params'], {'serverName': 'test-server', 'cursor': None})


if __name__ == '__main__':
    unittest.main()
