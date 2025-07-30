import requests
from typing import Dict, Optional, List, Any, Union
from .exceptions import ThradsError, AuthenticationError, APIError, RateLimitExceeded, NetworkError
from .models.ad import Ad


class ThradsClient:
    """Client for interacting with the Thrads platform API."""

    def __init__(self, api_key: str, base_url: str = "https://api.thrads.ai"):
        """
        Initialize Thrads client.

        Args:
            api_key: Your Thrads API key
            base_url: Base URL for API (defaults to production)
        """
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.session.headers.update({
            "X-THRADS-API-KEY": api_key,
            "Content-Type": "application/json"
        })
        # Store response metadata
        self.last_request_id = None
        self.last_response_time = None
        self.api_version = None
        self.timestamp = None

    def get_ad(self,
               user_id: str,
               chat_id: str,
               content: Dict[str, str],
               user_region: Optional[str] = None,
               meta_data: Optional[Dict[str, Any]] = None,
               production: bool = False,
               conversation_offset: int = 2,
               ad_frequency_limit: int = 5,
               ad_aggressiveness: str = "high",
               force: Optional[bool] = None) -> Optional[Ad]:
        """
        Retrieve a contextual ad recommendation.

        Args:
            user_id: Unique identifier for the user
            chat_id: Unique identifier for the conversation
            content: Dict with 'user' and 'chatbot' keys containing the latest messages
            user_region: Optional two-letter country code (ISO 3166-1 alpha-2)
            meta_data: Optional object containing user demographic information
            production: Whether the request is from a production environment
            conversation_offset: Minimum turns to wait before first ad (default: 2)
            ad_frequency_limit: Minimum turns between ads (default: 5)
            ad_aggressiveness: Ad matching flexibility: "low", "medium", or "high" (default: "high")
            force: Flag to force ad serving/suppression

        Returns:
            Ad object if successful, None if no ad was served

        Raises:
            AuthenticationError: If API key is invalid
            APIError: If API request fails
        """
        try:
            if not isinstance(content, dict) or 'user' not in content or 'chatbot' not in content:
                raise ValueError(
                    "Content must be a dictionary with 'user' and 'chatbot' keys")

            payload = {
                "userId": user_id,
                "chatId": chat_id,
                "content": content,
                "production": production
            }

            # Add optional parameters
            if user_region:
                payload["userRegion"] = user_region

            if meta_data:
                payload["metaData"] = meta_data

            if conversation_offset != 2:
                payload["conversationOffset"] = conversation_offset

            if ad_frequency_limit != 5:
                payload["adFrequencyLimit"] = ad_frequency_limit

            if ad_aggressiveness != "high":
                payload["adAggressiveness"] = ad_aggressiveness

            if force is not None:
                payload["force"] = force

            response = self.session.post(
                f"{self.base_url}/developer/serve-ad/",
                json=payload
            )

            if response.status_code == 401:
                raise AuthenticationError(
                    "Invalid API key", request_id=data.get("requestId"))
            elif response.status_code == 429:
                raise RateLimitExceeded(
                    "Rate limit exceeded", response.status_code, data.get("requestId"))

            response.raise_for_status()
            data = response.json()

            # Store response metadata
            self.last_request_id = data.get("requestId")
            self.last_response_time = data.get("totalTime")
            self.api_version = data.get("apiVersion")
            self.timestamp = data.get("timestamp")

            if data.get("status") == "error":
                raise APIError(data.get("message", "Unknown error"),
                               response.status_code,
                               data.get("requestId"))

            if data.get("adStatus") == "served" and data.get("data"):
                return Ad.from_dict(data.get("data"))
            else:
                return None

        except requests.exceptions.ConnectionError as e:
            raise NetworkError(f"Connection failed: {str(e)}")
        except requests.RequestException as e:
            raise ThradsError(f"Request failed: {str(e)}")
