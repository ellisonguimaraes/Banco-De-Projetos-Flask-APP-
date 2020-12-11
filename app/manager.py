import datetime as dt
import os
from flask import Blueprint, render_template, request, redirect, url_for, abort, flash, current_app
from flask_login import login_required, current_user
from app import db
from .models.projeto import Projeto
from .models.pessoa_projeto import PessoaProjeto
from .models.tag_projeto import TagProjeto
from .models.historico import Historico
from .models.notificacao import Notificacao
from .models.user import User
from .models.tag import Tag
from werkzeug.utils import secure_filename


manager = Blueprint('manager', __name__)


@manager.app_template_filter()
def is_leader(project_id):
    pp = PessoaProjeto.query.filter_by(project_id=project_id).filter_by(user_id=current_user.id).first()
    if pp:
        return pp.type == 0
    return False


@manager.app_template_filter()
def is_component(project_id):
    pp = PessoaProjeto.query.filter_by(project_id=project_id).filter_by(user_id=current_user.id).first()
    return pp is not None


@manager.app_template_filter()
def file_exists(file):
    return os.path.exists(os.path.join(current_app.config['UPLOAD_FOLDER'], 'project', str(file)))


@manager.app_template_filter()
def file_exists_pdf(file):
    return os.path.exists(os.path.join(current_app.config['UPLOAD_FOLDER'], 'pdf', str(file)))


@manager.route('/manager/project')
@login_required
def project_list():
    list_projects_leader = Projeto.query.join(PessoaProjeto, PessoaProjeto.project_id == Projeto.id) \
        .filter(PessoaProjeto.user_id == current_user.id)\
        .filter(PessoaProjeto.type == 0)\
        .all()

    list_projects_participant = Projeto.query.join(PessoaProjeto, PessoaProjeto.project_id == Projeto.id) \
        .filter(PessoaProjeto.user_id == current_user.id) \
        .filter(PessoaProjeto.type == 1) \
        .all()

    return render_template('manager/project/list.html',
                           list_leader=list_projects_leader,
                           list_participant=list_projects_participant)


@manager.route('/manager/project/add', methods=['GET', 'POST'])
@login_required
def project_add():
    if request.method == 'GET':
        return render_template('manager/project/add.html')

    status = request.form['status']
    title = request.form['title']
    summary = request.form['summary']
    date = dt.datetime.strptime(request.form['date'], '%Y-%m-%dT%H:%M')
    area = request.form['area']
    url = request.form['url']
    contact_email = request.form['contact_email']
    tags = request.form['tags']

    # Addes new project in database
    new_project = Projeto(status, title, summary, date, area, url, contact_email, 1)
    db.session.add(new_project)
    db.session.commit()

    # Add linking User ~ Projects
    new_pessoa_projeto = PessoaProjeto(current_user.id, new_project.id, 0)
    db.session.add(new_pessoa_projeto)
    db.session.commit()

    # Added Tags
    if tags is not None:
        tags = request.form['tags'].upper().split(',')

        for i in tags:
            if i.strip():
                existing_tag = Tag.query.filter_by(category=i.strip()).first()

                if not existing_tag:
                    new_tag = Tag(i.strip())
                    db.session.add(new_tag)
                    db.session.commit()

                    tp = TagProjeto(new_tag.id, new_project.id)
                else:
                    tp = TagProjeto(existing_tag.id, new_project.id)

                db.session.add(tp)
                db.session.commit()

    # Added Images
    images = request.files.getlist('images')
    if images:
        for n, i in enumerate(images):
            if i.filename != '':
                i.filename = str(new_project.id)+'_'+str(n)
                i.save(os.path.join(current_app.config['UPLOAD_FOLDER'], 'project', secure_filename(i.filename)))

    # Added PDF
    pdf = request.files['pdf']
    if pdf.filename:
        pdf.filename = str(new_project.id)+'.pdf'
        pdf.save(os.path.join(current_app.config['UPLOAD_FOLDER'], 'pdf', secure_filename(pdf.filename)))

    flash('AddedProject')

    return redirect(url_for('manager.project_list'))


