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


def timeMenuClick():
    # creates a canvas for edit menu
    editCanvas = menu.createCanvas(shared.root, 0.5, 0.5, 0, 0.5)
    # creates a label on the corner for edit
    menu.createLabel("Edit:", editCanvas, 1, 0.25, 0.1, 0, 0)
    # Buttons for edit menu
    menu.createButton("Sharpen", sharpenMenuClick, editCanvas, 0.1, 0.1, 0.4, 0)
    menu.createButton("Delay/Adv", delayMenuClick, editCanvas, 0.2, 0.1, 0.5, 0)
    menu.createButton("Fold", foldMenuClick, editCanvas, 0.1, 0.1, 0.7, 0)