import tkinter as tk
import points as points



root = tk.Tk()

# Defining Global tk Variables
# Useful for dynamic variable that can be changed by user (used with setters and taken with getters)

sampleFreq_var = tk.DoubleVar()
cutFreq_var = tk.DoubleVar()
firstFreq_var = tk.DoubleVar()
secondFreq_var = tk.DoubleVar()
stopAtten_var = tk.IntVar()
transBand_var = tk.DoubleVar()

type_var = tk.StringVar()
dark_var = tk.StringVar()
file_var = tk.StringVar()
amp_var = tk.IntVar()
startingPos_var = tk.IntVar()
theta_var = tk.DoubleVar()
freq_var = tk.DoubleVar()
originalFunctionString = tk.StringVar()
line_var = tk.StringVar()
quantype_var = tk.StringVar()
remove_DC_var = tk.IntVar()
quanum_var = tk.IntVar()
export_var = tk.IntVar()
delay_var = tk.IntVar()
dark_mode = 1

# Defining Global Objects for Original Graph and Edited Graph
originalPoints = points.Points()
originalWave = points.Wave()
editedWave = points.Wave()
postEditPoints = points.Points()
quantizedPoints = points.quantPoints()
convertPoints = points.freqPoints()



# Creating Canvases then configuring its background then placing it on the window
canvases = []
buttons = []
borders = []
labels = []
high_labels = []
menuCanvas = tk.Canvas()
originalWaveCanvas = tk.Canvas()
editedWaveCanvas = tk.Canvas()
canvases.append(menuCanvas)
canvases.append(originalWaveCanvas)
canvases.append(editedWaveCanvas)