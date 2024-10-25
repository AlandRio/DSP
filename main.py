# Library for GUI
import tkinter as tk
import matplotlib.pyplot as plt
from tkinter import filedialog
import numpy as np
import math as math
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class Wave:  # class for wave used in generate
    def __init__(self, trigFunc="cos", amp=1, theta=0.0, sampleFreq=2.0,
                 freq=1.0):  # initializes class with default arguments
        self.trigFunc = trigFunc  # Wither the function is sin or cos
        self.amp = amp  # Amplitude
        self.theta = theta  # Phase shift
        self.sampleFreq = sampleFreq  # Sample Frequency
        self.freq = freq  # Frequency


class Points:  # class for storing points
    def __init__(self, x_points=[], y_points=[], signalType=0, isPeriodic=1, samples=1000):
        self.x_points = x_points  # Points on the X-Axis
        self.y_points = y_points  # Points on the Y-Axis
        self.signalType = signalType  # Wither the signal is Time (0) or Frequency (1)
        self.isPeriodic = isPeriodic  # Wither the signal is Non-Periodic (0) or Periodic (1)
        self.samples = samples


class quantPoints:
    def __init__(self,points = Points(),err = [], levels = [],levelsBin = []):
        self.points = points,
        self.err = err,
        self.levels = levels
        self.levelsBin = levelsBin


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
quantype_var = tk.StringVar()
quanum_var = tk.IntVar()
# Defining Global Objects for Original Graph and Edited Graph
originalPoints = Points()
originalWave = Wave()
editedPoints = Points()
editedWave = Wave()
postEditPoints = Points()
quantizedPoints = quantPoints()


# functions to optimize code
def getBin(n,l):
    binary = bin(n).split("b")
    length = l - len(binary[1])
    binaryString = ""
    if length > 0:
        for x in range (length):
            binaryString = binaryString + "0"
    binaryString = binaryString + binary[1]
    return binaryString


def createCanvas(canvas, relwidth, relheight, relx, rely):
    width = root.winfo_width()
    height = root.winfo_height()
    canvas = tk.Canvas(canvas, width=width, height=height, highlightthickness=2, highlightbackground="green")
    canvas.configure(bg="black")
    canvas.place(relwidth=relwidth, relheight=relheight, relx=relx, rely=rely)
    return canvas


def createLabel(label, canvas, highlight, relwidth, relheight, relx, rely):
    originalFunctionLabel = tk.Label(canvas, text=label, fg="green", bg="black")
    if highlight == 1:
        originalFunctionLabel.configure(highlightthickness=2, highlightbackground="green")
    originalFunctionLabel.place(relwidth=relwidth, relheight=relheight, relx=relx, rely=rely)


def createEntry(var, canvas, relwidth, relheight, relx, rely):
    entry = tk.Entry(canvas, textvariable=var)
    entry.place(relwidth=relwidth, relheight=relheight, relx=relx, rely=rely)


def createButton(label, func, canvas, relwidth, relheight, relx, rely):
    Border = tk.Frame(canvas, bd=0, highlightthickness=2, highlightcolor="green", highlightbackground="green")
    Button = tk.Button(Border, text=label, command=func, width='20')
    Button.configure(fg="green", bg="black", bd=0, borderwidth=0)
    Border.place(relwidth=relwidth, relheight=relheight, relx=relx, rely=rely)
    Button.place(relwidth=1, relheight=1, relx=0, rely=0)


def createGraph(points_x, points_y, graph_label, x_label, canvas):
    shownPoints_X = []
    shownPoints_Y = []
    i = 0
    if startingPos_var.get() >= min(points_x) or startingPos_var.get() < max(points_x):
        i = points_x.index(startingPos_var.get())
    for x in range(40):
        try:
            shownPoints_X.append(points_x[i + x])
            shownPoints_Y.append(points_y[i + x])
        except IndexError:
            break
    fig, ax = plt.subplots()  # creates a figure in fig and sub-plots in ax
    # plots the graph using the original points object
    ax.plot(shownPoints_X, shownPoints_Y, color="darkgreen")
    ax.set_title(graph_label)
    ax.set_xlabel(x_label)
    ax.set_ylabel("Amplitude")
    # creates a graph gui in original wave canvas then draws the graph and places it
    originalGraph = FigureCanvasTkAgg(fig, master=canvas)
    originalGraph.draw()
    originalGraph.get_tk_widget().place(relwidth=1, relheight=0.9, relx=0, rely=0.1)