@manager.route('/manager/project/<project_id>/update', methods=['GET', 'POST'])
@login_required
def project_update(project_id):
    project = Projeto.query.get(project_id)

    if project is None or not is_leader(project_id):
        abort(404)

    if request.method == 'GET':
        return render_template('manager/project/update.html', project=project)

    project.status = request.form['status']
    project.title = request.form['title']
    project.summary = request.form['summary']
    project.date = dt.datetime.strptime(request.form['date'], '%Y-%m-%dT%H:%M')
    project.area = request.form['area']
    project.url = request.form['url']
    project.contact_email = request.form['contact_email']
    tags = request.form['tags']

    # Removed Tags
    TagProjeto.query.filter_by(project_id=project.id).delete()

    # Added Tags
    if tags is not None:
        tags = request.form['tags'].upper().split(',')

        for i in tags:
            if i.strip():
                existing_tag = Tag.query.filter_by(category=i.strip()).first()

                if not existing_tag:
                    new_tag = Tag(i.strip())
                    db.session.add(new_tag)
                    db.session.commit()

                    tp = TagProjeto(new_tag.id, project.id)
                else:
                    tp = TagProjeto(existing_tag.id, project.id)

                db.session.add(tp)

    # Removed Images
    images = request.files.getlist('images')

    list_dir = os.listdir(os.path.join(current_app.config['UPLOAD_FOLDER'], 'project'))
    if images:
        if images[0].filename != '':
            for ld in list_dir:
                if ld.split('_')[0] == str(project.id):
                    os.remove(os.path.join(current_app.config['UPLOAD_FOLDER'], 'project', ld))
    # Added Images
    if images:
        for n, i in enumerate(images):
            if i.filename != '':
                i.filename = str(project.id) + '_' + str(n)
                i.save(os.path.join(current_app.config['UPLOAD_FOLDER'], 'project', secure_filename(i.filename)))

    # Update PDF
    pdf = request.files['pdf']
    if pdf.filename:
        pdf.filename = str(project.id) + '.pdf'
        pdf.save(os.path.join(current_app.config['UPLOAD_FOLDER'], 'pdf', secure_filename(pdf.filename)))

    flash('UpdatedProject')

    db.session.commit()

    return redirect(url_for('manager.project_list'))


@manager.route('/manager/project/<project_id>/delete', methods=['GET', 'POST'])
@login_required
def project_delete(project_id):
    project = Projeto.query.get(project_id)

    if project is None or not is_leader(project_id):
        abort(404)

    if request.method == 'GET':
        return render_template('manager/project/delete.html', project=project)

    TagProjeto.query.filter_by(project_id=project_id).delete()
    Notificacao.query.filter_by(project_id=project_id).delete()
    Historico.query.filter_by(project_id=project_id).delete()
    PessoaProjeto.query.filter_by(project_id=project_id).delete()
    Projeto.query.filter_by(id=project_id).delete()

    # Delete Images
    list_dir = os.listdir(os.path.join(current_app.config['UPLOAD_FOLDER'], 'project'))
    if list_dir:
        for ld in list_dir:
            if ld.split('_')[0] == str(project.id):
                os.remove(os.path.join(current_app.config['UPLOAD_FOLDER'], 'project', ld))

    # Delete PDF
    if file_exists_pdf(str(project.id) + '.pdf'):
        os.remove(os.path.join(current_app.config['UPLOAD_FOLDER'], 'pdf', str(project.id) + '.pdf'))

    db.session.commit()

    flash('DeletedProject')

    return redirect(url_for('manager.project_list'))


