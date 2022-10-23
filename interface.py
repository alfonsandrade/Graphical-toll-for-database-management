from tkinter import *
from tkinter import ttk
from tkinter import filedialog


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

def doStuff():
    folder1 = directorySelect.folder_path
    print("Doing stuff with folder", folder1)

folderPath = StringVar()

directorySelect = FolderSelect(gui,"Select Folder ")
directorySelect.grid(row=0)

load = ttk.Button(gui, text="Load", command=doStuff)
load.grid(row=4,column=0)

quitter = ttk.Button(gui, text = "Quit",command = gui.quit)
quitter.grid(row=5,column=0)

gui.mainloop()