def createCheck(var,onvalue,offvalue,canvas,relx,rely):
    check = tk.Checkbutton(canvas, variable=var, onvalue=onvalue, offvalue=offvalue, bg="black")
    check.place(relwidth=0.05, relheight=0.1, relx=relx, rely=rely)


# Creating Canvases then configuring its background then placing it on the window
menuCanvas = createCanvas(root, 0.5, 0.5, 0, 0)
originalWaveCanvas = createCanvas(root, 0.5, 0.5, 0.5, 0)
editedWaveCanvas = createCanvas(root, 0.5, 0.5, 0.5, 0.5)
createCanvas(root, 0.5, 0.5, 0, 0.5)


def importFile():
    if file_var.get() != "":  # so the user can not give an empty path
        tempPoints = Points()
        # Opens file using the path user gave
        file = open(file_var.get())
        # takes the 1st line of the file which is SignalType
        originalSignalType = int(file.readline())
        print(f"Signal type: {originalSignalType}")  # Prints for debugging purposes
        # takes the 2nd line of the file which is isPeriodic
        originalIsPeriodic = int(file.readline())
        print(f"Periodic: {originalIsPeriodic}")  # Prints for debugging purposes
        # takes the 3rd line of the file which is number of samples
        samples = int(file.readline())
        x_ax = [0] * samples  # initializes an empty array with size samples
        y_ax = [0] * samples  # initializes an empty array with size samples
        i = 0  # variable used in the while loop incase loop does not find starting position
        for x in range(samples):
            temp = file.readline().split(" ")
            x_ax[x] = int(temp[0])
            y_ax[x] = float(temp[1])
            print(f"{x_ax[x]} and {y_ax[x]}")
        tempPoints.y_points = y_ax  # puts y-axis points inside the global original points variable
        tempPoints.x_points = x_ax  # puts x axis points inside the global original points variable
        tempPoints.isPeriodic = originalIsPeriodic  # puts periodic flag inside the global original points variable
        tempPoints.signalType = originalSignalType  # puts signal type flag inside the global original points variable
        tempPoints.samples = samples
        return tempPoints


def importFromFile():
    global originalPoints
    originalPoints = importFile()
    if originalPoints.signalType == 1:
        createGraph(originalPoints.x_points, originalPoints.y_points, "Original Graph", "Frequency", originalWaveCanvas)
    else:
        createGraph(originalPoints.x_points, originalPoints.y_points, "Original Graph", "Sample", originalWaveCanvas)


def browseClick():
    # Opens the browse menu and specifies that only text files can be taken
    file_var.set(filedialog.askopenfilename(title="Select a txt File", filetypes=[("Text files", "*.txt")]))


def importMenuClick():
    importCanvas = createCanvas(root, 0.5, 0.5, 0, 0.5)

    createLabel("Import", importCanvas, 1, 0.25, 0.1, 0, 0)
    createLabel("Starting Pos only works within the range of X", importCanvas, 0, 0.6, 0.1, 0.25, 0.1)

    createLabel("File:", importCanvas, 0, 0.2, 0.1, 0.05, 0.2)
    createEntry(file_var, importCanvas, 0.6, 0.1, 0.25, 0.2)

    createLabel("Starting Pos:", importCanvas, 0, 0.2, 0.1, 0.05, 0.3)
    createEntry(startingPos_var, importCanvas, 0.65, 0.1, 0.25, 0.3)

    createButton("Browse", browseClick, importCanvas, 0.1, 0.1, 0.8, 0.2)
    createButton("Import", importFromFile, importCanvas, 0.2, 0.1, 0.4, 0.9)


