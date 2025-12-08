from flask import Blueprint, request, jsonify
from functools import wraps
import jwt

from src.controllers.transaction_controller import create_transaction, get_transactions, update_transaction, delete_transaction
from src.models.user import User
from src.extensions import db
from src.config import Config

transaction_routes = Blueprint('transaction_routes', __name__)


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        header = request.headers.get('Authorization')

        if not header:
            return jsonify({'message': 'Token ausente!'}), 401

        parts = header.split()

        if len(parts) != 2 or parts[0].lower() != 'bearer':
            return jsonify({'message': 'Formato inválido do token!'}), 401

        token = parts[1]

        try:
            data = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])
            current_user = db.session.get(User, data['user_id'])

        except Exception:
            return jsonify({'message': 'Token inválido!'}), 401

        return f(current_user, *args, **kwargs)

    return decorated


@transaction_routes.route('/transactions', methods=['POST'])
@token_required
def create_transaction_route(current_user):
    data = request.get_json()
    transaction = create_transaction(current_user.id, data)
    return jsonify({
        'id': transaction.id,
        'tipo': transaction.tipo,
        'categoria': transaction.categoria,
        'valor': transaction.valor
    }), 201


@transaction_routes.route('/transactions', methods=['GET'])
@token_required
def get_transactions_route(current_user):
    filters = request.args.to_dict()
    transactions = get_transactions(current_user.id, filters)
    output = [{
        'id': t.id,
        'tipo': t.tipo,
        'categoria': t.categoria,
        'valor': t.valor,
        'data': t.data.isoformat(),
        'descricao': t.descricao
    } for t in transactions]
    return jsonify({'transactions': output}), 200


@transaction_routes.route('/transactions/<int:id>', methods=['PUT'])
@token_required
def update_transaction_route(current_user, id):
    data = request.get_json()
    transaction = update_transaction(current_user.id, id, data)
    if not transaction:
        return jsonify({'message': 'Transação não encontrada!'}), 404
    
    return jsonify({
        'id': transaction.id,
        'tipo': transaction.tipo,
        'categoria': transaction.categoria,
        'valor': transaction.valor,
        'descricao': transaction.descricao
    }), 200


@transaction_routes.route('/transactions/<int:id>', methods=['DELETE'])
@token_required
def delete_transaction_route(current_user, id):
    success = delete_transaction(current_user.id, id)
    if not success:
        return jsonify({'message': 'Transação não encontrada!'}), 404
    
    return jsonify({'message': 'Transação deletada com sucesso!'}), 200
