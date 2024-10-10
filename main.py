# Library for GUI
from tkinter import *

def generateMenuClick():
    print("hi")
def importMenuClick():
    print("hi")

# Creating and defining Root Window
root = Tk()
root.title("Digital Signal Processing")
root.iconbitmap("wave-sine.ico")
root.minsize(854,480)
root.configure(bg='black')
menuCanvas = Canvas(root)
menuCanvas.configure(bg="black")
menuCanvas.grid(row=0,column=0)

# Creating Label
menuName = Label(menuCanvas, text="DSP")
menuName.configure(fg="green", bg="black")

# Creating Buttons
importButton = Button(menuCanvas, text="Import",command=importMenuClick,width='20', borderwidth=3, relief="solid")
importButton.configure(fg="green", bg="black")
generateButton = Button(menuCanvas, text="Generate",command= generateMenuClick,width='20',borderwidth=3, relief="solid")
generateButton.configure(fg="green", bg="black")

# Putting content on screen
menuName.grid(row=1,column=0, padx=50,pady= 20)
importButton.grid(row=2, column = 0,padx=50,pady= 40)
generateButton.grid(row=3, column = 0,padx=50,pady= 40)

root.mainloop()
