import math
import tkinter as tk

from utils import Wave


def generatePoints(wave):
    points = []
    for x in range(wave.sampleNum):
        insideCos = 0;
        if(wave.type == "sin"):
            insideCos = 0
        elif (wave.type == "cos"):
            insideCos = math.cos(((2*math.pi*x*wave.freq)/wave.sampleFreq)+wave.theta)
        posY = wave.amp * insideCos
        points[x] = (x, posY)
    return points

def generateClick():
    wave = Wave()
    generatePoints(wave)

def createGenerateMenu(root, type_var, amp_var, sampleNum_var,theta_var, sampleFreq_var,freq_var ):
    root.update()
    width = 0.5*root.winfo_width()
    height = 0.5*root.winfo_height()
    generateCanvas = tk.Canvas(root, width=width,height=height,highlightthickness=2,highlightbackground="green")
    generateCanvas.configure(bg="black")

    generateLabel = tk.Label(generateCanvas, text="Generate:", highlightthickness=2, highlightbackground="green")
    generateLabel.configure(fg="green", bg="black")
    generateLabel.place(relwidth=0.25, relheight=0.1, relx=0, rely=0)

    typeLabel = tk.Label(generateCanvas, text="Type:")
    typeLabel.configure(fg="green", bg="black")
    typeLabel.place(relwidth=0.2, relheight=0.1, relx=0.1, rely=0.1)

    typeEntry = tk.Entry(generateCanvas, textvariable= type_var)
    typeEntry.place(relwidth=0.6,relheight=0.1,relx=0.3,rely=0.1)


    ampLabel = tk.Label(generateCanvas, text="Amplitude:")
    ampLabel.configure(fg="green", bg="black")
    ampLabel.place(relwidth=0.2, relheight=0.1, relx=0.1, rely=0.2)



    sampleNumLabel = tk.Label(generateCanvas, text="Number of Samples:")
    sampleNumLabel.configure(fg="green", bg="black")
    sampleNumLabel.place(relwidth=0.2, relheight=0.1, relx=0.1, rely=0.3)


    thetaLabel = tk.Label(generateCanvas, text="Theta:")
    thetaLabel.configure(fg="green", bg="black")
    thetaLabel.place(relwidth=0.2, relheight=0.1, relx=0.1, rely=0.4)


    sampleFreqLabel = tk.Label(generateCanvas, text="Sample Frequency:")
    sampleFreqLabel.configure(fg="green", bg="black")
    sampleFreqLabel.place(relwidth=0.2, relheight=0.1, relx=0.1, rely=0.5)


    freqLabel = tk.Label(generateCanvas, text="Frequency:")
    freqLabel.configure(fg="green", bg="black")
    freqLabel.place(relwidth=0.2, relheight=0.1, relx=0.1, rely=0.6)

    generateButtonBorder = tk.Frame(generateCanvas, bd=0, highlightthickness=2, highlightcolor="green", highlightbackground="green")
    generateButton = tk.Button(generateButtonBorder, text="Generate", command=generateClick, width='20')
    generateButton.configure(fg="green", bg="black", bd=0, borderwidth=0)
    generateButtonBorder.place(relwidth=0.2, relheight=0.2, relx=0.4, rely=0.8)
    generateButton.place(relwidth=1, relheight=1, relx=0, rely=0)

    return generateCanvas