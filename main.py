#   Graphical toll for  database  query execution   #   For graphical interface instalation execute the following commands in terminal  #
#                   Made by:                        #   Through package manager:                                                         #
#       João Vitor Caversan dos Passos              #       sudo apt install python3-tk                                                 #
#   Contact: joaopassos@alunos.utfpr.edu.br         #                                                                                   #
#   Alfons Carlos César Heiermann de Andrade        #   Through pip command:                                                             #
#       Contact: alfons@alunos.utfpr.edu.br         #       pip install tk                                                              #


from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from Database import Database
import os

gui = Tk()
gui.geometry("400x200")
gui.title("Folder selection")
icon = PhotoImage(file = 'icon.png')
gui.iconphoto(False, icon)
class FolderSelect(Frame):

    def __init__(self,parent=None,folderDescription="",**kw):
        Frame.__init__(self,master=parent,**kw)
        self.folderPath = StringVar()
        self.lblName = Label(self, text=folderDescription)
        self.lblName.grid(row=0,column=0)

        self.entPath = Entry(self, textvariable=self.folderPath)
        self.entPath.grid(row=0,column=1)

        self.btnFind = ttk.Button(self, text="Browse Folder",command=self.setFolderPath)
        self.btnFind.grid(row=0,column=2)

    def setFolderPath(self):
        folder_selected = filedialog.askdirectory()
        self.folderPath.set(folder_selected)

    @property
    def folder_path(self):
        return self.folderPath.get()

def loadFile():
    folder1 = directorySelect.folder_path
    os.chdir(folder1)
    print(folder1)

    print("Creating table files based on...")

    dataBase = Database(folder1)
    dataBase.searchLoop()

    gui.destroy()

    return

directorySelect = FolderSelect(gui,"Select Folder ")
directorySelect.grid(row=0)

load = ttk.Button(gui, text="Load", command=loadFile)
load.grid(row=4,column=0)

gui.mainloop()
