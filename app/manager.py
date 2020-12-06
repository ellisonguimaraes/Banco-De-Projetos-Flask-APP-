from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app import db
from .models.projeto import Projeto
from .models.pessoa_projeto import PessoaProjeto

manager = Blueprint('manager', __name__)


@manager.route('/manager')
@login_required
def manager_projects():
    list_projects = Projeto.query.join(PessoaProjeto, PessoaProjeto.project_id == Projeto.id)\
        .filter(PessoaProjeto.user_id == current_user.id)\
        .all()

    return render_template('manager/index.html', list_projects=list_projects)
