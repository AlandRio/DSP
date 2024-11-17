import menu as menu
import shared as shared

def sharpen(type = 1):
    sharpenedPoints = []
    sharpenedPoints.append(shared.originalPoints.y_points[0])
    for x in range(len(shared.originalPoints.x_points)):
        sharp_point = 0
        try:
            if type == 1:
                sharp_point = shared.originalPoints.y_points[x] - shared.originalPoints.y_points[x-1]
            elif type == 2:
                sharp_point = shared.originalPoints.y_points[x+1] - (2*shared.originalPoints.y_points[x]) + shared.originalPoints.y_points[x-1]
        except IndexError:
            sharp_point = shared.originalPoints.y_points[x]
        sharp_point = round(sharp_point,3)
        print(f"Sharpened point at {shared.originalPoints.x_points[x]}: {sharp_point}\n")
        sharpenedPoints.append(sharp_point)
    shared.postEditPoints.x_points = shared.originalPoints.x_points
    shared.postEditPoints.y_points = sharpenedPoints  
    menu.createGraph(shared.postEditPoints.x_points, shared.postEditPoints.y_points, "1st Derivative Wave", "Sample", shared.editedWaveCanvas)


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


def delayMenuClick():
    return


def foldMenuClick():
    return


def timeMenuClick():
    # creates a canvas for edit menu
    editCanvas = menu.createCanvas(shared.root, 0.5, 0.5, 0, 0.5)
    # creates a label on the corner for edit
    menu.createLabel("Edit:", editCanvas, 1, 0.25, 0.1, 0, 0)
    # Buttons for edit menu
    menu.createButton("Sharpen", sharpenMenuClick, editCanvas, 0.1, 0.1, 0.4, 0)
    menu.createButton("Delay/Adv", delayMenuClick, editCanvas, 0.2, 0.1, 0.5, 0)
    menu.createButton("Fold", foldMenuClick, editCanvas, 0.1, 0.1, 0.7, 0)