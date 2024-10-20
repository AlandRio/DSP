# Library for GUI
import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib import style
from tkinter import filedialog
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class Wave:  # class for wave used in generate
    def __init__(self, trigFunc="cos", amp=1, theta=0.0, sampleFreq=2.0,
                 freq=1.0):  # intializes class with default arguments
        self.trigFunc = trigFunc  # Wither the function is sin or cos
        self.amp = amp  # Amplitude
        self.theta = theta  # Phase shift
        self.sampleFreq = sampleFreq  # Sample Frequency
        self.freq = freq  # Frequency


class Points:  # class for storing points
    def __init__(self, x_points=range(40), y_points=[0] * 40, signalType=0, isPeriodic=1,
                 samples=40):  # intializes class with default arguments
        self.x_points = x_points  # Points on the X-Axis
        self.y_points = y_points  # Points on the Y-Axis
        self.signalType = signalType  # Wither the signal is Time (0) or Frequency (1)
        self.isPeriodic = isPeriodic  # Wither the signal is Non-Periodic (0) or Periodic (1)
        self.samples = samples


# Creating and defining Root Window for the app
root = tk.Tk()
root.title("Digital Signal Processing")
root.minsize(1280, 720)
root.configure(bg='black')

# Changes the style of the graph to have a dark background
plt.style.use("dark_background")

# Defining Global tk Variables
# Useful for dynamic variable that can be changed by user (used with setters and taken with getters)
type_var = tk.StringVar()
file_var = tk.StringVar()
amp_var = tk.IntVar()
startingPos_var = tk.IntVar()
theta_var = tk.DoubleVar()
sampleFreq_var = tk.DoubleVar()
freq_var = tk.DoubleVar()
originalFunctionString = tk.StringVar()
line_var = tk.StringVar()

# Defining Global Objects for Original Graph and Edited Graph
originalPoints = Points()
originalWave = Wave()
editedPoints = Points()
editedWave = Wave()
postEditPoints = Points()

# Creating Canvases then configuring its background then placing it on the window
menuCanvas = tk.Canvas(root, width=640, height=360, highlightthickness=2, highlightbackground="green")
menuCanvas.configure(bg="black")
menuCanvas.place(relwidth=0.5, relheight=0.5, relx=0, rely=0)

originalWaveCanvas = tk.Canvas(root, width=640, height=360, highlightthickness=2, highlightbackground="green")
originalWaveCanvas.configure(bg="black")
originalWaveCanvas.place(relwidth=0.5, relheight=0.5, relx=0.5, rely=0)

editedWaveCanvas = tk.Canvas(root, width=640, height=360, highlightthickness=2, highlightbackground="green")
editedWaveCanvas.configure(bg="black")
editedWaveCanvas.place(relwidth=0.5, relheight=0.5, relx=0.5, rely=0.5)


# Placeholder function for exporting (not task 2)
def originalExportClick():
    print("export")


def importFile():
    if (file_var.get() != ""):  # so the user can not give an empty path
        tempPoints = Points()
        # Opens file using the path user gave
        file = open(file_var.get())
        # takes the 1st line of the file which is SignalType
        originalSignalType = bool(file.readline())
        print(f"Signal type: {originalSignalType}")  # Prints for debugging purposes
        # takes the 2nd line of the file which is isPeriodic
        originalIsPeriodic = bool(file.readline())
        print(f"Periodic: {originalIsPeriodic}")  # Prints for debugging purposes
        # takes the 3rd line of the file which is number of samples
        samples = int(file.readline())
        x_ax = [0] * samples  # initializes an empty array with size samples
        y_ax = [0] * samples  # initializes an empty array with size samples
        i = 0  # variable used in the while loop incase loop does not find starting position
        for x in range(samples):
            temp = file.readline().split(" ")
            print(f"{temp[0]} and {temp[1]}")
            x_ax[x] = float(temp[0])
            y_ax[x] = float(temp[1])
        tempPoints.y_points = y_ax  # puts y-axis points inside the global original points variable
        tempPoints.x_points = x_ax  # puts x axis points inside the global original points variable
        tempPoints.isPeriodic = originalIsPeriodic  # puts periodic flag inside the global original points variable
        tempPoints.signalType = originalSignalType  # puts signaltype flag inside the global original points variable
        tempPoints.samples = samples
        return tempPoints


def importFromFile():
    originalFunctionString.set(f"Imported from file")  # changes the variable on top of the original graph

    # Creates a label to put on top of the graph using the originalFunctionString variable
    # and places it on originalWave Canvas
    originalFunctionLabel = tk.Label(originalWaveCanvas, text=originalFunctionString.get(), highlightthickness=2,
                                     highlightbackground="green")
    originalFunctionLabel.configure(fg="green", bg="black")
    originalFunctionLabel.place(relwidth=0.5, relheight=0.1, relx=0.25, rely=0)

    global originalPoints
    originalPoints = importFile()
    samplesShown = 0
    if (originalPoints.x_points[0] > startingPos_var.get() or originalPoints.x_points[
        originalPoints.samples - 1] > startingPos_var.get()):
        if (originalPoints.samples - abs(startingPos_var.get()) < 40):
            samplesShown = originalPoints.samples - abs(startingPos_var.get())
        else:
            samplesShown = 40
    shownPoints_X = [0] * samplesShown
    shownPoints_Y = [0] * samplesShown
    i = 0
    if startingPos_var.get() >= min(originalPoints.x_points) or startingPos_var.get() < max(originalPoints.x_points):
        i = originalPoints.x_points.index(startingPos_var.get())
    for x in range(40):
        try:
            shownPoints_X[x] = originalPoints.x_points[i + x]
            shownPoints_Y[x] = originalPoints.y_points[i + x]
        except:
            break

    fig, ax = plt.subplots()
    # takes X axis points and Y axis points and plots them on a graph with a darkgreen line
    ax.plot(shownPoints_X, shownPoints_Y, color="darkgreen")
    ax.set_title("Original Graph")  # Self-explanatory
    if originalPoints.signalType == 1:  # if the signal type is 1 will replace time with frequency on the x axis
        ax.set_xlabel("Frequency")
    else:  # else if its 0 then will label x as time
        ax.set_xlabel("Sample")
    ax.set_ylabel("Amplitude")  # labels y as amplitude

    # Creates graph on originalWave Canvas and draws then places it
    originalGraph = FigureCanvasTkAgg(fig, master=originalWaveCanvas)
    originalGraph.draw()
    originalGraph.get_tk_widget().place(relwidth=1, relheight=0.9, relx=0, rely=0.1)


