from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate


db = SQLAlchemy()


def create_app():
    app = Flask(__name__, template_folder='templates', static_folder='static')
    login_manager = LoginManager()

    # Configure SECRET_KEY and CONNECTION STRINGS
    app.config['SECRET_KEY'] = 'secret'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Configure route login
    login_manager.login_view = 'auth.login'

    # Configure get_user
    @login_manager.user_loader
    def get_user(user_id):
        from .models.user import User
        return User.query.filter_by(id=user_id).first()

    # Start DB and LoginManager
    db.init_app(app)
    login_manager.init_app(app)

    # Migrate
    from .models.user import User
    from .models.projeto import Projeto
    from .models.pessoa_projeto import PessoaProjeto
    from .models.tag import Tag
    from .models.tag_projeto import TagProjeto
    from .models.historico import Historico
    from .models.notificacao import Notificacao
    Migrate(app, db)

    # Register Blueprints
    from .main import main
    from .auth import auth
    from .manager import manager
    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(manager)

    return app
