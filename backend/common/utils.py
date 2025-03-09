from config.settings import FIELD_ENCRYPTION_KEY
from cryptography import fernet


def encrypt(cleartext: str) -> str:
    f = fernet.Fernet(FIELD_ENCRYPTION_KEY)
    return f.encrypt(cleartext.encode()).decode()


def decrypt(ciphertext: str) -> str:
    f = fernet.Fernet(FIELD_ENCRYPTION_KEY)
    return f.decrypt(ciphertext.encode()).decode()