def browseClick():
    # Opens the browse menu and specifies that only text files can be taken
    file_var.set(filedialog.askopenfilename(title="Select a txt File", filetypes=[("Text files", "*.txt")]))


def importMenuClick():
    startingPos_var.set(0)  # intitializes the value incase use does not provide it
    width = 0.5 * root.winfo_width()  # gets half the width of the window
    height = 0.5 * root.winfo_height()  # gets half the height of the window

    # creates the canvas and adds it to import canvas
    importCanvas = tk.Canvas(root, width=width, height=height, highlightthickness=2, highlightbackground="green")
    importCanvas.configure(bg="black")
    importLabel = tk.Label(importCanvas, text="Import:", highlightthickness=2, highlightbackground="green")

    # creates the corner label for the tab
    importLabel.configure(fg="green", bg="black")
    importLabel.place(relwidth=0.25, relheight=0.1, relx=0, rely=0)

    # creates a label for the note
    noteLabel = tk.Label(importCanvas, text="Starting Pos only works within the range of X")
    noteLabel.configure(fg="green", bg="black")
    noteLabel.place(relwidth=0.6, relheight=0.1, relx=0.25, rely=0.1)

    # creates a label beside the file input
    fileLabel = tk.Label(importCanvas, text="File:")
    fileLabel.configure(fg="green", bg="black")
    fileLabel.place(relwidth=0.2, relheight=0.1, relx=0.05, rely=0.2)

    # creates an input field for the file path which is stored in file_var
    fileEntry = tk.Entry(importCanvas, textvariable=file_var)
    fileEntry.place(relwidth=0.6, relheight=0.1, relx=0.25, rely=0.2)

    # creates a label for starting position input
    startingPosLabel = tk.Label(importCanvas, text="Starting Pos:")
    startingPosLabel.configure(fg="green", bg="black")
    startingPosLabel.place(relwidth=0.2, relheight=0.1, relx=0.05, rely=0.3)

    # creates an input field for the starting entry
    startingPosEntry = tk.Entry(importCanvas, textvariable=startingPos_var)
    startingPosEntry.place(relwidth=0.65, relheight=0.1, relx=0.25, rely=0.3)

    # creates a frame to put the button in (to get the border)
    browseButtonBorder = tk.Frame(importCanvas, bd=0, highlightthickness=2, highlightcolor="green",
                                  highlightbackground="green")
    # creates a button that calls browseClick function when pressed
    browseButton = tk.Button(browseButtonBorder, text="Browse", command=browseClick, width='20')
    browseButton.configure(fg="green", bg="black", bd=0, borderwidth=0)
    # places both the frame and button
    browseButtonBorder.place(relwidth=0.1, relheight=0.1, relx=0.8, rely=0.2)
    browseButton.place(relwidth=1, relheight=1, relx=0, rely=0)

    # same as above
    importButtonBorder = tk.Frame(importCanvas, bd=0, highlightthickness=2, highlightcolor="green",
                                  highlightbackground="green")
    importButton = tk.Button(importButtonBorder, text="Import", command=importFromFile, width='20')
    importButton.configure(fg="green", bg="black", bd=0, borderwidth=0)
    importButtonBorder.place(relwidth=0.2, relheight=0.1, relx=0.4, rely=0.9)
    importButton.place(relwidth=1, relheight=1, relx=0, rely=0)
    importCanvas.place(relwidth=0.5, relheight=0.5, relx=0, rely=0.5)


def generatePoints(wave, startingPos):
    pointsX = [0] * 40  # initializes an array of 40 indexes
    pointsY = [0] * 40  # initializes an array of 40 indexes
    for x in range(40):
        insideCos = 0  # function for the value inside the Cos or Sin
        if wave.trigFunc == "sin":  # if trigFunc is sin will use the sin version of the equation
            insideInsideCos = (2 * np.pi * startingPos * wave.freq) / wave.sampleFreq
            insideCos = np.sin(
                insideInsideCos + np.radians(wave.theta))  # splitting up the function to make it easier to read
        elif wave.trigFunc == "cos":  # if trigFunc is sin will use the sin version of the equation
            insideInsideCos = (2 * np.pi * startingPos * wave.freq) / wave.sampleFreq
            insideCos = np.cos(
                insideInsideCos + np.radians(wave.theta))  # splitting up the function to make it easier to read
        posY = wave.amp * insideCos  # Multiplies amplitude by the
        pointsY[x] = posY  # adds the point at Y to the array to the y axis
        pointsX[x] = startingPos  # adds the starting point to the x axis
        startingPos += 1  # increment starting point by 1
    points = Points(pointsX, pointsY)  # adds the values into a class for easier management
    return points  # returns an array of points for graph


