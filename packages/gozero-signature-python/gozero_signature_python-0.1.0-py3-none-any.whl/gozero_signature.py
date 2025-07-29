# Rename this file to gozero_signature.py
import base64
import hashlib
import hmac
import json
import time
from typing import Dict, Union, Any
from urllib.parse import urlparse

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5


class GoZeroSigner:
    """
    A Python implementation of go-zero framework signature functionality.
    This class generates security signatures compatible with go-zero framework.
    """

    def __init__(self, public_key: str, key: str):
        """
        Initialize the GoZeroSigner with a public key and key.
        
        Args:
            public_key: RSA public key in PEM format
            key: Secret key for HMAC signing (will be base64 encoded)
        """
        self.public_key = public_key
        self.key = base64.b64decode(key) if self._is_base64(key) else key.encode('utf-8')
        
    @staticmethod
    def _is_base64(s: str) -> bool:
        """Check if a string is base64 encoded."""
        try:
            return base64.b64encode(base64.b64decode(s)).decode() == s
        except Exception:
            return False
            
    @staticmethod
    def _fingerprint(key: str) -> str:
        """
        Generate MD5 fingerprint of the key.
        
        Args:
            key: The key to generate fingerprint for
            
        Returns:
            Base64 encoded MD5 hash
        """
        h = hashlib.md5()
        h.update(key.encode('utf-8'))
        return base64.b64encode(h.digest()).decode('utf-8')
        
    @staticmethod
    def _hs256(key: bytes, body: str) -> str:
        """
        Generate HMAC-SHA256 signature.
        
        Args:
            key: The key for HMAC
            body: The content to sign
            
        Returns:
            Base64 encoded HMAC-SHA256 signature
        """
        h = hmac.new(key, body.encode('utf-8'), hashlib.sha256)
        return base64.b64encode(h.digest()).decode('utf-8')
        
    def _encrypt_with_rsa(self, content: str) -> str:
        """
        Encrypt content with RSA public key.
        
        Args:
            content: The content to encrypt
            
        Returns:
            Base64 encoded encrypted content
        """
        rsa_key = RSA.importKey(self.public_key)
        cipher = PKCS1_v1_5.new(rsa_key)
        encrypted = cipher.encrypt(content.encode('utf-8'))
        return base64.b64encode(encrypted).decode('utf-8')
        
    def generate_get_signature(self, url: str) -> str:
        """
        Generate security signature header value specifically for GET requests.
        
        Args:
            url: Request URL
            
        Returns:
            The value for X-Content-Security header
        """
        return self.generate_signature(
            method="GET",
            url=url,
            payload="",
            content_type="application/json"
        )

    def generate_post_signature(self, url: str, payload: Dict[str, Any]) -> str:
        """
        Generate security signature header value specifically for POST requests.
        
        Args:
            url: Request URL
            payload: Request payload (dict or JSON string)
            
        Returns:
            The value for X-Content-Security header
        """
        return self.generate_signature(
            method="POST",
            url=url,
            payload=payload,
            content_type="application/json"
        )
    


    def generate_signature(self, 
                          method: str, 
                          url: str, 
                          payload: Union[Dict[str, Any], str], 
                          content_type: str = "application/json") -> str:
        """
        Generate security signature header value for an API request.
        
        Args:
            method: HTTP method (GET, POST, etc.)
            url: Request URL
            payload: Request payload (dict or JSON string)
            content_type: Content type of the request
            
        Returns:
            The value for X-Content-Security header
        """
        # Convert dict payload to JSON string if needed
        if isinstance(payload, dict):
            payload = json.dumps(payload)
            
        # Parse URL
        parsed_url = urlparse(url)
        path = parsed_url.path
        query = parsed_url.query
        
        # Calculate body hash
        sha = hashlib.sha256()
        sha.update(payload.encode('utf-8'))
        body_sign = sha.hexdigest()
        
        # Current timestamp
        timestamp = int(time.time())
        
        # Content to sign
        content_of_sign = "\n".join([
            str(timestamp),
            method,
            path,
            query,
            body_sign
        ])
        
        # Generate HMAC signature
        sign = self._hs256(self.key, content_of_sign)
        
        # Generate content for encryption
        content = "; ".join([
            "version=v1",
            "type=0",
            f"key={base64.b64encode(self.key).decode('utf-8')}",
            f"time={timestamp}"
        ])
        
        # Encrypt content with RSA
        encrypted_content = self._encrypt_with_rsa(content)
        
        # Generate X-Content-Security header value
        header_value = "; ".join([
            f"key={self._fingerprint(self.public_key)}",
            f"secret={encrypted_content}",
            f"signature={sign}"
        ])
        
        return header_value