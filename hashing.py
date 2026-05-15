import math
import struct


def _left_rotate(value: int, shift: int, width: int = 32) -> int:
    mask = (1 << width) - 1
    shift %= width
    return ((value << shift) | (value >> (width - shift))) & mask


def _md5(message: bytes) -> str:
    original_bits = (len(message) * 8) & 0xffffffffffffffff
    message += b"\x80"
    while len(message) % 64 != 56:
        message += b"\x00"
    message += struct.pack("<Q", original_bits)

    shifts = (
        [7, 12, 17, 22] * 4
        + [5, 9, 14, 20] * 4
        + [4, 11, 16, 23] * 4
        + [6, 10, 15, 21] * 4
    )
    constants = [int(abs(math.sin(i + 1)) * (1 << 32)) & 0xffffffff for i in range(64)]

    a0 = 0x67452301
    b0 = 0xefcdab89
    c0 = 0x98badcfe
    d0 = 0x10325476

    for offset in range(0, len(message), 64):
        words = list(struct.unpack("<16I", message[offset:offset + 64]))
        a, b, c, d = a0, b0, c0, d0

        for i in range(64):
            if i < 16:
                f = (b & c) | (~b & d)
                g = i
            elif i < 32:
                f = (d & b) | (~d & c)
                g = (5 * i + 1) % 16
            elif i < 48:
                f = b ^ c ^ d
                g = (3 * i + 5) % 16
            else:
                f = c ^ (b | ~d)
                g = (7 * i) % 16

            f = (f + a + constants[i] + words[g]) & 0xffffffff
            a, d, c, b = d, c, b, (b + _left_rotate(f, shifts[i])) & 0xffffffff

        a0 = (a0 + a) & 0xffffffff
        b0 = (b0 + b) & 0xffffffff
        c0 = (c0 + c) & 0xffffffff
        d0 = (d0 + d) & 0xffffffff

    return struct.pack("<4I", a0, b0, c0, d0).hex()


def _sha1(message: bytes) -> str:
    original_bits = len(message) * 8
    message += b"\x80"
    while len(message) % 64 != 56:
        message += b"\x00"
    message += struct.pack(">Q", original_bits)

    h0 = 0x67452301
    h1 = 0xefcdab89
    h2 = 0x98badcfe
    h3 = 0x10325476
    h4 = 0xc3d2e1f0

    for offset in range(0, len(message), 64):
        words = list(struct.unpack(">16I", message[offset:offset + 64]))
        for i in range(16, 80):
            words.append(_left_rotate(words[i - 3] ^ words[i - 8] ^ words[i - 14] ^ words[i - 16], 1))

        a, b, c, d, e = h0, h1, h2, h3, h4

        for i in range(80):
            if i < 20:
                f = (b & c) | (~b & d)
                k = 0x5a827999
            elif i < 40:
                f = b ^ c ^ d
                k = 0x6ed9eba1
            elif i < 60:
                f = (b & c) | (b & d) | (c & d)
                k = 0x8f1bbcdc
            else:
                f = b ^ c ^ d
                k = 0xca62c1d6

            temp = (_left_rotate(a, 5) + f + e + k + words[i]) & 0xffffffff
            a, b, c, d, e = temp, a, _left_rotate(b, 30), c, d

        h0 = (h0 + a) & 0xffffffff
        h1 = (h1 + b) & 0xffffffff
        h2 = (h2 + c) & 0xffffffff
        h3 = (h3 + d) & 0xffffffff
        h4 = (h4 + e) & 0xffffffff

    return f"{h0:08x}{h1:08x}{h2:08x}{h3:08x}{h4:08x}"


def _right_rotate(value: int, shift: int) -> int:
    return ((value >> shift) | (value << (32 - shift))) & 0xffffffff


def _sha256(message: bytes) -> str:
    original_bits = len(message) * 8
    message += b"\x80"
    while len(message) % 64 != 56:
        message += b"\x00"
    message += struct.pack(">Q", original_bits)

    h = [
        0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a,
        0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19,
    ]
    k = [
        0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5,
        0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
        0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3,
        0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
        0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc,
        0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
        0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7,
        0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
        0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13,
        0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
        0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3,
        0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
        0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5,
        0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
        0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208,
        0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2,
    ]

    for offset in range(0, len(message), 64):
        words = list(struct.unpack(">16I", message[offset:offset + 64]))
        for i in range(16, 64):
            s0 = _right_rotate(words[i - 15], 7) ^ _right_rotate(words[i - 15], 18) ^ (words[i - 15] >> 3)
            s1 = _right_rotate(words[i - 2], 17) ^ _right_rotate(words[i - 2], 19) ^ (words[i - 2] >> 10)
            words.append((words[i - 16] + s0 + words[i - 7] + s1) & 0xffffffff)

        a, b, c, d, e, f, g, hh = h

        for i in range(64):
            s1 = _right_rotate(e, 6) ^ _right_rotate(e, 11) ^ _right_rotate(e, 25)
            ch = (e & f) ^ (~e & g)
            temp1 = (hh + s1 + ch + k[i] + words[i]) & 0xffffffff
            s0 = _right_rotate(a, 2) ^ _right_rotate(a, 13) ^ _right_rotate(a, 22)
            maj = (a & b) ^ (a & c) ^ (b & c)
            temp2 = (s0 + maj) & 0xffffffff

            hh, g, f, e, d, c, b, a = g, f, e, (d + temp1) & 0xffffffff, c, b, a, (temp1 + temp2) & 0xffffffff

        h = [(current + new) & 0xffffffff for current, new in zip(h, (a, b, c, d, e, f, g, hh))]

    return "".join(f"{part:08x}" for part in h)


def hash_text(plaintext: str, algorithm: str) -> str:
    data = plaintext.encode("utf-8")

    if algorithm == "MD5":
        return _md5(data)
    elif algorithm == "SHA-1":
        return _sha1(data)
    elif algorithm == "SHA-256":
        return _sha256(data)
    else:
        raise ValueError("Unsupported hashing algorithm")
