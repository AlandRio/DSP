from tkinter import *

def importFromFile(filePath):
    file = open(filePath)

def createImportMenu(root):
    width = 0.5*root.winfo_width()
    height = 0.5*root.winfo_height()
    importCanvas = Canvas(root, width=width,height=height,highlightthickness=2,highlightbackground="green")
    importCanvas.configure(bg="black")
    return importCanvas