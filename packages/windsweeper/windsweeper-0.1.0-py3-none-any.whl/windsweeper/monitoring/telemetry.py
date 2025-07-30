"""
Telemetry module for the Windsweeper SDK.
Provides monitoring, usage tracking, and error detection capabilities.
"""

import os
import sys
import uuid
import time
import json
import platform
import threading
import logging
import atexit
from typing import Dict, List, Optional, Any, Union, Callable
from datetime import datetime
import urllib.request
import urllib.error
import importlib.metadata
from typing import cast, AnyStr, IO

try:
    from typing import TypedDict
except ImportError:
    from typing_extensions import TypedDict  # type: ignore

# Configure logging
logger = logging.getLogger("windsweeper.telemetry")
logger.setLevel(logging.DEBUG)
handler = logging.NullHandler()
logger.addHandler(handler)

# Type for telemetry event
TelemetryEvent = Dict[str, Any]


class TelemetryManager:
    """Telemetry manager for tracking SDK usage and errors."""

    def __init__(self, options: Optional[Dict[str, Any]] = None):
        """
        Initialize the telemetry manager.

        Args:
            options: Telemetry configuration options
        """
        self.options = {
            "enabled": False,  # Default to off for privacy
            "endpoint": "https://telemetry.windsweeper.com/v1/events",
            "sampling_rate": 0.1,
            "error_reporting": True,
            "performance_metrics": True,
            "usage_metrics": True,
        }

        # Update with provided options
        if options:
            self.options.update(options)

        # Generate a random instance ID if not provided
        self.instance_id = self.options.get("instance_id", self._generate_instance_id())
        
        # Get package version
        try:
            self.package_version = importlib.metadata.version("windsweeper")
        except importlib.metadata.PackageNotFoundError:
            self.package_version = "unknown"

        self.operation_timers = {}
        self.queue = []
        self.send_lock = threading.Lock()
        self.initialized = False
        self.stop_event = threading.Event()
        self.sender_thread = None

        # Register cleanup on exit
        atexit.register(self.dispose)

    def initialize(self):
        """Initialize the telemetry manager and start periodic sending."""
        if self.initialized:
            return

        if self.options["enabled"]:
            # Start a thread to send telemetry periodically
            self.sender_thread = threading.Thread(
                target=self._sender_thread_func,
                daemon=True,
                name="WindsweeperTelemetrySender"
            )
            self.sender_thread.start()

            # Send initial SDK initialization event
            self.track_event("usage", "sdk.initialize", {
                "sdk_version": self.sdk_version,
                "python_version": sys.version,
                "platform": platform.system(),
                "platform_release": platform.release(),
                "architecture": platform.machine(),
            })

        self.initialized = True

    def _sender_thread_func(self):
        """Background thread function to send telemetry periodically."""
        while not self.stop_event.is_set():
            # Sleep for 60 seconds, but check for stop every second
            for _ in range(60):
                if self.stop_event.is_set():
                    break
                time.sleep(1)
            
            if not self.stop_event.is_set():
                self.send_queued_events()

    def start_operation(self, operation: str) -> str:
        """
        Start timing an operation for performance tracking.

        Args:
            operation: Name of the operation to time

        Returns:
            A unique operation ID
        """
        if not self.options["enabled"] or not self.options["performance_metrics"]:
            return operation

        op_id = f"{operation}_{time.time()}_{uuid.uuid4().hex[:8]}"
        self.operation_timers[op_id] = time.time()
        return op_id

    def end_operation(self, operation_id: str, success: bool, properties: Optional[Dict[str, Any]] = None):
        """
        End timing an operation and record performance metrics.

        Args:
            operation_id: ID of the operation to end
            success: Whether the operation was successful
            properties: Additional properties to record
        """
        if not self.options["enabled"] or not self.options["performance_metrics"]:
            return

        start = self.operation_timers.get(operation_id)
        if start is None:
            return

        duration = (time.time() - start) * 1000  # Convert to milliseconds
        self.operation_timers.pop(operation_id, None)

        # Extract the operation name from the ID
        operation = operation_id.split("_")[0]

        props = properties or {}
        props.update({
            "duration_ms": duration,
            "success": success,
        })

        self.track_event("performance", operation, props)

    def track_method_call(self, method: str, params: Optional[Dict[str, Any]] = None):
        """
        Track a method call or API request.

        Args:
            method: Name of the method being called
            params: Parameters passed to the method (sensitive data should be removed)
        """
        if not self.options["enabled"] or not self.options["usage_metrics"]:
            return

        # Check if this event should be sampled
        if self.options["sampling_rate"] < 1.0 and (
            self.options["sampling_rate"] <= 0.0 or 
            self.options["sampling_rate"] < random.random()
        ):
            return

        self.track_event("call", method, {"params": params or {}})

    def track_error(self, operation: str, error: Exception, properties: Optional[Dict[str, Any]] = None):
        """
        Track an error that occurred during SDK operation.

        Args:
            operation: Name of the operation where the error occurred
            error: The error object
            properties: Additional context properties
        """
        if not self.options["enabled"] or not self.options["error_reporting"]:
            return

        # Always track errors, regardless of sampling rate
        import traceback
        error_details = {
            "message": str(error),
            "type": error.__class__.__name__,
            "traceback": traceback.format_exc(),
        }

        props = properties or {}
        props["error"] = error_details

        self.track_event("error", operation, props)

    def track_event(self, event_type: str, operation: str, properties: Optional[Dict[str, Any]] = None):
        """
        Track a custom event.

        Args:
            event_type: Type of the event ('call', 'error', 'performance', 'usage')
            operation: Name of the operation
            properties: Custom properties for the event
        """
        if not self.options["enabled"]:
            return

        # Create telemetry event
        event = {
            "event_type": event_type,
            "operation": operation,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "properties": {
                **(properties or {}),
                "sdk_version": self.sdk_version,
                "instance_id": self.instance_id,
                "application_id": self.options.get("application_id"),
            }
        }

        # Add global context if available
        if "context" in self.options:
            event["properties"].update(self.options["context"])

        # Add to queue
        with self.send_lock:
            self.queue.append(event)

        # If queue gets too large, send immediately
        if len(self.queue) >= 100:
            self._trigger_send()

    def _trigger_send(self):
        """Trigger sending of telemetry in the background."""
        # In a more sophisticated implementation, this could wake up the sender thread
        # For simplicity, we'll just send immediately on a separate thread
        if self.options["enabled"]:
            send_thread = threading.Thread(
                target=self.send_queued_events,
                daemon=True,
                name="WindsweeperTelemetrySender-oneshot"
            )
            send_thread.start()

    def send_queued_events(self):
        """Send all queued telemetry events to the endpoint."""
        if not self.options["enabled"]:
            return

        with self.send_lock:
            if not self.queue:
                return
            events = list(self.queue)
            self.queue.clear()

        if not self.options.get("endpoint"):
            return

        # In a real implementation, this would send the events to a telemetry service
        # For this example, we'll just log them
        try:
            self._send_events_to_endpoint(events, self.options["endpoint"])
        except Exception as e:
            logger.debug(f"[Telemetry] Failed to send events: {str(e)}")
            # Put events back in queue for retry
            with self.send_lock:
                self.queue = events + self.queue

    def _send_events_to_endpoint(self, events: List[Dict[str, Any]], endpoint: str):
        """
        Send events to the telemetry endpoint.

        Args:
            events: Events to send
            endpoint: Endpoint URL
        """
        # In a real implementation, this would send data to a telemetry service
        # For privacy and simplicity in this example, we'll just log locally
        logger.debug(f"[Telemetry] Would send {len(events)} events to {endpoint}")
        
        # Actual implementation would look like:
        """
        data = json.dumps({"events": events}).encode("utf-8")
        
        headers = {
            "Content-Type": "application/json",
            "Content-Length": str(len(data)),
        }
        
        req = urllib.request.Request(endpoint, data=data, headers=headers, method="POST")
        
        try:
            with urllib.request.urlopen(req, timeout=10) as response:
                if response.status >= 200 and response.status < 300:
                    return
                else:
                    raise Exception(f"HTTP {response.status}: Failed to send telemetry")
        except urllib.error.URLError as e:
            raise Exception(f"Failed to send telemetry: {str(e)}")
        """

    def _generate_instance_id(self) -> str:
        """Generate a unique instance ID."""
        return str(uuid.uuid4())

    def dispose(self):
        """Clean up resources used by the telemetry manager."""
        # Signal the sender thread to stop
        self.stop_event.set()
        
        # Wait for the sender thread to finish (with timeout)
        if self.sender_thread and self.sender_thread.is_alive():
            self.sender_thread.join(timeout=1.0)
        
        # Send any remaining events
        self.send_queued_events()


