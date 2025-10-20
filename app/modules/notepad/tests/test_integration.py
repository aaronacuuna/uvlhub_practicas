import pytest

from app import db
from app.modules.notepad.models import Notepad
from app.modules.auth.models import User
from app.modules.conftest import login, logout

from core.locust.common import get_csrf_token

@pytest.fixture
def setup_notepad(test_client):
    """
    Fixture que crea un usuario y una nota en la base de datos
    para probar la integración completa (DB + login + vistas).
    """
    with test_client.application.app_context():
        user = User(email="user@example.com", password="test1234")
        db.session.add(user)
        db.session.commit()

        note = Notepad(title="Práctica 4 de EGC", body="Hacer test a Uvlhub", user_id=user.id)
        db.session.add(note)
        db.session.commit()

    yield test_client

    with test_client.application.app_context():
        db.session.query(Notepad).delete()
        db.session.query(User).delete()
        db.session.commit()


def test_get_notepads_endpoint_returns_existing_notepads(setup_notepad):
    """ 
        GET /notepad debe devolver un elemento HTML donde se encuentre la información acerca del título y cuerpo de cada Notepad. 
    """
    test_client = setup_notepad

    login_response = login(test_client, "user@example.com", "test1234")
    assert login_response.status_code == 200, "Login failed during integration test"

    response = test_client.get("/notepad")
    assert response.status_code == 200, "The notepad page could not be accessed."
    html = response.data.decode("utf-8")

    assert "Práctica 4 de EGC" in html, "The expected title is not present on the page"
    assert "Hacer test a Uvlhub" in html, "The expected body is not present on the page"

    logout(test_client)


def test_get_notepad_creation_form(setup_notepad):
    """
        GET /notepad/create
    """
    test_client = setup_notepad

    login_response = login(test_client, "user@example.com", "test1234")
    assert login_response.status_code == 200, "Login failed during integration test"

    response = test_client.get("/notepad/create")
    assert response.status_code == 200, "The notepad page could not be accessed."
    html = response.data.decode("utf-8")

    assert "Title" in html, "The title field is not present on the page"
    assert "Body" in html, "The body field is not present on the page"
    assert "Save notepad" in html, "The save notepad button is not present on the page"

    logout(test_client)
  
