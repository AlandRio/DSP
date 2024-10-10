# Library for GUI
import tkinter as tk

import utils
from importMenu import createImportMenu
from editMenu import createEditMenu
from utils import Wave

# Creating and defining Root Window
root = tk.Tk()
root.title("Digital Signal Processing")
root.iconbitmap("wave-sine.ico")
root.minsize(1280, 720)
root.configure(bg='black')

# Global Variable
type_var = tk.StringVar()
amp_var = tk.IntVar()
sampleNum_var = tk.IntVar()
theta_var = tk.DoubleVar()
sampleFreq_var = tk.DoubleVar()
freq_var = tk.DoubleVar()
originalPoints = Wave("cos",1,0,1,1,1)

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

def generateClick():
    tempWave = Wave(type_var,amp_var,theta_var,sampleNum_var,sampleFreq_var,freq_var)
    originalPoints = utils.generatePoints(tempWave)
    for x in range(len(originalPoints)):
        print(f"{x}: {originalPoints[x]}")

def generateMenuClick():
    root.update()
    width = 0.5*root.winfo_width()
    height = 0.5*root.winfo_height()
    generateCanvas = tk.Canvas(root, width=width,height=height,highlightthickness=2,highlightbackground="green")
    generateCanvas.configure(bg="black")

    generateLabel = tk.Label(generateCanvas, text="Generate:", highlightthickness=2, highlightbackground="green")
    generateLabel.configure(fg="green", bg="black")
    generateLabel.place(relwidth=0.25, relheight=0.1, relx=0, rely=0)

    typeLabel = tk.Label(generateCanvas, text="Check for Cos():")
    typeLabel.configure(fg="green", bg="black")
    typeLabel.place(relwidth=0.2, relheight=0.1, relx=0.1, rely=0.1)

    typeCheck = tk.Checkbutton(generateCanvas, variable= type_var,onvalue="cos",offvalue="sin",bg="black")
    typeCheck.place(relwidth=0.1,relheight=0.1,relx=0.3,rely=0.1)


    ampLabel = tk.Label(generateCanvas, text="Amplitude:")
    ampLabel.configure(fg="green", bg="black")
    ampLabel.place(relwidth=0.2, relheight=0.1, relx=0.1, rely=0.2)

    ampEntry = tk.Entry(generateCanvas, textvariable=amp_var)
    ampEntry.place(relwidth=0.6, relheight=0.1, relx=0.3, rely=0.2)

    ampEntry = tk.Entry(generateCanvas, textvariable=amp_var)
    ampEntry.place(relwidth=0.6, relheight=0.1, relx=0.3, rely=0.2)

    sampleNumLabel = tk.Label(generateCanvas, text="Number of Samples:")
    sampleNumLabel.configure(fg="green", bg="black")
    sampleNumLabel.place(relwidth=0.2, relheight=0.1, relx=0.1, rely=0.3)

    sampleNumEntry = tk.Entry(generateCanvas, textvariable=sampleNum_var)
    sampleNumEntry.place(relwidth=0.6, relheight=0.1, relx=0.3, rely=0.3)

    thetaLabel = tk.Label(generateCanvas, text="Theta:")
    thetaLabel.configure(fg="green", bg="black")
    thetaLabel.place(relwidth=0.2, relheight=0.1, relx=0.1, rely=0.4)


    thetaEntry = tk.Entry(generateCanvas, textvariable=theta_var)
    thetaEntry.place(relwidth=0.6, relheight=0.1, relx=0.3, rely=0.4)


    sampleFreqLabel = tk.Label(generateCanvas, text="Sample Frequency:")
    sampleFreqLabel.configure(fg="green", bg="black")
    sampleFreqLabel.place(relwidth=0.2, relheight=0.1, relx=0.1, rely=0.5)

    sampFreqEntry = tk.Entry(generateCanvas, textvariable=sampleFreq_var)
    sampFreqEntry.place(relwidth=0.6, relheight=0.1, relx=0.3, rely=0.5)


    freqLabel = tk.Label(generateCanvas, text="Frequency:")
    freqLabel.configure(fg="green", bg="black")
    freqLabel.place(relwidth=0.2, relheight=0.1, relx=0.1, rely=0.6)


    freqEntry = tk.Entry(generateCanvas, textvariable=freq_var)
    freqEntry.place(relwidth=0.6, relheight=0.1, relx=0.3, rely=0.6)

    generateButtonBorder = tk.Frame(generateCanvas, bd=0, highlightthickness=2, highlightcolor="green", highlightbackground="green")
    generateButton = tk.Button(generateButtonBorder, text="Generate", command=generateClick, width='20')
    generateButton.configure(fg="green", bg="black", bd=0, borderwidth=0)
    generateButtonBorder.place(relwidth=0.2, relheight=0.2, relx=0.4, rely=0.8)
    generateButton.place(relwidth=1, relheight=1, relx=0, rely=0)
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
