import os
import base64
import hashlib
from typing import Tuple
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import hmac
from cryptography.exceptions import InvalidKey

# 상수 정의
SALT_SIZE = 32
IV_SIZE = 16
KEY_LENGTH = 32
ITERATIONS = 480000

def _derive_key(master_key: bytes, salt: bytes) -> bytes:
    """PBKDF2를 사용하여 마스터 키로부터 암호화 키 유도"""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA512(),
        length=KEY_LENGTH,
        salt=salt,
        iterations=ITERATIONS,
    )
    return kdf.derive(master_key)

def _create_hmac(key: bytes, data: bytes) -> bytes:
    """데이터 무결성을 위한 HMAC 생성"""
    h = hmac.HMAC(key, hashes.SHA512())
    h.update(data)
    return h.finalize()

def _verify_hmac(key: bytes, data: bytes, signature: bytes) -> bool:
    """HMAC 검증"""
    h = hmac.HMAC(key, hashes.SHA512())
    h.update(data)
    try:
        h.verify(signature)
        return True
    except InvalidKey:
        return False

def _aes_encrypt(key: bytes, iv: bytes, data: bytes) -> bytes:
    """AES-256-GCM 암호화"""
    cipher = Cipher(algorithms.AES256(key), modes.GCM(iv))
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(data) + encryptor.finalize()
    return ciphertext + encryptor.tag

def _aes_decrypt(key: bytes, iv: bytes, data: bytes) -> bytes:
    """AES-256-GCM 복호화"""
    tag = data[-16:]  # GCM 태그는 마지막 16바이트
    ciphertext = data[:-16]
    cipher = Cipher(algorithms.AES256(key), modes.GCM(iv, tag))
    decryptor = cipher.decryptor()
    return decryptor.update(ciphertext) + decryptor.finalize()

def _chacha20_encrypt(key: bytes, nonce: bytes, data: bytes) -> bytes:
    """ChaCha20 암호화"""
    cipher = Cipher(algorithms.ChaCha20(key, nonce), mode=None)
    encryptor = cipher.encryptor()
    return encryptor.update(data)

def _chacha20_decrypt(key: bytes, nonce: bytes, data: bytes) -> bytes:
    """ChaCha20 복호화"""
    cipher = Cipher(algorithms.ChaCha20(key, nonce), mode=None)
    decryptor = cipher.decryptor()
    return decryptor.update(data)

def encrypt(text: str, key: str) -> str:
    """텍스트를 암호화합니다.
    
    Args:
        text (str): 암호화할 텍스트
        key (str): 암호화 키
        
    Returns:
        str: 암호화된 텍스트 (base64 인코딩)
    """
    # 초기 값들 생성
    salt = os.urandom(SALT_SIZE)
    iv = os.urandom(IV_SIZE)
    nonce = os.urandom(16)
    
    # 키 유도
    master_key = key.encode()
    main_key = _derive_key(master_key, salt)
    aes_key = hashlib.sha512(main_key + b"aes").digest()[:32]
    chacha_key = hashlib.sha512(main_key + b"chacha").digest()[:32]
    hmac_key = hashlib.sha512(main_key + b"hmac").digest()[:32]

    # 데이터 암호화 (이중 암호화)
    data_bytes = text.encode()
    aes_encrypted = _aes_encrypt(aes_key, iv, data_bytes)
    chacha_encrypted = _chacha20_encrypt(chacha_key, nonce, aes_encrypted)

    # 모든 데이터를 하나로 결합
    combined_data = salt + iv + nonce + chacha_encrypted

    # HMAC 생성
    signature = _create_hmac(hmac_key, combined_data)

    # 최종 결과물 인코딩
    final_data = combined_data + signature
    return base64.b64encode(final_data).decode()

def decrypt(encrypted_text: str, key: str) -> str:
    """암호화된 텍스트를 복호화합니다.
    
    Args:
        encrypted_text (str): 복호화할 암호문 (base64 인코딩)
        key (str): 복호화 키
        
    Returns:
        str: 복호화된 텍스트
        
    Raises:
        ValueError: 복호화 중 오류가 발생한 경우
    """
    try:
        # base64 디코딩
        raw_data = base64.b64decode(encrypted_text.encode())

        # 데이터 분리
        salt = raw_data[:SALT_SIZE]
        iv = raw_data[SALT_SIZE:SALT_SIZE + IV_SIZE]
        nonce = raw_data[SALT_SIZE + IV_SIZE:SALT_SIZE + IV_SIZE + 16]
        signature = raw_data[-64:]  # HMAC-SHA512는 64바이트
        encrypted_content = raw_data[SALT_SIZE + IV_SIZE + 16:-64]

        # 키 유도
        master_key = key.encode()
        main_key = _derive_key(master_key, salt)
        aes_key = hashlib.sha512(main_key + b"aes").digest()[:32]
        chacha_key = hashlib.sha512(main_key + b"chacha").digest()[:32]
        hmac_key = hashlib.sha512(main_key + b"hmac").digest()[:32]

        # HMAC 검증
        if not _verify_hmac(hmac_key, raw_data[:-64], signature):
            raise ValueError("Data has been tampered with or corrupted.")

        # 복호화 (역순으로)
        chacha_decrypted = _chacha20_decrypt(chacha_key, nonce, encrypted_content)
        aes_decrypted = _aes_decrypt(aes_key, iv, chacha_decrypted)

        return aes_decrypted.decode()

    except Exception as e:
        raise ValueError(f"Error during decryption: {str(e)}")