def generateClick():
    # changes the label variable on top of the graph based on wither its sin or cos purely for cosmetic reasons
    if type_var.get() == "sin":
        originalFunctionString.set(
            f"{amp_var.get()} * Sin(((2π*{freq_var.get()})/{sampleFreq_var.get()})+{theta_var.get()})")
    else:
        originalFunctionString.set(
            f"{amp_var.get()} * Cos(((2π*{freq_var.get()})/{sampleFreq_var.get()})+{theta_var.get()})")
    # makes a label with the label variable
    originalFunctionLabel = tk.Label(originalWaveCanvas, text=originalFunctionString.get(), highlightthickness=2,
                                     highlightbackground="green")
    originalFunctionLabel.configure(fg="green", bg="black")
    originalFunctionLabel.place(relwidth=0.5, relheight=0.1, relx=0.25, rely=0)

    # using the input the user gave in generate function changes the global original wave object
    global originalWave
    originalWave = Wave(type_var.get(), amp_var.get(), theta_var.get(), sampleFreq_var.get(), freq_var.get())
    # calls the generate points function and puts the points generated into global original wave points
    global originalPoints
    originalPoints = generatePoints(originalWave, startingPos_var.get())
    fig, ax = plt.subplots()  # creates a figure in fig and sub-plots in ax
    # plots the graph using the original points object
    ax.plot(originalPoints.x_points, originalPoints.y_points, color="darkgreen")
    ax.set_title("Original Graph")
    ax.set_xlabel("Sample")
    ax.set_ylabel("Amplitude")
    # creates a graph gui in original wave canvas then draws the graph and places it
    originalGraph = FigureCanvasTkAgg(fig, master=originalWaveCanvas)
    originalGraph.draw()
    originalGraph.get_tk_widget().place(relwidth=1, relheight=0.9, relx=0, rely=0.1)


def generateMenuClick():
    type_var.set("cos")  # initializes type variable as cos for default incase user does not press
    width = 0.5 * root.winfo_width()  # gets the size of the window
    height = 0.5 * root.winfo_height()  # gets the size of the window

    # creates a canvas for the generate menu
    generateCanvas = tk.Canvas(root, width=width, height=height, highlightthickness=2, highlightbackground="green")
    generateCanvas.configure(bg="black")

    # creates the corner generate label
    generateLabel = tk.Label(generateCanvas, text="Generate:", highlightthickness=2, highlightbackground="green")
    generateLabel.configure(fg="green", bg="black")
    generateLabel.place(relwidth=0.25, relheight=0.1, relx=0, rely=0)

    # Creates a label for a variable then its input from the user
    typeLabel = tk.Label(generateCanvas, text="Sin():")
    typeLabel.configure(fg="green", bg="black")
    typeLabel.place(relwidth=0.2, relheight=0.1, relx=0.1, rely=0.1)

    typeCheck = tk.Checkbutton(generateCanvas, variable=type_var, onvalue="sin", offvalue="cos", bg="black")
    typeCheck.place(relwidth=0.1, relheight=0.1, relx=0.3, rely=0.1)

    ampLabel = tk.Label(generateCanvas, text="Amplitude:")
    ampLabel.configure(fg="green", bg="black")
    ampLabel.place(relwidth=0.2, relheight=0.1, relx=0.1, rely=0.2)

    ampEntry = tk.Entry(generateCanvas, textvariable=amp_var)
    ampEntry.place(relwidth=0.6, relheight=0.1, relx=0.3, rely=0.2)

    ampEntry = tk.Entry(generateCanvas, textvariable=amp_var)
    ampEntry.place(relwidth=0.6, relheight=0.1, relx=0.3, rely=0.2)

    startingPosLabel = tk.Label(generateCanvas, text="Starting Pos:")
    startingPosLabel.configure(fg="green", bg="black")
    startingPosLabel.place(relwidth=0.2, relheight=0.1, relx=0.1, rely=0.3)

    startingPosEntry = tk.Entry(generateCanvas, textvariable=startingPos_var)
    startingPosEntry.place(relwidth=0.6, relheight=0.1, relx=0.3, rely=0.3)

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

    # creates the generate button and its frame
    generateButtonBorder = tk.Frame(generateCanvas, bd=0, highlightthickness=2, highlightcolor="green",
                                    highlightbackground="green")
    generateButton = tk.Button(generateButtonBorder, text="Generate", command=generateClick, width='20')
    generateButton.configure(fg="green", bg="black", bd=0, borderwidth=0)
    generateButtonBorder.place(relwidth=0.2, relheight=0.1, relx=0.4, rely=0.9)
    generateButton.place(relwidth=1, relheight=1, relx=0, rely=0)
    # places the canvas
    generateCanvas.place(relwidth=0.5, relheight=0.5, relx=0, rely=0.5)


def generateEditedWaveClick():
    global editedPoints
    global editedWave
    editedWave = Wave(type_var.get(), amp_var.get(), theta_var.get(), sampleFreq_var.get(), freq_var.get())
    editedPoints = generatePoints(editedWave, startingPos_var.get())


def addImportWaveClick():
    global editedPoints
    editedPoints = importFile()


def addSubEditWave(type="add"):
    global editedPoints
    global originalPoints
    global postEditPoints
    minimum_point = min(min(editedPoints.x_points), min(originalPoints.x_points))
    maximum_point = max(max(editedPoints.x_points), max(originalPoints.x_points))
    total_samples = int(maximum_point - minimum_point) + 1
    print(f"total: {total_samples}")
    postEditPoints.x_points = [0] * total_samples
    postEditPoints.y_points = [0] * total_samples
    i = minimum_point
    x = 0
    z = 0
    while i <= maximum_point:
        flag_found = 0
        for y in range(total_samples):
            try:
                if editedPoints.x_points[z] == i:
                    if originalPoints.x_points[y] == i:
                        if type == "add":
                            postEditPoints.x_points[x] = int(editedPoints.x_points[z])
                            postEditPoints.y_points[x] = editedPoints.y_points[z] + originalPoints.y_points[y]
                            flag_found = 1
                        elif type == "sub":
                            postEditPoints.x_points[x] = int(editedPoints.x_points[z])
                            postEditPoints.y_points[x] = editedPoints.y_points[z] - originalPoints.y_points[y]
                            flag_found = 1
                elif originalPoints.x_points[y] == i:
                    postEditPoints.x_points[x] = int(originalPoints.x_points[y])
                    postEditPoints.y_points[x] = originalPoints.y_points[y]
                    flag_found = 1
            except IndexError:
                break
        try:
            if flag_found == 0:
                if editedPoints.x_points[x] == i:
                    postEditPoints.x_points[x] = int(editedPoints.x_points[z])
                    postEditPoints.y_points[x] = editedPoints.y_points[z]
            print(f"{postEditPoints.x_points[x]} and {postEditPoints.y_points[x]}")
        except IndexError:
            break
        z = z + 1
        if z > editedPoints.samples:
            z = 0
        x = x + 1
        i = i + 1
    shown_samples = 0
    if maximum_point - shown_samples < 40:
        shown_samples = maximum_point - shown_samples
    else:
        shown_samples = 40
    shownPoints_X = [0] * shown_samples
    shownPoints_Y = [0] * shown_samples

    i = 0
    if startingPos_var.get() >= min(postEditPoints.x_points) or startingPos_var.get() < max(postEditPoints.x_points):
        i = postEditPoints.x_points.index(startingPos_var.get())
    for x in range(40):
        try:
            shownPoints_X[x] = postEditPoints.x_points[i + x]
            shownPoints_Y[x] = postEditPoints.y_points[i + x]
        except IndexError:
            break
    fig, ax = plt.subplots()
    ax.plot(shownPoints_X, shownPoints_Y, color="darkgreen")
    ax.set_title("Edited Wave")
    ax.set_xlabel("Sample")
    ax.set_ylabel("Amplitude")
    editedGraph = FigureCanvasTkAgg(fig, master=editedWaveCanvas)
    editedGraph.draw()
    editedGraph.get_tk_widget().place(relwidth=1, relheight=0.9, relx=0, rely=0.1)
    return


