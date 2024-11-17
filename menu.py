import tkinter as tk
import math as math
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import shared as shared

def createCanvas(canvas, relwidth, relheight, relx, rely):
    width = shared.root.winfo_width()
    height = shared.root.winfo_height()
    canvas = tk.Canvas(canvas, width=width, height=height, highlightthickness=2, highlightbackground="green")
    canvas.configure(bg="black")
    canvas.place(relwidth=relwidth, relheight=relheight, relx=relx, rely=rely)
    return canvas


def createLabel(label, canvas, highlight, relwidth, relheight, relx, rely):
    originalFunctionLabel = tk.Label(canvas, text=label, fg="green", bg="black")
    if highlight == 1:
        originalFunctionLabel.configure(highlightthickness=2, highlightbackground="green")
    originalFunctionLabel.place(relwidth=relwidth, relheight=relheight, relx=relx, rely=rely)


def createEntry(var, canvas, relwidth, relheight, relx, rely):
    entry = tk.Entry(canvas, textvariable=var)
    entry.place(relwidth=relwidth, relheight=relheight, relx=relx, rely=rely)


def createButton(label, func, canvas, relwidth, relheight, relx, rely):
    Border = tk.Frame(canvas, bd=0, highlightthickness=2, highlightcolor="green", highlightbackground="green")
    Button = tk.Button(Border, text=label, command=func, width='20')
    Button.configure(fg="green", bg="black", bd=0, borderwidth=0)
    Border.place(relwidth=relwidth, relheight=relheight, relx=relx, rely=rely)
    Button.place(relwidth=1, relheight=1, relx=0, rely=0)


def createGraph(points_x, points_y, graph_label, x_label, canvas):
    shownPoints_X = []
    shownPoints_Y = []
    i = 0
    if shared.startingPos_var.get() >= min(points_x) or shared.startingPos_var.get() < max(points_x):
        i = points_x.index(shared.startingPos_var.get())
    for x in range(40):
        try:
            shownPoints_X.append(points_x[i + x])
            shownPoints_Y.append(points_y[i + x])
        except IndexError:
            break
    
    fig, ax = plt.subplots()  # creates a figure in fig and sub-plots in ax
    # plots the graph using the original points object
    ax.scatter(shownPoints_X, shownPoints_Y, color="darkgreen")
    ax.axhline(y=0, color='black', linewidth=0.8)
    ax.set_title(graph_label)
    ax.set_xlabel(x_label)
    ax.set_ylabel("Amplitude")
    # creates a graph gui in original wave canvas then draws the graph and places it
    
    originalGraph = FigureCanvasTkAgg(fig, master=canvas)
    originalGraph.draw()
    originalGraph.get_tk_widget().place(relwidth=1, relheight=0.9, relx=0, rely=0.1)


def createCheck(var,onvalue,offvalue,canvas,relx,rely):
    check = tk.Checkbutton(canvas, variable=var, onvalue=onvalue, offvalue=offvalue, bg="black")
    check.place(relwidth=0.05, relheight=0.1, relx=relx, rely=rely)

