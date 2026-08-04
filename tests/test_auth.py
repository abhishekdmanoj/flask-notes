import pytest

from app import create_app
from config import TestingConfig

@pytest.fixture
def app():
	return create_app(TestingConfig)

@pytest.fixture
def client(app):
	return app.test_client()

def test_login_page(client):
	response = client.get("/")

	assert response.status_code == 200
	assert b"Username or Email" in response.data
	assert b"Username" in response.data
	assert b"Password" in response.data


def test_register_page(client):
	response = client.get("/register")

	assert response.status_code == 200
	assert b"Username" in response.data
	assert b"Password" in response.data
	assert b"Email" in response.data
	assert b"Create User" in response.data


def test_notes_page_requires_login(client):
	response = client.get("/notes")

	assert response.status_code == 302
	assert response.headers["Location"] == "/"

#def test_notes_page_logged_in(client):
#	response = client.get("/notes")
#	
#	assert response.status_code == 200
#	assert b"Edit" in response.data
#	assert b"Delete" in response.data
#	assert b"Add Note" in response.data


def test_edit_page_requires_login(client):
	response = client.get("/edit/1")

	assert response.status_code == 302
	assert response.headers["Location"] == "/"



def test_login_no_user(client):
	response = client.post("/login",
	data = {
	"user": "hahahahhahahathisaccountwillnevereverexist24424134676767",
	"password": "hahahhathispasswordwillneverexistdie912039203"
	}
	)

	assert response.status_code == 302
	print(response.headers["Location"])
	assert response.headers["Location"] == "/"


def test_login_no_user_flash(client):
	response = client.post("/login",
	data = {
	"user": "hahahahhahahathisaccountwillnevereverexist24424134676767",
	"password": "hahahhathispasswordwillneverexistdie912039203"
	},
	follow_redirects = True
	)

	assert response.status_code == 200
	assert b"This account does not exist" in response.data
