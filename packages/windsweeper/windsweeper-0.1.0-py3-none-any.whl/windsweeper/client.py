"""
Windsweeper Client module
Provides the main client class for interacting with the Windsweeper MCP server
"""

import json
from typing import Any, Dict, List, Optional, TypedDict, Union
import requests
from urllib.parse import urljoin

from .monitoring import tracked, get_telemetry, configure_telemetry


class ValidationIssue(TypedDict):
    """Represents an issue found during validation"""
    message: str
    severity: str  # 'error' | 'warning' | 'info'
    ruleId: str
    line: Optional[int]
    column: Optional[int]


class ValidationResult(TypedDict):
    """Result of a validation operation"""
    valid: bool
    issues: List[ValidationIssue]
    message: str
    metadata: Optional[Dict[str, Any]]


class Resource(TypedDict):
    """Represents a resource from the MCP server"""
    id: str
    name: str
    type: str
    description: Optional[str]
    metadata: Optional[Dict[str, Any]]


class GenerateOptions(TypedDict, total=False):
    """Options for generation requests"""
    mode: Optional[str]
    format: Optional[str]
    temperature: Optional[float]
    max_tokens: Optional[int]
    include_sources: Optional[bool]


class WindsweeperClient:
    """
    Client for interacting with the Windsweeper MCP server.
    
    This client provides methods for all main operations supported by the MCP server,
    including validation, resource management, and content generation.
    """
    
    def __init__(self, server_url: str, api_key: Optional[str] = None, timeout: int = 30, 
                 telemetry: Optional[Dict[str, Any]] = None):
        """
        Initialize a new Windsweeper client.
        
        Args:
            server_url: The URL of the Windsweeper MCP server
            api_key: Optional API key for authentication
            timeout: Request timeout in seconds (default: 30)
        """
        self.server_url = server_url[:-1] if server_url.endswith('/') else server_url
        self.api_key = api_key
        self.timeout = timeout
        
        # Configure telemetry if options are provided
        if telemetry:
            telemetry_enabled = telemetry.get('enabled', False)
            telemetry_options = telemetry.get('options', {})
            application_id = telemetry.get('application_id')
            
            if application_id:
                telemetry_options['application_id'] = application_id
                
            configure_telemetry(telemetry_enabled, telemetry_options)
            
            if telemetry_enabled:
                get_telemetry().initialize()
    
    @tracked
    def _make_request(
        self, 
        endpoint: str, 
        method: str = 'GET', 
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Make a request to the MCP server.
        
        Args:
            endpoint: The API endpoint to request
            method: HTTP method to use (default: 'GET')
            params: Query parameters to include
            data: Request body data
            
        Returns:
            The JSON response from the server
            
        Raises:
            requests.exceptions.HTTPError: If the server returns an error status
            requests.exceptions.RequestException: For other request-related errors
        """
        url = urljoin(self.server_url, endpoint)
        
        headers = {'Content-Type': 'application/json'}
        if self.api_key:
            headers['Authorization'] = f'Bearer {self.api_key}'
        
        response = requests.request(
            method=method,
            url=url,
            params=params,
            json=data,
            headers=headers,
            timeout=self.timeout
        )
        
        # Raise exception for 4XX/5XX responses
        response.raise_for_status()
        
        return response.json()
    
    def check_health(self) -> bool:
        """
        Check the health of the MCP server.
        
        Returns:
            True if the server is healthy, False otherwise
        """
        try:
            response = self._make_request('/health')
            return response.get('status') == 'ok'
        except Exception:
            return False
    
    def list_resources(
        self, 
        server_name: str, 
        cursor: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        List resources from the MCP server.
        
        Args:
            server_name: Name of the server to list resources from
            cursor: Optional pagination cursor
            
        Returns:
            Dictionary containing resources and optional next cursor
            
        Raises:
            requests.exceptions.HTTPError: If the server returns an error status
        """
        return self._make_request(
            '/resources',
            params={'serverName': server_name, 'cursor': cursor}
        )
    
    def get_resource(self, server_name: str, resource_id: str) -> Any:
        """
        Get a specific resource from the MCP server.
        
        Args:
            server_name: Name of the server to get the resource from
            resource_id: ID of the resource to get
            
        Returns:
            The requested resource
            
        Raises:
            requests.exceptions.HTTPError: If the server returns an error status
        """
        return self._make_request(
            f'/resources/{resource_id}',
            params={'serverName': server_name}
        )
    
    def validate_rule(
        self,
        content: str,
        language_id: Optional[str] = 'yaml',
        uri: Optional[str] = None
    ) -> ValidationResult:
        """
        Validate a rule definition.
        
        Args:
            content: Rule content to validate
            language_id: Language of the rule content (default: 'yaml')
            uri: Optional URI of the rule
            
        Returns:
            Validation result
            
        Raises:
            requests.exceptions.HTTPError: If the server returns an error status
        """
        return self._make_request(
            '/validate/rule',
            method='POST',
            data={
                'rule': content,
                'languageId': language_id,
                'uri': uri
            }
        )
    
    def validate_code(
        self,
        code: str,
        rule_ids: List[str],
        language_id: str
    ) -> Dict[str, ValidationResult]:
        """
        Validate code against multiple rules.
        
        Args:
            code: Code to validate
            rule_ids: IDs of rules to validate against
            language_id: Language of the code
            
        Returns:
            Dictionary mapping rule IDs to validation results
            
        Raises:
            requests.exceptions.HTTPError: If the server returns an error status
        """
        return self._make_request(
            '/validate/code',
            method='POST',
            data={
                'code': code,
                'ruleIds': rule_ids,
                'languageId': language_id
            }
        )
    
    def apply_template(
        self,
        template_id: str,
        variables: Dict[str, Any]
    ) -> str:
        """
        Apply a template.
        
        Args:
            template_id: ID of the template to apply
            variables: Variables to use in the template
            
        Returns:
            Generated content
            
        Raises:
            requests.exceptions.HTTPError: If the server returns an error status
        """
        response = self._make_request(
            '/templates/apply',
            method='POST',
            data={
                'templateId': template_id,
                'variables': variables
            }
        )
        
        return response['result']
    
    def generate(
        self,
        prompt: str,
        options: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Generate content.
        
        Args:
            prompt: Prompt to generate from
            options: Generation options
            
        Returns:
            Generated content
            
        Raises:
            requests.exceptions.HTTPError: If the server returns an error status
        """
        data = {'prompt': prompt}
        if options:
            data.update(options)
            
        response = self._make_request(
            '/generate',
            method='POST',
            data=data
        )
        
        return response['result']
