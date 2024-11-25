import numpy as np
from files import browseClick, importFile
import menu as menu
import shared as shared

def sharpen(type = 1):
    sharpenedPoints = []
    for x in range(len(shared.originalPoints.x_points)):
        if type == 1:
            if x == 0:
                sharp_point = shared.originalPoints.y_points[x+1] - shared.originalPoints.y_points[x]
            else:
                sharp_point = shared.originalPoints.y_points[x] - shared.originalPoints.y_points[x-1]
        elif type == 2:
            if x == 0:
                sharp_point = shared.originalPoints.y_points[x+2] - (2*shared.originalPoints.y_points[x+1]) + shared.originalPoints.y_points[x]
            elif x >= len(shared.originalPoints.x_points) - 1:
                sharp_point = shared.originalPoints.y_points[x] - (2*shared.originalPoints.y_points[x-1]) + shared.originalPoints.y_points[x-2]
            else:
                sharp_point = shared.originalPoints.y_points[x+1] - (2*shared.originalPoints.y_points[x]) + shared.originalPoints.y_points[x-1]
        
        sharp_point = round(sharp_point,3)
        print(f"Sharpened point at {shared.originalPoints.x_points[x]}: {sharp_point}\n")
        sharpenedPoints.append(sharp_point)
    shared.postEditPoints.x_points = shared.originalPoints.x_points
    shared.postEditPoints.y_points = sharpenedPoints  
    menu.createGraph(shared.postEditPoints.x_points, shared.postEditPoints.y_points, "Sharpened Wave", "Sample", shared.editedWaveCanvas)


def sharpenClick1():
    sharpen(1)


def sharpenClick2():
    sharpen(2)

def sharpenMenuClick():
    sharpenCanvas = menu.createCanvas(shared.root, 0.5, 0.45, 0, 0.55)
    menu.createLabel("Sharpen:", sharpenCanvas, 1, 0.25, 0.1, 0, 0)

    menu.createLabel("Starting Pos:", sharpenCanvas, 0, 0.2, 0.1, 0.05, 0.3)
    menu.createEntry(shared.startingPos_var, sharpenCanvas, 0.2, 0.1, 0.25, 0.3)
    menu.createButton("1st Derivative", sharpenClick1, sharpenCanvas, 0.2, 0.2, 0.2, 0.6)
    menu.createButton("2nd Derivative", sharpenClick2, sharpenCanvas, 0.2, 0.2, 0.4, 0.6)


def changeForm(type = "adv"):
    change = shared.delay_var.get()
    new_pointsX = []
    new_pointsY = []
    print("new points: ")
    for x in range(len(shared.originalPoints.x_points)):
        if type == "adv":
            changed = shared.originalPoints.x_points[x] - change
        if type == "del":
            changed = shared.originalPoints.x_points[x] + change
        new_pointsX.append(changed)
        new_pointsY.append(shared.originalPoints.y_points[x])
        print(f"({new_pointsX[x]},{new_pointsY[x]}) ")

    print("\n")
    shared.postEditPoints.x_points = new_pointsX
    shared.postEditPoints.y_points = new_pointsY
    
    menu.createGraph(shared.postEditPoints.x_points, shared.postEditPoints.y_points, "Changed Wave", "Sample", shared.editedWaveCanvas)

def advanceClick():
    changeForm("adv")

def delayClick():
    changeForm("del")



def delayMenuClick():
    sharpenCanvas = menu.createCanvas(shared.root, 0.5, 0.45, 0, 0.55)
    menu.createLabel("Delay/Advance:", sharpenCanvas, 1, 0.25, 0.1, 0, 0)

    menu.createLabel("Starting Pos:", sharpenCanvas, 0, 0.2, 0.1, 0.05, 0.3)
    menu.createEntry(shared.startingPos_var, sharpenCanvas, 0.2, 0.1, 0.25, 0.3)
    menu.createLabel("Change:", sharpenCanvas, 0, 0.2, 0.1, 0.05, 0.4)
    menu.createEntry(shared.delay_var, sharpenCanvas, 0.2, 0.1, 0.25, 0.4)
    menu.createButton("Advance", advanceClick, sharpenCanvas, 0.2, 0.2, 0.2, 0.6)
    menu.createButton("Delay", delayClick, sharpenCanvas, 0.2, 0.2, 0.4, 0.6)


