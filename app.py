from flask import Flask, request, redirect, render_template, session, url_for, flash
from helpers import login_required, isEmpty
from werkzeug.security import generate_password_hash, check_password_hash
import os
from database import conn, cursor
from users import username_exists, email_exists, create_user
from notes import get_notes, create_note, fetch_note, update_note_db, delete_note_db

from routes_auth import auth

app = Flask(__name__)

app.secret_key = os.getenv("SECRET_KEY")

app.register_blueprint(auth)


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

	if isEmpty(note):

		flash("The note cannot be blank.")
		return redirect(url_for("notes")) 
	
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
