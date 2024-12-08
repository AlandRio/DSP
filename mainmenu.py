

import matplotlib.pyplot as plt
from check import compareMenuClick
from filters import filtersMenuClick
from freq import convertMenuClick, quantizeMenuClick
from generate import generateMenuClick
from files import editedExportClick, importMenuClick, originalExportClick
import menu as menu
import shared as shared
from edit import editMenuClick
from time_domain import timeMenuClick


def quitClick():
    shared.root.destroy()

def swapClick():
    originalPointsVar = shared.originalPoints
    originalWaveVar = shared.originalWave
    editedPointsVar = shared.postEditPoints
    editedWaveVar = shared.editedWave
    shared.originalPoints = editedPointsVar
    shared.originalWave = editedWaveVar
    shared.postEditPoints = originalPointsVar
    shared.editedWave = originalWaveVar

    menu.createGraph(shared.originalPoints.x_points, shared.originalPoints.y_points, "Original Wave", "Sample", shared.originalWaveCanvas)
    menu.createGraph(shared.postEditPoints.x_points, shared.postEditPoints.y_points, "Edited Wave", "Sample", shared.editedWaveCanvas)

def dark_mode():
    if shared.dark_mode == 0:
        shared.dark_mode = 1
        menu.bg.set("black")
        menu.fg.set("green")
        shared.dark_var.set("⋆⁺₊ 𖤓 ₊⋆")
        plt.style.use("dark_background")

    elif shared.dark_mode == 1:
        shared.dark_mode = 0
        shared.dark_var.set("⋆⁺₊ ☾⋆⁺₊⋆")
        menu.bg.set("white")
        menu.fg.set("black")
        plt.style.use('default')
    for canvas in shared.canvases:
        canvas.config(bg = menu.bg.get())
        canvas.config(highlightbackground=menu.fg.get())
    for button in shared.buttons:
        button.config(bg = menu.bg.get())
        button.config(fg = menu.fg.get())
    for label in shared.labels:
        label.config(bg = menu.bg.get())
        label.config(fg = menu.fg.get())
    for high in shared.high_labels:
        high.config(highlightbackground=menu.fg.get())
    for border in shared.borders:
        border.config(highlightcolor=menu.fg.get(), highlightbackground=menu.fg.get())



def createMain():
    # Creating and defining Root Window for the app
    shared.root.title("Digital Signal Processing")
    shared.root.minsize(1280, 720)
    shared.root.configure(bg=menu.bg.get())

    # Creating Canvases
    shared.menuCanvas = menu.createCanvas(shared.root, 0.5, 0.5, 0, 0)
    shared.originalWaveCanvas = menu.createCanvas(shared.root, 0.5, 0.5, 0.5, 0)
    shared.editedWaveCanvas = menu.createCanvas(shared.root, 0.5, 0.5, 0.5, 0.5)
    menu.createCanvas(shared.root, 0.5, 0.5, 0, 0.5)

    # Changes the style of the graph to have a dark background
    plt.style.use("dark_background")
    # Creating dark mode button
    shared.dark_var.set("⋆⁺₊ ☾⋆⁺₊⋆")
    menu.createButton(shared.dark_var.get(), dark_mode, shared.menuCanvas, 0.25, 0.1, 0, 0)
    # Creating Label
    menu.createLabel("Dsp - Section 1", shared.menuCanvas, 1, 0.25, 0.1, 0.375, 0)
    menu.createLabel("Original Wave:", shared.originalWaveCanvas, 1, 0.25, 0.1, 0, 0)
    menu.createLabel("Edited Wave:", shared.editedWaveCanvas, 1, 0.25, 0.1, 0, 0)
    # Creating Buttons
    menu.createButton("Export", originalExportClick, shared.originalWaveCanvas, 0.25, 0.1, 0.75, 0)
    menu.createButton("Export", editedExportClick, shared.editedWaveCanvas, 0.25, 0.1, 0.75, 0)

    menu.createButton("Swap Graphs", swapClick, shared.menuCanvas, 0.25, 0.1, 0.75, 0.55)

    shared.export_var.set(40)
    menu.createLabel("How many to export:", shared.menuCanvas, 0, 0.25, 0.1, 0.65, 0.2)
    menu.createEntry(shared.export_var,shared.menuCanvas, 0.1, 0.1, 0.895, 0.2)
    menu.createLabel("Starting var to export:", shared.menuCanvas, 0, 0.25, 0.1, 0.65, 0.3)
    menu.createEntry(shared.startingPos_var,shared.menuCanvas, 0.1, 0.1, 0.895, 0.3)

    menu.createButton("Import", importMenuClick, shared.menuCanvas, 0.25, 0.1, 0, 0.1)
    menu.createButton("Filters", filtersMenuClick, shared.menuCanvas, 0.25, 0.1, 0, 0.2)
    menu.createButton("Generate", generateMenuClick, shared.menuCanvas, 0.25, 0.1, 0, 0.3)
    menu.createButton("Quantize", quantizeMenuClick, shared.menuCanvas, 0.25, 0.1, 0, 0.4)
    menu.createButton("Frequency Domain", convertMenuClick, shared.menuCanvas, 0.25, 0.1, 0, 0.5)
    menu.createButton("Time Domain", timeMenuClick, shared.menuCanvas, 0.25, 0.1, 0, 0.6)
    menu.createButton("Edit", editMenuClick, shared.menuCanvas, 0.25, 0.1, 0, 0.7)
    menu.createButton("Compare", compareMenuClick, shared.menuCanvas, 0.25, 0.1, 0, 0.8)
    menu.createButton("Quit", quitClick, shared.menuCanvas, 0.25, 0.1, 0, 0.9)