def shiftLeft(arr = []):
    new_points = []
    for x in range(len(arr)):
        new_points.append(arr[x-1])
    return new_points


def fixPoints(arr = []):
    new_points = []
    new_points.append(round(float(arr[0]),3))
    for x in range (1, len(arr)):
        new_points.append(round(float(arr[0-x]),3))
    return new_points


def correlateClick():
    first = shared.originalPoints
    second = importFile()
    new_points = []
    denominator = sum(np.pow(first.y_points,2)) * sum(np.pow(second.y_points,2))
    denominator =  np.sqrt(denominator)/len(first.x_points)
    for j in range(len(second.x_points)):
        num_sum = 0
        for n in range(len(second.x_points)):
            num_sum += first.y_points[n] * second.y_points[n]
        second.y_points = shiftLeft(second.y_points)
        numerator = num_sum/len(first.x_points)
        new_point = numerator/denominator
        new_points.append(new_point)
    shared.postEditPoints.x_points = first.x_points
    new_points = fixPoints(new_points)
    print(f"{new_points}")
    shared.postEditPoints.y_points = new_points
    menu.createGraph(shared.postEditPoints.x_points, shared.postEditPoints.y_points, "Convolved Wave", "Sample", shared.editedWaveCanvas)



def correlateMenuClick(): 
    correlateCanvas = menu.createCanvas(shared.root, 0.5, 0.45, 0, 0.55)
    menu.createLabel("Correlate", correlateCanvas, 1, 0.25, 0.1, 0, 0)
    menu.createLabel("File:", correlateCanvas, 0, 0.2, 0.1, 0.05, 0.2)
    menu.createEntry(shared.file_var, correlateCanvas, 0.6, 0.1, 0.25, 0.2)

    menu.createButton("Browse", browseClick, correlateCanvas, 0.1, 0.1, 0.8, 0.2)
    
    menu.createButton("Correlate", correlateClick, correlateCanvas, 0.2, 0.1, 0.4, 0.6)


def foldClick():
    new_points = []
    for x in range(len(shared.originalPoints.x_points)):
        point = 0
        for y in range(len(shared.originalPoints.x_points)):
            if shared.originalPoints.x_points[x] == - shared.originalPoints.x_points[y]:
                point = shared.originalPoints.y_points[y]
        new_points.append(point)
    
    shared.postEditPoints.x_points = shared.originalPoints.x_points
    shared.postEditPoints.y_points = new_points
    
    menu.createGraph(shared.postEditPoints.x_points, shared.postEditPoints.y_points, "Changed Wave", "Sample", shared.editedWaveCanvas)



def foldMenuClick():
    sharpenCanvas = menu.createCanvas(shared.root, 0.5, 0.45, 0, 0.55)
    menu.createLabel("Fold:", sharpenCanvas, 1, 0.25, 0.1, 0, 0)

    menu.createLabel("Starting Pos:", sharpenCanvas, 0, 0.2, 0.1, 0.05, 0.3)
    menu.createEntry(shared.startingPos_var, sharpenCanvas, 0.2, 0.1, 0.25, 0.3)
    menu.createButton("Fold", foldClick, sharpenCanvas, 0.2, 0.2, 0.4, 0.6)


def convolveClick():
    first = shared.originalPoints
    second = importFile()
    new_points = np.convolve(first.y_points,second.y_points,mode="full")
    min_point = min(min(first.x_points),min(second.x_points))
    max_point = min_point + len(first.x_points) + len(second.x_points) - 1
    shared.postEditPoints.x_points = range(min_point,max_point)
    shared.postEditPoints.y_points = new_points
    menu.createGraph(shared.postEditPoints.x_points, shared.postEditPoints.y_points, "Convolved Wave", "Sample", shared.editedWaveCanvas)