def generatePoints(wave, startingPos):
    pointsX = []  # initializes an array of 40 indexes
    pointsY = []  # initializes an array of 40 indexes
    for x in range(1000):
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
        pointsY.append(posY)  # adds the point at Y to the array to the y-axis
        pointsX.append(startingPos)  # adds the starting point to the x-axis
        startingPos += 1  # increment starting point by 1
    points = Points(pointsX, pointsY)  # adds the values into a class for easier management
    return points  # returns an array of points for graph


def generateClick():
    # using the input the user gave in generate function changes the global original wave object
    global originalWave,originalPoints
    originalWave = Wave(type_var.get(), amp_var.get(), theta_var.get(), sampleFreq_var.get(), freq_var.get())
    # calls the generate points function and puts the points generated into global original wave points
    originalPoints = generatePoints(originalWave, startingPos_var.get())
    originalPoints.samples = len(originalPoints.x_points)
    createGraph(originalPoints.x_points, originalPoints.y_points, "Original Graph", "Sample", originalWaveCanvas)


def generateMenuClick():
    type_var.set("cos")
    generateCanvas = createCanvas(root, 0.5, 0.5, 0, 0.5)
    createLabel("Generate:", generateCanvas, 1, 0.25, 0.1, 0, 0)

    createLabel("Sin():", generateCanvas, 0, 0.2, 0.1, 0.1, 0.1)
    createCheck(quantype_var,"sin","cos",generateCanvas,0.3,0.1)
    createLabel("Amplitude:", generateCanvas, 0, 0.2, 0.1, 0.1, 0.2)
    createEntry(amp_var, generateCanvas, 0.6, 0.1, 0.3, 0.2)
    createLabel("Starting Pos:", generateCanvas, 0, 0.2, 0.1, 0.1, 0.3)
    createEntry(startingPos_var, generateCanvas, 0.6, 0.1, 0.3, 0.3)
    createLabel("Theta:", generateCanvas, 0, 0.2, 0.1, 0.1, 0.4)
    createEntry(theta_var, generateCanvas, 0.6, 0.1, 0.3, 0.4)
    createLabel("Sample Frequency:", generateCanvas, 0, 0.2, 0.1, 0.1, 0.5)
    createEntry(sampleFreq_var, generateCanvas, 0.6, 0.1, 0.3, 0.5)
    createLabel("Frequency:", generateCanvas, 0, 0.2, 0.1, 0.1, 0.6)
    createEntry(freq_var, generateCanvas, 0.6, 0.1, 0.3, 0.6)

    createButton("Generate", generateClick, generateCanvas, 0.2, 0.1, 0.4, 0.9)

def quantClick():
    global originalPoints,quantizedPoints,postEditPoints
    points_x = []
    points_y = []
    levels = 0
    bits = 0
    if quantype_var.get() == "levels":
        levels = quanum_var.get()
        bits = math.ceil(math.log2(quanum_var.get()))
    elif quantype_var.get() == "bits":
        levels = pow(2,quanum_var.get())
        bits = quanum_var.get()
    print(f"\nLevels: {levels}\n")
    min_point = min(originalPoints.y_points)
    max_point = max(originalPoints.y_points)
    jump = max_point - min_point
    jumpPerLvl = jump / (levels)
    ranges_arr = []
    levels_arr = []
    levelDec_arr = []
    levelBin_arr = []
    error_arr = []
    for x in range(levels + 1):
        ranges_arr.append(round(min_point + (jumpPerLvl*x),3))
        print(f"{ranges_arr[x]}")
    for x in range(levels):
        approx_y = round((ranges_arr[x] + ranges_arr[x + 1])/2,3)
        levels_arr.append(approx_y)
        print(f"Level: ")
    for x in range(len(originalPoints.x_points)):
        for y in range(levels):
            if originalPoints.y_points[x] >= ranges_arr[y] and originalPoints.y_points[x] <= ranges_arr[y + 1]:
                points_x.append(originalPoints.x_points[x])
                points_y.append(levels_arr[y])
                levelDec_arr.append(y + 1)
                levelBin_arr.append(getBin(y,bits))
                error_arr.append(round(points_y[x] - originalPoints.y_points[x],3))
                print(f"{levelBin_arr[x]}: ({originalPoints.x_points[x]},{points_y[x]}) and Error = {error_arr[x]}")
                break
    quantizedPoints.points = Points(points_x,points_y,originalPoints.signalType,originalPoints.isPeriodic,originalPoints.samples)
    quantizedPoints.levelsBin = levelBin_arr
    quantizedPoints.levels = levelDec_arr
    quantizedPoints.err = error_arr
    postEditPoints = quantizedPoints.points
    createGraph(points_x,points_y,"Quantized Graph","Sample",editedWaveCanvas)
    

