# app.py
from flask import Flask
from config import Config
from extensions import db, migrate
from routes.auth_routes import auth_routes
from routes.transaction_routes import transaction_routes

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate.init_app(app, db)

app.register_blueprint(auth_routes)
app.register_blueprint(transaction_routes)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
