# coding: utf-8
DEBUG=False

import sys
major=sys.version_info.major
minor=sys.version_info.minor
if major==2 and minor==7 :
    import Tkinter as tk
    import tkFileDialog as filedialog
elif major==3 :
    import tkinter as tk
    from tkinter import filedialog
else :
    if __name__ == "__main__" :
        print("Your python version is : ",major,minor)
        print("... I guess it will work !")
    import tkinter as tk
    from tkinter import filedialog 

from models import Communication
from observer import Observer

class Screen(Observer) :
    def __init__(self,parent,bg="white",largeur=150,hauteur=60):
        self.parent=parent
        self.bg=bg
        self.largeur,self.hauteur=largeur,hauteur
        self.color="red"
        self.gui() 
        self.actions_binding()
        self.draw_axes()

        self.to_be_actualized = 1

        self.vitesse_repere = [10 for i in range(0, 100)]
        self.vitesses = [1 for i in range(0, 100)]
        self.intensites = [1 for i in range(0, 100)]
        self.observe_vitesse = 1

        self.vitesse_a_observer = []
        self.intensite_a_observer = []

        self.temps_min = 10
        self.temps_max = 90


    def get_vitesses(self):
        return self.vitesses
    def get_intensites(self):
        return self.intensites

    def get_vitesse_repere(self):
        return self.vitesse_repere

    def get_temps_min(self):
        return self.temps_min
    def get_temps_max(self):
        return self.temps_max

    def set_vitesse_repere(self,vitesse_repere) :
        self.vitesse_repere=[vitesse_repere for i in range(0,100)]

    def set_vitesses(self,vitesse):
        self.vitesses = self.vitesses[1:] + [vitesse]

    def set_intensites(self,intensite):
        self.intensites = self.intensites[1:] + [intensite]


    def set_temps_min(self, temps):
        self.temps_min = temps

    def set_temps_max(self, temps):
        self.temps_max = temps


    def get_parent(self) :
        return self.parent
    def set_parent(self,parent) :
        self.parent=parent
    def gui(self) :
        self.frame = tk.Frame(self.parent)

        self.vitesse = tk.Canvas(self.frame, width=self.largeur, height=self.hauteur, bg="black", highlightthickness=2, highlightbackground="gray")
        self.intensite = tk.Canvas(self.frame, width=self.largeur, height=self.hauteur, bg="black", highlightthickness=2, highlightbackground="gray")

        self.temps_aservissement = tk.Canvas(self.frame, width=self.largeur, height=self.hauteur, bg="black", highlightthickness=2, highlightbackground="gray")

        self.visualisation=tk.Canvas(self.parent,bg=self.bg,width=600,height=300, background="black")
        self.text_vitesse = self.vitesse.create_text(
            self.largeur - 10, self.hauteur // 2,
            text="--", fill="lime", font=("Arial", 24, "bold"), anchor="e"
        )
        self.text_intensite = self.intensite.create_text(
            self.largeur - 10, self.hauteur // 2,
            text="--", fill="cyan", font=("Arial", 24, "bold"), anchor="e"
        )
        self.text_temps_aservissement = self.temps_aservissement.create_text(
            self.largeur - 10, self.hauteur // 2,
            text="--", fill="red", font=("Arial", 24, "bold"), anchor="e"
        )
        
    def actions_binding(self) :
        if DEBUG :
            print(type(self).__name__+".actions_binding()")
        
    def update(self,subject):
        if subject:
            vitesse = subject.get_vitesse()
            intensite = subject.get_intensite()

            if vitesse is not None and intensite is not None:
                self.vitesse.itemconfig(self.text_vitesse, text=str(vitesse) + " mV")
                self.intensite.itemconfig(self.text_intensite, text=str(intensite) + " mA")
            else:
                self.vitesse.itemconfig(self.text_vitesse, text="--")
                self.intensite.itemconfig(self.text_intensite, text="--")

            #tracer la courbe des vitesses
            self.set_vitesses(vitesse)  # pour garder les vraies valeurs j'actualise toujours
            self.set_intensites(intensite)

            if self.to_be_actualized == 1:
                self.vitesse_a_observer = self.get_vitesses()
                self.intensite_a_observer = self.get_intensites()
            if self.observe_vitesse == 1 :
                self.plot_line(self.vitesse_a_observer, "blue", "data_to_observe")
            else :
                self.plot_line(self.intensite_a_observer, "green", "data_to_observe")

            #print(self.get_vitesses())

        else:
            self.vitesse.itemconfig(self.text_vitesse, text="N/A")
            self.intensite.itemconfig(self.text_intensite, text="N/A")

    # à implementer
    def update_on_pause(self):
        pass

    def update_vitesse_repere(self):
        if self.to_be_actualized == 1:
            # Tracer la ligne de la vitesse repere
            self.plot_line(self.get_vitesse_repere(), "red", "vitesse_reference")
            print(self.get_vitesse_repere())

    def update_temps(self):
        temps_min = self.get_temps_min()
        temps_max = self.get_temps_max()

        if temps_min and temps_max:
            self.tracer_axes_temps(self.get_temps_min(),"temps_min")
            self.tracer_axes_temps(self.get_temps_max(),"temps_max")

            self.temps_aservissement.itemconfig(self.text_vitesse, text=str(temps_max-temps_min) + " s")

        else:
            self.temps_aservissement.itemconfig(self.text_vitesse, text="--")
            print("temps_max ou temps min non defini")


    def plot_line(self, vitesses, color, name):
        width = 600
        height = 300
        margin_x = 40
        margin_y = 20

        coords = []
        for t, v in enumerate(vitesses):
            # Conversion vers coordonnées Canvas (t: 0–99, v: 0–100)
            x = margin_x + (t / 100) * (width - margin_x - 10)
            y = height - margin_y - (v / 100) * (height - margin_y - 10)
            coords.extend((x, y))
        self.visualisation.delete(name)
        self.visualisation.create_line(coords, fill=color, smooth=1, width=3, tags=name)

    def tracer_axes_temps(self, temps, name ):
        # height = int(self.visualisation['height'])
        height = 300
        width = 600
        margin_x = 40
        t =margin_x +  (temps / 100) * (width - margin_x - 10)
        self.visualisation.delete(name)
        self.visualisation.create_line(t, 0, t, height, fill="yellow", width=2, tags=name)

    def resize(self,event):
        if DEBUG :
            print(type(self).__name__+".resize()")
            print("width,height : ",(event.width,event.height))
        self.width,self.height=event.width,event.height
        # TODO : manage grid and signal refresh in resizing()

    def draw_axes(self):
        width = 600
        height = 300
        margin_x = 40
        margin_y = 20

        self.visualisation.delete("axes")
        self.visualisation.create_line(margin_x, height - margin_y, width - 10, height - margin_y, width=2, arrow=tk.LAST, tags="axes", fill="white")
        self.visualisation.create_line(margin_x, height - margin_y, margin_x, 10, width=2, arrow=tk.LAST, tags="axes", fill="white")

        # Label des axes
        self.visualisation.create_text(width - 20, height - 10, text="t (s)", font=("Arial", 10), tags="axes", fill="white")
        self.visualisation.create_text(20, 15, text="V(t)", font=("Arial", 10), tags="axes", fill="white")

        for i in range(0, 101, 20):
            # Axe X : t(s)
            x = margin_x + (i / 100) * (width - margin_x - 10)
            self.visualisation.create_line(x, height - margin_y - 5, x, height - margin_y + 5, tags="axes" , fill="white")
            self.visualisation.create_text(x, height - margin_y + 15, text=str(i), font=("Arial", 8), tags="axes", fill="white")

            # Axe Y : V(t)
            y = height - margin_y - (i / 100) * (height - margin_y - 10)
            self.visualisation.create_line(margin_x - 5, y, margin_x + 5, y, tags="axes" , fill="white")
            self.visualisation.create_text(margin_x - 20, y, text=str(i), font=("Arial", 8), tags="axes", fill="white")

    def layout(self) :
        self.frame.pack(padx=20, pady=20)
        self.vitesse.pack(side="left", padx=10)
        self.intensite.pack(side="left", padx=10)
        self.temps_aservissement.pack(side="left", padx=10)
        self.visualisation.pack(side="left", padx=10)

if   __name__ == "__main__" :
   root=tk.Tk()
   model=Communication()
   model.set_intensite(100)

   model.set_vitesse(150)

   view=Screen(root)
   view.layout()

   model.attach(view)
   model.notify()
   view.update_vitesse_repere()
   view.update_temps()

   root.mainloop()

