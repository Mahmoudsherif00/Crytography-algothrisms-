import base64
import logging

logger = logging.getLogger("vernam_cipher")
logger.setLevel(logging.DEBUG)

def encrypt(plaintext: str, key: str) -> str:
    """Vernam cipher using XOR on characters. Returns Base64."""
    logger.debug(f"Starting Vernam encrypt. Input len: {len(plaintext)}, Key len: {len(key)}")
    # XORing each character's ASCII value
    cipher_bytes = bytearray()
    for p, k in zip(plaintext, key):
        cipher_bytes.append(ord(p) ^ ord(k))
    result = base64.b64encode(cipher_bytes).decode('utf-8')
    logger.debug(f"Vernam encrypt finished. Output: {result}")
    return result

def decrypt(ciphertext_b64: str, key: str) -> str:
    """Decrypts Base64 string back to plaintext using Vernam XOR."""
    cipher_bytes = base64.b64decode(ciphertext_b64.encode('utf-8'))
    plain_chars = []
    for c, k in zip(cipher_bytes, key):
        plain_chars.append(chr(c ^ ord(k)))
    result = "".join(plain_chars)
    logger.debug(f"Vernam decrypt finished. Output len: {len(result)}")
    return result
