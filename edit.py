from files import browseClick, importFile
import points as points
import shared as shared
import menu as menu

def generateEditedWaveClick():
    shared.editedWave = points.Wave(shared.type_var.get(), shared.amp_var.get(), shared.theta_var.get(), shared.sampleFreq_var.get(), shared.freq_var.get())
    shared.editedPoints = points.generatePoints(shared.editedWave, shared.startingPos_var.get())


def addImportWaveClick():
    shared.editedPoints = importFile()


def addSubEditWave(math_type="add"):
    minimum_point = min(min(shared.editedPoints.x_points), min(shared.originalPoints.x_points))
    maximum_point = max(max(shared.editedPoints.x_points), max(shared.originalPoints.x_points))
    total_samples = int(maximum_point - minimum_point) + 1
    print(f"total: {total_samples}")
    shared.postEditPoints.x_points = [0] * total_samples
    shared.postEditPoints.y_points = [0] * total_samples
    i = minimum_point
    x = 0
    z = 0
    while i <= maximum_point:
        flag_found = 0
        for y in range(total_samples):
            try:
                if shared.editedPoints.x_points[z] == i:
                    if shared.originalPoints.x_points[y] == i:
                        if math_type == "add":
                            shared.postEditPoints.x_points[x] = int(shared.editedPoints.x_points[z])
                            shared.postEditPoints.y_points[x] = shared.editedPoints.y_points[z] + shared.originalPoints.y_points[y]
                            flag_found = 1
                        elif math_type == "sub":
                            shared.postEditPoints.x_points[x] = int(shared.editedPoints.x_points[z])
                            shared.postEditPoints.y_points[x] = shared.editedPoints.y_points[z] - shared.originalPoints.y_points[y]
                            flag_found = 1
                elif shared.originalPoints.x_points[y] == i:
                    shared.postEditPoints.x_points[x] = int(shared.originalPoints.x_points[y])
                    shared.postEditPoints.y_points[x] = shared.originalPoints.y_points[y]
                    flag_found = 1
            except IndexError:
                break
        try:
            if flag_found == 0:
                if shared.editedPoints.x_points[x] == i:
                    shared.postEditPoints.x_points[x] = int(shared.editedPoints.x_points[z])
                    shared.postEditPoints.y_points[x] = shared.editedPoints.y_points[z]
            print(f"{shared.postEditPoints.x_points[x]} and {shared.postEditPoints.y_points[x]}")
        except IndexError:
            break
        z = z + 1
        if z > shared.editedPoints.samples:
            z = 0
        x = x + 1
        i = i + 1
    menu.createGraph(shared.postEditPoints.x_points, shared.postEditPoints.y_points, "Edited Wave", "Sample", shared.editedWaveCanvas)


def addWaveClick():
    addSubEditWave("add")


def subWaveClick():
    addSubEditWave("sub")


