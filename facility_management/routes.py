from flask import render_template, request, redirect, \
    url_for, flash, get_flashed_messages
import psycopg2
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from flask_cors import cross_origin


from facility_management import db, app
from facility_management.settings import *
from facility_management.models import User, Profile

conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)


@cross_origin()
@app.get('/')
def home():
    if current_user.is_authenticated:
        return redirect(url_for("get_objects_list"))
    else:
        return render_template("home.html")


@cross_origin()
@app.post('/')
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    if username and password:
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            flash('Вы авторизованы', category='success')
            return redirect(url_for("get_objects_list"))

        else:
            flash('Неверные логин или пароль', category='danger')

    else:
        flash('Пожалуйста заполните все поля', category='danger')
    return render_template("home.html",
                           message=get_flashed_messages(with_categories=True))


@cross_origin()
@app.get('/register')
@app.get('/users/add')
def register():
    profile = Profile.query.all()
    rule = request.url_rule
    if 'register' in rule.rule:
        return render_template(
            "user/registration.html",
            profile=profile)
    elif 'add' in rule.rule:
        return render_template(
            "user/add_user.html",
            profile=profile)


@cross_origin()
@app.post('/register')
@app.post('/users/add')
def registration():
    rule = request.url_rule
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    patronymic = request.form.get('patronymic')
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    password2 = request.form.get('password2')
    profile_id = request.form.get('profile_id')

    if not (first_name or last_name or username or password or password2):
        flash('Пожалуйста, заполните все поля', category='warning')
        if 'register' in rule.rule:
            return render_template("user/registration.html")
        elif 'add' in rule.rule:
            return render_template("user/add_user.html")

    elif password != password2:
        flash('Пароли не совпадают', category='warning')
        if 'register' in rule.rule:
            return render_template("user/registration.html")
        elif 'add' in rule.rule:
            return render_template("user/add_user.html")

    elif User.query.filter(User.username == username).all():
        flash('Username уже существует', category='warning')
        if 'register' in rule.rule:
            return render_template("user/registration.html")
        elif 'add' in rule.rule:
            return render_template("user/add_user.html")

    else:
        hash_pwd = generate_password_hash(password)
        new_user = User(first_name=first_name,
                        last_name=last_name,
                        patronymic=patronymic,
                        username=username,
                        email=email,
                        password=hash_pwd,
                        profile_id=profile_id)
        db.session.add(new_user)
        db.session.commit()
    if 'register' in rule.rule:
        flash('Пользователь успешно зарегистрирован', category='success')
        return redirect('/')
    elif 'add' in rule.rule:
        flash('Пользователь успешно добавлен', category='success')
        return redirect('/')


@cross_origin()
@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@cross_origin()
@app.get('/users')
def get_all_users():
    if current_user.is_authenticated:
        return render_template("user/users_list.html",
                               users=User.query.all()
                               )
    else:
        return redirect(url_for('home'))


@cross_origin()
@app.get('/<int:id>/delete')
def delete_user_get(id):
    if current_user.is_authenticated:
        return render_template("user/profile_delete.html")
    else:
        return redirect(url_for('home'))


@cross_origin()
@app.post('/<int:id>/delete')
def delete_user_post(id):
    if current_user.is_authenticated:
        user = User.query.filter_by(id=id).first()
        db.session.delete(user)
        db.session.commit()
        return redirect(url_for('get_all_users'))
    else:
        return redirect(url_for('home'))


@cross_origin()
@app.get('/<int:id>/update')
def update_user_get(id):
    if current_user.is_authenticated:
        profile = Profile.query.all()
        user_to_upd = User.query.filter_by(id=id).first()
        return render_template("user/update.html",
                               user_to_upd=user_to_upd,
                               profile=profile)
    else:
        return redirect(url_for('home'))


@cross_origin()
@app.post('/<int:id>/update')
def update_user_post(id):
    if current_user.is_authenticated:
        user_to_upd = User.query.filter_by(id=id).first()
        user_to_upd.first_name = request.form['first_name']
        user_to_upd.last_name = request.form['last_name']
        user_to_upd.patronymic = request.form['patronymic']
        user_to_upd.username = request.form['username']
        user_to_upd.email = request.form['email']
        password = request.form['password']
        user_to_upd.password = generate_password_hash(password)
        user_to_upd.profile_id = request.form['profile_id']
        try:
            db.session.commit()
            flash("Пользователь успешно обновлен", category='success')
            return render_template("user/users_list.html", users=User.query.all())
        except:
            flash("Что-то пошло не так", category='warning')
            return redirect(url_for('get_all_users'))
