# Library for GUI
import tkinter as tk
import matplotlib.pyplot as plt
from tkinter import filedialog
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Wave:
    def __init__(self, type, amp, theta, sampleNum, sampleFreq, freq):
        self.type = type
        self.amp = amp
        self.sampleNum = sampleNum
        self.theta = theta
        self.sampleFreq = sampleFreq
        self.freq = freq

def generatePoints(wave):
        points = [0]*wave.sampleNum.get()
        for x in range(wave.sampleNum.get()):
            insideCos = 0;
            if (wave.type.get() == "sin"):
                insideInsideCos = (2 * np.pi * x * wave.freq.get()) / wave.sampleFreq.get()
                insideCos = np.sin(insideInsideCos + np.radians(wave.theta.get()))
            else:
                insideInsideCos = (2 * np.pi * x * wave.freq.get()) / wave.sampleFreq.get()
                insideCos = np.cos(insideInsideCos + np.radians(wave.theta.get()))
            posY = wave.amp.get() * insideCos
            points[x] = posY
        return points

# Creating and defining Root Window
root = tk.Tk()
root.title("Digital Signal Processing")
root.iconbitmap("wave-sine.ico")
root.minsize(1280, 720)
root.configure(bg='black')

# Global Variable
type_var = tk.StringVar()
file_var = tk.StringVar()
amp_var = tk.IntVar()
sampleNum_var = tk.IntVar()
theta_var = tk.DoubleVar()
sampleFreq_var = tk.DoubleVar()
freq_var = tk.DoubleVar()
originalSignalType = 0
originalIsPeriodic = 0


originalPoints = Wave("cos",1,0,1,1,1)
originalWave = Wave("cos",1,0,1,1,1)
editedPoints = Wave("cos",1,0,1,1,1)
editedWave = Wave("cos",1,0,1,1,1)

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


def originalExportClick():
    print("export")

def importFromFile():
    if(file_var.get() != ""):
        file = open(file_var.get())
        originalSignalType = file.readline()
        print(f"Signal type: {originalSignalType}")
        originalIsPeriodic = file.readline()
        print(f"Periodic: {originalIsPeriodic}")
        sampleNum_var.set(file.readline())
        x_ax = [0]*sampleNum_var.get()
        originalPoints = [0]*sampleNum_var.get()
        for x in range(sampleNum_var.get()):
            temp = file.readline().split(" ")
            print(f"{temp[0]} and {temp[1]}")
            x_ax[x] = float(temp[0])
            originalPoints[x] = float(temp[1])
        y_ax = originalPoints
        fig, ax = plt.subplots()
        ax.plot(x_ax, y_ax)
        ax.set_title("Original Graph")
        ax.set_xlabel("Sample")
        ax.set_ylabel("Amplitude")
        originalGraph = FigureCanvasTkAgg(fig, master=originalWaveCanvas)
        originalGraph.draw()
        originalGraph.get_tk_widget().place(relwidth=1, relheight=0.9, relx=0, rely=0.1)
def browseClick():
    file_var.set(filedialog.askopenfilename(title="Select a txt File",filetypes=[("Text files","*.txt")]))

def importMenuClick():
    width = 0.5*root.winfo_width()
    height = 0.5*root.winfo_height()
    importCanvas = tk.Canvas(root, width=width,height=height,highlightthickness=2,highlightbackground="green")
    importCanvas.configure(bg="black")
    importLabel = tk.Label(importCanvas, text="Import:", highlightthickness=2, highlightbackground="green")
    importLabel.configure(fg="green", bg="black")
    importLabel.place(relwidth=0.25, relheight=0.1, relx=0, rely=0)

    fileLabel = tk.Label(importCanvas, text="File:")
    fileLabel.configure(fg="green", bg="black")
    fileLabel.place(relwidth=0.2, relheight=0.1, relx=0.05, rely=0.2)

    fileEntry = tk.Entry(importCanvas, textvariable=file_var)
    fileEntry.place(relwidth=0.6, relheight=0.1, relx=0.25, rely=0.2)

    browseButtonBorder = tk.Frame(importCanvas, bd=0, highlightthickness=2, highlightcolor="green", highlightbackground="green")
    browseButton = tk.Button(browseButtonBorder, text="Browse", command=browseClick, width='20')
    browseButton.configure(fg="green", bg="black", bd=0, borderwidth=0)
    browseButtonBorder.place(relwidth=0.1, relheight=0.1, relx=0.8, rely=0.2)
    browseButton.place(relwidth=1, relheight=1, relx=0, rely=0)

    importButtonBorder = tk.Frame(importCanvas, bd=0, highlightthickness=2, highlightcolor="green", highlightbackground="green")
    importButton = tk.Button(importButtonBorder, text="Import", command=importFromFile, width='20')
    importButton.configure(fg="green", bg="black", bd=0, borderwidth=0)
    importButtonBorder.place(relwidth=0.2, relheight=0.2, relx=0.4, rely=0.8)
    importButton.place(relwidth=1, relheight=1, relx=0, rely=0)
    importCanvas.place(relwidth = 0.5, relheight = 0.5,relx = 0, rely = 0.5)
    return importCanvas

