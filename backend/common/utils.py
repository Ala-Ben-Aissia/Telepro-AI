from cryptography import fernet

from config.settings import FIELD_ENCRYPTION_KEY


def encrypt(cleartext: str) -> str:
    if not cleartext:
        return ""
    f = fernet.Fernet(FIELD_ENCRYPTION_KEY)
    return f.encrypt(cleartext.encode()).decode()


def decrypt(ciphertext: str) -> str:
    if not ciphertext:
        return ""
    f = fernet.Fernet(FIELD_ENCRYPTION_KEY)
    return f.decrypt(ciphertext.encode()).decode()
