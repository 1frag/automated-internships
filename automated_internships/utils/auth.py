from passlib.hash import pbkdf2_sha256


def get_password(password: str) -> str:
    return pbkdf2_sha256.hash(password)


def check_password(decrypted_password: str, encrypted_password: str) -> bool:
    return pbkdf2_sha256.verify(decrypted_password, encrypted_password)