def editAddClick():
    shared.type_var.set("cos")
    editAddCanvas = menu.createCanvas(shared.root, 0.5, 0.45, 0, 0.55)
    menu.createLabel("Add/Sub:", editAddCanvas, 1, 0.25, 0.1, 0, 0)
    # Creates a label for a variable then its input from the user
    menu.createLabel("Sin():", editAddCanvas, 0, 0.2, 0.1, 0.05, 0.2)
    menu.createCheck(shared.quantype_var,"sin","cos",editAddCanvas,0.25,0.2)

    menu.createLabel("Starting Pos:", editAddCanvas, 0, 0.2, 0.1, 0.25, 0.1)
    menu.createEntry(shared.startingPos_var, editAddCanvas, 0.2, 0.1, 0.45, 0.1)

    menu.createLabel("Amplitude:", editAddCanvas, 0, 0.2, 0.1, 0.05, 0.3)
    menu.createEntry(shared.amp_var, editAddCanvas, 0.2, 0.1, 0.25, 0.3)

    menu.createLabel("Theta:", editAddCanvas, 0, 0.2, 0.1, 0.05, 0.4)
    menu.createEntry(shared.theta_var, editAddCanvas, 0.2, 0.1, 0.25, 0.4)

    menu.createLabel("Sample Frequency:", editAddCanvas, 0, 0.2, 0.1, 0.05, 0.5)
    menu.createEntry(shared.sampleFreq_var, editAddCanvas, 0.2, 0.1, 0.25, 0.5)

    menu.createLabel("Frequency:", editAddCanvas, 0, 0.2, 0.1, 0.05, 0.6)
    menu.createEntry(shared.freq_var, editAddCanvas, 0.2, 0.1, 0.25, 0.6)

    menu.createLabel("File Path:", editAddCanvas, 0, 0.2, 0.1, 0.6, 0.3)
    menu.createEntry(shared.file_var, editAddCanvas, 0.4, 0.1, 0.5, 0.4)
    # buttons
    menu.createButton("Browse", browseClick, editAddCanvas, 0.2, 0.1, 0.6, 0.6)
    menu.createButton("Generate", generateEditedWaveClick, editAddCanvas, 0.2, 0.1, 0.25, 0.75)
    menu.createButton("Import", addImportWaveClick, editAddCanvas, 0.2, 0.1, 0.6, 0.75)
    menu.createButton("Add", addWaveClick, editAddCanvas, 0.2, 0.1, 0.6, 0.9)
    menu.createButton("Subtract", subWaveClick, editAddCanvas, 0.2, 0.1, 0.25, 0.9)


def mulClick():
    shared.postEditPoints.samples = len(shared.originalPoints.x_points)
    shared.postEditPoints.x_points = [0] * shared.postEditPoints.samples
    shared.postEditPoints.y_points = [0] * shared.postEditPoints.samples
    for x in range(shared.postEditPoints.samples):
        shared.postEditPoints.x_points[x] = (shared.originalPoints.x_points[x])
        shared.postEditPoints.y_points[x] = (shared.originalPoints.y_points[x] * shared.amp_var.get())
    menu.createGraph(shared.postEditPoints.x_points, shared.postEditPoints.y_points, "Edited Wave", "Sample", shared.editedWaveCanvas)


def editMulClick():
    editMulCanvas = menu.createCanvas(shared.root, 0.5, 0.45, 0, 0.55)
    menu.createLabel("Multiply:", editMulCanvas, 1, 0.25, 0.1, 0, 0)

    menu.createLabel("Multiply by:", editMulCanvas, 0, 0.2, 0.1, 0.05, 0.4)
    menu.createEntry(shared.amp_var, editMulCanvas, 0.2, 0.1, 0.25, 0.4)
    menu.createLabel("Starting Pos:", editMulCanvas, 0, 0.2, 0.1, 0.05, 0.3)
    menu.createEntry(shared.startingPos_var, editMulCanvas, 0.2, 0.1, 0.25, 0.3)
    menu.createButton("MULTIPLY", mulClick, editMulCanvas, 0.2, 0.2, 0.4, 0.6)

    return


def sqrClick():
    shared.postEditPoints.samples = len(shared.originalPoints.x_points)
    shared.postEditPoints.x_points = [0] * shared.postEditPoints.samples
    shared.postEditPoints.y_points = [0] * shared.postEditPoints.samples
    for x in range(shared.postEditPoints.samples):
        shared.postEditPoints.x_points[x] = (shared.originalPoints.x_points[x])
        shared.postEditPoints.y_points[x] = (shared.originalPoints.y_points[x] * shared.originalPoints.y_points[x])

    menu.createGraph(shared.postEditPoints.x_points, shared.postEditPoints.y_points, "Edited Wave", "Sample", shared.editedWaveCanvas)
    return


def editSqrClick():
    editSqrCanvas = menu.createCanvas(shared.root, 0.5, 0.45, 0, 0.55)
    menu.createLabel("Square:", editSqrCanvas, 1, 0.25, 0.1, 0, 0)

    menu.createLabel("Starting Pos:", editSqrCanvas, 0, 0.2, 0.1, 0.05, 0.3)
    menu.createEntry(shared.startingPos_var, editSqrCanvas, 0.2, 0.1, 0.25, 0.3)
    menu.createButton("SQUARE", sqrClick, editSqrCanvas, 0.2, 0.2, 0.4, 0.6)
    return


