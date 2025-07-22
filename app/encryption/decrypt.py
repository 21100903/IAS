from app.encryption.classic_ciphers import shift_cipher, swap_characters, vigenere_decrypt, transposition_decrypt
from app.encryption.rsa_utils import rsa_decrypt
from app.encryption.hashing import verify_sha256, compute_sha256
import base64

def decrypt_file(encrypted_bytes, metadata):
    private_key = metadata['rsa_private_key'].encode()

    # Step 0: RSA Decryption
    decrypted_rsa = rsa_decrypt(encrypted_bytes, private_key)
    print(f"[DECRYPT] RSA Decrypted (UTF-8 preview): {decrypted_rsa[:60]}...")

    # Step 1: Reverse transposition
    text = decrypted_rsa.decode('utf-8')
    transposed = transposition_decrypt(text)
    print(f"[DECRYPT] Transposition Reversed: {transposed[:60]}...")

    # Step 2: Vigenère Decryption
    vigenere_key = metadata['vigenere_key']
    vigenere_decrypted = vigenere_decrypt(transposed, vigenere_key)
    print(f"[DECRYPT] Vigenère Decrypted: {vigenere_decrypted[:60]}...")

    # Step 3: Undo even-odd swap
    unswapped = swap_characters(vigenere_decrypted)
    print(f"[DECRYPT] Characters Unswapped: {unswapped[:60]}...")

    # Step 4: Reverse shift cipher
    shifted_back = shift_cipher(unswapped, shift=-3)
    print(f"[DECRYPT] Shift Reversed (Base64): {shifted_back[:60]}...")

    # Step 5: Base64 decode back to original bytes
    try:
        original_bytes = base64.b64decode(shifted_back.encode('utf-8'))
        print(f"[DECRYPT] Base64 Decoded (raw preview): {original_bytes[:60]}...")
    except Exception as e:
        print(f"❌ Base64 decoding failed: {e}")
        return b''

    # Step 6: Verify hash
    actual_hash = compute_sha256(original_bytes)
    expected_hash = metadata['hash']

    if not verify_sha256(original_bytes, expected_hash):
        print(f"⚠️ Hash mismatch — possible tampering.")
        print(f"Expected Hash: {expected_hash}")
        print(f"Actual Hash:   {actual_hash}")
    else:
        print(f"✅ Hash matched. SHA-256: {actual_hash}")

    return original_bytes