def addWaveClick():
    addSubEditWave("add")
    return


def subWaveClick():
    addSubEditWave("sub")
    return


def editAddClick():
    type_var.set("cos")
    editAddCanvas = tk.Canvas(root, bg="black", highlightthickness=2, highlightcolor="green",
                              highlightbackground="green")

    addLabel = tk.Label(editAddCanvas, text="Add/Sub:", highlightthickness=2, highlightbackground="green")
    addLabel.configure(fg="green", bg="black")
    addLabel.place(relwidth=0.25, relheight=0.1, relx=0, rely=0)

    # Creates a label for a variable then its input from the user
    typeLabel = tk.Label(editAddCanvas, text="Sin():")
    typeLabel.configure(fg="green", bg="black")
    typeLabel.place(relwidth=0.2, relheight=0.1, relx=0.05, rely=0.2)

    typeCheck = tk.Checkbutton(editAddCanvas, variable=type_var, onvalue="sin", offvalue="cos", bg="black")
    typeCheck.place(relwidth=0.1, relheight=0.1, relx=0.25, rely=0.2)

    posLabel = tk.Label(editAddCanvas, text="Starting Pos:")
    posLabel.configure(fg="green", bg="black")
    posLabel.place(relwidth=0.2, relheight=0.1, relx=0.25, rely=0.1)

    posEntry = tk.Entry(editAddCanvas, textvariable=startingPos_var)
    posEntry.place(relwidth=0.2, relheight=0.1, relx=0.45, rely=0.1)

    ampLabel = tk.Label(editAddCanvas, text="Amplitude:")
    ampLabel.configure(fg="green", bg="black")
    ampLabel.place(relwidth=0.2, relheight=0.1, relx=0.05, rely=0.3)

    ampEntry = tk.Entry(editAddCanvas, textvariable=amp_var)
    ampEntry.place(relwidth=0.2, relheight=0.1, relx=0.25, rely=0.3)

    thetaLabel = tk.Label(editAddCanvas, text="Theta:")
    thetaLabel.configure(fg="green", bg="black")
    thetaLabel.place(relwidth=0.2, relheight=0.1, relx=0.05, rely=0.4)

    thetaEntry = tk.Entry(editAddCanvas, textvariable=theta_var)
    thetaEntry.place(relwidth=0.2, relheight=0.1, relx=0.25, rely=0.4)

    sampleFreqLabel = tk.Label(editAddCanvas, text="Sample Frequency:")
    sampleFreqLabel.configure(fg="green", bg="black")
    sampleFreqLabel.place(relwidth=0.2, relheight=0.1, relx=0.05, rely=0.5)

    sampFreqEntry = tk.Entry(editAddCanvas, textvariable=sampleFreq_var)
    sampFreqEntry.place(relwidth=0.2, relheight=0.1, relx=0.25, rely=0.5)

    freqLabel = tk.Label(editAddCanvas, text="Frequency:")
    freqLabel.configure(fg="green", bg="black")
    freqLabel.place(relwidth=0.2, relheight=0.1, relx=0.05, rely=0.6)

    freqEntry = tk.Entry(editAddCanvas, textvariable=freq_var)
    freqEntry.place(relwidth=0.2, relheight=0.1, relx=0.25, rely=0.6)

    browseLabel = tk.Label(editAddCanvas, text="File Path:")
    browseLabel.configure(fg="green", bg="black")
    browseLabel.place(relwidth=0.2, relheight=0.1, relx=0.6, rely=0.3)

    browseEntry = tk.Entry(editAddCanvas, textvariable=file_var)
    browseEntry.place(relwidth=0.4, relheight=0.1, relx=0.5, rely=0.4)

    # buttons
    browseWaveButtonBorder = tk.Frame(editAddCanvas, bd=0, highlightthickness=2, highlightcolor="green",
                                      highlightbackground="green")
    browseWaveButton = tk.Button(browseWaveButtonBorder, text="Browse", command=browseClick, width='20')
    browseWaveButton.configure(fg="green", bg="black", bd=0, borderwidth=0)
    browseWaveButtonBorder.place(relwidth=0.2, relheight=0.1, relx=0.6, rely=0.6)
    browseWaveButton.place(relwidth=1, relheight=1, relx=0, rely=0)

    generateWaveButtonBorder = tk.Frame(editAddCanvas, bd=0, highlightthickness=2, highlightcolor="green",
                                        highlightbackground="green")
    generateWaveButton = tk.Button(generateWaveButtonBorder, text="Generate", command=generateEditedWaveClick,
                                   width='20')
    generateWaveButton.configure(fg="green", bg="black", bd=0, borderwidth=0)
    generateWaveButtonBorder.place(relwidth=0.2, relheight=0.1, relx=0.25, rely=0.75)
    generateWaveButton.place(relwidth=1, relheight=1, relx=0, rely=0)

    importWaveButtonBorder = tk.Frame(editAddCanvas, bd=0, highlightthickness=2, highlightcolor="green",
                                      highlightbackground="green")
    importWaveButton = tk.Button(importWaveButtonBorder, text="Import", command=addImportWaveClick, width='20')
    importWaveButton.configure(fg="green", bg="black", bd=0, borderwidth=0)
    importWaveButtonBorder.place(relwidth=0.2, relheight=0.1, relx=0.6, rely=0.75)
    importWaveButton.place(relwidth=1, relheight=1, relx=0, rely=0)

    addWaveButtonBorder = tk.Frame(editAddCanvas, bd=0, highlightthickness=2, highlightcolor="green",
                                   highlightbackground="green")
    addWaveButton = tk.Button(addWaveButtonBorder, text="Add", command=addWaveClick, width='20')
    addWaveButton.configure(fg="green", bg="black", bd=0, borderwidth=0)
    addWaveButtonBorder.place(relwidth=0.2, relheight=0.1, relx=0.6, rely=0.9)
    addWaveButton.place(relwidth=1, relheight=1, relx=0, rely=0)

    subWaveButtonBorder = tk.Frame(editAddCanvas, bd=0, highlightthickness=2, highlightcolor="green",
                                   highlightbackground="green")
    subWaveButton = tk.Button(subWaveButtonBorder, text="Subtract", command=subWaveClick, width='20')
    subWaveButton.configure(fg="green", bg="black", bd=0, borderwidth=0)
    subWaveButtonBorder.place(relwidth=0.2, relheight=0.1, relx=0.25, rely=0.9)
    subWaveButton.place(relwidth=1, relheight=1, relx=0, rely=0)

    # placing canvas
    editAddCanvas.place(relwidth=0.5, relheight=0.45, relx=0, rely=0.55)
    return

