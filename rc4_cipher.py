import base64



def _ksa(key_bytes: bytes) -> list[int]:
    state = list(range(256))
    j = 0

    for i in range(256):
        j = (j + state[i] + key_bytes[i % len(key_bytes)]) % 256
        state[i], state[j] = state[j], state[i]

    return state


def _keystream(key_bytes: bytes):
    state = _ksa(key_bytes)
    i = 0
    j = 0

    while True:
        i = (i + 1) % 256
        j = (j + state[i]) % 256
        state[i], state[j] = state[j], state[i]
        yield state[(state[i] + state[j]) % 256]


def _xor_with_rc4(data: bytes, key: str) -> bytes:
    key_bytes = key.encode("utf-8")
    stream = _keystream(key_bytes)
    return bytes(byte ^ next(stream) for byte in data)


def encrypt(plaintext: str, key: str) -> str:
    encrypted_bytes = _xor_with_rc4(plaintext.encode("utf-8"), key)
    return base64.b64encode(encrypted_bytes).decode("utf-8")


def decrypt(ciphertext_b64: str, key: str) -> str:
    encrypted_bytes = base64.b64decode(ciphertext_b64)
    decrypted_bytes = _xor_with_rc4(encrypted_bytes, key)
    return decrypted_bytes.decode("utf-8")
