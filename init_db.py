import sqlite3
import datetime

connection = sqlite3.connect('database.db')
cursor = connection.cursor()

# --- newsテーブルの処理 ---
cursor.execute('DROP TABLE IF EXISTS news')
cursor.execute('''
    CREATE TABLE news (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT NOT NULL,
        content TEXT NOT NULL
    )
''')
cursor.execute("INSERT INTO news (date, content) VALUES (?, ?)", ('2025-07-01', '7月7日は七夕イベントを開催します。特別なカクテルをご用意してお待ちしております。'))
# (他のお知らせのINSERT文は省略)

# --- contactsテーブルの処理 ---
cursor.execute('DROP TABLE IF EXISTS contacts')
cursor.execute('''
    CREATE TABLE contacts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        message TEXT NOT NULL,
        received_at TEXT NOT NULL
    )
''')

# --- ↓ここからreservationsテーブルの処理を新しく追加↓ ---
cursor.execute('DROP TABLE IF EXISTS reservations')
cursor.execute('''
    CREATE TABLE reservations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        phone_number TEXT NOT NULL,
        reservation_date TEXT NOT NULL,
        reservation_time TEXT NOT NULL,
        number_of_people INTEGER NOT NULL,
        notes TEXT,
        request_received_at TEXT NOT NULL
    )
''')
# --- ↑ここまで追加↑ ---

connection.commit()
connection.close()
print("データベースの初期化が完了し、reservationsテーブルを追加しました。")