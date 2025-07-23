"""
Custom URL Encryption System
Completely original implementation for privacy protection
"""

import secrets
import hashlib
import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os


class SecureURLShield:
    """
    Custom URL encryption system - completely unique implementation
    Replaces Whoogle's gAAA system with our own approach
    """
    
    # Custom Base64 alphabet - completely different from standard
    CUSTOM_ALPHABET = "ZYXWVUTSRQPONMLKJIHGFEDCBAzyxwvutsrqponmlkjihgfedcba9876543210-_"
    STANDARD_ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
    
    # Our unique prefix (instead of gAAA)
    SHIELD_PREFIX = "SX"  # SecureX prefix - customize this to your brand
    
    def __init__(self, master_key: bytes):
        """
        Initialize with a master key for encryption
        
        Args:
            master_key (bytes): Master encryption key
        """
        self.master_key = master_key
        
    def _custom_encode(self, data: bytes) -> str:
        """
        Custom encoding using our own alphabet
        Makes the output completely unrecognizable
        """
        # First do standard base64
        standard_b64 = base64.b64encode(data).decode()
        
        # Translate to our custom alphabet
        result = ""
        for char in standard_b64:
            if char in self.STANDARD_ALPHABET:
                idx = self.STANDARD_ALPHABET.index(char)
                result += self.CUSTOM_ALPHABET[idx]
            else:
                result += char  # Keep padding chars as is
                
        return result
    
    def _custom_decode(self, encoded: str) -> bytes:
        """
        Decode from our custom alphabet back to bytes
        """
        # Translate back to standard alphabet
        result = ""
        for char in encoded:
            if char in self.CUSTOM_ALPHABET:
                idx = self.CUSTOM_ALPHABET.index(char)
                result += self.STANDARD_ALPHABET[idx]
            else:
                result += char  # Keep padding chars as is
                
        return base64.b64decode(result)
    
    def _derive_key(self, salt: bytes, url_hash: bytes) -> bytes:
        """
        Derive encryption key using PBKDF2
        """
        return hashlib.pbkdf2_hmac(
            'sha256',
            self.master_key + url_hash,
            salt,
            100000,  # iterations
            32  # key length
        )
    
    def shield_url(self, url: str) -> str:
        """
        Encrypt and encode URL with custom system
        
        Args:
            url (str): Original URL to protect
            
        Returns:
            str: Shielded URL with our custom prefix
        """
        # Create URL hash for key derivation
        url_hash = hashlib.sha256(url.encode()).digest()[:8]
        
        # Generate random salt
        salt = secrets.token_bytes(16)
        
        # Derive unique key for this URL
        derived_key = self._derive_key(salt, url_hash)
        
        # Generate random IV
        iv = secrets.token_bytes(16)
        
        # Encrypt URL with AES-256-CBC
        cipher = Cipher(
            algorithms.AES(derived_key),
            modes.CBC(iv),
            backend=default_backend()
        )
        encryptor = cipher.encryptor()
        
        # Pad URL to block size
        url_bytes = url.encode('utf-8')
        padding_length = 16 - (len(url_bytes) % 16)
        padded_url = url_bytes + bytes([padding_length]) * padding_length
        
        encrypted_url = encryptor.update(padded_url) + encryptor.finalize()
        
        # Combine salt + iv + url_hash + encrypted_url
        combined = salt + iv + url_hash + encrypted_url
        
        # Encode with our custom system
        encoded = self._custom_encode(combined)
        
        # Add our unique prefix
        return f"{self.SHIELD_PREFIX}{encoded}"
    
    def unshield_url(self, shielded_url: str) -> str:
        """
        Decrypt and decode URL from shielded format
        
        Args:
            shielded_url (str): Encrypted URL with our prefix
            
        Returns:
            str: Original URL
        """
        if not shielded_url.startswith(self.SHIELD_PREFIX):
            return shielded_url  # Not our format, return as-is
            
        # Remove our prefix
        encoded_data = shielded_url[len(self.SHIELD_PREFIX):]
        
        try:
            # Decode from our custom encoding
            combined = self._custom_decode(encoded_data)
            
            # Extract components
            salt = combined[:16]
            iv = combined[16:32]
            url_hash = combined[32:40]
            encrypted_url = combined[40:]
            
            # Derive the same key
            derived_key = self._derive_key(salt, url_hash)
            
            # Decrypt
            cipher = Cipher(
                algorithms.AES(derived_key),
                modes.CBC(iv),
                backend=default_backend()
            )
            decryptor = cipher.decryptor()
            
            padded_url = decryptor.update(encrypted_url) + decryptor.finalize()
            
            # Remove padding
            padding_length = padded_url[-1]
            url = padded_url[:-padding_length].decode('utf-8')
            
            # Verify URL hash matches (integrity check)
            expected_hash = hashlib.sha256(url.encode()).digest()[:8]
            if url_hash != expected_hash:
                raise ValueError("URL integrity check failed")
                
            return url
            
        except Exception as e:
            # If decryption fails, return original (might be unencrypted URL)
            return shielded_url
    
    def is_shielded(self, url: str) -> bool:
        """
        Check if URL is in our shielded format
        
        Args:
            url (str): URL to check
            
        Returns:
            bool: True if URL is shielded
        """
        return url.startswith(self.SHIELD_PREFIX)


# Convenience functions for easy integration
def create_url_shield(session_key: bytes) -> SecureURLShield:
    """Create URL shield instance with session key"""
    return SecureURLShield(session_key)

def shield_external_url(url: str, session_key: bytes) -> str:
    """Quick function to shield a URL"""
    shield = create_url_shield(session_key)
    return shield.shield_url(url)

def unshield_external_url(shielded_url: str, session_key: bytes) -> str:
    """Quick function to unshield a URL"""
    shield = create_url_shield(session_key)
    return shield.unshield_url(shielded_url)