def quantizeMenuClick():
    quantype_var.set("levels")
    quantCanvas = createCanvas(root, 0.5, 0.5, 0, 0.5)
    createLabel("Quantize:", quantCanvas, 1, 0.25, 0.1, 0, 0)

    createLabel("Bits?", quantCanvas, 0, 0.15, 0.1, 0.1, 0.2)
    createCheck(quantype_var,"bits","levels",quantCanvas,0.25,0.2)
    createEntry(quanum_var, quantCanvas, 0.6, 0.1, 0.3, 0.2)
    createLabel("Starting Pos:", quantCanvas, 0, 0.2, 0.1, 0.1, 0.3)
    createEntry(startingPos_var, quantCanvas, 0.6, 0.1, 0.3, 0.3)

    createButton("QUANTIZE", quantClick, quantCanvas, 0.2, 0.2, 0.4, 0.5)


def generateEditedWaveClick():
    global editedPoints,editedWave
    editedWave = Wave(type_var.get(), amp_var.get(), theta_var.get(), sampleFreq_var.get(), freq_var.get())
    editedPoints = generatePoints(editedWave, startingPos_var.get())


def addImportWaveClick():
    global editedPoints
    editedPoints = importFile()


def addSubEditWave(math_type="add"):
    global editedPoints,originalPoints,postEditPoints
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
                        if math_type == "add":
                            postEditPoints.x_points[x] = int(editedPoints.x_points[z])
                            postEditPoints.y_points[x] = editedPoints.y_points[z] + originalPoints.y_points[y]
                            flag_found = 1
                        elif math_type == "sub":
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
    createGraph(postEditPoints.x_points, postEditPoints.y_points, "Edited Wave", "Sample", editedWaveCanvas)
    return


def addWaveClick():
    addSubEditWave("add")
    return


def subWaveClick():
    addSubEditWave("sub")
    return


def editAddClick():
    type_var.set("cos")
    editAddCanvas = createCanvas(root, 0.5, 0.45, 0, 0.55)
    createLabel("Add/Sub:", editAddCanvas, 1, 0.25, 0.1, 0, 0)
    # Creates a label for a variable then its input from the user
    createLabel("Sin():", editAddCanvas, 0, 0.2, 0.1, 0.05, 0.2)
    createCheck(quantype_var,"sin","cos",editAddCanvas,0.25,0.2)

    createLabel("Starting Pos:", editAddCanvas, 0, 0.2, 0.1, 0.25, 0.1)
    createEntry(startingPos_var, editAddCanvas, 0.2, 0.1, 0.45, 0.1)

    createLabel("Amplitude:", editAddCanvas, 0, 0.2, 0.1, 0.05, 0.3)
    createEntry(amp_var, editAddCanvas, 0.2, 0.1, 0.25, 0.3)

    createLabel("Theta:", editAddCanvas, 0, 0.2, 0.1, 0.05, 0.4)
    createEntry(theta_var, editAddCanvas, 0.2, 0.1, 0.25, 0.4)

    createLabel("Sample Frequency:", editAddCanvas, 0, 0.2, 0.1, 0.05, 0.5)
    createEntry(sampleFreq_var, editAddCanvas, 0.2, 0.1, 0.25, 0.5)

    createLabel("Frequency:", editAddCanvas, 0, 0.2, 0.1, 0.05, 0.6)
    createEntry(freq_var, editAddCanvas, 0.2, 0.1, 0.25, 0.6)

    createLabel("File Path:", editAddCanvas, 0, 0.2, 0.1, 0.6, 0.3)
    createEntry(file_var, editAddCanvas, 0.4, 0.1, 0.5, 0.4)
    # buttons
    createButton("Browse", browseClick, editAddCanvas, 0.2, 0.1, 0.6, 0.6)
    createButton("Generate", generateEditedWaveClick, editAddCanvas, 0.2, 0.1, 0.25, 0.75)
    createButton("Import", addImportWaveClick, editAddCanvas, 0.2, 0.1, 0.6, 0.75)
    createButton("Add", addWaveClick, editAddCanvas, 0.2, 0.1, 0.6, 0.9)
    createButton("Subtract", subWaveClick, editAddCanvas, 0.2, 0.1, 0.25, 0.9)
    return


