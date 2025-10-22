import tkinter as tk

root = tk.Tk()
root.title("Afficheurs sur Canvas")

frame = tk.Frame(root, bg="lightgray")
frame.pack(padx=20, pady=20)

# Taille des afficheurs
largeur = 150
hauteur = 60

# Création de 2 Canvas
canvas1 = tk.Canvas(frame, width=largeur, height=hauteur, bg="black", highlightthickness=2, highlightbackground="gray")
canvas1.pack(side="left", padx=10)

canvas2 = tk.Canvas(frame, width=largeur, height=hauteur, bg="black", highlightthickness=2, highlightbackground="gray")
canvas2.pack(side="left", padx=10)

# Ajout de texte aligné à droite
text1 = canvas1.create_text(
    largeur-10, hauteur//2,      # position X=à droite (marge de 10 px), Y=milieu
    text="123",
    fill="lime",
    font=("Arial", 24, "bold"),
    anchor="e"                   # alignement à droite
)

text2 = canvas2.create_text(
    largeur-10, hauteur//2,
    text="456",
    fill="cyan",
    font=("Arial", 24, "bold"),
    anchor="e"
)

# Fonction pour mettre à jour la valeur d’un Canvas
def update_display(canvas, text_id, value):
    canvas.itemconfig(text_id, text=str(value))

# Exemple : incrémenter la valeur de gauche
def incrementer():
    current = int(canvas1.itemcget(text1, "text"))
    update_display(canvas1, text1, current + 1)

btn = tk.Button(root, text="Incrémenter gauche", command=incrementer)
btn.pack(pady=10)

root.mainloop()
