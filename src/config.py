import os


basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, "data")
os.makedirs(db_path, exist_ok=True)
SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(db_path, "tasks.db")


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'supersecretkey')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///finance.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