def mulClick():
    global postEditPoints
    postEditPoints.samples = len(originalPoints.x_points)
    postEditPoints.x_points = [0] * postEditPoints.samples
    postEditPoints.y_points = [0] * postEditPoints.samples
    for x in range(postEditPoints.samples):
        postEditPoints.x_points[x] = (originalPoints.x_points[x])
        postEditPoints.y_points[x] = (originalPoints.y_points[x] * amp_var.get())
    createGraph(postEditPoints.x_points, postEditPoints.y_points, "Edited Wave", "Sample", editedWaveCanvas)
    return


def editMulClick():
    editMulCanvas = createCanvas(root, 0.5, 0.45, 0, 0.55)
    createLabel("Multiply:", editMulCanvas, 1, 0.25, 0.1, 0, 0)

    createLabel("Multiply by:", editMulCanvas, 0, 0.2, 0.1, 0.05, 0.4)
    createEntry(amp_var, editMulCanvas, 0.2, 0.1, 0.25, 0.4)
    createLabel("Starting Pos:", editMulCanvas, 0, 0.2, 0.1, 0.05, 0.3)
    createEntry(startingPos_var, editMulCanvas, 0.2, 0.1, 0.25, 0.3)
    createButton("MULTIPLY", mulClick, editMulCanvas, 0.2, 0.2, 0.4, 0.6)

    return


def sqrClick():
    global postEditPoints
    postEditPoints.samples = len(originalPoints.x_points)
    postEditPoints.x_points = [0] * postEditPoints.samples
    postEditPoints.y_points = [0] * postEditPoints.samples
    for x in range(postEditPoints.samples):
        postEditPoints.x_points[x] = (originalPoints.x_points[x])
        postEditPoints.y_points[x] = (originalPoints.y_points[x] * originalPoints.y_points[x])

    createGraph(postEditPoints.x_points, postEditPoints.y_points, "Edited Wave", "Sample", editedWaveCanvas)
    return


def editSqrClick():
    editSqrCanvas = createCanvas(root, 0.5, 0.45, 0, 0.55)
    createLabel("Square:", editSqrCanvas, 1, 0.25, 0.1, 0, 0)

    createLabel("Starting Pos:", editSqrCanvas, 0, 0.2, 0.1, 0.05, 0.3)
    createEntry(startingPos_var, editSqrCanvas, 0.2, 0.1, 0.25, 0.3)
    createButton("SQUARE", sqrClick, editSqrCanvas, 0.2, 0.2, 0.4, 0.6)
    return