def mulClick():
    global postEditPoints
    postEditPoints.samples = len(originalPoints.x_points)
    postEditPoints.x_points = [0] * postEditPoints.samples
    postEditPoints.y_points = [0] * postEditPoints.samples
    for x in range(postEditPoints.samples):
        postEditPoints.x_points[x] = (originalPoints.x_points[x])
        postEditPoints.y_points[x] = (originalPoints.y_points[x] * amp_var.get())
    shownPoints_X = [0] * 40
    shownPoints_Y = [0] * 40
    i = 0
    if startingPos_var.get() >= min(postEditPoints.x_points) or startingPos_var.get() < max(postEditPoints.x_points):
        i = postEditPoints.x_points.index(startingPos_var.get())
    for x in range(40):
        try:
            shownPoints_X[x] = postEditPoints.x_points[i + x]
            shownPoints_Y[x] = postEditPoints.y_points[i + x]
        except IndexError:
            break
    fig, ax = plt.subplots()
    ax.plot(shownPoints_X, shownPoints_Y, color="darkgreen")
    ax.set_title("Edited Wave")
    ax.set_xlabel("Sample")
    ax.set_ylabel("Amplitude")
    editedGraph = FigureCanvasTkAgg(fig, master=editedWaveCanvas)
    editedGraph.draw()
    editedGraph.get_tk_widget().place(relwidth=1, relheight=0.9, relx=0, rely=0.1)
    return
def editMulClick():
    editMulCanvas = tk.Canvas(root, bg="black", highlightthickness=2, highlightcolor="green",
                              highlightbackground="green")

    mulLabel = tk.Label(editMulCanvas, text="Multiply:", highlightthickness=2, highlightbackground="green")
    mulLabel.configure(fg="green", bg="black")
    mulLabel.place(relwidth=0.25, relheight=0.1, relx=0, rely=0)

    ampLabel = tk.Label(editMulCanvas, text="Multiply by:")
    ampLabel.configure(fg="green", bg="black")
    ampLabel.place(relwidth=0.2, relheight=0.1, relx=0.05, rely=0.4)

    ampEntry = tk.Entry(editMulCanvas, textvariable=amp_var)
    ampEntry.place(relwidth=0.2, relheight=0.1, relx=0.25, rely=0.4)

    posLabel = tk.Label(editMulCanvas, text="Starting Pos:")
    posLabel.configure(fg="green", bg="black")
    posLabel.place(relwidth=0.2, relheight=0.1, relx=0.05, rely=0.3)

    posEntry = tk.Entry(editMulCanvas, textvariable=startingPos_var)
    posEntry.place(relwidth=0.2, relheight=0.1, relx=0.25, rely=0.3)

    mulWaveButtonBorder = tk.Frame(editMulCanvas, bd=0, highlightthickness=2, highlightcolor="green",
                                   highlightbackground="green")
    mulWaveButton = tk.Button(mulWaveButtonBorder, text="MULTIPLY", command=mulClick, width='20')
    mulWaveButton.configure(fg="green", bg="black", bd=0, borderwidth=0)
    mulWaveButtonBorder.place(relwidth=0.2, relheight=0.2, relx=0.4, rely=0.6)
    mulWaveButton.place(relwidth=1, relheight=1, relx=0, rely=0)

    editMulCanvas.place(relwidth=0.5, relheight=0.45, relx=0, rely=0.55)
    return

def sqrClick():
    global postEditPoints
    postEditPoints.samples = len(originalPoints.x_points)
    postEditPoints.x_points = [0] * postEditPoints.samples
    postEditPoints.y_points = [0] * postEditPoints.samples
    for x in range(postEditPoints.samples):
        postEditPoints.x_points[x] = (originalPoints.x_points[x])
        postEditPoints.y_points[x] = (originalPoints.y_points[x] * originalPoints.y_points[x])
    shownPoints_X = [0] * 40
    shownPoints_Y = [0] * 40
    i = 0
    if startingPos_var.get() >= min(postEditPoints.x_points) or startingPos_var.get() < max(postEditPoints.x_points):
        i = postEditPoints.x_points.index(startingPos_var.get())
    for x in range(40):
        try:
            shownPoints_X[x] = postEditPoints.x_points[i + x]
            shownPoints_Y[x] = postEditPoints.y_points[i + x]
        except IndexError:
            break
    fig, ax = plt.subplots()
    ax.plot(shownPoints_X, shownPoints_Y, color="darkgreen")
    ax.set_title("Edited Wave")
    ax.set_xlabel("Sample")
    ax.set_ylabel("Amplitude")
    editedGraph = FigureCanvasTkAgg(fig, master=editedWaveCanvas)
    editedGraph.draw()
    editedGraph.get_tk_widget().place(relwidth=1, relheight=0.9, relx=0, rely=0.1)
    return
