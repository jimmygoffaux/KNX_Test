import tkinter as tk
from tkinter import simpledialog
from tkinter import messagebox


# Création de la fenêtre racine
root = tk.Tk()
root.withdraw()  # Cacher la fenêtre racine


# Fonction pour demander une chaîne de caractères à l'utilisateur
def Value(ind):
    answer = simpledialog.askstring("Enter a value for group adress ", ind)
    return answer


def main():
    Main = Value("main")
    Main = int(Main, 10)
    Middle = Value("Middle")
    Middle = int(Middle, 10)
    Subgroup = Value("Subgroup")
    Subgroup = int(Subgroup, 10)
    print("the group adresse is : ", Main, "/", Middle, "/", Subgroup)
    adresse = (Main << 11) + (Middle << 8) + Subgroup
    adresse = hex(adresse)
    print(adresse)
    messagebox.showinfo("Valeur", f"the group adress in Hex is : {adresse}")


if __name__ == '__main__':
    main()