@manager.route('/manager/project/<project_id>/historic', methods=['GET', 'POST'])
@login_required
def project_historic(project_id):
    project = Projeto.query.get(project_id)

    if project is None or not is_component(project_id):
        abort(404)

    project_historic_list = Historico.query.join(User, Historico.user_id == User.id) \
        .filter(Historico.project_id == project_id) \
        .order_by(Historico.date.desc())\
        .all()

    if request.method == 'GET':
        return render_template('manager/historic.html', project_historic_list=project_historic_list, project=project)

    description = request.form['description']
    new_historic = Historico(dt.datetime.now(), description, current_user.id, project.id)
    db.session.add(new_historic)
    db.session.commit()

    flash('AddedHistoric')

    return redirect(url_for('manager.project_historic', project_id=project.id))


@manager.route('/manager/project/<project_id>/historic/<historic_id>/delete')
@login_required
def project_historic_delete(project_id, historic_id):
    if not is_leader(project_id):
        abort(404)

    historic = Historico.query.get(historic_id)

    db.session.delete(historic)
    db.session.commit()

    flash('DeletedHistoric')

    return redirect(url_for('manager.project_historic', project_id=project_id))


@manager.route('/manager/project/<project_id>/members', methods=['GET', 'POST'])
@login_required
def project_members(project_id):
    project = Projeto.query.get(project_id)

    if project is None or not is_leader(project_id):
        abort(404)

    if request.method == 'GET':
        list_pessoa_projeto = PessoaProjeto.query.filter_by(project_id=project_id).filter(PessoaProjeto.user_id != current_user.id).all()
        return render_template('manager/members.html', list_pessoa_projeto=list_pessoa_projeto, project=project)

    email = request.form['email']
    type = request.form['role']

    user = User.query.filter_by(email=email).first()

    if user is None:
        flash('UserNotExists')
        return redirect(url_for('manager.project_members', project_id=project_id))

    db.session.add(PessoaProjeto(user.id, project_id, int(type)))
    db.session.commit()

    flash('AddedMember')
    return redirect(url_for('manager.project_members', project_id=project_id))


@manager.route('/manager/project/<project_id>/members/<user_id>/delete')
@login_required
def project_members_delete(project_id, user_id):
    project = Projeto.query.get(project_id)

    if project is None or not is_leader(project_id):
        abort(404)

    pp = PessoaProjeto.query.filter_by(user_id=user_id).filter_by(project_id=project_id).first()

    if pp:
        db.session.delete(pp)
        db.session.commit()

    return redirect(url_for('manager.project_members', project_id=project_id))


@manager.route('/manager/notify', methods=['GET'])
@login_required
def notify():
    # Get my notifications
    my_notifications = Notificacao.query.filter_by(user_id=current_user.id).all()

    # Get notifications of projects
    projects_leader = [pp.projetos for pp in PessoaProjeto.query.filter_by(user_id=current_user.id).filter_by(type=0).all()]
    project_notifications = []
    for p in projects_leader:
        project_notifications.extend(list(p.notificacoes))

    return render_template('manager/notify.html', my_notifications=my_notifications, project_notifications=project_notifications)


@manager.route('/manager/notify/<notify_id>/accept')
@login_required
def notify_accept(notify_id):
    notify = Notificacao.query.get(notify_id)

    if notify is None or not is_leader(notify.project_id) or notify.was_accepted != 0:
        abort(404)

    notify.was_accepted = 1

    # Linking user in project
    db.session.add(PessoaProjeto(notify.user_id, notify.project_id, 1))

    db.session.commit()

    return redirect(url_for('manager.notify'))


@manager.route('/manager/notify/<notify_id>/reject')
@login_required
def notify_reject(notify_id):
    notify = Notificacao.query.get(notify_id)

    if notify is None or not is_leader(notify.project_id) or notify.was_accepted != 0:
        abort(404)

    notify.was_accepted = -1

    db.session.commit()

    return redirect(url_for('manager.notify'))


@manager.route('/manager/notify/<notify_id>/cancel')
@login_required
def notify_cancel(notify_id):
    notify = Notificacao.query.get(notify_id)

    if notify is None or is_leader(notify.project_id) or current_user.id != notify.user_id or notify.was_accepted != 0:
        abort(404)

    db.session.delete(notify)
    db.session.commit()

    return redirect(url_for('manager.notify'))