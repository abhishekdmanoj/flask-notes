import pytest

from app import create_app
from config import TestingConfig
from users import create_user, delete_user, get_user_id
from notes import create_note, delete_note_db, get_notes, delete_notes, fetch_note
from werkzeug.security import generate_password_hash, check_password_hash

@pytest.fixture
def app():
	return create_app(TestingConfig)

@pytest.fixture
def client(app):
	return app.test_client()

#def test_notes_page_logged_in(client):

	#ARRANGE
	
	username = "pytest_user"
	email = "pytest_user@gmail.com"
	password = "password123"	

	password_hash = generate_password_hash(password)

	delete_user(username)

	create_user(username, email, password_hash)

	response = client.post("/login",
	data = {
	"user": username,
	"password": password
	},
	follow_redirects = True
	)
	
	assert response.status_code == 200
	assert b"Nothing to see here. Scram!" in response.data 
	assert b"Add Note" in response.data



def test_edit_page_logged_in(client):

	#ARRANGE

	username = "pytest_user"
	email = "pytest_user@gmail.com"
	password = "password123"       	

	password_hash = generate_password_hash(password)

	delete_user(username)

	create_user(username, email, password_hash)

	client.post("/login",
	data = {
	"user": username,
	"password": password
	}
	)

	with client.session_transaction() as sess:
		user_id = sess["user_id"]

	note_id = create_note("Test Note lalalala", user_id)

	#ACT

	response = client.get(f"/edit/{note_id}")

	#ASSERT

	assert response.status_code == 200
	assert b"Update" in response.data

	#CLEANUP

	delete_note_db(note_id, user_id)


def test_add_note_success(client):

	#ARRANGE

	username = "pytest_user"
	email = "pytest_user@gmail.com"
	password = "password123"

	password_hash = generate_password_hash(password)

	delete_user(username)

	create_user(username, email, password_hash)

	user_id = get_user_id(username)

	client.post(
	"/login",
	data = {
	"user": username,
	"password": password
	}

	)

	#ACT

	response = client.post("/add-note",
	data = {
	"note": "My first note!"
	},
	follow_redirects = True
	)


	assert response.status_code == 200
	assert b"Note created." in response.data
	rows = get_notes(user_id)
	assert len(rows) == 1
	assert rows[0][1] == "My first note!"
	assert rows[0][2] == user_id

	delete_notes(user_id)

def test_add_note_blank(client):


	#ARRANGE

	username = "pytest_user"
	email = "pytest_user@gmail.com"
	password = "password123"

	password_hash = generate_password_hash(password)

	delete_user(username)

	create_user(username, email, password_hash)

	user_id = get_user_id(username)

	client.post(
	"/login",
	data = {
	"user": username,
	"password": password
	}

	)

	#ACT

	response = client.post("/add-note",
	data = {
	"note": " "
	},
	follow_redirects = True
	)

	assert response.status_code == 200
	assert b"The note cannot be blank." in response.data
	assert len(get_notes(user_id)) == 0


def test_edit_note_success(client):

	#ARRANGE

	username = "pytest_user"
	email = "pytest_user@gmail.com"
	password = "password123"
	password_hash = generate_password_hash(password)

	delete_user(username)

	create_user(username, email, password_hash)

	client.post("/login",
	data = {
	"user": username,
	"password": password,
	"email": email
	},
	follow_redirects = True 
	)

	user_id = get_user_id(username)

	note_id = create_note("My first Note! Waw mcuh fun!", user_id)

	#ACT

	response = client.post(f"/edit/{note_id}",
	data = {
	"note": "My first Note has been edited! Call me Chipfat!"
	},	
	follow_redirects = True
	)

	#ASSERT

	assert response.status_code == 200
	row = fetch_note(note_id, user_id)
	assert row[1] == "My first Note has been edited! Call me Chipfat!"
	assert b"Note Updated." in response.data	

	delete_notes(user_id)

def test_edit_note_blank(client):


	#ARRANGE

	username = "pytest_user"
	email = "pytest_user@gmail.com"
	password = "password123"
	password_hash = generate_password_hash(password)

	delete_user(username)

	create_user(username, email, password_hash)

	client.post("/login",
	data = {
	"user": username,
	"password": password,
	"email": email
	},
	follow_redirects = True 
	)

	user_id = get_user_id(username)

	note_id = create_note("My first Note! Waw mcuh fun!", user_id)

	#ACT

	response = client.post(f"/edit/{note_id}",
	data = {
	"note": " "
	},
	follow_redirects = True
	)

	#ASSERT

	assert response.status_code == 200
	assert b"The note cannot be blank." in response.data
	rows = get_notes(user_id)
	assert rows[0][1] == "My first Note! Waw mcuh fun!"
	
	delete_notes(user_id)


def test_delete_note_success(client):

	#ARRANGE

	username = "pytest_user"
	email = "pytest_user@gmail.com"
	password = "password123"
	password_hash = generate_password_hash(password)

	delete_user(username)

	create_user(username, email, password_hash)

	client.post("/login",
	data = {
	"user": username,
	"password": password,
	"email": email
	},
	follow_redirects = True 
	)

	user_id = get_user_id(username)

	note_id = create_note("My first Note! Waw mcuh fun!", user_id)

	#ACT

	response = client.post(f"/delete/{note_id}", follow_redirects = True)

	#ASSERT

	assert response.status_code == 200
	assert b"Note Deleted" in response.data
	rows = get_notes(user_id)
	assert len(rows) == 0

		
