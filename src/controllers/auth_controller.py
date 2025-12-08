from src.models.user import User
from src.extensions import db
from src.config import Config
import jwt
import datetime


def generate_token(user):
    payload = {
        'user_id': user.id,
        'role': user.role,
        'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=24)
    }
    token = jwt.encode(payload, Config.SECRET_KEY, algorithm='HS256')
    return token


def signup(data):
    if User.query.filter_by(email=data['email']).first():
        return {'message': 'Email já existe!'}, 400

    user = User(
        username=data['username'],
        email=data['email']
    )
    user.set_password(data['password'])

    db.session.add(user)
    db.session.commit()

    return {'message': 'Usuário criado com sucesso!'}, 201


def login(data):
    user = User.query.filter_by(email=data['email']).first()

    if not user or not user.check_password(data['password']):
        return {'message': 'Credenciais inválidas!'}, 401

    token = generate_token(user)
    return {'token': token}, 200


def promote_user(user_id):
    user = User.query.get(user_id)

    if not user:
        return {'message': 'Usuário não encontrado!'}, 404

    user.role = 'admin'
    db.session.commit()

    return {'message': f'Usuário {user.username} agora é admin!'}, 200
