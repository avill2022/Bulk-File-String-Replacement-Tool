import tkinter as tk
from tkinter import *

import os
from pathlib import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter import scrolledtext

class FolderSelectGUI:
    def __init__(self, master):
        self.master = master
        master.title("Change reference")
        master.geometry('350x280')

        self.folder_path = tk.StringVar()

        self.label = tk.Label(master, textvariable=self.folder_path)
        self.label.pack(fill=X)

        self.select_button = tk.Button(master, text="Select Folder", command=lambda:select_folder())
        self.select_button.pack(fill=X)

        #frame 1
        self.frame1 = Frame(master=self.master, width=200, height=100)
        self.frame1.pack(fill=X)
        #elements textFrom ...
        self.lbl = Label(self.frame1, text="change")
        self.lbl.grid(column=0, row=0)
        self.textFrom = Entry(self.frame1,width=48)
        self.textFrom.grid(column=1, row=0)

        #frame 2
        self.frame2 = Frame(master=self.master, width=100)
        self.frame2.pack(fill=X)
        #elements to ...
        self.lb2 = Label(self.frame2, text="to")
        self.lb2.grid(column=0, row=0)
        self.textTo = Entry(self.frame2,width=50)
        self.textTo.grid(column=1, row=0)

        self.frame3 = Frame(master=self.master, width=50)
        self.frame3.pack(fill=X)
        self.txt3 = scrolledtext.ScrolledText(self.frame3,width=40,height=10)
        self.txt3.grid(column=0,row=0)

        btn = Button(self.frame3, text="Start",command=lambda:start_scan())
        btn.grid(column=0, row=1)

        def select_folder():
            folder_path = filedialog.askdirectory()
            self.folder_path.set(folder_path)

        def changeFile(campo):
            file=open(campo,'r+')
            l=file.readlines()
            result=[]
            for i in l:
                result.append(i.replace(self.textFrom.get(),self.textTo.get()))
            file.close()

            file=open(campo,'w')
            file.truncate(0)
            for a in result:
                file.write(a)
            file.close()

        def changeFiles():
            #os.walk(os.getcwd())
            for root, dirs, files in os.walk(self.folder_path.get()):
                for file in files:
                    if file.endswith(".kt") or file.endswith(".xml") or file.endswith(".java"):
                        changeFile(os.path.join(root, file))
                        os.rename(os.path.join(root, file), os.path.join(root, file).replace(self.textFrom.get(),self.textTo.get()))
                        self.txt3.insert(INSERT,os.path.join(root, file)+'\n')

        def start_scan():
            if self.label.cget("text"):
                if self.textFrom.get() and self.textTo.get():
                    changeFiles()
                else:
                    messagebox.showinfo("I need the reference", "WARNING! All the files reference will be changed!")
            else:
                messagebox.showinfo("Select a Folder", "WARNING! All the files in the folder will be changed!")

root = tk.Tk()
my_gui = FolderSelectGUI(root)
root.mainloop()