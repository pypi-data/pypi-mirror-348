"""
Feedback collection module for the Windsweeper SDK
This allows users to provide feedback directly from their application
"""

import json
import platform
import sys
import time
from datetime import datetime
from typing import Dict, Literal, Optional, TypedDict, Union, Any

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False


class FeedbackOptions(TypedDict, total=False):
    """Options for sending feedback"""
    sdk: Literal["nodejs", "python"]
    version: str
    rating: Optional[int]  # 1-5 rating
    category: Optional[Literal["bug", "feature", "usability", "documentation", "other"]]
    email: Optional[str]  # Optional email for follow-up
    allow_collect_env: Optional[bool]  # Whether to collect environment info


class FeedbackPayload(FeedbackOptions):
    """Complete feedback payload with message and environment info"""
    message: str
    timestamp: str
    environment: Optional[Dict[str, str]]


def send_feedback(
    message: str,
    options: FeedbackOptions
) -> Dict[str, Union[bool, str]]:
    """
    Send feedback about the SDK to the Windsweeper team
    
    Args:
        message: Feedback message
        options: Additional options for the feedback
        
    Returns:
        Dict with success status and message
    """
    if not message or not message.strip():
        return {"success": False, "message": "Feedback message cannot be empty"}

    payload: Dict[str, Any] = {
        **options,
        "message": message,
        "timestamp": datetime.now().isoformat()
    }

    # Collect environment info if allowed
    if options.get("allow_collect_env"):
        payload["environment"] = {
            "os": f"{platform.system()} {platform.release()}",
            "pythonVersion": sys.version,
        }

    try:
        # In a real implementation, this would send the feedback to a server
        # For this example, we'll just log it and simulate a server response
        print(f"Sending feedback to Windsweeper team: {json.dumps(payload, indent=2)}")
        
        # Simulate API call
        time.sleep(0.5)  # Simulate network delay
        return {
            "success": True,
            "message": "Thank you for your feedback! We appreciate your input."
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"Failed to send feedback: {str(e)}"
        }


"""
Real implementation would look like this:
This is commented out since we don't have an actual feedback endpoint
"""
'''
def send_to_server(payload: Dict[str, Any]) -> Dict[str, Union[bool, str]]:
    """Send feedback to the server"""
    if not HAS_REQUESTS:
        return {
            "success": False, 
            "message": "The 'requests' package is required to send feedback. Install with: pip install requests"
        }
    
    try:
        response = requests.post(
            "https://feedback.windsweeper.com/api/sdk-feedback",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        response.raise_for_status()
        data = response.json()
        
        return {
            "success": True,
            "message": data.get("message", "Feedback received")
        }
    except requests.RequestException as e:
        return {
            "success": False,
            "message": f"Failed to send feedback: {str(e)}"
        }
'''
