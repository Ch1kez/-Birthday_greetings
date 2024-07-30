import hashlib
from flask import Flask, render_template, redirect, url_for, request, session
from extensions import db

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Регистрация Blueprint для API
from api.api import api_bp
app.register_blueprint(api_bp, url_prefix='/api')

@app.route('/')
def welcome_page():
    """Начальная страница приложения для поздравления сотрудников"""
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Страница для входа и регистрации в приложении"""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        action = request.form.get('action')  # Получаем действие (вход или регистрация)
        print(username, password)
        hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
        if action == 'register':
            # Регистрация нового пользователя
            if db.check_user(username):
                error = 'Пользователь с таким именем уже существует'
                return render_template('login.html', error=error)

            db.create_user(username, hashed_password)
            return redirect(url_for('login'))

        elif action == 'login':
            # Вход пользователя
            user = db.check_user(username=username)
            print(user)
            print(user[2] == hashed_password)
            print(user[2] , hashed_password)
            if user and user[2] == hashed_password:
                session['user_id'] = user[0]
                return redirect(url_for('personal_panel'))
            else:
                error = 'Неправильное имя пользователя или пароль'
                return render_template('login.html', error=error)

    return render_template('login.html')

@app.route('/personal')
def personal_panel():
    """Личный кабинет сотрудника"""
    if 'user_id' in session:
        return render_template('personal_panel.html')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
