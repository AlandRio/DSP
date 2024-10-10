# Library for GUI
import tkinter as tk
from generateMenu import createGenerateMenu
from importMenu import createImportMenu
from editMenu import createEditMenu

# Creating and defining Root Window
root = tk.Tk()
root.title("Digital Signal Processing")
root.iconbitmap("wave-sine.ico")
root.minsize(1280, 720)
root.configure(bg='black')

# Global Variable
type_var = tk.BooleanVar()
amp_var = tk.IntVar()
sampleNum_var = tk.IntVar()
theta_var = tk.DoubleVar()
sampleFreq_var = tk.DoubleVar()
freq_var = tk.DoubleVar()

# Creating Canvases
menuCanvas = tk.Canvas(root, width= 640 , height=360,highlightthickness=2,highlightbackground="green")
menuCanvas.configure(bg="black")
menuCanvas.place(relwidth = 0.5, relheight = 0.5,relx = 0, rely = 0)

originalWaveCanvas = tk.Canvas(root, width= 640 , height=360,highlightthickness=2,highlightbackground="green")
originalWaveCanvas.configure(bg="black")
originalWaveCanvas.place(relwidth = 0.5, relheight = 0.5,relx = 0.5, rely = 0)

editedWaveCanvas = tk.Canvas(root, width= 640 , height=360,highlightthickness=2,highlightbackground="green")
editedWaveCanvas.configure(bg="black")
editedWaveCanvas.place(relwidth = 0.5, relheight = 0.5,relx = 0.5, rely = 0.5)

def generateMenuClick():
    generateCanvas = createGenerateMenu(root,type_var, amp_var, sampleNum_var,theta_var, sampleFreq_var,freq_var)
    generateCanvas.place(relwidth = 0.5, relheight = 0.5,relx = 0, rely = 0.5)

def importMenuClick():
    importCanvas = createImportMenu(root)
    importCanvas.place(relwidth = 0.5, relheight = 0.5,relx = 0, rely = 0.5)

def editMenuClick():
    editCanvas = createEditMenu(root)
    editCanvas.place(relwidth = 0.5, relheight = 0.5,relx = 0, rely = 0.5)

# Creating Label
menuName = tk.Label(menuCanvas, text="DSP - Section 1")
menuName.configure(fg="green", bg="black",highlightthickness=2,highlightbackground="green")

originalLabel = tk.Label(originalWaveCanvas, text="Original Wave:",highlightthickness=2,highlightbackground="green")
originalLabel.configure(fg="green", bg="black")

editedLabel = tk.Label(editedWaveCanvas, text="Edited Wave:",highlightthickness=2,highlightbackground="green")
editedLabel.configure(fg="green", bg="black")


# Creating Buttons
importButtonBorder = tk.Frame(menuCanvas, bd=0,highlightthickness=2,highlightcolor="green",highlightbackground="green")
importButton = tk.Button(importButtonBorder, text="Import", command=importMenuClick, width='20', borderwidth=3)
importButton.configure(fg="green", bg="black",bd=0, borderwidth=0)

generateButtonBorder = tk.Frame(menuCanvas, bd=0,highlightthickness=2,highlightcolor="green",highlightbackground="green")
generateButton = tk.Button(generateButtonBorder, text="Generate", command=generateMenuClick, width='20', borderwidth=3)
generateButton.configure(fg="green", bg="black",bd=0, borderwidth=0)

editButtonBorder = tk.Frame(menuCanvas, bd=0,highlightthickness=2,highlightcolor="green",highlightbackground="green")
editButton = tk.Button(editButtonBorder, text="Edit", command=editMenuClick, width='20')
editButton.configure(fg="green", bg="black",bd=0, borderwidth=0)

# Putting content on screen
menuName.place(relwidth= 0.25,relheight=0.1,relx= 0, rely=0)
originalLabel.place(relwidth= 0.25,relheight=0.1,relx= 0, rely=0)
editedLabel.place(relwidth= 0.25,relheight=0.1,relx= 0, rely=0)


importButtonBorder.place(relwidth= 0.25,relheight=0.25,relx= 0, rely=0.25)
importButton.place(relwidth=1,relheight=1,relx=0,rely=0)

generateButtonBorder.place(relwidth= 0.25,relheight=0.25,relx= 0, rely=0.5)
generateButton.place(relwidth=1,relheight=1,relx=0,rely=0)

editButtonBorder.place(relwidth= 0.25,relheight=0.25,relx= 0, rely=0.75)
editButton.place(relwidth=1,relheight=1,relx=0,rely=0)



root.mainloop()
