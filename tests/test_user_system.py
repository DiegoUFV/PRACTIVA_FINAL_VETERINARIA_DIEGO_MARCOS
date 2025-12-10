from src.db import Database

def test_create_user():
    db = Database(":memory:")
    db.init_schema()

    db.execute("INSERT INTO users (username, password, role) VALUES ('juan','123','vet')")
    rows = db.query("SELECT * FROM users")

    assert len(rows) == 1

def test_login_query():
    db = Database(":memory:")
    db.init_schema()

    db.execute("INSERT INTO users (username, password, role) VALUES ('ana','pass','admin')")

    result = db.query(
        "SELECT username FROM users WHERE username='ana' AND password='pass'"
    )

    assert result[0][0] == "ana"
