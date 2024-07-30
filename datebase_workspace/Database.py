import hashlib
import sqlite3


class DatabaseConnection:
    def __init__(self, db_name: str) -> None:
        self._db_name = f"./{db_name}.db"

    def __enter__(self):
        self.conn = sqlite3.connect(self._db_name)
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is not None:
            self.conn.rollback()
        else:
            self.conn.commit()
        self.conn.close()


class Database:
    def __init__(self, db_name: str):
        self.__database_connection = DatabaseConnection(db_name)
        self.__create_db_structure()

    def __create_db_structure(self):
        with self.__database_connection as cursor:
            cursor.execute("""CREATE TABLE IF NOT EXISTS blocks (
                     id INTEGER PRIMARY KEY AUTOINCREMENT,
                     idblock TEXT,
                     short_title TEXT,
                     img TEXT,
                     altimg TEXT,
                     title TEXT,
                     contenttext TEXT,
                     author TEXT,
                     timestampdata DATETIME)""")

            cursor.execute("""CREATE TABLE IF NOT EXISTS users (
                                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                                 username TEXT,
                                 password TEXT,
                                 birthday DATE)""")

            cursor.execute("""CREATE TABLE IF NOT EXISTS subscriptions (
                                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                                 user_id INTEGER,
                                 subscribed_to INTEGER,
                                 FOREIGN KEY(user_id) REFERENCES users(id),
                                 FOREIGN KEY(subscribed_to) REFERENCES users(id))""")

            cursor.execute("""CREATE TABLE IF NOT EXISTS api_tokens (
                                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                                 user_id INTEGER,
                                 token TEXT,
                                 FOREIGN KEY(user_id) REFERENCES users(id))""")
    def create_user(self, username, password):
        # Хеширование пароля
        hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()

        # Подключение к нашей базе данных
        with self.__database_connection as cursor:
            # Добавление нового сотрудника
            cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_password))

    def check_user(self, username: str):
        # создаем запрос для поиска пользователя по username,
        # если такой пользователь существует, то получаем все данные id, password
        with self.__database_connection as cursor:
            return cursor.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()

    def subscribe_to_user(self, user_id, subscribed_to_id):
        with self.__database_connection as cursor:
            cursor.execute('INSERT INTO subscriptions (user_id, subscribed_to) VALUES (?, ?)',
                           (user_id, subscribed_to_id))

    def unsubscribe_from_user(self, user_id, subscribed_to_id):
        with self.__database_connection as cursor:
            cursor.execute('DELETE FROM subscriptions WHERE user_id = ? AND subscribed_to = ?',
                           (user_id, subscribed_to_id))

    def set_api_token(self, user_id):
        with db.__database_connection as cursor:
            cursor.execute('INSERT INTO api_tokens (user_id, token) VALUES (?, ?)', (user_id, token))


if __name__ == '__main__':
    db = Database('test_database')
    db.create_db_structure()
    db.create_user('12312321321312', '32123123123')
