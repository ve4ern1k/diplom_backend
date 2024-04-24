import re
from hashlib import sha256


HASH_SALT = 'dp6jICak3usvUJEWd5hQtfGWImCKxOVBbEuy0'


def generate_hash(data: str) -> str:
    return sha256(f'{HASH_SALT}{data}{HASH_SALT}'.encode()).hexdigest()


def to_camel_case(snake_str):
    return "".join(x.capitalize() for x in snake_str.lower().split("_"))


def to_lower_camel_case(snake_str):
    camel_string = to_camel_case(snake_str)
    return snake_str[0].lower() + camel_string[1:]


def to_snake_case(camel_str):
    return re.sub(r'(?<!^)(?=[A-Z])', '_', camel_str).lower()
