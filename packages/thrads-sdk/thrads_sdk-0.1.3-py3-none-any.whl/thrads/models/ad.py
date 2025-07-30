from typing import Optional, Dict, Any
from dataclasses import dataclass
import base64
from io import BytesIO
from PIL import Image


@dataclass
class Ad:
    """Represents an ad from the Thrads platform."""

    creative: str
    prod_name: str
    prod_url: str
    img_url: str

    @classmethod
    def from_dict(cls, data: dict) -> 'Ad':
        """Create an Ad instance from API response data."""
        return cls(
            creative=data.get("creative", ""),
            prod_name=data.get("prod_name", ""),
            prod_url=data.get("prod_url", ""),
            img_url=data.get("img_url", "")
        )

    def get_image(self):
        """Convert base64 image to PIL Image if available."""
        if not self.img_url or not self.img_url.startswith('data:image'):
            return None

        try:
            # Extract base64 data after the comma
            img_data = self.img_url.split(',')[1]
            image_bytes = base64.b64decode(img_data)
            return Image.open(BytesIO(image_bytes))
        except:
            return None
