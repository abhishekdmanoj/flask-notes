from flask import Blueprint, render_template, redirect, url_for, request, session, flash
from database import cursor
from helpers import login_required, isEmpty
from notes import get_notes, create_note, fetch_note, update_note_db, delete_note_db


notes_bp = Blueprint("notes_bp", __name__)


@notes_bp.route("/notes")
@login_required
def notes():

	if "user_id" not in session:
		return redirect("/")

	
	rows = get_notes(session["user_id"])
	return render_template("home.html", rows = rows)


@notes_bp.route("/add-note", methods=["POST"])
@login_required
def add_note():

	print("ADD NOTE ROUTE HIT")
	
	note = request.form["note"]

	if isEmpty(note):

		flash("The note cannot be blank.")
		return redirect(url_for("notes_bp.notes")) 
	
	try:

		create_note(note, session["user_id"])
		flash("Note created.")
		return redirect(url_for("notes_bp.notes"))

	except Exception as e:
		print(f"Failed to create note: {e}")
		raise
		return redirect(url_for("notes_bp.notes"))

@notes_bp.route("/edit/<int:id>")
@login_required
def edit_note(id):

	note = fetch_note(id, session["user_id"])	

	if note is None:
		return "Not Found", 404

	return render_template("edit.html", row = note)


@notes_bp.route("/edit/<int:id>", methods = ["POST"])
@login_required
def update_note(id):
	
	note = request.form["note"]


	if isEmpty(note):

		flash("The note cannot be blank.")
		return redirect(url_for(f"notes_bp.edit_note", id = id)) 

	try:

		update_note_db(note, id, session["user_id"])
		flash("Note Updated.")
		return redirect(url_for("notes_bp.notes"))

	except Exception as e:
		
		conn.rollback()
		print(f"Unable to update note: {e}")
		flash("Unable to update note.")
		return redirect(url_for("notes_bp.edit_note", id = id))

@notes_bp.route("/delete/<int:id>", methods = ["POST"])
@login_required
def delete_note(id):
	
	try:
		delete_note_db(id, session["user_id"])
		flash("Note Deleted.")
		return redirect(url_for("notes_bp.notes"))

	except Exception as e:
		
		conn.rollback()
		print(f"Failed to delete note: {e}")
		flash("Failed to delete note.")
		return redirect(url_for("notes_bp.notes", id=id))

