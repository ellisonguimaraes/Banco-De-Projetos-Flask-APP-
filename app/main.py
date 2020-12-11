import datetime as dt
from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from app import db
from .manager import is_component
from .models.projeto import Projeto
from .models.notificacao import Notificacao
from .models.form_contact import FormContact
from .models.tag_projeto import TagProjeto
from .models.user import User
from .models.tag import Tag


main = Blueprint('main', __name__)


@main.app_template_filter()
def was_notify(project_id):
    notifies = list(filter(lambda x: x.project_id == project_id, current_user.notificacoes))
    if notifies:
        return True
    return False


@main.route('/')
def index():
    recent_projects = Projeto.query.order_by(Projeto.date.desc()).limit(3).all()

    projects = Projeto.query.all()

    len_projects = len(projects)
    len_projects_completed = len([p for p in projects if p.status == 1])
    len_projects_incompleted = len([p for p in projects if p.status == 0])

    return render_template('index.html', recent_projects=recent_projects, len_projects=len_projects, len_projects_completed=len_projects_completed, len_projects_incompleted=len_projects_incompleted)


@main.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'GET':
        return render_template('contact.html')

    name = request.form['name']
    email = request.form['email']
    message = request.form['message']
    date = dt.datetime.now()

    db.session.add(FormContact(name, email, message, date))
    db.session.commit()

    flash("Enviado com sucesso! Aguarde a resposta no seu email.")

    return redirect(url_for('main.contact'))


@main.route('/project/<project_id>')
def project_page(project_id):
    project = Projeto.query.filter_by(id=project_id).first()

    if project is None:
        abort(404)

    return render_template('project_page.html', project=project)


@main.route('/project/<project_id>/historic')
def project_historic(project_id):
    project = Projeto.query.get(project_id)

    if project is None:
        abort(404)

    return render_template('historic.html', project=project)


@main.route('/project/<project_id>/join')
@login_required
def project_join(project_id):
    project = Projeto.query.get(project_id)
    has_notifies = any(x.project_id == int(project_id) for x in current_user.notificacoes)

    if project is None or is_component(project.id) or has_notifies:
        abort(404)

    db.session.add(Notificacao(dt.datetime.now(), 0, 0, current_user.id, project_id))
    db.session.commit()

    flash('SuccessRequestJoin')

    return redirect(url_for('main.project_page', project_id=project_id))


@main.route('/project/<project_id>/cancelnotify')
@login_required
def notify_cancel(project_id):
    notify = Notificacao.query.filter_by(user_id=current_user.id).filter_by(project_id=project_id).first()

    if notify is None or is_component(project_id):
        abort(404)

    db.session.delete(notify)
    db.session.commit()

    flash('DeleteRequest')

    return redirect(url_for('main.project_page', project_id=project_id))


@main.route('/profile/<user_id>')
def profile(user_id):
    user = User.query.get(user_id)

    if not user:
        abort(404)

    return render_template('profile.html', user=user)


@main.route('/projects', methods=['GET', 'POST'])
@main.route('/projects/<tag_id>', methods=['GET', 'POST'])
def projects(tag_id=None):
    all_projects = Projeto.query.all()
    filter_projects = set()
    all_tags = sorted(Tag.query.all(), key=lambda t: len(list(t.tag_projeto)), reverse=True)[:20]

    # Filtering by Search Input
    search = request.form.get('search')
    print(f'Search: {search}')
    if search is not None and search:
        print('Entrou em SEARCH!**********')
        if len(search.strip()):
            # Added projects with search in title
            filter_projects.update([p for p in all_projects if search.upper() in p.title.upper()])
            # Added projects with search in tags
            filter_projects.update([p for p in all_projects if search.upper() in (tp.tags.category.upper() for tp in p.tag_projeto)])
    else:
        filter_projects.update(all_projects)

    # Filtering by Status
    status = request.form.get('status')
    print(f'Status: {status} ~ {type(status)}')
    if status is not None and status != 'None':
        print('Entrou em STATUS!*******')
        filter_projects = set(p for p in filter_projects if p.status == int(status))

    # Filtering by Tags
    select_tags = request.form.getlist('tags')
    if tag_id is not None:
        select_tags.append(str(tag_id))
    print(f'Select Tags: {select_tags}')
    if select_tags:
        print('Entrou em TAGS!**********')
        new_filter_projects = set()
        for tag_id in select_tags:
            new_filter_projects.update(p for p in filter_projects if int(tag_id) in [tp.tag_id for tp in p.tag_projeto])

        print(len(new_filter_projects))
        filter_projects = new_filter_projects

    # Filtering by Order
    order = request.form.get('order')
    print(f'Order: {order}')
    if order and order != 'None':
        print('Entrou em ORDER!********')
        order = int(order)
        if order == 1:
            filter_projects = sorted(filter_projects, key=lambda p: p.date, reverse=True)
        elif order == 2:
            filter_projects = sorted(filter_projects, key=lambda p: p.date, reverse=False)
        elif order == 3:
            filter_projects = sorted(filter_projects, key=lambda p: p.title, reverse=False)
        elif order == 4:
            filter_projects = sorted(filter_projects, key=lambda p: p.title, reverse=True)

    return render_template('projects.html',
                           projects=list(filter_projects),
                           tags=all_tags,
                           search=search,
                           select_tags=select_tags,
                           status=status,
                           order=order)