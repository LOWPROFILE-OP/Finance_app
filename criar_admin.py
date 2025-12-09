from app import create_app
from src.extensions import db
from src.models.user import User


def main():
    app = create_app()
    with app.app_context():
        username = input("Digite o nome do usuário admin: ")
        email = input("Digite o email do admin: ")
        password = input("Digite a senha do admin: ")

        if User.query.filter_by(email=email).first():
            print("Usuário já existe!")
            return

        admin_user = User(username=username, email=email, role='admin')
        admin_user.set_password(password)

        db.session.add(admin_user)
        db.session.commit()
        print(f"Admin {username} criado com sucesso!")

if __name__ == "__main__":
    main()
