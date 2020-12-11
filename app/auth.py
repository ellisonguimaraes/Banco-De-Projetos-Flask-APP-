import os
from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
from flask_login import login_required, logout_user, login_user, current_user
from werkzeug.utils import secure_filename
from .models.user import User
from app import db

auth = Blueprint('auth', __name__)


@auth.app_template_filter()
def file_exists_profile(user_id):
    return os.path.exists(os.path.join(current_app.config['UPLOAD_FOLDER'], 'profile', str(user_id)))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('auth/register.html')

    name = request.form['name']
    email = request.form['email']
    specialty = request.form['specialty']
    summary = request.form['summary']
    ref = request.form['ref']
    password = request.form['password']
    password_verify = request.form['password_verify']
    perfil_image = request.files['perfil_image']

    if password_verify != password:
        flash('As senhas não correspodem.')
        return redirect(url_for('auth.register'))

    user = User.query.filter_by(email=email).first()

    if user:
        flash('Endereço de email já está em uso.')
        return redirect(url_for('auth.register'))

    new_user = User(name, email, password, specialty, summary, ref, 0)

    db.session.add(new_user)
    db.session.commit()

    if perfil_image.filename:
        perfil_image.filename = str(new_user.id)
        perfil_image.save(os.path.join(current_app.config['UPLOAD_FOLDER'], 'profile', secure_filename(perfil_image.filename)))

    return redirect(url_for('auth.login'))


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('auth/login.html')

    email = request.form['email']
    password = request.form['password']

    user = User.query.filter_by(email=email).first()

    if not user or not user.verify_password(password):
        flash('Algo deu errado. Verifique seus dados novamente!')
        return redirect(url_for('auth.login'))

    login_user(user, remember=True)

    return redirect(url_for('main.index'))


@auth.route('/update', methods=['GET', 'POST'])
@login_required
def update():
    user = User.query.get(current_user.id)
    if request.method == 'GET':
        return render_template('auth/update.html', user=user)

    if request.form['email'] in [u.email for u in User.query.all() if u.email != user.email]:
        flash('EmailHasExists')
        return redirect(url_for('auth.update'))

    user.name = request.form['name']
    user.email = request.form['email']
    user.specialty = request.form['specialty']
    user.summary = request.form['summary']
    user.ref = request.form['ref']

    db.session.commit()

    perfil_image = request.files['perfil_image']
    if perfil_image.filename:
        perfil_image.filename = str(user.id)
        perfil_image.save(os.path.join(current_app.config['UPLOAD_FOLDER'], 'profile', secure_filename(perfil_image.filename)))

    flash('SuccessEdit')

    return redirect(url_for('auth.update'))


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return render_template('auth/login.html')