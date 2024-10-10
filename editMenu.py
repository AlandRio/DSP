from tkinter import *
def createEditMenu(root):
    root.update()
    width = 0.5*root.winfo_width()
    height = 0.5*root.winfo_height()
    editCanvas = Canvas(root, width=width,height=height,highlightthickness=2,highlightbackground="green")
    editCanvas.configure(bg="grey")
    return editCanvas