from flask import Flask, request, redirect, render_template, session, url_for, flash
from helpers import login_required, isEmpty
from werkzeug.security import generate_password_hash, check_password_hash
import os
from database import conn, cursor
from users import username_exists, email_exists, create_user
from notes import get_notes, create_note, fetch_note, update_note_db, delete_note_db

from routes_auth import auth
from routes_notes import notes_bp
from config import Config

def create_app(config_class=Config):

	app = Flask(__name__)

	app.config.from_object(Config)

	app.register_blueprint(auth)

	app.register_blueprint(notes_bp)
 
	return app


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