def normWave(norm_type="-1"):
    global postEditPoints
    postEditPoints.samples = len(originalPoints.x_points)
    postEditPoints.x_points = [0] * postEditPoints.samples
    postEditPoints.y_points = [0] * postEditPoints.samples
    max_point = max(originalPoints.y_points)
    min_point = min(originalPoints.y_points)
    for x in range(postEditPoints.samples):
        postEditPoints.x_points[x] = (originalPoints.x_points[x])
        fraction = (originalPoints.y_points[x] - min_point) / (max_point - min_point)
        if norm_type == "0":
            postEditPoints.y_points[x] = fraction
        elif norm_type == "-1":
            postEditPoints.y_points[x] = 2 * fraction - 1
    createGraph(postEditPoints.x_points, postEditPoints.y_points, "Edited Wave", "Sample", editedWaveCanvas)
    return


def norm1Click():
    normWave("-1")
    return


def norm0Click():
    normWave("0")
    return


def editNormClick():
    editNormCanvas = createCanvas(root, 0.5, 0.45, 0, 0.55)
    createLabel("Normalize:", editNormCanvas, 1, 0.25, 0.1, 0, 0)

    createLabel("Starting Pos:", editNormCanvas, 0, 0.2, 0.1, 0.05, 0.3)
    createEntry(startingPos_var, editNormCanvas, 0.2, 0.1, 0.25, 0.3)
    createButton("-1 to 1", norm1Click, editNormCanvas, 0.2, 0.2, 0.6, 0.6)
    createButton("0 to 1", norm0Click, editNormCanvas, 0.2, 0.2, 0.2, 0.6)
    return


def sumClick():
    global postEditPoints
    postEditPoints.samples = len(originalPoints.x_points)
    postEditPoints.x_points = [0] * postEditPoints.samples
    postEditPoints.y_points = [0] * postEditPoints.samples
    point_sum = 0
    for x in range(postEditPoints.samples):
        postEditPoints.x_points[x] = (originalPoints.x_points[x])
        point_sum = point_sum + originalPoints.y_points[x]
        postEditPoints.y_points[x] = point_sum
    createGraph(postEditPoints.x_points, postEditPoints.y_points, "Edited Wave", "Sample", editedWaveCanvas)
    return


def editSumClick():
    editSumCanvas = createCanvas(root, 0.5, 0.45, 0, 0.55)
    createLabel("Accumulate:", editSumCanvas, 1, 0.25, 0.1, 0, 0)

    createLabel("Starting Pos:", editSumCanvas, 0, 0.2, 0.1, 0.05, 0.3)
    createEntry(startingPos_var, editSumCanvas, 0.2, 0.1, 0.25, 0.3)
    createButton("ACCUMULATE", sumClick, editSumCanvas, 0.2, 0.2, 0.4, 0.6)
    return


def editMenuClick():
    # creates a canvas for edit menu
    editCanvas = createCanvas(root, 0.5, 0.5, 0, 0.5)
    # creates a label on the corner for edit
    createLabel("Edit:", editCanvas, 1, 0.25, 0.1, 0, 0)
    # Buttons for edit menu
    createButton("Add/Sub", editAddClick, editCanvas, 0.2, 0.1, 0.3, 0)
    createButton("Multi", editMulClick, editCanvas, 0.1, 0.1, 0.5, 0)
    createButton("Square", editSqrClick, editCanvas, 0.1, 0.1, 0.6, 0)
    createButton("Normal", editNormClick, editCanvas, 0.1, 0.1, 0.7, 0)
    createButton("Sum", editSumClick, editCanvas, 0.1, 0.1, 0.8, 0)


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
        f.readline()
        f.readline()
        f.readline()
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
    createLabel(line_var.get(), root, 0, 0.4, 0.05, 0.05, 0.55)


def compareOriginalClick():
    SignalSamplesAreEqual("original")
    return


def compareEditedClick():
    SignalSamplesAreEqual("edited")
    return

