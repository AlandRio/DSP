import menu as menu
import points as points
import shared as shared

def generateClick():
    # using the input the user gave in generate function changes the global original wave object
    shared.originalWave = points.Wave(shared.type_var.get(), shared.amp_var.get(), shared.theta_var.get(), shared.sampleFreq_var.get(), shared.freq_var.get())
    # calls the generate points function and puts the points generated into global original wave points
    shared.originalPoints = points.generatePoints(shared.originalWave, shared.startingPos_var.get())
    shared.originalPoints.samples = len(shared.originalPoints.x_points)
    menu.createGraph(shared.originalPoints.x_points, shared.originalPoints.y_points, "Original Graph", "Sample", shared.originalWaveCanvas)


def generateMenuClick():
    shared.type_var.set("cos")
    generateCanvas = menu.createCanvas(shared.root, 0.5, 0.5, 0, 0.5)
    menu.createLabel("Generate:", generateCanvas, 1, 0.25, 0.1, 0, 0)

    menu.createLabel("Sin():", generateCanvas, 0, 0.2, 0.1, 0.1, 0.1)
    menu.createCheck(shared.quantype_var,"sin","cos",generateCanvas,0.3,0.1)
    menu.createLabel("Amplitude:", generateCanvas, 0, 0.2, 0.1, 0.1, 0.2)
    menu.createEntry(shared.amp_var, generateCanvas, 0.6, 0.1, 0.3, 0.2)
    menu.createLabel("Starting Pos:", generateCanvas, 0, 0.2, 0.1, 0.1, 0.3)
    menu.createEntry(shared.startingPos_var, generateCanvas, 0.6, 0.1, 0.3, 0.3)
    menu.createLabel("Theta:", generateCanvas, 0, 0.2, 0.1, 0.1, 0.4)
    menu.createEntry(shared.theta_var, generateCanvas, 0.6, 0.1, 0.3, 0.4)
    menu.createLabel("Sample Frequency:", generateCanvas, 0, 0.2, 0.1, 0.1, 0.5)
    menu.createEntry(shared.sampleFreq_var, generateCanvas, 0.6, 0.1, 0.3, 0.5)
    menu.createLabel("Frequency:", generateCanvas, 0, 0.2, 0.1, 0.1, 0.6)
    menu.createEntry(shared.freq_var, generateCanvas, 0.6, 0.1, 0.3, 0.6)

    menu.createButton("Generate", generateClick, generateCanvas, 0.2, 0.1, 0.4, 0.9)
