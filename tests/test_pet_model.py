from src.models import Pet

def test_pet_attributes():
    p = Pet(id=1, owner_id=5, name="Luna", species="cat", breed="persian", sex="F")
    assert p.name == "Luna"
    assert p.owner_id == 5
    assert p.species == "cat"
