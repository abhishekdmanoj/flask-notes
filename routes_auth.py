from flask import Blueprint, render_template, redirect, url_for, request, session, flash
from database import cursor
from werkzeug.security import generate_password_hash, check_password_hash
from users import username_exists, email_exists, create_user


auth = Blueprint("auth", __name__)

@auth.route("/")
def login_page():

	return render_template("login.html")

@auth.route("/register")
def register():

	return render_template("register.html")

@auth.route("/register-user", methods = ["POST"])
def register_user():

	username = request.form["username"]
	email = request.form["email"]
	password = request.form["password"]


	if not username.strip():
		flash("Username is required.")
		return redirect(url_for("auth.register"))

	if len(username) < 3:
		flash("Username must be at least 3 characters.")
		return redirect(url_for("auth.register"))
	
	if not email.strip():
		flash("Email is required.")
		return redirect(url_for("auth.register"))

	if len(password) < 8:
		flash("Password must be at least 8 characters.")
		return redirect(url_for("auth.register"))

	password_hash = generate_password_hash(password)

	#CHECK WHETHER USERNAME AND EMAIL EXIST

	if username_exists(username):
		flash("Username already exists.")
		return redirect(url_for("auth.register"))


	if email_exists(email):
		flash("An account with this email already exists.")
		return redirect(url_for("auth.register"))	

	#INSERT USER

	try:

		create_user(username, email, password_hash)
		flash("User created successfully.")
		return redirect(url_for("auth.login_page"))

	except Exception as e:
		print(f"Failed to create user: {e}")
		raise
		return redirect(url_for("auth.register"))


@auth.route("/login", methods = ["POST"])
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
		return redirect(url_for("auth.login_page"))

	user_id = account[0]
	password_hash = account[3]

	if check_password_hash(password_hash, password):

		session["user_id"] = user_id

		flash(f"Welcome, {account[1]}.")

		return redirect("/notes")

	flash("Invalid username/email or password")
	return redirect(url_for("auth.login_page"))



@auth.route("/logout")
def logout():

	flash("Logged out successfully")
	session.pop("user_id", None)
	session.pop("_flashes", None)

	return redirect("/")