def generateClick():
    originalWave = Wave(type_var,amp_var,theta_var,sampleNum_var,sampleFreq_var,freq_var)
    originalPoints = generatePoints(originalWave)
    x_ax = [0]*sampleNum_var.get()
    for x in range(sampleNum_var.get()):
        print(f"{x}: {originalPoints[x]}")
        x_ax[x] = x
    y_ax = originalPoints
    fig,ax = plt.subplots()
    ax.plot(x_ax,y_ax)
    ax.set_title("Original Graph")
    ax.set_xlabel("Sample")
    ax.set_ylabel("Amplitude")
    originalGraph = FigureCanvasTkAgg(fig, master = originalWaveCanvas)
    originalGraph.draw()
    originalGraph.get_tk_widget().place(relwidth = 1, relheight = 0.9,relx = 0, rely = 0.1)
def generateMenuClick():
    width = 0.5*root.winfo_width()
    height = 0.5*root.winfo_height()
    generateCanvas = tk.Canvas(root, width=width,height=height,highlightthickness=2,highlightbackground="green")
    generateCanvas.configure(bg="black")

    generateLabel = tk.Label(generateCanvas, text="Generate:", highlightthickness=2, highlightbackground="green")
    generateLabel.configure(fg="green", bg="black")
    generateLabel.place(relwidth=0.25, relheight=0.1, relx=0, rely=0)

    typeLabel = tk.Label(generateCanvas, text="Sin():")
    typeLabel.configure(fg="green", bg="black")
    typeLabel.place(relwidth=0.2, relheight=0.1, relx=0.1, rely=0.1)

    typeCheck = tk.Checkbutton(generateCanvas, variable= type_var,onvalue="sin",offvalue="cos",bg="black")
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

def editMenuClick():
    width = 0.5 * root.winfo_width()
    height = 0.5 * root.winfo_height()
    editCanvas = tk.Canvas(root, width=width, height=height, highlightthickness=2, highlightbackground="green")
    editCanvas.configure(bg="black")
    editLabel = tk.Label(editCanvas, text="Edit:", highlightthickness=2, highlightbackground="green")
    editLabel.configure(fg="green", bg="black")
    editLabel.place(relwidth=0.25, relheight=0.1, relx=0, rely=0)

    editCanvas.place(relwidth=0.5,relheight=0.5,relx=0,rely=0.5)

# Creating Label
menuName = tk.Label(menuCanvas, text="DSP - Section 1")
menuName.configure(fg="green", bg="black",highlightthickness=2,highlightbackground="green")

originalLabel = tk.Label(originalWaveCanvas, text="Original Wave:",highlightthickness=2,highlightbackground="green")
originalLabel.configure(fg="green", bg="black")

editedLabel = tk.Label(editedWaveCanvas, text="Edited Wave:",highlightthickness=2,highlightbackground="green")
editedLabel.configure(fg="green", bg="black")

# Creating Buttons
importButtonBorder = tk.Frame(menuCanvas, bd=0,highlightthickness=2,highlightcolor="green",highlightbackground="green")
importButton = tk.Button(importButtonBorder, text="Import", command=importMenuClick, width='20')
importButton.configure(fg="green", bg="black",bd=0, borderwidth=0)

generateButtonBorder = tk.Frame(menuCanvas, bd=0,highlightthickness=2,highlightcolor="green",highlightbackground="green")
generateButton = tk.Button(generateButtonBorder, text="Generate", command=generateMenuClick, width='20',)
generateButton.configure(fg="green", bg="black",bd=0, borderwidth=0)

exportOriginalButtonBorder = tk.Frame(originalWaveCanvas, bd=0,highlightthickness=2,highlightcolor="green",highlightbackground="green")
exportOriginalButton = tk.Button(exportOriginalButtonBorder, text="Export", command=originalExportClick, width='20')
exportOriginalButton.configure(fg="green", bg="black",bd=0, borderwidth=0)

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

exportOriginalButtonBorder.place(relwidth= 0.25,relheight=0.1,relx= 0.75, rely=0)
exportOriginalButton.place(relwidth=1,relheight=1,relx=0,rely=0)

editButtonBorder.place(relwidth= 0.25,relheight=0.25,relx= 0, rely=0.75)
editButton.place(relwidth=1,relheight=1,relx=0,rely=0)



root.mainloop()
