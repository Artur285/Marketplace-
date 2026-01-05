"""
Authentication Module for API Integrations
Handles various authentication methods for supplier APIs
"""

from abc import ABC, abstractmethod
from typing import Dict, Optional
from datetime import datetime, timedelta
import hashlib
import hmac


class AuthProvider(ABC):
    """Base class for authentication providers"""
    
    @abstractmethod
    def authenticate(self, credentials: Dict) -> Optional[str]:
        """Authenticate and return token/key"""
        pass
    
    @abstractmethod
    def validate(self, token: str) -> bool:
        """Validate an authentication token"""
        pass
    
    @abstractmethod
    def refresh(self, token: str) -> Optional[str]:
        """Refresh an authentication token"""
        pass


class APIKeyAuthProvider(AuthProvider):
    """API Key authentication provider"""
    
    def __init__(self):
        self.api_keys: Dict[str, Dict] = {}
        
    def authenticate(self, credentials: Dict) -> Optional[str]:
        """Authenticate using API key"""
        api_key = credentials.get('api_key')
        if api_key and self._validate_key(api_key):
            return api_key
        return None
    
    def validate(self, token: str) -> bool:
        """Validate API key"""
        return self._validate_key(token)
    
    def refresh(self, token: str) -> Optional[str]:
        """API keys don't need refresh"""
        return token
    
    def _validate_key(self, api_key: str) -> bool:
        """Validate API key format and existence"""
        return api_key in self.api_keys
    
    def register_key(self, api_key: str, metadata: Dict):
        """Register a new API key"""
        self.api_keys[api_key] = {
            'created_at': datetime.now(),
            'metadata': metadata
        }


class OAuth2AuthProvider(AuthProvider):
    """OAuth 2.0 authentication provider"""
    
    def __init__(self):
        self.tokens: Dict[str, Dict] = {}
        
    def authenticate(self, credentials: Dict) -> Optional[str]:
        """Authenticate using OAuth 2.0"""
        client_id = credentials.get('client_id')
        client_secret = credentials.get('client_secret')
        
        if not client_id or not client_secret:
            return None
        
        # Generate access token (simplified)
        token = self._generate_token(client_id, client_secret)
        
        self.tokens[token] = {
            'client_id': client_id,
            'issued_at': datetime.now(),
            'expires_at': datetime.now() + timedelta(hours=1)
        }
        
        return token
    
    def validate(self, token: str) -> bool:
        """Validate OAuth token"""
        token_data = self.tokens.get(token)
        if not token_data:
            return False
        
        return datetime.now() < token_data['expires_at']
    
    def refresh(self, token: str) -> Optional[str]:
        """Refresh OAuth token"""
        token_data = self.tokens.get(token)
        if not token_data:
            return None
        
        # Generate new token
        new_token = self._generate_token(token_data['client_id'], 'refresh')
        
        self.tokens[new_token] = {
            'client_id': token_data['client_id'],
            'issued_at': datetime.now(),
            'expires_at': datetime.now() + timedelta(hours=1)
        }
        
        # Invalidate old token
        del self.tokens[token]
        
        return new_token
    
    def _generate_token(self, client_id: str, secret: str) -> str:
        """Generate an access token"""
        data = f"{client_id}:{secret}:{datetime.now().isoformat()}"
        return hashlib.sha256(data.encode()).hexdigest()


class HMACAuthProvider(AuthProvider):
    """HMAC signature authentication provider"""
    
    def __init__(self):
        self.secrets: Dict[str, str] = {}
        
    def authenticate(self, credentials: Dict) -> Optional[str]:
        """Authenticate using HMAC signature"""
        access_key = credentials.get('access_key')
        signature = credentials.get('signature')
        message = credentials.get('message')
        
        if not all([access_key, signature, message]):
            return None
        
        secret = self.secrets.get(access_key)
        if not secret:
            return None
        
        expected_signature = self._generate_signature(secret, message)
        
        if hmac.compare_digest(signature, expected_signature):
            return access_key
        
        return None
    
    def validate(self, token: str) -> bool:
        """Validate HMAC access key"""
        return token in self.secrets
    
    def refresh(self, token: str) -> Optional[str]:
        """HMAC keys don't need refresh"""
        return token
    
    def register_secret(self, access_key: str, secret: str):
        """Register a new HMAC secret"""
        self.secrets[access_key] = secret
    
    def _generate_signature(self, secret: str, message: str) -> str:
        """Generate HMAC signature"""
        return hmac.new(
            secret.encode(),
            message.encode(),
            hashlib.sha256
        ).hexdigest()


class AuthenticationManager:
    """Manages multiple authentication providers"""
    
    def __init__(self):
        self.providers: Dict[str, AuthProvider] = {
            'api_key': APIKeyAuthProvider(),
            'oauth2': OAuth2AuthProvider(),
            'hmac': HMACAuthProvider()
        }
        
    def get_provider(self, auth_type: str) -> Optional[AuthProvider]:
        """Get an authentication provider by type"""
        return self.providers.get(auth_type)
    
    def authenticate(self, auth_type: str, credentials: Dict) -> Optional[str]:
        """Authenticate using specified provider"""
        provider = self.get_provider(auth_type)
        if provider:
            return provider.authenticate(credentials)
        return None
    
    def validate(self, auth_type: str, token: str) -> bool:
        """Validate a token using specified provider"""
        provider = self.get_provider(auth_type)
        if provider:
            return provider.validate(token)
        return False