def editSqrClick():
    editSqrCanvas = tk.Canvas(root, bg="black", highlightthickness=2, highlightcolor="green",
                              highlightbackground="green")

    sqrLabel = tk.Label(editSqrCanvas, text="Square:", highlightthickness=2, highlightbackground="green")
    sqrLabel.configure(fg="green", bg="black")
    sqrLabel.place(relwidth=0.25, relheight=0.1, relx=0, rely=0)

    posLabel = tk.Label(editSqrCanvas, text="Starting Pos:")
    posLabel.configure(fg="green", bg="black")
    posLabel.place(relwidth=0.2, relheight=0.1, relx=0.05, rely=0.3)

    posEntry = tk.Entry(editSqrCanvas, textvariable=startingPos_var)

    posEntry.place(relwidth=0.2, relheight=0.1, relx=0.25, rely=0.3)

    sqrWaveButtonBorder = tk.Frame(editSqrCanvas, bd=0, highlightthickness=2, highlightcolor="green",
                                   highlightbackground="green")
    sqrWaveButton = tk.Button(sqrWaveButtonBorder, text="SQUARE", command=sqrClick, width='20')
    sqrWaveButton.configure(fg="green", bg="black", bd=0, borderwidth=0)
    sqrWaveButtonBorder.place(relwidth=0.2, relheight=0.2, relx=0.4, rely=0.6)
    sqrWaveButton.place(relwidth=1, relheight=1, relx=0, rely=0)

    editSqrCanvas.place(relwidth=0.5, relheight=0.45, relx=0, rely=0.55)
    return

def normClick():
    return
def editNormClick():
    editNormCanvas = tk.Canvas(root, bg="black", highlightthickness=2, highlightcolor="green",
                               highlightbackground="green")

    normLabel = tk.Label(editNormCanvas, text="Normalize:", highlightthickness=2, highlightbackground="green")
    normLabel.configure(fg="green", bg="black")
    normLabel.place(relwidth=0.25, relheight=0.1, relx=0, rely=0)


    editNormCanvas.place(relwidth=0.5, relheight=0.45, relx=0, rely=0.55)
    return

def sumClick():
    global postEditPoints
    postEditPoints.samples = len(originalPoints.x_points)
    postEditPoints.x_points = [0] * postEditPoints.samples
    postEditPoints.y_points = [0] * postEditPoints.samples
    sum = 0
    for x in range(postEditPoints.samples):
        postEditPoints.x_points[x] = (originalPoints.x_points[x])
        sum = sum + originalPoints.y_points[x]
        postEditPoints.y_points[x] = sum
    shownPoints_X = [0] * 40
    shownPoints_Y = [0] * 40
    i = 0
    if startingPos_var.get() >= min(postEditPoints.x_points) or startingPos_var.get() < max(postEditPoints.x_points):
        i = postEditPoints.x_points.index(startingPos_var.get())
    for x in range(40):
        try:
            shownPoints_X[x] = postEditPoints.x_points[i + x]
            shownPoints_Y[x] = postEditPoints.y_points[i + x]
        except IndexError:
            break
    fig, ax = plt.subplots()
    ax.plot(shownPoints_X, shownPoints_Y, color="darkgreen")
    ax.set_title("Edited Wave")
    ax.set_xlabel("Sample")
    ax.set_ylabel("Amplitude")
    editedGraph = FigureCanvasTkAgg(fig, master=editedWaveCanvas)
    editedGraph.draw()
    editedGraph.get_tk_widget().place(relwidth=1, relheight=0.9, relx=0, rely=0.1)
    return
def editSumClick():
    editSumCanvas = tk.Canvas(root, bg="black", highlightthickness=2, highlightcolor="green",
                              highlightbackground="green")

    sumLabel = tk.Label(editSumCanvas, text="Accumulate:", highlightthickness=2, highlightbackground="green")
    sumLabel.configure(fg="green", bg="black")
    sumLabel.place(relwidth=0.25, relheight=0.1, relx=0, rely=0)

    posLabel = tk.Label(editSumCanvas, text="Starting Pos:")
    posLabel.configure(fg="green", bg="black")
    posLabel.place(relwidth=0.2, relheight=0.1, relx=0.05, rely=0.3)

    posEntry = tk.Entry(editSumCanvas, textvariable=startingPos_var)

    posEntry.place(relwidth=0.2, relheight=0.1, relx=0.25, rely=0.3)

    sumWaveButtonBorder = tk.Frame(editSumCanvas, bd=0, highlightthickness=2, highlightcolor="green",
                                   highlightbackground="green")
    sumWaveButton = tk.Button(sumWaveButtonBorder, text="ACCUMULATE", command=sumClick, width='20')
    sumWaveButton.configure(fg="green", bg="black", bd=0, borderwidth=0)
    sumWaveButtonBorder.place(relwidth=0.2, relheight=0.2, relx=0.4, rely=0.6)
    sumWaveButton.place(relwidth=1, relheight=1, relx=0, rely=0)

    editSumCanvas.place(relwidth=0.5, relheight=0.45, relx=0, rely=0.55)
    return


