from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64

def generate_rsa_keys(key_size=2048):
    key = RSA.generate(key_size)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    return public_key, private_key

def rsa_encrypt(data: bytes, public_key_pem: bytes) -> bytes:
    key = RSA.import_key(public_key_pem)
    cipher = PKCS1_OAEP.new(key)
    
    chunk_size = key.size_in_bytes() - 42  # PKCS1_OAEP padding overhead
    encrypted_chunks = []

    for i in range(0, len(data), chunk_size):
        chunk = data[i:i + chunk_size]
        encrypted_chunk = cipher.encrypt(chunk)
        encrypted_chunks.append(encrypted_chunk)

    return b"".join(encrypted_chunks)

def rsa_decrypt(data: bytes, private_key_pem: bytes) -> bytes:
    key = RSA.import_key(private_key_pem)
    cipher = PKCS1_OAEP.new(key)

    chunk_size = key.size_in_bytes()
    decrypted_chunks = []

    for i in range(0, len(data), chunk_size):
        chunk = data[i:i + chunk_size]
        decrypted_chunk = cipher.decrypt(chunk)
        decrypted_chunks.append(decrypted_chunk)

    return b"".join(decrypted_chunks)
