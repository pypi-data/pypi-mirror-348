"""
Extensions system for the Windsweeper SDK.
Provides a plugin architecture for customizing and extending SDK behavior.
"""

from typing import Any, Callable, Dict, List, Optional, Protocol, TypeVar, Union, cast
from abc import ABC, abstractmethod
import inspect

# Forward reference types
T = TypeVar('T')


class WindsweeperExtension(ABC):
    """Interface for SDK extension plugins."""
    
    @property
    @abstractmethod
    def id(self) -> str:
        """Unique identifier for the extension."""
        pass
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Human-readable name of the extension."""
        pass
    
    @property
    @abstractmethod
    def description(self) -> str:
        """Brief description of what the extension does."""
        pass
    
    @property
    @abstractmethod
    def version(self) -> str:
        """Version of the extension."""
        pass
    
    @abstractmethod
    async def initialize(self, client: Any, options: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize the extension.
        
        Args:
            client: WindsweeperClient instance
            options: Optional configuration options
        """
        pass
    
    async def dispose(self) -> None:
        """Clean up resources before extension is removed."""
        pass


class RequestInterceptor:
    """Hook for intercepting and modifying requests."""
    
    def __init__(self, interceptor_id: str):
        """
        Initialize a request interceptor.
        
        Args:
            interceptor_id: Unique identifier for the interceptor
        """
        self._id = interceptor_id
    
    @property
    def id(self) -> str:
        """Unique identifier for the interceptor."""
        return self._id
    
    async def before_request(
        self, 
        endpoint: str, 
        options: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """
        Process a request before it's sent.
        
        Args:
            endpoint: API endpoint
            options: Request options
            
        Returns:
            Modified options or None to use original options
        """
        return None
    
    async def after_response(
        self, 
        endpoint: str, 
        options: Dict[str, Any], 
        response: Any
    ) -> Any:
        """
        Process a response after it's received.
        
        Args:
            endpoint: API endpoint
            options: Request options
            response: API response
            
        Returns:
            Modified response or None to use original response
        """
        return response
    
    async def on_error(
        self,
        endpoint: str,
        options: Dict[str, Any],
        error: Exception
    ) -> Optional[Any]:
        """
        Handle request errors.
        
        Args:
            endpoint: API endpoint
            options: Request options
            error: Error that occurred
            
        Returns:
            Alternative response to use instead of raising the error, or None to re-raise
        """
        return None


class ExtensionRegistry:
    """Extension registry for managing SDK extensions."""
    
    def __init__(self):
        """Create a new extension registry."""
        self.extensions = {}
        self.request_interceptors = []
        self.client = None
    
    def set_client(self, client: Any) -> None:
        """
        Set the client instance for this registry.
        
        Args:
            client: WindsweeperClient instance
        """
        self.client = client
    
    async def register_extension(
        self, 
        extension: WindsweeperExtension, 
        options: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Register a new extension.
        
        Args:
            extension: Extension to register
            options: Options to pass to the extension's initialize method
        
        Raises:
            ValueError: If an extension with the same ID is already registered
        """
        if extension.id in self.extensions:
            raise ValueError(f"Extension with ID {extension.id} is already registered")
        
        self.extensions[extension.id] = extension
        
        if self.client:
            await extension.initialize(self.client, options)
    
    async def unregister_extension(self, extension_id: str) -> bool:
        """
        Unregister an extension.
        
        Args:
            extension_id: ID of the extension to unregister
            
        Returns:
            True if the extension was found and unregistered, False otherwise
        """
        extension = self.extensions.get(extension_id)
        
        if not extension:
            return False
        
        await extension.dispose()
        
        del self.extensions[extension_id]
        
        # Remove any interceptors registered by this extension
        self.request_interceptors = [
            i for i in self.request_interceptors 
            if not i.id.startswith(f"{extension_id}:")
        ]
        
        return True
    
    def get_extension(self, extension_id: str) -> Optional[WindsweeperExtension]:
        """
        Get an extension by ID.
        
        Args:
            extension_id: ID of the extension to get
            
        Returns:
            The extension if found, None otherwise
        """
        return self.extensions.get(extension_id)
    
    def get_extensions(self) -> List[WindsweeperExtension]:
        """
        Get all registered extensions.
        
        Returns:
            List of all registered extensions
        """
        return list(self.extensions.values())
    
    def register_interceptor(self, interceptor: RequestInterceptor) -> None:
        """
        Register a request interceptor.
        
        Args:
            interceptor: Interceptor to register
            
        Raises:
            ValueError: If an interceptor with the same ID is already registered
        """
        # Check for duplicate ID
        if any(i.id == interceptor.id for i in self.request_interceptors):
            raise ValueError(f"Interceptor with ID {interceptor.id} is already registered")
        
        self.request_interceptors.append(interceptor)
    
    def unregister_interceptor(self, interceptor_id: str) -> bool:
        """
        Unregister a request interceptor.
        
        Args:
            interceptor_id: ID of the interceptor to unregister
            
        Returns:
            True if the interceptor was found and unregistered, False otherwise
        """
        initial_length = len(self.request_interceptors)
        self.request_interceptors = [i for i in self.request_interceptors if i.id != interceptor_id]
        return len(self.request_interceptors) != initial_length
    
    async def process_request(
        self,
        endpoint: str,
        options: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Process a request through all registered interceptors.
        
        Args:
            endpoint: API endpoint
            options: Request options
            
        Returns:
            Modified request options
        """
        current_endpoint = endpoint
        current_options = options.copy()
        
        # Apply all before_request interceptors
        for interceptor in self.request_interceptors:
            try:
                result = await interceptor.before_request(current_endpoint, current_options)
                if result is not None:
                    current_options = result
            except Exception as e:
                print(f"Error in interceptor {interceptor.id} before_request: {str(e)}")
        
        return current_options
    
    async def process_response(
        self,
        endpoint: str,
        options: Dict[str, Any],
        response: Any
    ) -> Any:
        """
        Process a response through all registered interceptors.
        
        Args:
            endpoint: API endpoint
            options: Request options
            response: API response
            
        Returns:
            Modified response
        """
        current_response = response
        
        # Apply all after_response interceptors in reverse order
        for interceptor in reversed(self.request_interceptors):
            try:
                result = await interceptor.after_response(endpoint, options, current_response)
                if result is not None:
                    current_response = result
            except Exception as e:
                print(f"Error in interceptor {interceptor.id} after_response: {str(e)}")
        
        return current_response
    
    async def process_error(
        self,
        endpoint: str,
        options: Dict[str, Any],
        error: Exception
    ) -> Any:
        """
        Process an error through all registered interceptors.
        
        Args:
            endpoint: API endpoint
            options: Request options
            error: Error that occurred
            
        Returns:
            Alternative response if an interceptor handled the error
            
        Raises:
            The original error if no interceptor handled it
        """
        # Apply all on_error interceptors
        for interceptor in self.request_interceptors:
            try:
                result = await interceptor.on_error(endpoint, options, error)
                if result is not None:
                    return result
            except Exception as e:
                # Ignore errors in error handlers to avoid cascading failures
                print(f"Error in interceptor {interceptor.id} on_error: {str(e)}")
        
        # Re-raise the original error if no interceptor handled it
        raise error


# Create a global extension registry
extension_registry = ExtensionRegistry()


class BasicExtension(WindsweeperExtension):
    """Basic implementation of a Windsweeper extension."""
    
    def __init__(
        self,
        ext_id: str,
        ext_name: str,
        ext_description: str,
        ext_version: str,
        init_func: Optional[Callable] = None,
        dispose_func: Optional[Callable] = None
    ):
        """
        Initialize a basic extension.
        
        Args:
            ext_id: Unique identifier for the extension
            ext_name: Human-readable name of the extension
            ext_description: Brief description of what the extension does
            ext_version: Version of the extension
            init_func: Function to call when initializing the extension
            dispose_func: Function to call when disposing the extension
        """
        self._id = ext_id
        self._name = ext_name
        self._description = ext_description
        self._version = ext_version
        self._init_func = init_func
        self._dispose_func = dispose_func
    
    @property
    def id(self) -> str:
        return self._id
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def description(self) -> str:
        return self._description
    
    @property
    def version(self) -> str:
        return self._version
    
    async def initialize(self, client: Any, options: Optional[Dict[str, Any]] = None) -> None:
        if self._init_func:
            # Handle both async and non-async initialization functions
            if inspect.iscoroutinefunction(self._init_func):
                await self._init_func(client, options)
            else:
                self._init_func(client, options)
    
    async def dispose(self) -> None:
        if self._dispose_func:
            # Handle both async and non-async disposal functions
            if inspect.iscoroutinefunction(self._dispose_func):
                await self._dispose_func()
            else:
                self._dispose_func()


class BasicInterceptor(RequestInterceptor):
    """Basic implementation of a request interceptor."""
    
    def __init__(
        self,
        interceptor_id: str,
        before_request_func: Optional[Callable] = None,
        after_response_func: Optional[Callable] = None,
        on_error_func: Optional[Callable] = None
    ):
        """
        Initialize a basic interceptor.
        
        Args:
            interceptor_id: Unique identifier for the interceptor
            before_request_func: Function to call before a request is sent
            after_response_func: Function to call after a response is received
            on_error_func: Function to call when an error occurs
        """
        super().__init__(interceptor_id)
        self._before_request_func = before_request_func
        self._after_response_func = after_response_func
        self._on_error_func = on_error_func
    
    async def before_request(
        self, 
        endpoint: str, 
        options: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        if self._before_request_func:
            if inspect.iscoroutinefunction(self._before_request_func):
                return await self._before_request_func(endpoint, options)
            else:
                return self._before_request_func(endpoint, options)
        return None
    
    async def after_response(
        self, 
        endpoint: str, 
        options: Dict[str, Any], 
        response: Any
    ) -> Any:
        if self._after_response_func:
            if inspect.iscoroutinefunction(self._after_response_func):
                return await self._after_response_func(endpoint, options, response)
            else:
                return self._after_response_func(endpoint, options, response)
        return response
    
    async def on_error(
        self,
        endpoint: str,
        options: Dict[str, Any],
        error: Exception
    ) -> Optional[Any]:
        if self._on_error_func:
            if inspect.iscoroutinefunction(self._on_error_func):
                return await self._on_error_func(endpoint, options, error)
            else:
                return self._on_error_func(endpoint, options, error)
        return None


def create_extension(
    ext_id: str,
    ext_name: str,
    ext_description: str,
    ext_version: str,
    init_func: Optional[Callable] = None,
    dispose_func: Optional[Callable] = None
) -> WindsweeperExtension:
    """
    Create a basic extension with provided handlers.
    
    Args:
        ext_id: Unique identifier for the extension
        ext_name: Human-readable name of the extension
        ext_description: Brief description of what the extension does
        ext_version: Version of the extension
        init_func: Function to call when initializing the extension
        dispose_func: Function to call when disposing the extension
        
    Returns:
        A new extension instance
    """
    return BasicExtension(
        ext_id=ext_id,
        ext_name=ext_name,
        ext_description=ext_description,
        ext_version=ext_version,
        init_func=init_func,
        dispose_func=dispose_func
    )


def create_interceptor(
    interceptor_id: str,
    before_request_func: Optional[Callable] = None,
    after_response_func: Optional[Callable] = None,
    on_error_func: Optional[Callable] = None
) -> RequestInterceptor:
    """
    Create a request interceptor with provided handlers.
    
    Args:
        interceptor_id: Unique identifier for the interceptor
        before_request_func: Function to call before a request is sent
        after_response_func: Function to call after a response is received
        on_error_func: Function to call when an error occurs
        
    Returns:
        A new interceptor instance
    """
    return BasicInterceptor(
        interceptor_id=interceptor_id,
        before_request_func=before_request_func,
        after_response_func=after_response_func,
        on_error_func=on_error_func
    )
