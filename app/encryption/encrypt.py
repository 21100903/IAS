from app.encryption.classic_ciphers import shift_cipher, swap_characters, vigenere_encrypt, transposition_encrypt
from app.encryption.rsa_utils import generate_rsa_keys, rsa_encrypt
from app.encryption.hashing import compute_sha256
import base64

def encrypt_file(file_bytes, filename):
    # 🔍 Step 0: Raw input (first 60 chars only for preview)
    print(f"[ENCRYPT] Raw Input Preview (bytes): {file_bytes[:60]}...")

    # Step 1: Base64 encode to string
    text = base64.b64encode(file_bytes).decode('utf-8')
    print(f"[ENCRYPT] Base64 Encoded: {text[:60]}...")

    # Step 2: Shift Cipher
    shifted = shift_cipher(text, shift=3)
    print(f"[ENCRYPT] Shifted: {shifted[:60]}...")

    # Step 3: Swap even-odd characters
    swapped = swap_characters(shifted)
    print(f"[ENCRYPT] Swapped: {swapped[:60]}...")

    # Step 4: Vigenère Cipher
    vigenere_key = "SECURE"
    vigenere_encrypted = vigenere_encrypt(swapped, vigenere_key)
    print(f"[ENCRYPT] Vigenère: {vigenere_encrypted[:60]}...")

    # Step 5: Transposition Cipher
    transposed = transposition_encrypt(vigenere_encrypted)
    print(f"[ENCRYPT] Transposed: {transposed[:60]}...")

    # Step 6: RSA Encryption
    public_key, private_key = generate_rsa_keys()
    rsa_encrypted_bytes = rsa_encrypt(transposed.encode('utf-8'), public_key)
    print(f"[ENCRYPT] RSA encrypted length: {len(rsa_encrypted_bytes)}")

    # Hash of original
    original_hash = compute_sha256(file_bytes)
    print(f"[ENCRYPT] Hash Value [SHA256]: {original_hash}")

    metadata = {
        "hash": original_hash,
        "vigenere_key": vigenere_key,
        "rsa_public_key": public_key.decode(),
        "rsa_private_key": private_key.decode()
    }

    return rsa_encrypted_bytes, metadata
