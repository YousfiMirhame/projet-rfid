from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

def chercher_utilisateur(rfid_code):
    conn = sqlite3.connect("rfid_users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT nom, prenom, date_naissance, adresse, email, photo_path FROM users WHERE rfid_code = ?", (rfid_code,))
    user = cursor.fetchone()
    conn.close()
    return user

@app.route('/', methods=['GET', 'POST'])
def index():
    user = None
    if request.method == 'POST':
        code = request.form['code']
        user = chercher_utilisateur(code)
    return render_template('index.html', user=user)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