def QuantizationTest1():
    file_name = file_var.get()
    Your_EncodedValues = quantizedPoints.levelsBin
    Your_QuantizedValues = quantizedPoints.points.y_points
    expectedEncodedValues=[]
    expectedQuantizedValues=[]
    test_failed = 0
    with open(file_name, 'r') as f:
        line = f.readline()
        line = f.readline()
        line = f.readline()
        line = f.readline()
        while line:
            # process line
            L=line.strip()
            if len(L.split(' '))==2:
                L=line.split(' ')
                V2=str(L[0])
                V3=float(L[1])
                expectedEncodedValues.append(V2)
                expectedQuantizedValues.append(V3)
                line = f.readline()
            else:
                break
    if( (len(Your_EncodedValues)!=len(expectedEncodedValues)) or (len(Your_QuantizedValues)!=len(expectedQuantizedValues))):
        line_var.set("QuantizationTest1 Test case failed, your signal have different length from the expected one")
        print("QuantizationTest1 Test case failed, your signal have different length from the expected one")
        test_failed = 1
    if test_failed == 0:
        for i in range(len(Your_EncodedValues)):
            if(Your_EncodedValues[i]!=expectedEncodedValues[i]):
                line_var.set("QuantizationTest1 Test case failed, your EncodedValues have different EncodedValues from the expected one")
                print("QuantizationTest1 Test case failed, your EncodedValues have different EncodedValues from the expected one") 
                test_failed = 1
    if test_failed == 0:
        for i in range(len(expectedQuantizedValues)):
            if abs(Your_QuantizedValues[i] - expectedQuantizedValues[i]) < 0.01:
                continue
            else:
                line_var.set("QuantizationTest1 Test case failed, your QuantizedValues have different values from the expected one")
                print("QuantizationTest1 Test case failed, your QuantizedValues have different values from the expected one") 
                test_failed = 1
    
    # creates a label for the note
    if test_failed == 0:
        line_var.set("QuantizationTest1 Test case passed successfully")
        print("QuantizationTest1 Test case passed successfully")
    createLabel(line_var.get(), root, 0, 0.45, 0.05, 0.025, 0.55)


def QuantizationTest2():
    file_name = file_var.get()
    Your_IntervalIndices = quantizedPoints.levels
    Your_EncodedValues = quantizedPoints.levelsBin
    Your_QuantizedValues = quantizedPoints.points.y_points
    Your_SampledError = quantizedPoints.err
    test_failed = 0
    expectedIntervalIndices=[]
    expectedEncodedValues=[]
    expectedQuantizedValues=[]
    expectedSampledError=[]
    with open(file_name, 'r') as f:
        line = f.readline()
        line = f.readline()
        line = f.readline()
        line = f.readline()
        while line:
            # process line
            L=line.strip()
            if len(L.split(' '))==4:
                L=line.split(' ')
                V1=int(L[0])
                V2=str(L[1])
                V3=float(L[2])
                V4=float(L[3])
                expectedIntervalIndices.append(V1)
                expectedEncodedValues.append(V2)
                expectedQuantizedValues.append(V3)
                expectedSampledError.append(V4)
                line = f.readline()
            else:
                break
    if(len(Your_IntervalIndices)!=len(expectedIntervalIndices)
     or len(Your_EncodedValues)!=len(expectedEncodedValues)
      or len(Your_QuantizedValues)!=len(expectedQuantizedValues)
      or len(Your_SampledError)!=len(expectedSampledError)):
        line_var.set("QuantizationTest2 Test case failed, your signal have different length from the expected one")
        print("QuantizationTest2 Test case failed, your signal have different length from the expected one")
        test_failed = 1
    if test_failed == 0:
        for i in range(len(Your_IntervalIndices)):
            if(Your_IntervalIndices[i]!=expectedIntervalIndices[i]):
                line_var.set("QuantizationTest2 Test case failed, your signal have different indicies from the expected one") 
                print("QuantizationTest2 Test case failed, your signal have different indicies from the expected one") 
                test_failed = 1
    if test_failed == 0:
        for i in range(len(Your_EncodedValues)):
            if(Your_EncodedValues[i]!=expectedEncodedValues[i]):
                line_var.set("uantizationTest2 Test case failed, your EncodedValues have different EncodedValues from the expected one") 
                print("QuantizationTest2 Test case failed, your EncodedValues have different EncodedValues from the expected one") 
                test_failed = 1
    if test_failed == 0: 
        for i in range(len(expectedQuantizedValues)):
            if abs(Your_QuantizedValues[i] - expectedQuantizedValues[i]) < 0.01:
                continue
            else:
                line_var.set("QuantizationTest2 Test case failed, your QuantizedValues have different values from the expected one") 
                print("QuantizationTest2 Test case failed, your QuantizedValues have different values from the expected one") 
                test_failed = 1
    if test_failed == 0:
        for i in range(len(expectedSampledError)):
            if abs(Your_SampledError[i] - expectedSampledError[i]) < 0.01:
                continue
            else:
                line_var.set("QuantizationTest2 Test case failed, your SampledError have different values from the expected one")
                print("QuantizationTest2 Test case failed, your SampledError have different values from the expected one") 
                test_failed = 1
    if test_failed == 0:
        line_var.set("QuantizationTest2 Test case passed successfully")
        print("QuantizationTest2 Test case passed successfully")
    createLabel(line_var.get(), root, 0, 0.45, 0.05, 0.025, 0.55)


