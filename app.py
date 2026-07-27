from flask import Flask, request, redirect, render_template, session, url_for, flash
from helpers import login_required
from werkzeug.security import generate_password_hash, check_password_hash

from database import conn, cursor
from users import username_exists, email_exists, create_user
from notes import get_notes, create_note, fetch_note, update_note_db, delete_note_db

app = Flask(__name__)

app.secret_key = os.getenv("SECRET_KEY")

@app.route("/register")
def register():

	return render_template("register.html")

@app.route("/register-user", methods = ["POST"])
def register_user():

	username = request.form["username"]
	email = request.form["email"]
	password = request.form["password"]


	if len(username) < 3:
		flash("Username must be at least 3 characters.")
		return redirect(url_for("register"))

	if not username.strip():
		flash("Username is required.")
		return redirect(url_for("register"))

	if len(password) < 8:
		flash("Password must be at least 8 characters.")
		return redirect(url_for("register"))

	password_hash = generate_password_hash(password)

	#CHECK WHETHER USERNAME AND EMAIL EXIST

	if username_exists(username):
		flash("Username already exists.")
		return redirect(url_for("register"))


	if email_exists(email):
		flash("An account with this email already exists.")
		return redirect(url_for("register"))	

	#INSERT USER

	try:

		create_user(username, email, password_hash)
		flash("User created successfully.")
		return redirect(url_for("login_page"))

	except Exception as e:
		print(f"Failed to create user: {e}")
		raise
		return redirect(url_for("register"))



@app.route("/")
def login_page():

	return render_template("login.html")


@app.route("/login", methods = ["POST"])
def login():

	user = request.form["user"]
	password = request.form["password"]
	
	cursor.execute(
	"""SELECT id, username, email, password_hash
	FROM users
	WHERE username = (%s) OR email = (%s)
	""", (user, user)
	)

	account = cursor.fetchone()

	if account is None:
		flash("This account does not exist")
		return redirect(url_for("login_page"))

	user_id = account[0]
	password_hash = account[3]

	if check_password_hash(password_hash, password):

		session["user_id"] = user_id

		flash(f"Welcome, {account[1]}.")

		return redirect("/notes")

	flash("Invalid username/email or password")
	return redirect(url_for("login_page"))


@login_required
@app.route("/notes")

def notes():

	if "user_id" not in session:
		return redirect("/")

	
	rows = get_notes(session["user_id"])
	return render_template("home.html", rows = rows)


@login_required
@app.route("/add-note", methods=["POST"])
def add_note():

	print("ADD NOTE ROUTE HIT")
	
	note = request.form["note"]
	
	try:

		create_note(note, session["user_id"])
		flash("Note created.")
		return redirect(url_for("notes"))

	except Exception as e:
		print(f"Failed to create note: {e}")
		raise
		return redirect(url_for("notes"))

@login_required
@app.route("/edit/<int:id>")
def edit_note(id):

	note = fetch_note(id, session["user_id"])	
	
	if note is None:
		return "Not Found", 404

	return render_template("edit.html", row = note)


@login_required
@app.route("/edit/<int:id>", methods = ["POST"])
def update_note(id):
	
	note = request.form["note"]

	try:

		update_note_db(note, id, session["user_id"])
		flash("Note Updated.")
		return redirect(url_for("notes"))

	except Exception as e:
		
		conn.rollback()
		print(f"Unable to update note: {e}")
		flash("Unable to update note.")
		return redirect(url_for("edit_note", id = id))

@login_required
@app.route("/delete/<int:id>")
def delete_note(id):
	
	try:
		delete_note_db(id, session["user_id"])
		flash("Note Deleted.")
		return redirect(url_for("notes"))

	except Exception as e:
		
		conn.rollback()
		print(f"Failed to delete note: {e}")
		flash("Failed to delete note.")
		return redirect(url_for("notes", id=id))


@app.route("/logout")
def logout():

	flash("Logged out successfully")
	session.pop("user_id", None)
	session.pop("_flashes", None)

	return redirect("/")
 
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
