import os

from flask import send_from_directory
from flask import Flask, request, make_response, session, redirect, render_template, url_for
from flask_login import LoginManager, login_user, login_required, logout_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileAllowed
from sqlalchemy.sql.functions import user
from werkzeug.utils import secure_filename, send_from_directory
from wtforms import FileField

from data import db_session
from data.users import User
from forms.flowers import FlowerForm
from forms.loginform import LoginForm
from forms.registerform import RegisterForm

KEY = False
app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


###############################################################
@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route("/cookie_test")
def cookie_test():
    visits_count = int(request.cookies.get("visits_count", 0))
    if visits_count:
        res = make_response(
            f"Вы пришли на эту страницу {visits_count + 1} раз")
        res.set_cookie("visits_count", str(visits_count + 1),
                       max_age=60 * 60 * 24 * 365 * 2)
    else:
        res = make_response(
            "Вы пришли на эту страницу в первый раз за последние 2 года")
        res.set_cookie("visits_count", '1',
                       max_age=60 * 60 * 24 * 365 * 2)
    return res


@app.route("/session_test")
def session_test():
    visits_count = session.get('visits_count', 0)
    session['visits_count'] = visits_count + 1
    return make_response(
        f"Вы пришли на эту страницу {visits_count + 1} раз")


#################################################################################################


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        print(user and user.check_password(form.password.data))
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect('/success')
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)

#######################################################################
####
@app.route("/")
@app.route("/success", methods=['GET', 'POST'])
def success():
    form = FlowerForm()
    pic = url_for('static', filename='im/1.jpg')
    pic2 = url_for('static', filename='im/fl2.jpg')
    pic3 = url_for('static', filename='im/fl3.jpg')
    pic4 = url_for('static', filename='im/fl4.jpg')
    return render_template('success.html', pic=pic, pic2=pic2, pic3=pic3, pic4=pic4, form=form)


####################################################

@app.route("/pay")
def pay():
    return render_template('pay.html')


################################################

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


def main():
    db_session.global_init("db/blogs.db")
    db_sess = db_session.create_session()

    # user = User()
    # user.name = "Пушкин А.С."
    # user.about = "биография Пушкин"
    # user.email = "puskin@email.ru"
    # db_sess.add(user)
    # db_sess.commit()
    #
    # user = User()
    # user.name = "Лермонтов М.Ю."
    # user.about = "биография Лермонтова М.Ю."
    # user.email = "lermontov@email.ru"
    # db_sess.add(user)
    # db_sess.commit()
    #
    # user = User()
    # user.name = "Толстой Л.Н."
    # user.about = "биография Толстой Л.Н."
    # user.email = "tolstoy@email.ru"
    # db_sess.add(user)
    # db_sess.commit()

    # for user in db_sess.query(User).all():
    #     print(user)
    # user = User()
    # user.name = "Фет А."
    # user.about = "биография Фет А."
    # user.email = "fet@email.ru"
    # user.set_password("12345")
    # db_sess.add(user)
    # db_sess.commit()
    # fet = db_sess.query(User).filter(User.id == 4).first()
    # print(fet.check_password('12345'))
    # print(fet.check_password('1235'))
    app.run(debug=True)


if __name__ == '__main__':
    main()
