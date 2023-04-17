import customtkinter
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import os
import shutil

customtkinter.set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  

build_gradle_project = ""
build_gradle_app = ""
folder_path=""
count_files = 0

to_folder="\\project"

def howManyFiles():
    global count_files
    global folder_path 
    if(folder_path):
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                dire = os.path.join(root, file)
                if file.endswith(".kt") or file.endswith(".xml") or file.endswith(".java") or file.endswith(".gradle"):
                        count_files +=1
    return count_files



def copyFile(file_url):
    #os.walk(os.getcwd())
    global to_folder
    print(file_url)
    dst_file_path = "app\src\main\java"+"\\"+file_url.split("\\")[5]+"\\"+file_url.split("\\")[6]+"\\"+file_url.split("\\")[7]    
    folder = file_url.split(dst_file_path)[1]
    #extract the file of the url
    a = folder.split("\\")[-1]
    #take the size of the name
    size = len(a)
    #take the first part
    my_string = folder[:-size]
    #current direction folder
    script_path = os.path.abspath(__file__)
    script_dir = os.path.dirname(script_path)
    folder_destiny = script_dir +to_folder+"\\app\\main"+ my_string

    if not os.path.exists(folder_destiny):
        os.makedirs(folder_destiny)

    file_destiny =  folder_destiny + a

    #copy the file
    shutil.copy(file_url, file_destiny)

    if os.path.exists(file_destiny):
        count_progress=progressbar_1.get()
        count_progress+=1
        progressbar_1.set(count_progress)
        print(f"The file '{file_destiny}' was copied successfully.")
    else:
        print(f"There was an error copying the file.")

    #change reference
    if(textFrom.get() and textTo.get()):
        changeFile(file_destiny)
        os.rename(file_destiny, file_destiny.replace(textFrom.get(),textTo.get()))

def changeFile(campo):
    file=open(campo,'r+')
    l=file.readlines()
    result=[]
    for i in l:
        result.append(i.replace(textFrom.get(),textTo.get()))
    file.close()

    file=open(campo,'w')
    file.truncate(0)
    for a in result:
        file.write(a)
    file.close()

def start_cleaning():
    global folder_path
    global to_folder

    if(folder_path):
        #current direction folder
        script_path = os.path.abspath(__file__)
        folderDestiny = os.path.dirname(script_path) + to_folder

        #copy the gradle
        f1 = folder_path+"/build.gradle"
        f2 = folderDestiny+"/build.gradle"

        if not os.path.exists(folderDestiny+"/app/"):
            os.makedirs(folderDestiny+"/app/")

        shutil.copy(f1, f2)
        #copy the gradle #2
        f1 = folder_path+"/app/build.gradle"
        f2 = folderDestiny+"/app/build.gradle"

        if not os.path.exists(folderDestiny+"/app/"):
            os.makedirs(folderDestiny+"/app/")
        shutil.copy(f1, f2)
        #copy the manifest 
        if not os.path.exists(folderDestiny+"\\app"):
            os.makedirs(folderDestiny+"\\app")
        shutil.copy(folder_path+"\\app\src\main\AndroidManifest.xml", folderDestiny+"\\app\AndroidManifest.xml")
        #copy the res folder
        # remove the destination folder if it already exists
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        if os.path.exists(folderDestiny+"\\app\\res"):
            shutil.rmtree(folderDestiny+"\\app\\res")
        shutil.copytree(folder_path+"\\app\\src\\main\\res", folderDestiny+"\\app\\res")

        print("Starting cleaning")
        if(folder_path):
            for root, dirs, files in os.walk(folder_path):
                for file in files:
                    dire = os.path.join(root, file)
                    if file.endswith(".kt") or file.endswith(".xml") or file.endswith(".java"):
                        if "app\src\main\java" in dire:
                            copyFile(os.path.join(root, file))
        messagebox.showinfo("####SUCCESS#####", "All files are clean!")
    else:
        messagebox.showinfo("There isn't a folder selected!", "Select a android project")


def select_folder():
    global folder_path 
    folder_path = filedialog.askdirectory()
    if os.path.exists(folder_path+"/gradle.properties") and os.path.exists(folder_path+"/build.gradle"):
        print(f"The file '{folder_path}' exists.")
        
        build_gradle_project = folder_path+"/gradle.properties"
        howManyFiles()
        progressbar_1.size= howManyFiles()

        entry_1.insert(0, "")
        entry_1.insert(0, folder_path)
    else:
        print(f"The file '{folder_path}' does not exist.")
        entry_1.insert(0, "")
        entry_1.insert(0, folder_path)
        messagebox.showinfo("This folder isn't a Gradle project", "WARNING! This folder isn't a Gradle project!")

app = customtkinter.CTk()
app.geometry("400x480")
app.title("Change Reference Android Projects")

mainWindow = customtkinter.CTkFrame(master=app)
mainWindow.pack(pady=20, padx=20, fill="both", expand=True)

titleLabel = customtkinter.CTkLabel(mainWindow, text="Clean Android Project", font=customtkinter.CTkFont(size=20, weight="bold"), justify=customtkinter.LEFT)
titleLabel.pack(pady=10, padx=10)

button_1 = customtkinter.CTkButton(master=mainWindow, text="Select folder", command=select_folder)
button_1.pack(pady=10, padx=10, fill="both")

entry_1 = customtkinter.CTkEntry(master=mainWindow, placeholder_text="C:/Users/james/Desktop/")
entry_1.pack(pady=10, padx=10, fill="both")


#frame 1
frame1 = customtkinter.CTkFrame(master=mainWindow, width=200, height=100)
frame1.pack(pady=10, padx=10, fill="both")
#elements textFrom ...
lbl = customtkinter.CTkLabel(frame1, text="change: ")
lbl.grid(column=0, row=0)
textFrom = customtkinter.CTkEntry(frame1, placeholder_text="com.something.something",width=100)
textFrom.grid(column=1, row=0)

#elements textFrom ...
lto = customtkinter.CTkLabel(frame1, text="to: ")
lto.grid(column=0, row=1)
textTo = customtkinter.CTkEntry(frame1, placeholder_text="com.something.something",width=100)
textTo.grid(column=1, row=1)

progressbar_1 = customtkinter.CTkProgressBar(master=mainWindow)
progressbar_1.pack(pady=10, padx=10,fill="both")
progressbar_1.set(0.0)

btn = customtkinter.CTkButton(mainWindow, text="Start",command=start_cleaning)
btn.pack(pady=10, padx=10)


app.mainloop()
