import re


def is_valid_condition(condition: str) -> bool:
    # Regex to match non empty strings that contain only H, D, A, or *, non repeating
    pattern = r"^(?!.*(.).*\1)[HDA\*]+$"
    pattern = re.compile(pattern, re.IGNORECASE)
    return bool(re.match(pattern, condition))
