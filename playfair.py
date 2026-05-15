def create_matrix(key: str) -> list:
    key = key.upper().replace('J', 'I')
    matrix = []
    seen = set()
    
    # Add key characters
    for char in key:
        if char.isalpha() and char not in seen:
            seen.add(char)
            matrix.append(char)
            
    # Add remaining alphabet
    for char in "ABCDEFGHIKLMNOPQRSTUVWXYZ":
        if char not in seen:
            seen.add(char)
            matrix.append(char)
            
    return [matrix[i:i+5] for i in range(0, 25, 5)]

def find_position(matrix: list, char: str):
    for i in range(5):
        for j in range(5):
            if matrix[i][j] == char:
                return i, j
    return -1, -1

def prepare_text(text: str) -> str:
    text = "".join([c.upper() for c in text if c.isalpha()]).replace('J', 'I')
    prepared = ""
    i = 0
    while i < len(text):
        prepared += text[i]
        if i + 1 < len(text):
            if text[i] == text[i+1]:
                prepared += 'X'
                i += 1
            else:
                prepared += text[i+1]
                i += 2
        else:
            prepared += 'X'
            i += 1
    return prepared

def encrypt(plaintext: str, key: str) -> str:
    matrix = create_matrix(key)
    prepared = prepare_text(plaintext)
    ciphertext = ""
    
    for i in range(0, len(prepared), 2):
        c1, c2 = prepared[i], prepared[i+1]
        r1, col1 = find_position(matrix, c1)
        r2, col2 = find_position(matrix, c2)
        
        if r1 == r2:
            ciphertext += matrix[r1][(col1 + 1) % 5] + matrix[r2][(col2 + 1) % 5]
        elif col1 == col2:
            ciphertext += matrix[(r1 + 1) % 5][col1] + matrix[(r2 + 1) % 5][col2]
        else:
            ciphertext += matrix[r1][col2] + matrix[r2][col1]
            
    return ciphertext

def decrypt(ciphertext: str, key: str) -> str:
    matrix = create_matrix(key)
    ciphertext = "".join([c.upper() for c in ciphertext if c.isalpha()])
    plaintext = ""
    
    for i in range(0, len(ciphertext), 2):
        c1, c2 = ciphertext[i], ciphertext[i+1]
        r1, col1 = find_position(matrix, c1)
        r2, col2 = find_position(matrix, c2)
        
        if r1 == r2:
            plaintext += matrix[r1][(col1 - 1) % 5] + matrix[r2][(col2 - 1) % 5]
        elif col1 == col2:
            plaintext += matrix[(r1 - 1) % 5][col1] + matrix[(r2 - 1) % 5][col2]
        else:
            plaintext += matrix[r1][col2] + matrix[r2][col1]
            
    return plaintext
