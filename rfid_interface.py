import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk, ImageOps
import sqlite3

# Connexion à la base
def chercher_utilisateur(rfid_code):
    conn = sqlite3.connect("rfid_users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT nom, prenom, date_naissance, adresse, email, photo_path FROM users WHERE rfid_code = ?", (rfid_code,))
    user = cursor.fetchone()
    conn.close()
    return user

# Fonction pour afficher les informations
def afficher_info():
    code = entry_code.get().strip()
    user = chercher_utilisateur(code)

    # Nettoyer l'affichage précédent
    for widget in resultat_frame.winfo_children():
        widget.destroy()

    if user:
        frame_saisie.pack_forget()
        frame_retour.pack(pady=10)

        infos = [
            f"Nom : {user[0]}",
            f"Prénom : {user[1]}",
            f"Date de naissance : {user[2]}",
            f"Adresse : {user[3]}",
            f"Email : {user[4]}"
        ]

        for info in infos:
            label = tk.Label(resultat_frame, text=info, font=("Helvetica", 12))
            label.pack(anchor='w', padx=10)

        try:
            image = Image.open(user[5])
            image = ImageOps.contain(image, (250, 250))  # Redimensionner proprement
            photo = ImageTk.PhotoImage(image)
            photo_label = tk.Label(resultat_frame, image=photo)
            photo_label.image = photo
            photo_label.pack(pady=10)
        except Exception as e:
            tk.Label(resultat_frame, text=f"Erreur lors du chargement de la photo : {e}", fg="red").pack()
    else:
        messagebox.showwarning("Non trouvé", "Utilisateur non trouvé pour ce code.")

# Fonction pour revenir à l'accueil
def retour_accueil():
    frame_retour.pack_forget()
    entry_code.delete(0, tk.END)
    frame_saisie.pack(pady=10)
    for widget in resultat_frame.winfo_children():
        widget.destroy()

# Interface principale
root = tk.Tk()
root.title("Lecteur RFID - Interface Utilisateur")
root.geometry("400x600")

# Saisie du code
frame_saisie = tk.Frame(root)
frame_saisie.pack(pady=10)

label_code = tk.Label(frame_saisie, text="Entrer le code RFID :", font=("Helvetica", 12))
label_code.pack(pady=5)

entry_code = tk.Entry(frame_saisie, font=("Helvetica", 14))
entry_code.pack(pady=5)

btn_rechercher = tk.Button(frame_saisie, text="Rechercher", command=afficher_info)
btn_rechercher.pack(pady=10)

# Résultats
resultat_frame = tk.Frame(root)
resultat_frame.pack()

# Bouton retour
frame_retour = tk.Frame(root)
btn_retour = tk.Button(frame_retour, text="⟵ Retour", command=retour_accueil)
btn_retour.pack()

root.mainloop()