def convolveMenuClick():
    convolveCanvas = menu.createCanvas(shared.root, 0.5, 0.45, 0, 0.55)
    menu.createLabel("Convolve", convolveCanvas, 1, 0.25, 0.1, 0, 0)
    menu.createLabel("File:", convolveCanvas, 0, 0.2, 0.1, 0.05, 0.2)
    menu.createEntry(shared.file_var, convolveCanvas, 0.6, 0.1, 0.25, 0.2)

    menu.createButton("Browse", browseClick, convolveCanvas, 0.1, 0.1, 0.8, 0.2)
    
    menu.createButton("Convolve", convolveClick, convolveCanvas, 0.2, 0.1, 0.4, 0.6)


def rmvDCClick():
    new_points = []
    mean = sum(shared.originalPoints.y_points)/len(shared.originalPoints.y_points)
    for x in range(len(shared.originalPoints.x_points)):
        new_points.append(shared.originalPoints.y_points[x] - mean)
    shared.postEditPoints.x_points = shared.originalPoints.x_points
    shared.postEditPoints.y_points = new_points
    menu.createGraph(shared.postEditPoints.x_points, shared.postEditPoints.y_points, "Removed DC Wave", "Sample", shared.editedWaveCanvas)


def rmvDCMenuClick():
    rmvDCCanvas = menu.createCanvas(shared.root, 0.5, 0.45, 0, 0.55)
    menu.createLabel("Remove DC:", rmvDCCanvas, 1, 0.25, 0.1, 0, 0)

    menu.createLabel("Starting Pos:", rmvDCCanvas, 0, 0.2, 0.1, 0.05, 0.3)
    menu.createEntry(shared.startingPos_var, rmvDCCanvas, 0.2, 0.1, 0.25, 0.3)
    menu.createButton("Remove DC", rmvDCClick, rmvDCCanvas, 0.2, 0.2, 0.4, 0.6)


def smoothClick():
    new_points = []
    window_size = shared.amp_var.get()
    for n in range(len(shared.originalPoints.x_points) - window_size + 1):
        num_sum = 0
        for k in range(window_size):
            num_sum += shared.originalPoints.y_points[n+k]
        new_points.append(num_sum / window_size)
    shared.postEditPoints.x_points = shared.originalPoints.x_points
    shared.postEditPoints.y_points = new_points
    menu.createGraph(shared.postEditPoints.x_points, shared.postEditPoints.y_points, "Removed DC Wave", "Sample", shared.editedWaveCanvas)
    

def smoothMenuClick():
    smoothCanvas = menu.createCanvas(shared.root, 0.5, 0.45, 0, 0.55)
    menu.createLabel("Smooth:", smoothCanvas, 1, 0.25, 0.1, 0, 0)

    menu.createLabel("Starting Pos:", smoothCanvas, 0, 0.2, 0.1, 0.05, 0.3)
    menu.createEntry(shared.startingPos_var, smoothCanvas, 0.2, 0.1, 0.25, 0.3)
    menu.createLabel("Window Size:", smoothCanvas, 0, 0.2, 0.1, 0.05, 0.3)
    menu.createEntry(shared.amp_var, smoothCanvas, 0.2, 0.1, 0.25, 0.3)
    menu.createButton("Smooth", smoothClick, smoothCanvas, 0.2, 0.2, 0.4, 0.6)


def timeMenuClick():
    # creates a canvas for edit menu
    editCanvas = menu.createCanvas(shared.root, 0.5, 0.5, 0, 0.5)
    # creates a label on the corner for edit
    menu.createLabel("Edit:", editCanvas, 1, 0.25, 0.1, 0, 0)
    # Buttons for edit menu
    menu.createButton("Sharpen", sharpenMenuClick, editCanvas, 0.1, 0.1, 0.25, 0)
    menu.createButton("Smooth", smoothMenuClick, editCanvas, 0.1, 0.1, 0.35, 0)
    menu.createButton("Delay", delayMenuClick, editCanvas, 0.1, 0.1, 0.45, 0)
    menu.createButton("Correlate", correlateMenuClick, editCanvas, 0.1, 0.1, 0.55, 0)
    menu.createButton("Fold", foldMenuClick, editCanvas, 0.1, 0.1, 0.65, 0)
    menu.createButton("Convolve", convolveMenuClick, editCanvas, 0.1, 0.1, 0.75, 0)
    menu.createButton("RMV DC", rmvDCMenuClick, editCanvas, 0.1, 0.1, 0.85, 0)