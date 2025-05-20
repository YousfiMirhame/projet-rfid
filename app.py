from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

def chercher_utilisateur(rfid_code):
    conn = sqlite3.connect("rfid_users.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT nom, prenom, date_naissance, adresse, email, photo_path FROM users WHERE rfid_code = ?",
        (rfid_code,)
    )
    user = cursor.fetchone()
    conn.close()
    return user

@app.route("/", methods=["GET", "POST"])
def index():
    user = None
    erreur = None
    if request.method == "POST":
        code = request.form.get("code", "").strip()
        if code:
            user = chercher_utilisateur(code)
            if not user:
                erreur = "Aucun utilisateur trouvé pour ce code."
        else:
            erreur = "Veuillez entrer un code RFID."
    return render_template("index.html", user=user, erreur=erreur)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
