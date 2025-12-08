from flask import Flask
from extensions import db
from routes.auth_routes import auth_routes
from routes.transaction_routes import transaction_routes
import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'supersecretkey')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///finance.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

app = Flask(__name__)
app.config.from_object(Config)


db.init_app(app)

app.register_blueprint(auth_routes)
app.register_blueprint(transaction_routes)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
