import pytest

from app import create_app
from config import TestingConfig
from users import create_user, delete_user, username_exists
from notes import create_note, delete_note_db
from werkzeug.security import generate_password_hash, check_password_hash

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

def test_login_wrong_password(client):

	#ARRANGE
	
	username = "pytest_user"
	email = "pytest_user@gmail.com"
	password = "password123"	

	password_hash = generate_password_hash(password)

	delete_user(username)

	create_user(username, email, password_hash)

	#ACT
	response = client.post(
	"/login",
	data = {
	"user": username,
	"password": "wrongpassword"	
	}
	)

	#ASSERT
	assert response.status_code == 302
	assert response.headers["Location"] == "/"
	

def test_login_user(client):

	#ARRANGE

	username = "pytest_user"
	email = "pytest_user@gmail.com"
	password = "password123"
	password_hash = generate_password_hash(password)

	delete_user(username)

	create_user(username, email, password_hash)

	#ACT
	response = client.post(
	"/login",
	data = {
	"user": username,
	"password": password
	},
	follow_redirects = True
	)

	#ASSERT
	assert response.status_code == 200
	assert b"Welcome, pytest_user" in response.data
	assert b"Add Note" in response.data

def test_register_success(client):

	#ARRANGE

	username = "pytest_user"
	email = "pytest_user@gmail.com"
	password = "password123"

	delete_user(username)	

	#ACT

	response = client.post("/register-user",
	data = {
	"username": username,
	"email": email,
	"password": password
	},
	follow_redirects = True
	)

	#ACT

	assert response.status_code == 200
	assert b"User created successfully" in response.data
	assert username_exists(username)

def test_register_username_exists(client):
	
	#ARRANGE

	username = "pytest_user"
	email = "pytest_user@gmail.com"
	password = "password123"
	password_hash = generate_password_hash(password)

	delete_user(username)

	create_user(username, email, password_hash)


	#ACT

	response = client.post("/register-user",
	data = {
	"username": username,
	"email": "fasfsafsdfdsfsdfdsfwadadawsdsanoemail@gmail.com",
	"password": password
	},
	follow_redirects = True
	)

	#ASSERT

	assert response.status_code == 200
	assert b"Username already exists" in response.data
	assert b"Username" in response.data
	assert b"Password" in response.data
	assert b"Create User" in response.data

def test_register_email_exists(client):


	#ARRANGE

	username = "pytest_user"
	email = "pytest_user@gmail.com"
	password = "password123"
	password_hash = generate_password_hash(password)

	delete_user(username)

	create_user(username, email, password_hash)


	#ACT

	response = client.post("/register-user",
	data = {
	"username": "hahahhaahthisusernamewillneverexists7878787878767676",
	"email": email,
	"password": password
	},
	follow_redirects = True
	)

	#ASSERT

	assert response.status_code == 200
	assert b"email already exists" in response.data
	assert b"Username" in response.data
	assert b"Password" in response.data
	assert b"Create User" in response.data

def test_register_username_username_too_short(client):


	#ARRANGE

	username = "ab"
	email = "pytest_user@gmail.com"
	password = "password123"

	#ACT

	response = client.post("/register-user",
	data = {
	"username": username,
	"email": email,
	"password": password
	},
	follow_redirects = True
	)

	#ASSERT

	assert response.status_code == 200
	assert b"Username must be at least" in response.data
	assert b"Username" in response.data
	assert b"Password" in response.data
	assert b"Create User" in response.data

def test_register_password_too_short(client):


	#ARRANGE

	username = "pytest_user"
	email = "pytest_user@gmail.com"
	password = "koskfdo"
	password_hash = generate_password_hash(password)

	delete_user(username)

	create_user(username, email, password_hash)


	#ACT

	response = client.post("/register-user",
	data = {
	"username": username,
	"email": email,
	"password": password
	},
	follow_redirects = True
	)

	#ASSERT

	assert response.status_code == 200
	assert b"Password must be at least" in response.data
	assert b"Username" in response.data
	assert b"Password" in response.data
	assert b"Create User" in response.data

def test_register_username_blank(client):

	#ARRANGE

	delete_user("pytest_user")

	username = " "
	email = "pytest_user@gmail.com"
	password = "password123"
	password_hash = generate_password_hash(password)

	#ACT

	response = client.post("/register-user",
	data = {
	"username": username,
	"email": email,
	"password": password
	},
	follow_redirects = True
	)

	#ASSERT

	assert response.status_code == 200
	assert b"Username is required" in response.data
	assert b"Username" in response.data
	assert b"Password" in response.data
	assert b"Create User" in response.data


def test_register_email_blank(client):

	#ARRANGE

	delete_user("pytest_user")

	username = "pytest_user"
	email = " "
	password = "password123"
	password_hash = generate_password_hash(password)

	#ACT

	response = client.post("/register-user",
	data = {
	"username": username,
	"email": email,
	"password": password
	},
	follow_redirects = True
	)

	#ASSERT

	assert response.status_code == 200
	assert b"Email is required" in response.data
	assert b"Username" in response.data
	assert b"Password" in response.data
	assert b"Create User" in response.data
