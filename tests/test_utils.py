from src.utils import validate_email, validate_phone

def test_validate_email():
    assert validate_email("test@example.com")
    assert validate_email("user.name+tag@domain.es")
    assert not validate_email("invalid-email")
    assert not validate_email("@domain.com")
    assert not validate_email("test@")
    assert not validate_email("")
    assert not validate_email(" ")

def test_validate_phone():
    assert validate_phone("600123456")
    assert validate_phone("+34 600 123 456")
    assert validate_phone("+34600123456")
    assert not validate_phone("abc")
    assert not validate_phone("12345")
    assert not validate_phone("+34-abc-123")
    assert not validate_phone("")
