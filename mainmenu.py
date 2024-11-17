

import matplotlib.pyplot as plt
from check import compareMenuClick
from freq import convertMenuClick, quantizeMenuClick
from generate import generateMenuClick
from files import editedExportClick, importMenuClick, originalExportClick
import menu as menu
import shared as shared
from time_domain import editMenuClick

def quitClick():
    shared.root.destroy()

def createMain():
    # Creating and defining Root Window for the app
    shared.root.title("Digital Signal Processing")
    shared.root.minsize(1280, 720)
    shared.root.configure(bg='black')

    # Creating Canvases
    shared.menuCanvas = menu.createCanvas(shared.root, 0.5, 0.5, 0, 0)
    shared.originalWaveCanvas = menu.createCanvas(shared.root, 0.5, 0.5, 0.5, 0)
    shared.editedWaveCanvas = menu.createCanvas(shared.root, 0.5, 0.5, 0.5, 0.5)
    menu.createCanvas(shared.root, 0.5, 0.5, 0, 0.5)

    # Changes the style of the graph to have a dark background
    plt.style.use("dark_background")
    
    # Creating Label
    menu.createLabel("Dsp - Section 1", shared.menuCanvas, 1, 0.25, 0.1, 0.375, 0)
    menu.createLabel("Original Wave:", shared.originalWaveCanvas, 1, 0.25, 0.1, 0, 0)
    menu.createLabel("Edited Wave:", shared.editedWaveCanvas, 1, 0.25, 0.1, 0, 0)
    # Creating Buttons
    menu.createButton("Export", originalExportClick, shared.originalWaveCanvas, 0.25, 0.1, 0.75, 0)
    menu.createButton("Export", editedExportClick, shared.editedWaveCanvas, 0.25, 0.1, 0.75, 0)
    menu.createButton("Import", importMenuClick, shared.menuCanvas, 0.25, 0.1, 0, 0.2)
    menu.createButton("Generate", generateMenuClick, shared.menuCanvas, 0.25, 0.1, 0, 0.3)
    menu.createButton("Quantize", quantizeMenuClick, shared.menuCanvas, 0.25, 0.1, 0, 0.4)
    menu.createButton("Convert", convertMenuClick, shared.menuCanvas, 0.25, 0.1, 0, 0.5)
    menu.createButton("Edit", editMenuClick, shared.menuCanvas, 0.25, 0.1, 0, 0.6)
    menu.createButton("Compare", compareMenuClick, shared.menuCanvas, 0.25, 0.1, 0, 0.7)
    menu.createButton("Quit", quitClick, shared.menuCanvas, 0.25, 0.1, 0, 0.8)