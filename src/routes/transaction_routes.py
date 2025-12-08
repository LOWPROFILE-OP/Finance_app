from flask import Blueprint, request, jsonify
from functools import wraps
import jwt

from src.controllers.transaction_controller import (
    create_transaction,
    get_transactions,
    update_transaction,
    delete_transaction
)
from src.models.user import User
from src.models.transaction import Transaction
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
            return jsonify({'message': 'Formato inválido do token! Use: Bearer <token>'}), 401

        token = parts[1]

        try:
            data = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])
            current_user = db.session.get(User, data['user_id'])
            if not current_user:
                return jsonify({'message': 'Usuário não encontrado!'}), 404
        except Exception:
            return jsonify({'message': 'Token inválido!'}), 401

        return f(current_user, *args, **kwargs)

    return decorated


def admin_required(f):
    @wraps(f)
    def decorated(current_user, *args, **kwargs):
        if current_user.role != 'admin':
            return jsonify({'message': 'Apenas administradores podem fazer isso!'}), 403
        return f(current_user, *args, **kwargs)
    return decorated


@transaction_routes.route('/transactions', methods=['POST'])
@token_required
def create_transaction_route(current_user):
    data = request.get_json()
    target_user_id = data.get("user_id", current_user.id)

    if current_user.role != 'admin' and target_user_id != current_user.id:
        return jsonify({'message': 'Você não pode criar transações para outros usuários.'}), 403

    transaction = create_transaction(target_user_id, data)

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

    if current_user.role == 'admin':
        user_id = None
    else:
        user_id = current_user.id

    transactions = get_transactions(user_id, filters)

    output = [{
        'id': t.id,
        'tipo': t.tipo,
        'categoria': t.categoria,
        'valor': t.valor,
        'data': t.data.isoformat(),
        'descricao': t.descricao,
        'user_id': t.user_id
    } for t in transactions]

    return jsonify({'transactions': output}), 200


@transaction_routes.route('/transactions/<int:id>', methods=['PUT'])
@token_required
def update_transaction_route(current_user, id):
    transaction = Transaction.query.get(id)

    if not transaction:
        return jsonify({'message': 'Transação não encontrada!'}), 404

    if current_user.role != 'admin' and transaction.user_id != current_user.id:
        return jsonify({'message': 'Você não tem permissão para atualizar esta transação.'}), 403

    data = request.get_json()
    updated = update_transaction(transaction.user_id, id, data)

    return jsonify({
        'id': updated.id,
        'tipo': updated.tipo,
        'categoria': updated.categoria,
        'valor': updated.valor,
        'descricao': updated.descricao
    }), 200


@transaction_routes.route('/transactions/<int:id>', methods=['DELETE'])
@token_required
def delete_transaction_route(current_user, id):
    transaction = Transaction.query.get(id)

    if not transaction:
        return jsonify({'message': 'Transação não encontrada!'}), 404

    if current_user.role != 'admin' and transaction.user_id != current_user.id:
        return jsonify({'message': 'Você não tem permissão para deletar esta transação.'}), 403

    db.session.delete(transaction)
    db.session.commit()

    return jsonify({'message': 'Transação deletada com sucesso!'}), 200
