def shift_cipher(text, shift=3):
    result = ""
    for char in text:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            result += chr((ord(char) - base + shift) % 26 + base)
        else:
            result += char
    return result

def swap_characters(text):
    chars = list(text)
    for i in range(0, len(chars) - 1, 2):
        chars[i], chars[i+1] = chars[i+1], chars[i]
    return ''.join(chars)

def vigenere_encrypt(text, key):
    result = ""
    key = key.upper()
    key_index = 0

    for char in text:
        if char.isalpha():
            shift = ord(key[key_index % len(key)]) - ord('A')
            base = ord('A') if char.isupper() else ord('a')
            result += chr((ord(char) - base + shift) % 26 + base)
            key_index += 1
        else:
            result += char
    return result

def transposition_encrypt(text, key=5):
    columns = [''] * key
    for i, char in enumerate(text):
        col = i % key
        columns[col] += char
    return ''.join(columns)

def vigenere_decrypt(text, key):
    result = ""
    key = key.upper()
    key_index = 0

    for char in text:
        if char.isalpha():
            shift = ord(key[key_index % len(key)]) - ord('A')
            base = ord('A') if char.isupper() else ord('a')
            result += chr((ord(char) - base - shift) % 26 + base)
            key_index += 1
        else:
            result += char
    return result

def transposition_decrypt(text, key=5):
    num_cols = key
    num_rows = len(text) // key
    short_cols = len(text) % key

    cols = []
    start = 0
    for i in range(num_cols):
        col_len = num_rows + (1 if i < short_cols else 0)
        cols.append(text[start:start + col_len])
        start += col_len

    decrypted = ''
    for i in range(num_rows + 1):
        for col in cols:
            if i < len(col):
                decrypted += col[i]
    return decrypted