def editMenuClick():
    width = 0.5 * root.winfo_width()  # gets size of window
    height = 0.5 * root.winfo_height()  # gets size of window
    # creates a canvas for edit menu
    editCanvas = tk.Canvas(root, width=width, height=height, highlightthickness=2, highlightbackground="green")
    editCanvas.configure(bg="black")
    # creates a label on the corner for edit
    editLabel = tk.Label(editCanvas, text="Edit:", highlightthickness=2, highlightbackground="green")
    editLabel.configure(fg="green", bg="black")
    editLabel.place(relwidth=0.25, relheight=0.1, relx=0, rely=0)

    # Buttons for edit menu
    addWaveButtonBorder = tk.Frame(editCanvas, bd=0, highlightthickness=2, highlightcolor="green",
                                   highlightbackground="green")
    addWaveButton = tk.Button(addWaveButtonBorder, text="Add/Sub", command=editAddClick, width='20')
    addWaveButton.configure(fg="green", bg="black", bd=0, borderwidth=0)
    addWaveButtonBorder.place(relwidth=0.2, relheight=0.1, relx=0.3, rely=0)
    addWaveButton.place(relwidth=1, relheight=1, relx=0, rely=0)

    mulWaveButtonBorder = tk.Frame(editCanvas, bd=0, highlightthickness=2, highlightcolor="green",
                                   highlightbackground="green")
    mulWaveButton = tk.Button(mulWaveButtonBorder, text="Multi", command=editMulClick, width='20')
    mulWaveButton.configure(fg="green", bg="black", bd=0, borderwidth=0)
    mulWaveButtonBorder.place(relwidth=0.1, relheight=0.1, relx=0.5, rely=0)
    mulWaveButton.place(relwidth=1, relheight=1, relx=0, rely=0)

    sqrWaveButtonBorder = tk.Frame(editCanvas, bd=0, highlightthickness=2, highlightcolor="green",
                                   highlightbackground="green")
    sqrWaveButton = tk.Button(sqrWaveButtonBorder, text="Square", command=editSqrClick, width='20')
    sqrWaveButton.configure(fg="green", bg="black", bd=0, borderwidth=0)
    sqrWaveButtonBorder.place(relwidth=0.1, relheight=0.1, relx=0.6, rely=0)
    sqrWaveButton.place(relwidth=1, relheight=1, relx=0, rely=0)

    normWaveButtonBorder = tk.Frame(editCanvas, bd=0, highlightthickness=2, highlightcolor="green",
                                    highlightbackground="green")
    normWaveButton = tk.Button(normWaveButtonBorder, text="Normal", command=editNormClick, width='20')
    normWaveButton.configure(fg="green", bg="black", bd=0, borderwidth=0)
    normWaveButtonBorder.place(relwidth=0.1, relheight=0.1, relx=0.7, rely=0)
    normWaveButton.place(relwidth=1, relheight=1, relx=0, rely=0)

    sumWaveButtonBorder = tk.Frame(editCanvas, bd=0, highlightthickness=2, highlightcolor="green",
                                   highlightbackground="green")
    sumWaveButton = tk.Button(sumWaveButtonBorder, text="Sum", command=editSumClick, width='20')
    sumWaveButton.configure(fg="green", bg="black", bd=0, borderwidth=0)
    sumWaveButtonBorder.place(relwidth=0.1, relheight=0.1, relx=0.8, rely=0)
    sumWaveButton.place(relwidth=1, relheight=1, relx=0, rely=0)

    # creates the edit button and its border

    # places the edit canvas
    editCanvas.place(relwidth=0.5, relheight=0.5, relx=0, rely=0.5)


def SignalSamplesAreEqual(compare_type="edited"):
    file_name = file_var.get()
    samples = []
    if compare_type == "edited":
        samples = postEditPoints.y_points
    elif compare_type == "original":
        samples = originalPoints.y_points
    else:
        return
    expected_indices = []
    expected_samples = []
    with open(file_name, 'r') as f:
        line = f.readline()
        line = f.readline()
        line = f.readline()
        line = f.readline()
        while line:
            # process line
            L = line.strip()
            if len(L.split(' ')) == 2:
                L = line.split(' ')
                V1 = int(L[0])
                V2 = float(L[1])
                expected_indices.append(V1)
                expected_samples.append(V2)
                line = f.readline()
            else:
                break

    test_failed = 0
    if len(expected_samples) != len(samples):
        line_var.set("Test case failed, your signal have different length from the expected one")
        if test_failed == 0:
            print("Test case failed, your signal have different values from the expected one1")
        test_failed = 1
    for i in range(len(expected_samples)):
        try:
            if abs(samples[i] - expected_samples[i]) < 0.01:
                continue
            else:
                line_var.set("Test case failed, your signal have different values from the expected one")
                if test_failed == 0:
                    print("Test case failed, your signal have different values from the expected one2")
                test_failed = 1
        except IndexError:
            line_var.set("Test case failed, your signal have different values from the expected one")
            if test_failed == 0:
                print("Test case failed, your signal have different values from the expected one2")
            test_failed = 1

    if test_failed == 0:
        line_var.set("Test case passed successfully")
        print("Test case passed successfully")

    # creates a label for the note
    noteLabel = tk.Label(root, text=line_var.get())
    noteLabel.configure(fg="green", bg="black")
    noteLabel.place(relwidth=0.4, relheight=0.05, relx=0.05, rely=0.55)


def compareOriginalClick():
    SignalSamplesAreEqual("original")
    return


def compareEditedClick():
    SignalSamplesAreEqual("edited")
    return


