from flask import Blueprint, request, jsonify
from controllers.auth_controller import signup, login

auth_routes = Blueprint('auth_routes', __name__)

@auth_routes.route('/signup', methods=['POST'])
def signup_route():
    data = request.get_json()
    response, status = signup(data)
    return jsonify(response), status

@auth_routes.route('/login', methods=['POST'])
def login_route():
    data = request.get_json()
    response, status = login(data)
    return jsonify(response), status
