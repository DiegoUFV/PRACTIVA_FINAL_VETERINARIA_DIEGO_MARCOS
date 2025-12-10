import re

EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")
PHONE_REGEX = re.compile(r"^[0-9 +()-]{6,20}$")

def validate_email(email: str) -> bool:
    return bool(EMAIL_REGEX.match(email))

def validate_phone(phone: str) -> bool:
    return bool(PHONE_REGEX.match(phone))
