import string
import random

from passlib.hash import pbkdf2_sha256


def get_password(password: str) -> str:
    return pbkdf2_sha256.hash(password)


def check_password(decrypted_password: str, encrypted_password: str) -> bool:
    return pbkdf2_sha256.verify(decrypted_password, encrypted_password)


def generate_password(
        length: int = 8,
        alp: str = string.ascii_letters,
):
    return "".join(random.choice(alp) for _ in range(length))
