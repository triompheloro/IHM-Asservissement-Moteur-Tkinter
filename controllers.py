# coding: utf-8
import sys
import serial
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
from views import Screen
from tkinter import ttk




class Control :
    def __init__(self,parent,model,view , droite_bg , gauche_bg, port):
        self.direction = 0
        self.brake = False
        self.gauche_bg = gauche_bg
        self.droite_bg = droite_bg
        self.parent=parent
        self.model=model
        self.view=view
        self.ser = serial.Serial(port, 115200, timeout=0.1)
        self.gui()
        self.actions_binding()
        self.update_from_system()

        self.style = ttk.Style()
        self.style.configure(
            "Custom.TCombobox",
            fieldbackground="#ffffff",
            background="#e1e1e1",
            foreground="#333333",
            bordercolor="#999999",
            lightcolor="#cccccc",
            darkcolor="#333333",
            padding=8
        )


    def set_direction(self,direction) :
        self.direction = direction
    def get_direction(self) :
        return self.direction

    def set_brake(self,brake) :
        self.brake = brake
    def get_brake(self) :
        return self.brake

    def update_from_system(self):
        line = self.ser.readline().decode('utf-8').strip()
        if line:
            try:
                vitesse, intensite = map(int, line.split(','))
                self.model.set_vitesse(vitesse)
                self.model.set_vitesses(vitesse)
                self.model.set_intensite(intensite)
                print(f"Vitesse={vitesse}, Intensité={intensite}")
            except ValueError:
                pass
        self.parent.after(100, self.update_from_system)


    def gui(self):
        self.frame=tk.LabelFrame(self.parent,text="Control")
        self.frame_temps = tk.Frame(self.frame)
        self.frame_rotations = tk.Frame(self.frame)
        self.frame_buttons = tk.Frame(self.frame)

        self.scale_vitesse()

        self.scale_temps_min()
        self.scale_temps_max()

        self.chage_rotation()

        self.pause()
        self.gauche()
        self.droite()
        self.braking()
        self.change_data_to_observe()
    
    def scale_vitesse(self) :
        self.var_vitesse=tk.IntVar()
        self.var_vitesse.set(0)
        self.scale_vitesse=tk.Scale(self.frame,variable=self.var_vitesse,
                             label="Vitesse",
                             orient="horizontal",length=500,
                             from_=0,to=100,tickinterval=10,resolution=1)

    def scale_temps_min(self) :
        self.var_temps_min=tk.IntVar()
        self.var_temps_min.set(0)
        self.scale_temps_min=tk.Scale(self.frame_temps,variable=self.var_temps_min,
                             label="Temps debut",
                             orient="horizontal",length=250,
                             from_=0,to=50,tickinterval=10,resolution=1)

    def scale_temps_max(self) :
        self.var_temps_max=tk.IntVar()
        self.var_temps_max.set(0)
        self.scale_temps_max=tk.Scale(self.frame_temps,variable=self.var_temps_max,
                             label="Temps final",
                             orient="horizontal",length=250,
                             from_=50,to=100,tickinterval=10,resolution=1)

    def chage_rotation(self) :
        self.change_rotation=ttk.Combobox(
            self.frame_rotations,
            values=["Sens Trigonométrique", "Sens aiguille d'une montre"],
            width=40,
            style="Custom.TCombobox",
        )
        self.change_rotation.set("Sens Trigonométrique")



    def pause(self) :
        self.pause_action = tk.Button(self.frame_buttons, text= "Pause" ,cursor="hand2", padx=20, pady=5, width=10)

    def gauche(self) :
        self.direction_gauche = tk.Button(self.frame_buttons, image=self.gauche_bg, text= "Gauche" ,cursor="hand2", padx=20, pady=5)

    def droite(self) :
        self.direction_droite = tk.Button(self.frame_buttons,image=self.droite_bg, text= "Droite" , cursor="hand2", padx=20, pady=5)

    def braking(self) :
        self.brake_action = tk.Button(self.frame_buttons, text= "Frein" ,cursor="hand2", padx=20, pady=5, width=10)

    def change_data_to_observe(self) :
        self.change_data_action = tk.Button(self.frame_rotations, text= "Frein" ,cursor="hand2", padx=20, pady=5, width=10)
        
    def actions_binding(self) :
        self.scale_vitesse.bind("<B1-Motion>",self.on_vitesse_action)
        self.scale_temps_min.bind("<B1-Motion>",self.on_temps_min_action)
        self.scale_temps_max.bind("<B1-Motion>",self.on_temps_max_action)
        self.pause_action.bind("<Button-1>", self.on_pause_action)
        self.direction_gauche.bind("<Button-1>", self.on_gauche_action)
        self.direction_droite.bind("<Button-1>", self.on_droite_action)
        self.brake_action.bind("<Button-1>", self.on_brake_action)
        self.change_rotation.bind("<<ComboboxSelected>>",self.on_change_rotation)
        self.change_data_action.bind("<Button-1>", self.on_change_data_action)

    def on_vitesse_action(self,event):
        vitesse = self.var_vitesse.get()
        print("Vitesse = ", vitesse)
        self.model.set_vitesse_repere(vitesse)

        if self.ser.is_open:
            msg = f"{vitesse}\n"
            self.ser.write(msg.encode('utf-8'))

    def on_temps_min_action(self,event):
        temps_min = self.var_temps_min.get()
        print("Vitesse = ", temps_min)
        self.model.set_temps_min(temps_min)

    def on_temps_max_action(self,event):
        temps_max = self.var_temps_max.get()
        print("Vitesse = ", temps_max)
        self.model.set_temps_max(temps_max)

    def on_change_rotation(self, event):
        nouveau_sens = self.change_rotation.get()
        if nouveau_sens == "Sens aiguille d'une montre":
            print("Sens : ", 1)
        else :
            print("Sens : ", 0)

    def on_change_data_action(self, event):
        print("Vous avez réussi à mettre en place le boutton")

    def on_pause_action(self, event):
        self.model.inform_obervers = 0 if self.model.inform_obervers == 1 else 1

        if self.model.inform_obervers == 1:
            self.pause_action.configure(text="Pause")
        else :
            self.pause_action.configure(text="Play")

    def on_gauche_action(self,event):
        self.set_direction(0)
        print("Direction = ",self.get_direction())

    def on_droite_action(self,event):
        self.set_direction(1)
        print("Direction = ",self.get_direction())

    def on_brake_action(self,event):
        self.set_brake(not self.brake)
        if self.brake:
            self.brake_action.configure(text="Brake")
            print("Brake = 1")
        else :
            self.brake_action.configure(text="Start")
            print("Brake = 0")

    def layout(self,side="top") :
        self.frame.pack(expand=1,padx=20)
        self.scale_vitesse.pack()

        self.frame_temps.pack(pady=5)
        self.scale_temps_min.pack(side="left")
        self.scale_temps_max.pack(side="left")

        self.frame_rotations.pack(pady=5)
        self.change_rotation.pack(side="left")
        self.change_data_action.pack(side="left", padx=5)

        self.frame_buttons.pack(pady=5)

        self.pause_action.pack(side="left", padx=5)
        self.direction_gauche.pack(side="left", padx=5)
        self.direction_droite.pack(side="left", padx=5)
        self.brake_action.pack(side="left", padx=5)




if   __name__ == "__main__" :
   root=tk.Tk()
   gauche_img = tk.PhotoImage(file="./assets/gauchepetit.png")
   droite_img = tk.PhotoImage(file="./assets/droite.png")

   gauche_img = gauche_img.subsample(3, 2)
   droite_img = droite_img.subsample(3, 2)
   model=Communication()

   view=Screen(root)
   view.layout()
   model.attach(view)

   model.set_intensite(100)
   model.set_vitesse(150)

   control=Control(root,model,view, droite_img,gauche_img, 'COM4')
   control.layout()
   root.mainloop()

