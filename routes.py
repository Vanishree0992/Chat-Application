from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from extensions import db
from models import User, ChatGroup
from forms import LoginForm
from werkzeug.security import generate_password_hash, check_password_hash

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return redirect(url_for('main.login'))

@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('main.chat'))  # or your desired route
        else:
            flash('Invalid username or password')
    return render_template('login.html', form=form)

@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        hashed_pw = generate_password_hash(request.form['password'])
        user = User(username=request.form['username'], password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        flash('Registered successfully!')
        return redirect(url_for('main.login'))
    return render_template('register.html')

@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))

@main.route('/chat')
@login_required
def chat():
    groups = ChatGroup.query.all()
    return render_template('chat.html', groups=groups)

@main.route('/groups')
@login_required
def group_list():
    groups = ChatGroup.query.all()
    return render_template('groups.html', groups=groups)