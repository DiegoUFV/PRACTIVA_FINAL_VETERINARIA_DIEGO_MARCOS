from src.utils import validate_email, validate_phone

def test_validate_email_basic():
    assert validate_email("test@example.com")
    assert not validate_email("invalid-email")

def test_validate_phone_basic():
    assert validate_phone("+34 600 123 456")
    assert not validate_phone("abc")