def compareMenuClick():
    compareCanvas = createCanvas(root, 0.5, 0.5, 0, 0.5)
    createLabel("Compare:", compareCanvas, 1, 0.25, 0.1, 0, 0)

    createLabel("File:", compareCanvas, 0, 0.2, 0.1, 0.1, 0.2)
    createEntry(file_var, compareCanvas, 0.4, 0.1, 0.3, 0.2)
    createButton("Browse", browseClick, compareCanvas, 0.2, 0.1, 0.7, 0.2)
    createButton("Compare OG", compareOriginalClick, compareCanvas, 0.2, 0.1, 0.1, 0.4)
    createButton("Compare ED", compareEditedClick, compareCanvas, 0.2, 0.1, 0.3, 0.4)
    createButton("QN Test 1", QuantizationTest1, compareCanvas, 0.2, 0.1, 0.5, 0.4)
    createButton("QN Test 2", QuantizationTest2, compareCanvas, 0.2, 0.1, 0.7, 0.4)


def fileExport(wave_type="original"):
    path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    file = open(path, "w")
    saved_points = Points
    if wave_type == "original":
        saved_points = originalPoints
    elif wave_type == "edited":
        saved_points = postEditPoints
    else:
        return
    string = f"{int(saved_points.signalType)}\n{int(saved_points.isPeriodic)}\n{int(saved_points.samples)}"
    for x in range(saved_points.samples):
        string = string + f"\n{int(originalPoints.x_points[x])} {float(originalPoints.y_points[x])}"
    file.write(string)


def originalExportClick():
    fileExport("original")
    print("export")


def editedExportClick():
    fileExport("edited")
    print("export")


def quitClick():
    root.destroy()


# Creating Label
createLabel("Dsp - Section 1", menuCanvas, 1, 0.25, 0.1, 0.375, 0)
createLabel("Original Wave:", originalWaveCanvas, 1, 0.25, 0.1, 0, 0)
createLabel("Edited Wave:", editedWaveCanvas, 1, 0.25, 0.1, 0, 0)
# Creating Buttons
createButton("Export", originalExportClick, originalWaveCanvas, 0.25, 0.1, 0.75, 0)
createButton("Export", editedExportClick, editedWaveCanvas, 0.25, 0.1, 0.75, 0)
createButton("Import", importMenuClick, menuCanvas, 0.25, 0.1, 0, 0.2)
createButton("Generate", generateMenuClick, menuCanvas, 0.25, 0.1, 0, 0.3)
createButton("Quantize", quantizeMenuClick, menuCanvas, 0.25, 0.1, 0, 0.4)
createButton("Edit", editMenuClick, menuCanvas, 0.25, 0.1, 0, 0.5)
createButton("Compare", compareMenuClick, menuCanvas, 0.25, 0.1, 0, 0.6)
createButton("Quit", quitClick, menuCanvas, 0.25, 0.1, 0, 0.7)

# causes app to start and enter a while loop while it is on
root.mainloop()
