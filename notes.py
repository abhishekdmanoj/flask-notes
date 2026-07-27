from database import cursor, conn

def get_notes(user_id):

	cursor.execute(
        	"SELECT * FROM notes WHERE user_id = %s",
        	(user_id,)
	)

	return cursor.fetchall()

def create_note(note, user_id):

	cursor.execute("INSERT INTO notes(note, user_id) VALUES (%s, %s)",
	(note, user_id))

	conn.commit()

def fetch_note(id, user_id):

	cursor.execute("SELECT * FROM notes WHERE id = %s AND user_id = %s", (id, user_id))
	return cursor.fetchone()

def update_note_db(note, id, user_id):


	cursor.execute("UPDATE notes SET note = %s WHERE id = %s AND user_id = %s", (note, id, user_id))
	conn.commit()

def delete_note_db(id, user_id):


	cursor.execute("DELETE FROM notes WHERE id = %s AND user_id = %s", (id, user_id))
	conn.commit()
