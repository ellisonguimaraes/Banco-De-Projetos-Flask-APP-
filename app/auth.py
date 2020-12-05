from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, logout_user, login_user
from .models.user import User
from app import db

auth = Blueprint('auth', __name__)


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')

    name = request.form['name']
    email = request.form['email']
    specialty = request.form['specialty']
    summary = request.form['summary']
    ref = request.form['ref']
    password = request.form['password']
    password_verify = request.form['password_verify']

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

    return redirect(url_for('auth.login'))


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    email = request.form['email']
    password = request.form['password']

    user = User.query.filter_by(email=email).first()

    if not user or not user.verify_password(password):
        flash('Algo deu errado. Verifique seus dados novamente!')
        return redirect(url_for('auth.login'))

    login_user(user, remember=True)

    return 'logou '+user.name


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return render_template('login.html')