def normWave(norm_type="-1"):
    shared.postEditPoints.samples = len(shared.originalPoints.x_points)
    shared.postEditPoints.x_points = [0] * shared.postEditPoints.samples
    shared.postEditPoints.y_points = [0] * shared.postEditPoints.samples
    max_point = max(shared.originalPoints.y_points)
    min_point = min(shared.originalPoints.y_points)
    for x in range(shared.postEditPoints.samples):
        shared.postEditPoints.x_points[x] = (shared.originalPoints.x_points[x])
        fraction = (shared.originalPoints.y_points[x] - min_point) / (max_point - min_point)
        if norm_type == "0":
            shared.postEditPoints.y_points[x] = fraction
        elif norm_type == "-1":
            shared.postEditPoints.y_points[x] = 2 * fraction - 1
    menu.createGraph(shared.postEditPoints.x_points, shared.postEditPoints.y_points, "Edited Wave", "Sample", shared.editedWaveCanvas)
    return


def norm1Click():
    normWave("-1")
    return


def norm0Click():
    normWave("0")
    return


def editNormClick():
    editNormCanvas = menu.createCanvas(shared.root, 0.5, 0.45, 0, 0.55)
    menu.createLabel("Normalize:", editNormCanvas, 1, 0.25, 0.1, 0, 0)

    menu.createLabel("Starting Pos:", editNormCanvas, 0, 0.2, 0.1, 0.05, 0.3)
    menu.createEntry(shared.startingPos_var, editNormCanvas, 0.2, 0.1, 0.25, 0.3)
    menu.createButton("-1 to 1", norm1Click, editNormCanvas, 0.2, 0.2, 0.6, 0.6)
    menu.createButton("0 to 1", norm0Click, editNormCanvas, 0.2, 0.2, 0.2, 0.6)
    return


def sumClick():
    shared.postEditPoints.samples = len(shared.originalPoints.x_points)
    shared.postEditPoints.x_points = [0] * shared.postEditPoints.samples
    shared.postEditPoints.y_points = [0] * shared.postEditPoints.samples
    point_sum = 0
    for x in range(shared.postEditPoints.samples):
        shared.postEditPoints.x_points[x] = (shared.originalPoints.x_points[x])
        point_sum = point_sum + shared.originalPoints.y_points[x]
        shared.postEditPoints.y_points[x] = point_sum
    menu.createGraph(shared.postEditPoints.x_points, shared.postEditPoints.y_points, "Edited Wave", "Sample", shared.editedWaveCanvas)
    return


def editSumClick():
    editSumCanvas = menu.createCanvas(shared.root, 0.5, 0.45, 0, 0.55)
    menu.createLabel("Accumulate:", editSumCanvas, 1, 0.25, 0.1, 0, 0)

    menu.createLabel("Starting Pos:", editSumCanvas, 0, 0.2, 0.1, 0.05, 0.3)
    menu.createEntry(shared.startingPos_var, editSumCanvas, 0.2, 0.1, 0.25, 0.3)
    menu.createButton("ACCUMULATE", sumClick, editSumCanvas, 0.2, 0.2, 0.4, 0.6)
    return


def editMenuClick():
    # creates a canvas for edit menu
    editCanvas = menu.createCanvas(shared.root, 0.5, 0.5, 0, 0.5)
    # creates a label on the corner for edit
    menu.createLabel("Edit:", editCanvas, 1, 0.25, 0.1, 0, 0)
    # Buttons for edit menu
    menu.createButton("Add/Sub", editAddClick, editCanvas, 0.2, 0.1, 0.3, 0)
    menu.createButton("Multi", editMulClick, editCanvas, 0.1, 0.1, 0.5, 0)
    menu.createButton("Square", editSqrClick, editCanvas, 0.1, 0.1, 0.6, 0)
    menu.createButton("Normal", editNormClick, editCanvas, 0.1, 0.1, 0.7, 0)
    menu.createButton("Sum", editSumClick, editCanvas, 0.1, 0.1, 0.8, 0)