# Create a function decorator for tracking method calls and performance
def tracked(func):
    """
    Decorator for tracking method calls and performance.
    
    Args:
        func: The function to track
    
    Returns:
        Wrapped function with telemetry tracking
    """
    def wrapper(*args, **kwargs):
        # Get the telemetry instance
        telemetry = _get_global_telemetry()
        if not telemetry or not telemetry.options["enabled"]:
            return func(*args, **kwargs)
        
        # Track method call
        method_name = func.__name__
        telemetry.track_method_call(method_name)
        
        # Start operation timing
        op_id = telemetry.start_operation(method_name)
        
        try:
            # Execute the original function
            result = func(*args, **kwargs)
            
            # End operation timing with success
            telemetry.end_operation(op_id, True)
            
            return result
        except Exception as error:
            # Track error
            telemetry.track_error(method_name, error)
            
            # End operation timing with failure
            telemetry.end_operation(op_id, False, {"error_message": str(error)})
            
            # Re-raise the error
            raise
    
    return wrapper


# Global telemetry instance
_telemetry = None


def _get_global_telemetry() -> Optional[TelemetryManager]:
    """Get the global telemetry instance."""
    global _telemetry
    return _telemetry


def get_telemetry() -> TelemetryManager:
    """Get the global telemetry manager instance."""
    global _telemetry
    if _telemetry is None:
        _telemetry = TelemetryManager()
    return _telemetry


def create_telemetry_manager(options: Optional[Dict[str, Any]] = None) -> TelemetryManager:
    """
    Create a new telemetry manager with the specified options.
    
    Args:
        options: Telemetry configuration options
        
    Returns:
        A new telemetry manager instance
    """
    return TelemetryManager(options)


def configure_telemetry(enabled: bool, options: Optional[Dict[str, Any]] = None):
    """
    Enable or disable telemetry for the SDK.
    
    Args:
        enabled: Whether telemetry should be enabled
        options: Additional telemetry options
    """
    global _telemetry
    
    if _telemetry:
        _telemetry.dispose()
    
    new_options = options or {}
    new_options["enabled"] = enabled
    
    _telemetry = TelemetryManager(new_options)
    
    if enabled:
        _telemetry.initialize()


# Initialize default telemetry instance
_telemetry = TelemetryManager()

# Import random here to avoid circular imports if this module is imported elsewhere
import random
