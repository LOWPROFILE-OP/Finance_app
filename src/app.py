from flask import Flask
from src.extensions import db
from src.routes.auth_routes import auth_routes
from src.routes.transaction_routes import transaction_routes
from src.config import Config


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    app.register_blueprint(auth_routes)
    app.register_blueprint(transaction_routes)

    with app.app_context():
        db.create_all()

    return app


app = create_app()
