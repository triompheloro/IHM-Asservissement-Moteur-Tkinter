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

from pathlib import Path
import pandas as pd
import time


from models import Communication
from views import Screen
from controllers import Control


actions={
        "File" : [
            ("New","<Control-n>"),
            ("Load","<Control-l>"),
            ("Save","<Control-s>"),
            ("SaveAs","<Control-S>"),
            ("Exit","<Control-e>")
            ],
        "Help" : [
            ("About Us","<Control-u>"),
            ("About Application","<Control-a>"),
            ("About TkInter","<Control-t>")
            ]
}


class MainWindow(tk.Tk) :
    def __init__(self) :
        tk.Tk.__init__(self)
        self.title("IPS")
        self.option_readfile("main.opt")
        self.menubar()
        self.create()

    def create(self) :

        self.model=Communication()
        frame=tk.LabelFrame(self)
        view=Screen(frame)
        frame.pack()
        view.layout()

        self.model.attach(view)

        # Les images de background pour les bouttons
        gauche_img = tk.PhotoImage(file="./assets/gauchepetit.png")
        droite_img = tk.PhotoImage(file="./assets/droite.png")

        # Mise en forme
        gauche_img = gauche_img.subsample(5, 2)
        droite_img = droite_img.subsample(5, 2)

        control=Control(self,self.model,view, droite_img, gauche_img, 'COM4')
        control.layout()
        control.view.update_vitesse_repere()
        control.view.update_temps()


    def menubar(self) :
        if DEBUG :
            print("menubar()")
        menubar=tk.Menu(self) 
        self.config(menu=menubar)

        self.menubar_actions(menubar, actions)

        return menubar
    
    def menubar_actions(self, menubar,actions) :
        if DEBUG :
            print("menubar_actions()")
        for key in actions.keys() :
            menu=tk.Menu(menubar)
            for action in actions[key] :
                item,ctrl=action 
                if key=="File" :
                    menu.add_command(label=item,accelerator=ctrl,command=lambda name=item: self.on_file_actions(name))
                    self.bind_all(ctrl,lambda x,name=item: self.on_file_actions(name))
                elif key=="Help" :
                    menu.add_command(label=item,accelerator=ctrl,command=lambda name=item: self.on_help_actions(name))
                    self.bind_all(ctrl,lambda x,name=item: self.on_help_actions(name))
                # if other key ("Help", ...)  : add  callbacks
            menubar.add_cascade(label=key,underline=0,menu=menu)
    
    def on_file_actions(self,name): 
        if DEBUG :
            print("on_file_actions()")  

        if  name=="New" :
            self.new_action(self.model)
        elif name=="Load" :
            self.load_action(self.model)
        elif  name=="Save" :
            self.save_action(self.model)
        elif  name=="SaveAs" :
            self.saveAs_action(self.model)
        elif  name=="Exit" :
            exit(0)
        else :
            print(name+" : action non implémentée")
        return
    
    def new_action(self, model) :
        pass
    
    def load_action(self,model) :
        if DEBUG :
            print("load_action()")
        types=(('db files', '*.db'),)
        result=filedialog.askopenfilename(filetypes=types)
        if result :
            name=Path(result).name
            model.read(db=name)
        return
    
    def save_action(self,model) :
        if DEBUG :
            print("save_action()")
        result= tk.messagebox.askquestion(title="Sauvegarde", message=" Souhaitez-vous sauvegarder le fichier ?")

        if result=='yes' :
            model.delete()
            model.create()
            #pass
        else :
            self.saveAs_action(model)
        return
    
    def saveAs_action(self,model) :
        pass

    def on_help_actions(self,name):
        if DEBUG :
            print("on_help_actions()")
        if  name=="About Us" :
            tk.messagebox.showinfo(title=name, message="Contacts",detail="Email : s25loro@enib.fr")
        elif name=="About Application" :
            print(name)
        elif  name=="About TkInter" :
            print(name)
        else :
            print(name+" : non reconnu")
        return


if __name__=="__main__" :
    app=MainWindow()
    app.mainloop()

class MainWindow(tk.Tk) :
    def __init__(self) :
        tk.Tk.__init__(self)
        self.title("IPS")
        self.option_readfile("main.opt")
        self.menubar()
        self.create()

    def create(self) :
        self.model=Communication()
        frame=tk.LabelFrame(self,name="IPS")
        view=Screen(frame)
        frame.pack()
        view.layout()
        self.model.attach(view)