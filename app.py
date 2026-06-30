from flask import Flask
from config import Config
from extensions import db, migrate
from api_layer import api_bp
from ui_layer import ui_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Register the Blueprints (Separating HTML routes from API JSON routes)
    app.register_blueprint(ui_bp)
    app.register_blueprint(api_bp)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
