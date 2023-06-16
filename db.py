import sqlite3
import csv

class BotDB:

    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()

    def user_exists(self, user_id):
        """Проверяем, есть ли юзер в базе"""
        result = self.cursor.execute("SELECT `id` FROM `users` WHERE `user_id` = ?", (user_id,))
        return bool(len(result.fetchall()))

    def get_user_id(self, user_id):
        """Достаем id юзера в базе по его user_id"""
        result = self.cursor.execute("SELECT `id` FROM `users` WHERE `user_id` = ? INSERT into records (mood_m, mood_w, mood_n, injuries) VALUES (?,?,?,?)", (user_id,), tuple(data.values()))
        return result.fetchone()[0]

    async def add_user(self, state):
        """Добавляем юзера в базу"""
        async with state.proxy() as data:
            self.cursor.execute("INSERT INTO users (user_id, gender, age, education, shift) VALUES (?,?,?,?,?)", tuple(data.values()))
        return self.conn.commit()

    async def add_record(self, state):
        async with state.proxy() as data:
            self.cursor.execute('INSERT into records (test, mood_m, mood_w, mood_n, injuries) VALUES (?,?,?,?,?)', tuple(data.values()) )
            return self.conn.commit()

    def get_records(self, user_id, within = "all"):
        """Получаем историю о доходах/расходах"""

        if within == "day":
            result = self.cursor.execute("SELECT * FROM `records` WHERE `users_id` = ? AND `date` BETWEEN datetime('now', 'start of day') AND datetime('now', 'localtime') ORDER BY `date`",
                (self.get_user_id(user_id),))
        elif within == "week":
            result = self.cursor.execute("SELECT * FROM `records` WHERE `users_id` = ? AND `date` BETWEEN datetime('now', '-6 days') AND datetime('now', 'localtime') ORDER BY `date`",
                (self.get_user_id(user_id),))
        elif within == "month":
            result = self.cursor.execute("SELECT * FROM `records` WHERE `users_id` = ? AND `date` BETWEEN datetime('now', 'start of month') AND datetime('now', 'localtime') ORDER BY `date`",
                (self.get_user_id(user_id),))
        else:
            result = self.cursor.execute("SELECT * FROM `records` WHERE `users_id` = ? ORDER BY `date`",
                (self.get_user_id(user_id),))

        return result.fetchall()

    def records_to_csv(self):
        records = self.cursor.execute("SELECT * FROM `records`")
        with open('records.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Тест', 'Настоение утром', 'Настоение в теч. раб. дня',  'Настоение в конце раб. дня', 'Травмы', 'Дата'])
            writer.writerows(records)
    
    def users_to_csv(self):
        users = self.cursor.execute("SELECT * FROM `users`")
        with open('users.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['id', 'userid', 'Зарегистрирован',  'Пол', 'Возраст', 'Образование', 'Смена'])
            writer.writerows(users)

        

    def close(self):
        """Закрываем соединение с БД"""
        self.connection.close()

BotDB = BotDB('accountant.db')