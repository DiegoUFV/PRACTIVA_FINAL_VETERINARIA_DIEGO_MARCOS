from src.models import Client, Pet

def test_client_no_pets():
    c = Client(id=1, full_name="Test", email="t@test.com", phone="123")
    assert c.has_active_pets() is False

def test_client_add_pet():
    c = Client(id=1, full_name="Test", email="t@test.com", phone="123")
    p = Pet(id=1, owner_id=1, name="Bobby", species="dog", breed="mix", sex="M")
    c.add_pet(p)
    assert c.has_active_pets() is True

def test_client_remove_pet():
    c = Client(id=1, full_name="Test", email="t@test.com", phone="123")

    p1 = Pet(id=1, owner_id=1, name="Bobby", species="dog", breed="mix", sex="M")
    p2 = Pet(id=2, owner_id=1, name="Luna", species="cat", breed="mix", sex="F")

    c.add_pet(p1)
    c.add_pet(p2)

    c.remove_pet(1)

    assert len(c.pets) == 1
    assert c.pets[0].id == 2
