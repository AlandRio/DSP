from tkinter import filedialog
import points as points
import menu as menu
import shared as shared

def importFile():
    path = shared.file_var.get()
    if path != "":  # so the user can not give an empty path
        tempPoints = points.Points()
        # Opens file using the path user gave
        file = open(path)
        # takes the 1st line of the file which is SignalType
        originalSignalType = int(file.readline())
        print(f"Signal type: {originalSignalType}")  # Prints for debugging purposes
        # takes the 2nd line of the file which is isPeriodic
        originalIsPeriodic = int(file.readline())
        print(f"Periodic: {originalIsPeriodic}")  # Prints for debugging purposes
        # takes the 3rd line of the file which is number of samples
        samples = int(file.readline())
        x_ax = []  # initializes an empty array with size samples
        y_ax = []   # initializes an empty array with size samples
        for x in range(samples):
            temp = file.readline().split(" ")
            x_ax.append(int(temp[0]))
            y_ax.append(float(temp[1]))
            print(f"{x_ax[x]} and {y_ax[x]}")
        tempPoints.y_points = y_ax  # puts y-axis points inside the global original points variable
        tempPoints.x_points = x_ax  # puts x axis points inside the global original points variable
        tempPoints.isPeriodic = originalIsPeriodic  # puts periodic flag inside the global original points variable
        tempPoints.signalType = originalSignalType  # puts signal type flag inside the global original points variable
        tempPoints.samples = samples
        return tempPoints


def freqFromFile():
    file_path = shared.file_var.get()
    if(file_path != ""):
        file = open(file_path)
        file.readline()
        file.readline()
        samples = int(file.readline())
        print(f"Samples: {samples}")
        amp_points = []
        phase_points = []
        for x in range(samples):
            temp = file.readline().split(" ")
            amp_points.append(float(temp[0]))
            phase_points.append(float(temp[1]))
        return amp_points,phase_points,samples


def importFromFile():
    shared.originalPoints = importFile()
    print("before")
    if shared.originalPoints.signalType == 1:
        menu.createGraph(shared.originalPoints.x_points, shared.originalPoints.y_points, "Original Graph", "Frequency", shared.originalWaveCanvas)
    else:
        menu.createGraph(shared.originalPoints.x_points, shared.originalPoints.y_points, "Original Graph", "Sample", shared.originalWaveCanvas)
        
    print("after")


def browseClick():
    # Opens the browse menu and specifies that only text files can be taken
    shared.file_var.set(filedialog.askopenfilename(title="Select a txt File", filetypes=[("Text files", "*.txt")]))


def importMenuClick():
    importCanvas = menu.createCanvas(shared.root, 0.5, 0.5, 0, 0.5)

    menu.createLabel("Import", importCanvas, 1, 0.25, 0.1, 0, 0)
    menu.createLabel("Starting Pos only works within the range of X", importCanvas, 0, 0.6, 0.1, 0.25, 0.1)

    menu.createLabel("File:", importCanvas, 0, 0.2, 0.1, 0.05, 0.2)
    menu.createEntry(shared.file_var, importCanvas, 0.6, 0.1, 0.25, 0.2)

    menu.createButton("Browse", browseClick, importCanvas, 0.1, 0.1, 0.8, 0.2)

    menu.createLabel("Starting Pos:", importCanvas, 0, 0.2, 0.1, 0.05, 0.3)
    menu.createEntry(shared.startingPos_var, importCanvas, 0.65, 0.1, 0.25, 0.3)
    
    menu.createButton("Import", importFromFile, importCanvas, 0.2, 0.1, 0.4, 0.9)

def fileExport(wave_type="original"):
    path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    file = open(path, "w")
    saved_points = points.Points
    if wave_type == "original":
        saved_points = points.originalPoints
    elif wave_type == "edited":
        saved_points = points.postEditPoints
    else:
        return
    string = f"{int(saved_points.signalType)}\n{int(saved_points.isPeriodic)}\n{int(saved_points.samples)}"
    for x in range(saved_points.samples):
        string = string + f"\n{int(points.originalPoints.x_points[x])} {float(points.originalPoints.y_points[x])}"
    file.write(string)


def originalExportClick():
    fileExport("original")
    print("export")


def editedExportClick():
    fileExport("edited")
    print("export")