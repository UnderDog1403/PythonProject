from core.security import hash_password
from modules.auth.models.auth_models import AuthProvider
from modules.user.models.user_model import User


def create_test_user(db):
    user = User(
        email="test@gmail.com",
        name="Test User",
        is_verified=True,
        is_active=True
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    auth = AuthProvider(
        user_id=user.id,
        provider="local",
        password_hash=hash_password("123456")
    )
    db.add(auth)
    db.commit()

def test_login_success(client, db_session):
    create_test_user(db_session)

    response = client.post(
        "/auth/login",
        json={
            "email": "test@gmail.com",
            "password": "123456"
        }
    )

    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login_wrong_password(client, db_session):
    create_test_user(db_session)

    response = client.post(
        "/auth/login",
        json={
            "email": "test@gmail.com",
            "password": "wrong"
        }
    )

    assert response.status_code == 401
#
def test_login_not_verified(client, db_session):
    user = User(
        email="notverify@gmail.com",
        name="Not Verify User",
        is_verified=False,
        is_active=True
    )
    db_session.add(user)
    db_session.commit()

    auth = AuthProvider(
        user_id=user.id,
        provider="local",
        password_hash=hash_password("123")
    )
    db_session.add(auth)
    db_session.commit()

    response = client.post(
        "/auth/login",
        json={
            "email": "notverify@gmail.com",
            "password": "123"
        }
    )

    assert response.status_code == 403

def test_login_missing_field(client):
    response = client.post(
        "/auth/login",
        json={"email": "test@gmail.com"}
    )

    assert response.status_code == 422


