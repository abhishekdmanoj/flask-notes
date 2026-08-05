from database import cursor, conn

def username_exists(username):

	cursor.execute("SELECT id FROM users WHERE username = %s", (username, ))

	existing = cursor.fetchone()

	return existing is not None



def email_exists(email):

	cursor.execute("select id FROM users WHERE email = %s", (email, ))

	existing = cursor.fetchone()

	return existing is not None


def create_user(username, email, password_hash):

	cursor.execute("INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s)", (username, email, password_hash))

	conn.commit()

def delete_user(username):

	cursor.execute("DELETE FROM users where username = %s", (username, ))

	conn.commit()
