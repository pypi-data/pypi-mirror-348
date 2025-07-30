"""
Tests for the Windsweeper client
"""

import unittest
from unittest.mock import patch, MagicMock

from windsweeper.client import WindsweeperClient


class TestWindsweeperClient(unittest.TestCase):
    """Test cases for the WindsweeperClient class"""
    
    def setUp(self):
        """Set up test fixtures before each test"""
        self.server_url = "http://localhost:9001"
        self.client = WindsweeperClient(server_url=self.server_url)
    
    @patch('windsweeper.client.requests.request')
    def test_init(self, mock_request):
        """Test client initialization"""
        # Test with default params
        client = WindsweeperClient(server_url=self.server_url)
        self.assertEqual(client.server_url, self.server_url)
        self.assertIsNone(client.api_key)
        self.assertEqual(client.timeout, 30)
        
        # Test with trailing slash in URL
        client = WindsweeperClient(server_url=f"{self.server_url}/")
        self.assertEqual(client.server_url, self.server_url)
        
        # Test with custom params
        api_key = "test_api_key"
        timeout = 60
        client = WindsweeperClient(
            server_url=self.server_url,
            api_key=api_key,
            timeout=timeout
        )
        self.assertEqual(client.server_url, self.server_url)
        self.assertEqual(client.api_key, api_key)
        self.assertEqual(client.timeout, timeout)
    
    @patch('windsweeper.client.requests.request')
    def test_check_health(self, mock_request):
        """Test health check functionality"""
        # Mock a healthy response
        mock_response = MagicMock()
        mock_response.json.return_value = {"status": "ok"}
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response
        
        # Check that we get a healthy response
        result = self.client.check_health()
        self.assertTrue(result)
        
        # Verify request parameters
        mock_request.assert_called_once_with(
            method="GET",
            url=f"{self.server_url}/health",
            params=None,
            json=None,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        # Mock an unhealthy response
        mock_response.json.return_value = {"status": "error"}
        result = self.client.check_health()
        self.assertFalse(result)
        
        # Mock a request exception
        mock_request.side_effect = Exception("Connection error")
        result = self.client.check_health()
        self.assertFalse(result)
    
    @patch('windsweeper.client.requests.request')
    def test_list_resources(self, mock_request):
        """Test listing resources from the server"""
        # Mock response with resources
        mock_resources = [
            {"id": "res1", "name": "Resource 1", "type": "rule"},
            {"id": "res2", "name": "Resource 2", "type": "template"}
        ]
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "resources": mock_resources,
            "nextCursor": "next_page"
        }
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response
        
        # Test listing resources
        result = self.client.list_resources(server_name="test_server")
        
        # Verify response handling
        self.assertEqual(result["resources"], mock_resources)
        self.assertEqual(result["nextCursor"], "next_page")
        
        # Verify request parameters
        mock_request.assert_called_once_with(
            method="GET",
            url=f"{self.server_url}/resources",
            params={"serverName": "test_server", "cursor": None},
            json=None,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        # Test with pagination cursor
        self.client.list_resources(server_name="test_server", cursor="page_token")
        # Check that the cursor was included in the request
        self.assertEqual(
            mock_request.call_args[1]["params"]["cursor"],
            "page_token"
        )
    
    @patch('windsweeper.client.requests.request')
    def test_validate_rule(self, mock_request):
        """Test rule validation"""
        # Mock validation response
        mock_validation = {
            "valid": True,
            "issues": [],
            "message": "Rule is valid"
        }
        mock_response = MagicMock()
        mock_response.json.return_value = mock_validation
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response
        
        # Test validating a rule
        result = self.client.validate_rule(content="rule content")
        
        # Verify response handling
        self.assertEqual(result, mock_validation)
        
        # Verify request parameters
        mock_request.assert_called_once_with(
            method="POST",
            url=f"{self.server_url}/validate/rule",
            params=None,
            json={
                "rule": "rule content",
                "languageId": "yaml",
                "uri": None
            },
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        # Test with custom parameters
        self.client.validate_rule(
            content="rule content",
            language_id="json",
            uri="test.json"
        )
        # Check that custom parameters were included
        self.assertEqual(
            mock_request.call_args[1]["json"]["languageId"],
            "json"
        )
        self.assertEqual(
            mock_request.call_args[1]["json"]["uri"],
            "test.json"
        )
    
    @patch('windsweeper.client.requests.request')
    def test_auth_headers(self, mock_request):
        """Test that API key is included in requests if provided"""
        # Create client with API key
        api_key = "test_api_key"
        client = WindsweeperClient(server_url=self.server_url, api_key=api_key)
        
        # Mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {"status": "ok"}
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response
        
        # Make request
        client.check_health()
        
        # Verify auth header was included
        headers = mock_request.call_args[1]["headers"]
        self.assertEqual(headers["Authorization"], f"Bearer {api_key}")
    
    @patch('windsweeper.client.requests.request')
    def test_error_handling(self, mock_request):
        """Test error handling in the client"""
        # Mock HTTP error
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = Exception("HTTP Error")
        mock_request.return_value = mock_response
        
        # Check that error is propagated
        with self.assertRaises(Exception):
            self.client.list_resources(server_name="test_server")


if __name__ == "__main__":
    unittest.main()
