from hashlib import sha256


HASH_SALT = 'dp6jICak3usvUJEWd5hQtfGWImCKxOVBbEuy0'


def generate_hash(data: str) -> str:
    return sha256(f'{HASH_SALT}{data}{HASH_SALT}'.encode()).hexdigest()
