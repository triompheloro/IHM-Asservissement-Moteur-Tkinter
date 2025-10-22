# coding: utf-8
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

from math import pi,sin
import copy    
import sqlite3

from observer import Subject

class Communication(Subject) :
    def __init__(self) :
        Subject.__init__(self)
        self.intensite = 0
        self.vitesse = 0
        self.vitesse_repere = [10 for i in range(0,100)]
        self.vitesses = [1 for i in range(0,100)]

        self.temps_min = 10
        self.temps_max = 90

        self.inform_obervers = 1

    def get_vitesse(self) :
        return self.vitesse

    def get_intensite(self) :
        return self.intensite

    def get_vitesses(self):
        return self.vitesses

    def get_vitesse_repere(self):
        return self.vitesse_repere

    def get_temps_min(self):
        return self.temps_min
    def get_temps_max(self):
        return self.temps_max



    def set_vitesse(self,vitesse) :
        self.vitesse=vitesse
        if self.inform_obervers == 1 :
            self.notify()
    def set_intensite(self,intensite) :
        self.intensite=intensite
        if self.inform_obervers == 1:
            self.notify()

    def set_vitesse_repere(self,vitesse_repere) :
        self.vitesse_repere=[vitesse_repere for i in range(0,100)]
        if self.inform_obervers == 1:
            self.notify()

    def set_vitesses(self,vitesse):
        self.vitesses = self.vitesses[1:] + [vitesse]
        if self.inform_obervers == 1:
            self.notify()


    def set_temps_min(self, temps):
        self.temps_min = temps
        self.notify_temps()

    def set_temps_max(self, temps):
        self.temps_max = temps
        self.notify_temps()

    # Ici, à chaque fois que je recois une nouvelle valeure,
    # je me à jour la liste des dernière valeur de vitesse
    # def update(self,vitesse_recue) :
    #     vitesse = self.vitesses[1:] + [vitesse_recue]
    #     self.vitesses = vitesse
    #     self.notify()
    
    # def create(self,db="signals.db") :
    #     connect=sqlite3.connect(db)
    #     cursor=connect.cursor()
    #     query="INSERT OR IGNORE INTO signals(id,frequency,phase,magnitude) VALUES(?,?,?,?)"
    #     to_insert=self.get_name(),self.get_frequency(),self.get_phase(),self.get_magnitude()
    #     cursor.execute(query,to_insert)
    #     query="INSERT OR IGNORE INTO samples(id,x,y,signal_id) VALUES(?,?,?,?)"
    #     key=1
    #     for value in self.get_signal() :
    #         cursor.execute(query,(key,value[0],value[1],self.get_name()))
    #         key+=1
    #     connect.commit()
    #     cursor.close()
    #     connect.close()

    # def read(self,db="signals.db") :
    #     connect=sqlite3.connect(db)
    #     cursor=connect.cursor()
    #     to_select=self.get_name()
    #     print("read",to_select)
    #     query="SELECT x,y FROM samples WHERE signal_id=?;"
    #     results=cursor.execute(query,to_select)
    #     if results :
    #         del self.signal[:]
    #         for result in results :
    #             self.signal.append((result[0],result[1]))
    #     else :
    #         print("no signal for name : ",to_select)
    #     cursor.close()
    #     connect.close()
    #     self.notify()

 
    # def update(self,db="signals.db") :
    #     connect=sqlite3.connect(db)
    #     cursor=connect.cursor()
    #     to_update=self.get_name(),self.get_frequency()
    #     query="UPDATE signals SET frequency=? WHERE id=?;"
    #     cursor.execute(query,to_update)
    #     key=1
    #     query="UPDATE samples SET x=?,y=? WHERE id=? AND signal_id=?;"
    #     key=1
    #     for value in self.get_signal() :
    #         cursor.execute(query,(value[0],value[1],key,self.get_name()))
    #         key+=1
    #     connect.commit()
    #     cursor.close()
    #     connect.close()
    #     self.notify()

    # def delete(self,db="signals.db") :
    #     connect=sqlite3.connect(db)
    #     cursor=connect.cursor()
    #     to_delete=self.get_name()
    #     query="DELETE FROM signals WHERE id=?;"
    #     cursor.execute(query,to_delete)
    #     query="DELETE FROM samples WHERE signal_id=?;"
    #     cursor.execute(query,to_delete)
    #     connect.commit()
    #     cursor.close()
    #     connect.close()
    #     self.notify()

# def delete_signal(name="X",db="signals.db") :
#     connect=sqlite3.connect(db)
#     cursor=connect.cursor()
#     to_delete=name
#     query="DELETE FROM signals WHERE id=?;"
#     cursor.execute(query,to_delete)
#     query="DELETE FROM samples WHERE signal_id=?;"
#     cursor.execute(query,to_delete)
#     connect.commit()
#     cursor.close()
#     connect.close()

# if   __name__ == "__main__" :
#     model=Generator()
#     model.set_samples(100)
#     model.set_frequency(2)
#     model.generate()
#     model.create()
#
#     model.set_frequency(5)
#     model.set_name("Y")
#     model.generate()
#     model.create()
 
 

