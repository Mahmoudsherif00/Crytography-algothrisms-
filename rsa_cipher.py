import base64
import secrets
from dataclasses import dataclass


@dataclass(frozen=True)
class PublicKey:
    n: int
    e: int


@dataclass(frozen=True)
class PrivateKey:
    n: int
    d: int


def _egcd(a: int, b: int) -> tuple[int, int, int]:
    if b == 0:
        return a, 1, 0

    gcd, x1, y1 = _egcd(b, a % b)
    return gcd, y1, x1 - (a // b) * y1


def _mod_inverse(value: int, modulus: int) -> int:
    gcd, x, _ = _egcd(value, modulus)
    if gcd != 1:
        raise ValueError("Value has no modular inverse.")
    return x % modulus


def _is_probable_prime(candidate: int, rounds: int = 40) -> bool:
    if candidate < 2:
        return False

    small_primes = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)
    if candidate in small_primes:
        return True
    if any(candidate % prime == 0 for prime in small_primes):
        return False

    d = candidate - 1
    r = 0
    while d % 2 == 0:
        d //= 2
        r += 1

    for _ in range(rounds):
        a = secrets.randbelow(candidate - 3) + 2
        x = pow(a, d, candidate)
        if x in (1, candidate - 1):
            continue

        for _ in range(r - 1):
            x = pow(x, 2, candidate)
            if x == candidate - 1:
                break
        else:
            return False

    return True


def _generate_prime(bits: int) -> int:
    while True:
        candidate = secrets.randbits(bits)
        candidate |= (1 << (bits - 1)) | 1
        if _is_probable_prime(candidate):
            return candidate


def generate_keys(keysize=1024):
    e = 65537
    half_bits = keysize // 2

    while True:
        p = _generate_prime(half_bits)
        q = _generate_prime(keysize - half_bits)
        if p == q:
            continue

        n = p * q
        phi = (p - 1) * (q - 1)
        if phi % e != 0:
            d = _mod_inverse(e, phi)
            return PublicKey(n, e), PrivateKey(n, d)


def encrypt(plaintext: str, public_key: PublicKey) -> str:
    plain_bytes = plaintext.encode("utf-8")
    modulus_size = (public_key.n.bit_length() + 7) // 8
    chunk_size = modulus_size - 1
    encrypted = bytearray()

    for start in range(0, len(plain_bytes), chunk_size):
        chunk = plain_bytes[start:start + chunk_size]
        message = int.from_bytes(chunk, "big")
        cipher = pow(message, public_key.e, public_key.n)
        encrypted.extend(len(chunk).to_bytes(2, "big"))
        encrypted.extend(cipher.to_bytes(modulus_size, "big"))

    return base64.b64encode(encrypted).decode("utf-8")


def decrypt(ciphertext_b64: str, private_key: PrivateKey) -> str:
    encrypted_bytes = base64.b64decode(ciphertext_b64)
    modulus_size = (private_key.n.bit_length() + 7) // 8
    record_size = 2 + modulus_size
    decrypted = bytearray()

    if len(encrypted_bytes) % record_size != 0:
        raise ValueError("Invalid RSA ciphertext.")

    for start in range(0, len(encrypted_bytes), record_size):
        chunk_len = int.from_bytes(encrypted_bytes[start:start + 2], "big")
        cipher_start = start + 2
        cipher_end = cipher_start + modulus_size
        cipher = int.from_bytes(encrypted_bytes[cipher_start:cipher_end], "big")
        message = pow(cipher, private_key.d, private_key.n)
        decrypted.extend(message.to_bytes(chunk_len, "big"))

    return decrypted.decode("utf-8")
