from flask import Flask

from routes_auth import auth
from routes_notes import notes_bp
from config import Config

def create_app(config_class=Config):

	app = Flask(__name__)

	app.config.from_object(config_class)

	app.register_blueprint(auth)

	app.register_blueprint(notes_bp)
 
	return app


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
