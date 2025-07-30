import re

def is_valid_url(url: str) -> bool:
    pattern = r'^(https?://)?comic-walker\.com/detail/KC_\d+_S(/episodes/KC_\d+_E)?(?:\?.*)?$'

    return bool(re.match(pattern, url))
