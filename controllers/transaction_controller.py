
from models.transaction import Transaction
from extensions import db
from datetime import datetime

def create_transaction(user_id, data):
    transaction = Transaction(
        user_id=user_id,
        tipo=data['tipo'],
        categoria=data['categoria'],
        valor=data['valor'],
        descricao=data.get('descricao')
    )
    db.session.add(transaction)
    db.session.commit()
    return transaction

def get_transactions(user_id, filters=None):
    query = Transaction.query.filter_by(user_id=user_id)
    if filters:
        if 'tipo' in filters:
            query = query.filter_by(tipo=filters['tipo'])
        if 'categoria' in filters:
            query = query.filter_by(categoria=filters['categoria'])
        if 'start_date' in filters and 'end_date' in filters:
            start = datetime.strptime(filters['start_date'], '%Y-%m-%d')
            end = datetime.strptime(filters['end_date'], '%Y-%m-%d')
            query = query.filter(Transaction.data.between(start, end))
        if 'min_valor' in filters:
            query = query.filter(Transaction.valor >= float(filters['min_valor']))
        if 'max_valor' in filters:
            query = query.filter(Transaction.valor <= float(filters['max_valor']))
    return query.all()

def update_transaction(user_id, transaction_id, data):
    transaction = Transaction.query.filter_by(id=transaction_id, user_id=user_id).first()
    if not transaction:
        return None
    if 'tipo' in data:
        transaction.tipo = data['tipo']
    if 'categoria' in data:
        transaction.categoria = data['categoria']
    if 'valor' in data:
        transaction.valor = data['valor']
    if 'descricao' in data:
        transaction.descricao = data['descricao']
    db.session.commit()
    return transaction

def delete_transaction(user_id, transaction_id):
    transaction = Transaction.query.filter_by(id=transaction_id, user_id=user_id).first()
    if not transaction:
        return False
    db.session.delete(transaction)
    db.session.commit()
    return True
