import menu as menu
import shared as shared

def sharpenClick():
    return

def sharpenMenuClick():
    sharepnCanvas = menu.createCanvas(shared.root, 0.5, 0.45, 0, 0.55)
    menu.createLabel("Sharpen:", sharepnCanvas, 1, 0.25, 0.1, 0, 0)

    menu.createLabel("Starting Pos:", sharepnCanvas, 0, 0.2, 0.1, 0.05, 0.3)
    menu.createEntry(shared.startingPos_var, sharepnCanvas, 0.2, 0.1, 0.25, 0.3)
    menu.createButton("SHARPEN", sharpenClick, sharepnCanvas, 0.2, 0.2, 0.4, 0.6)
    return


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