def compareMenuClick():
    width = 0.5 * root.winfo_width()  # gets size of window
    height = 0.5 * root.winfo_height()  # gets size of window
    # creates a canvas for edit menu
    compareCanvas = tk.Canvas(root, width=width, height=height, highlightthickness=2, highlightbackground="green")
    compareCanvas.configure(bg="black")

    compareLabel = tk.Label(compareCanvas, text="Compare:", highlightthickness=2, highlightbackground="green")
    compareLabel.configure(fg="green", bg="black")
    compareLabel.place(relwidth=0.25, relheight=0.1, relx=0, rely=0)


    # creates a label beside the file input
    fileLabel = tk.Label(compareCanvas, text="File:")
    fileLabel.configure(fg="green", bg="black")
    fileLabel.place(relwidth=0.2, relheight=0.1, relx=0.05, rely=0.2)

    # creates an input field for the file path which is stored in file_var
    fileEntry = tk.Entry(compareCanvas, textvariable=file_var)
    fileEntry.place(relwidth=0.6, relheight=0.1, relx=0.25, rely=0.2)

    browseButtonBorder = tk.Frame(compareCanvas, bd=0, highlightthickness=2, highlightcolor="green",
                                      highlightbackground="green")
    browseButton = tk.Button(browseButtonBorder, text="Browse", command=browseClick, width='20')
    browseButton.configure(fg="green", bg="black", bd=0, borderwidth=0)
    browseButtonBorder.place(relwidth=0.2, relheight=0.1, relx=0.45, rely=0.4)
    browseButton.place(relwidth=1, relheight=1, relx=0, rely=0)

    compareOriginalButtonBorder = tk.Frame(compareCanvas, bd=0, highlightthickness=2, highlightcolor="green",
                                      highlightbackground="green")
    compareOriginalButton = tk.Button(compareOriginalButtonBorder, text="Compare OG", command=compareOriginalClick, width='20')
    compareOriginalButton.configure(fg="green", bg="black", bd=0, borderwidth=0)
    compareOriginalButtonBorder.place(relwidth=0.2, relheight=0.1, relx=0.25, rely=0.4)
    compareOriginalButton.place(relwidth=1, relheight=1, relx=0, rely=0)

    compareEditedButtonBorder = tk.Frame(compareCanvas, bd=0, highlightthickness=2, highlightcolor="green",
                                      highlightbackground="green")
    compareEditedButton = tk.Button(compareEditedButtonBorder, text="Compare ED", command=compareEditedClick, width='20')
    compareEditedButton.configure(fg="green", bg="black", bd=0, borderwidth=0)
    compareEditedButtonBorder.place(relwidth=0.2, relheight=0.1, relx=0.65, rely=0.4)
    compareEditedButton.place(relwidth=1, relheight=1, relx=0, rely=0)

    compareCanvas.place(relwidth=0.5, relheight=0.5, relx=0, rely=0.5)


    return


# Creating Label
menuName = tk.Label(menuCanvas, text="DSP - Section 1")
menuName.configure(fg="green", bg="black", highlightthickness=2, highlightbackground="green")
menuName.place(relwidth=0.25, relheight=0.1, relx=0, rely=0)
originalLabel = tk.Label(originalWaveCanvas, text="Original Wave:", highlightthickness=2, highlightbackground="green")
originalLabel.configure(fg="green", bg="black")
originalLabel.place(relwidth=0.25, relheight=0.1, relx=0, rely=0)

editedLabel = tk.Label(editedWaveCanvas, text="Edited Wave:", highlightthickness=2, highlightbackground="green")
editedLabel.configure(fg="green", bg="black")
editedLabel.place(relwidth=0.25, relheight=0.1, relx=0, rely=0)

# Creating Buttons
importButtonBorder = tk.Frame(menuCanvas, bd=0, highlightthickness=2, highlightcolor="green",
                              highlightbackground="green")
importButton = tk.Button(importButtonBorder, text="Import", command=importMenuClick, width='20')
importButton.configure(fg="green", bg="black", bd=0, borderwidth=0)
importButtonBorder.place(relwidth=0.25, relheight=0.2, relx=0, rely=0.2)
importButton.place(relwidth=1, relheight=1, relx=0, rely=0)

generateButtonBorder = tk.Frame(menuCanvas, bd=0, highlightthickness=2, highlightcolor="green",
                                highlightbackground="green")
generateButton = tk.Button(generateButtonBorder, text="Generate", command=generateMenuClick, width='20', )
generateButton.configure(fg="green", bg="black", bd=0, borderwidth=0)
generateButtonBorder.place(relwidth=0.25, relheight=0.2, relx=0, rely=0.4)
generateButton.place(relwidth=1, relheight=1, relx=0, rely=0)

exportOriginalButtonBorder = tk.Frame(originalWaveCanvas, bd=0, highlightthickness=2, highlightcolor="green",
                                      highlightbackground="green")
exportOriginalButton = tk.Button(exportOriginalButtonBorder, text="Export", command=originalExportClick, width='20')
exportOriginalButton.configure(fg="green", bg="black", bd=0, borderwidth=0)
exportOriginalButtonBorder.place(relwidth=0.25, relheight=0.1, relx=0.75, rely=0)
exportOriginalButton.place(relwidth=1, relheight=1, relx=0, rely=0)

exportEditedButtonBorder = tk.Frame(editedWaveCanvas, bd=0, highlightthickness=2, highlightcolor="green",
                                    highlightbackground="green")
exportEditedButton = tk.Button(exportEditedButtonBorder, text="Export", command=originalExportClick, width='20')
exportEditedButton.configure(fg="green", bg="black", bd=0, borderwidth=0)
exportEditedButtonBorder.place(relwidth=0.25, relheight=0.1, relx=0.75, rely=0)
exportEditedButton.place(relwidth=1, relheight=1, relx=0, rely=0)

editButtonBorder = tk.Frame(menuCanvas, bd=0, highlightthickness=2, highlightcolor="green", highlightbackground="green")
editButton = tk.Button(editButtonBorder, text="Edit", command=editMenuClick, width='20')
editButton.configure(fg="green", bg="black", bd=0, borderwidth=0)
editButtonBorder.place(relwidth=0.25, relheight=0.2, relx=0, rely=0.6)
editButton.place(relwidth=1, relheight=1, relx=0, rely=0)

compareButtonBorder = tk.Frame(menuCanvas, bd=0, highlightthickness=2, highlightcolor="green",
                               highlightbackground="green")
compareButton = tk.Button(compareButtonBorder, text="Compare", command=compareMenuClick, width='20')
compareButton.configure(fg="green", bg="black", bd=0, borderwidth=0)
compareButtonBorder.place(relwidth=0.25, relheight=0.2, relx=0, rely=0.8)
compareButton.place(relwidth=1, relheight=1, relx=0, rely=0)

# Putting content on screen


# causes app to start and enter a while loop while it is on
root.mainloop()
