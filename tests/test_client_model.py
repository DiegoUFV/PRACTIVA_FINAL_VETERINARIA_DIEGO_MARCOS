from src.models import Client

def test_client_has_active_pets_empty():
    client = Client(id=1, full_name="Test", email="t@example.com", phone="123")
    assert client.has_active_pets() is False
