import hashlib

from flask import Flask, render_template, redirect, url_for, request, session

from datebase_workspace import Database

app = Flask(__name__)
db = Database('test_database')


@app.route('/')
def welcome_page():
    """
    Начальная страница приложения для поздравления сотрудников
    :return:
    """
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Страница для входа в приложение
    :return:
    """
    # error = None  # обнуляем переменную ошибок
    if request.method == 'POST':
        username = request.form['username']  # обрабатываем запрос с нашей формы который имеет атрибут name="username"
        password = request.form['password']  # обрабатываем запрос с нашей формы который имеет атрибут name="password"

        hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()  # шифруем пароль в sha-256
        user = db.check_user(username=username)
        print(user)

        # теперь проверяем если данные сходятся формы с данными БД
        if user and user['password'] == hashed_password:
            # в случае успеха создаем сессию в которую записываем id пользователя
            session['user_id'] = user['id']
            # и делаем переадресацию пользователя на новую страницу
            return redirect(url_for('personal_panel'))

        else:
            error = 'Неправильное имя пользователя или пароль'
            return render_template('login.html', error=error)
    return render_template('login.html')


# @app.route('/login', methods = ['GET', 'POST'])
# @oid.loginhandler
# def login():
#   if g.user is not None and g.user.is_authenticated():
#       return redirect(url_for('index'))
#   form = LoginForm()
#   if form.validate_on_submit():
#       session['remember_me'] = form.remember_me.data
#       return oid.try_login(form.openid.data, ask_for = ['nickname', 'email'])
#   return render_template('login.html',
#       title = 'Sign In',
#       form = form,
#       providers = app.config['OPENID_PROVIDERS'])


@app.route('/personal')
def personal_panel():
    """
    Личный кабинет сотрудника
    :return:
    """
    return render_template('personal_panel.html')


if __name__ == '__main__':
    app.run(debug=True)
