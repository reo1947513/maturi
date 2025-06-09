import sqlite3
import os
import datetime
from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.utils import secure_filename

# Flaskアプリを作成するためのおまじない
app = Flask(__name__)
# セッション機能を使うための「秘密の鍵」
app.secret_key = 'maturi' 
# アップロードするファイルの保存場所を指定
UPLOAD_FOLDER = os.path.join('static', 'images', 'gallery')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# --- データベース接続の補助関数 (変更なし) ---
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# --- フロントページ関連のルート ---
@app.route('/')
def index():
    conn = get_db_connection()
    news_list = conn.execute('SELECT * FROM news ORDER BY date DESC').fetchall()
    conn.close()
    gallery_path = os.path.join(app.static_folder, 'images/gallery')
    photo_list = [f for f in os.listdir(gallery_path) if not f.startswith('.')]
    return render_template('index.html', news_list=news_list, photo_list=photo_list)

# ↓ お問い合わせ処理の最後を、完了ページへのリダイレクトに変更 ↓
@app.route('/contact', methods=['POST'])
def contact():
    name = request.form['name']
    email = request.form['email']
    message = request.form['message']
    received_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    conn = get_db_connection()
    conn.execute('INSERT INTO contacts (name, email, message, received_at) VALUES (?, ?, ?, ?)',
                 (name, email, message, received_at))
    conn.commit()
    conn.close()
    return redirect(url_for('contact_success')) # ← 変更

# ↓ 予約リクエスト処理の最後を、完了ページへのリダイレクトに変更 ↓
@app.route('/reserve', methods=['POST'])
def reserve():
    name = request.form['name']
    phone_number = request.form['phone_number']
    reservation_date = request.form['reservation_date']
    reservation_time = request.form['reservation_time']
    number_of_people = request.form['number_of_people']
    notes = request.form['notes']
    request_received_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    conn = get_db_connection()
    conn.execute('INSERT INTO reservations (name, phone_number, reservation_date, reservation_time, number_of_people, notes, request_received_at) VALUES (?, ?, ?, ?, ?, ?, ?)',
                 (name, phone_number, reservation_date, reservation_time, number_of_people, notes, request_received_at))
    conn.commit()
    conn.close()
    return redirect(url_for('reserve_success')) # ← 変更

# --- ↓ここから完了ページ表示用のルートを2つ新しく追加↓ ---
@app.route('/contact/success')
def contact_success():
    return render_template('contact_success.html')

@app.route('/reserve/success')
def reserve_success():
    return render_template('reserve_success.html')
# --- ↑ここまで追加↑ ---


# --- 管理者ページ関連のルート (変更なし) ---
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['password'] == 'maturi':
            session['logged_in'] = True
            return redirect(url_for('admin_dashboard'))
        else:
            error = 'パスワードが間違っています'
    return render_template('login.html', error=error)
# (他の管理ページ関連のルートは変更なしのため省略)
@app.route('/admin')
def admin_dashboard():
    if not session.get('logged_in'): return redirect(url_for('login'))
    return render_template('dashboard.html')
@app.route('/admin/news')
def admin_news():
    if not session.get('logged_in'): return redirect(url_for('login'))
    conn = get_db_connection(); news_list = conn.execute('SELECT * FROM news ORDER BY date DESC').fetchall(); conn.close()
    return render_template('admin_news.html', news_list=news_list)
@app.route('/admin/news/add', methods=['POST'])
def admin_add_news():
    if not session.get('logged_in'): return redirect(url_for('login'))
    date, content = request.form['date'], request.form['content']
    conn = get_db_connection(); conn.execute('INSERT INTO news (date, content) VALUES (?, ?)', (date, content)); conn.commit(); conn.close()
    return redirect(url_for('admin_news'))
@app.route('/admin/news/edit/<int:news_id>')
def admin_edit_news(news_id):
    if not session.get('logged_in'): return redirect(url_for('login'))
    conn = get_db_connection(); news_item = conn.execute('SELECT * FROM news WHERE id = ?', (news_id,)).fetchone(); conn.close()
    return render_template('admin_edit_news.html', news_item=news_item)
@app.route('/admin/news/update/<int:news_id>', methods=['POST'])
def admin_update_news(news_id):
    if not session.get('logged_in'): return redirect(url_for('login'))
    date, content = request.form['date'], request.form['content']
    conn = get_db_connection(); conn.execute('UPDATE news SET date = ?, content = ? WHERE id = ?', (date, content, news_id)); conn.commit(); conn.close()
    return redirect(url_for('admin_news'))
@app.route('/admin/news/delete/<int:news_id>')
def admin_delete_news(news_id):
    if not session.get('logged_in'): return redirect(url_for('login'))
    conn = get_db_connection(); conn.execute('DELETE FROM news WHERE id = ?', (news_id,)); conn.commit(); conn.close()
    return redirect(url_for('admin_news'))
@app.route('/admin/gallery')
def admin_gallery():
    if not session.get('logged_in'): return redirect(url_for('login'))
    gallery_path = os.path.join(app.static_folder, 'images/gallery')
    photo_list = [f for f in os.listdir(gallery_path) if not f.startswith('.')]
    return render_template('admin_gallery.html', photo_list=photo_list)
@app.route('/admin/gallery/delete/<filename>', methods=['POST'])
def admin_delete_photo(filename):
    if not session.get('logged_in'): return redirect(url_for('login'))
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(filename))
    if os.path.exists(file_path): os.remove(file_path)
    return redirect(url_for('admin_gallery'))
@app.route('/admin/gallery/upload', methods=['POST'])
def admin_upload_photo():
    if not session.get('logged_in'): return redirect(url_for('login'))
    uploaded_files = request.files.getlist('photos')
    for file in uploaded_files:
        if file and file.filename != '':
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return redirect(url_for('admin_gallery'))
@app.route('/admin/contacts')
def admin_contacts():
    if not session.get('logged_in'): return redirect(url_for('login'))
    conn = get_db_connection()
    contacts_list = conn.execute('SELECT * FROM contacts ORDER BY received_at DESC').fetchall()
    conn.close()
    return render_template('admin_contacts.html', contacts_list=contacts_list)
@app.route('/admin/reservations')
def admin_reservations():
    if not session.get('logged_in'): return redirect(url_for('login'))
    conn = get_db_connection()
    reservations_list = conn.execute('SELECT * FROM reservations ORDER BY request_received_at DESC').fetchall()
    conn.close()
    return render_template('admin_reservations.html', reservations_list=reservations_list)
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

# --- サーバー起動の処理 (変更なし) ---
if __name__ == '__main__':
    app.run(debug=True)