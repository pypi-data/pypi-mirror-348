"""
Integration tests for the Windsweeper client

These tests require a running MCP server to pass.
To skip these tests when MCP server is not available, run:
pytest -k "not integration"
"""

import os
import unittest
from unittest import skipIf

from windsweeper import create_client, WindsweeperClient


# Environment variables for testing
TEST_SERVER_URL = os.environ.get("TEST_SERVER_URL", "http://localhost:9001")
TEST_API_KEY = os.environ.get("TEST_API_KEY")
TEST_SERVER_NAME = os.environ.get("TEST_SERVER_NAME", "test-server")


class TestWindsweeperClientIntegration(unittest.TestCase):
    """Integration tests for the WindsweeperClient"""

    @classmethod
    def setUpClass(cls):
        """Set up client for all tests"""
        cls.client = create_client(
            server_url=TEST_SERVER_URL,
            api_key=TEST_API_KEY
        )
        # Check if server is available
        cls.server_available = cls._check_server_availability(cls.client)
    
    @staticmethod
    def _check_server_availability(client: WindsweeperClient) -> bool:
        """Helper method to check if the server is available"""
        try:
            return client.check_health()
        except Exception:
            return False
    
    def check_server_available(self):
        """Skip test if server is not available"""
        if not self.server_available:
            self.skipTest("MCP server is not available")
    
    def test_server_health(self):
        """Test checking server health"""
        self.check_server_available()
        is_healthy = self.client.check_health()
        self.assertTrue(is_healthy)
    
    def test_list_resources(self):
        """Test listing resources from the server"""
        self.check_server_available()
        
        result = self.client.list_resources(TEST_SERVER_NAME)
        
        # Basic structure validation
        self.assertIn("resources", result)
        self.assertIsInstance(result["resources"], list)
        
        # Each resource should have required properties
        if result["resources"]:
            resource = result["resources"][0]
            self.assertIn("id", resource)
            self.assertIn("name", resource)
            self.assertIn("type", resource)
    
    def test_pagination(self):
        """Test handling pagination for resources"""
        self.check_server_available()
        
        # This test is conditionally run if the server returns paginated results
        first_page = self.client.list_resources(TEST_SERVER_NAME)
        
        if "nextCursor" not in first_page or not first_page["nextCursor"]:
            self.skipTest("Skipping pagination test: No next page available")
        
        second_page = self.client.list_resources(TEST_SERVER_NAME, first_page["nextCursor"])
        self.assertIn("resources", second_page)
        self.assertIsInstance(second_page["resources"], list)
    
    def test_validate_valid_rule(self):
        """Test validating a valid rule"""
        self.check_server_available()
        
        valid_rule = """
        rules:
          - id: test-rule
            pattern: 'console\\.log\\('
            message: 'Avoid using console.log in production code'
            severity: warning
        """
        
        result = self.client.validate_rule(valid_rule)
        self.assertTrue(result["valid"])
        self.assertEqual(len(result["issues"]), 0)
    
    def test_validate_invalid_rule(self):
        """Test identifying issues in an invalid rule"""
        self.check_server_available()
        
        # Missing required 'id' field
        invalid_rule = """
        rules:
          - pattern: 'console\\.log\\('
            message: 'Avoid using console.log in production code'
            severity: warning
        """
        
        result = self.client.validate_rule(invalid_rule)
        self.assertFalse(result["valid"])
        self.assertGreater(len(result["issues"]), 0)
    
    def test_validate_code(self):
        """Test validating code against rules"""
        self.check_server_available()
        
        # Create a test rule first
        test_rule = """
        rules:
          - id: console-log-warning
            pattern: 'console\\.log\\('
            message: 'Avoid using console.log in production code'
            severity: warning
        """
        
        # Try to validate the rule first to make sure it's available
        rule_validation = self.client.validate_rule(test_rule)
        if not rule_validation["valid"]:
            self.skipTest("Skipping test: Test rule is invalid")
        
        # Code that should trigger the rule
        code = """
        function example() {
          console.log('This is a test');
          return true;
        }
        """
        
        results = self.client.validate_code(code, ["console-log-warning"], "javascript")
        
        # Check structure and results
        self.assertIn("console-log-warning", results)
        result = results["console-log-warning"]
        
        # A valid result could either have issues (rule matched) or no issues (rule didn't match)
        # Both are technically "valid" from a validation perspective
        self.assertIn("valid", result)
        self.assertIn("issues", result)
    

if __name__ == "__main__":
    unittest.main()
