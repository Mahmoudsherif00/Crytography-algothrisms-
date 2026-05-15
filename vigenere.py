def _extend_key(text: str, key: str) -> str:
    key = list(key)
    if len(text) == len(key):
        return "".join(key)
    else:
        for i in range(len(text) - len(key)):
            key.append(key[i % len(key)])
    return "".join(key)

def encrypt(plaintext: str, key: str) -> str:
    plaintext = plaintext.upper()
    key = key.upper()
    key = _extend_key(plaintext, key)
    
    ciphertext = []
    for p, k in zip(plaintext, key):
        if p.isalpha():
            # Shift by the key character
            c = chr((ord(p) + ord(k)) % 26 + 65)
            ciphertext.append(c)
        else:
            ciphertext.append(p)
    return "".join(ciphertext)

def decrypt(ciphertext: str, key: str) -> str:
    ciphertext = ciphertext.upper()
    key = key.upper()
    key = _extend_key(ciphertext, key)
    
    plaintext = []
    for c, k in zip(ciphertext, key):
        if c.isalpha():
            p = chr((ord(c) - ord(k) + 26) % 26 + 65)
            plaintext.append(p)
        else:
            plaintext.append(c)
    return "".join(plaintext)
