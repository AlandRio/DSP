import numpy as np

class Wave:  # class for wave used in generate
    def __init__(self, trigFunc="cos", amp=1, theta=0.0, sampleFreq=2.0,
                 freq=1.0):  # initializes class with default arguments
        self.trigFunc = trigFunc  # Wither the function is sin or cos
        self.amp = amp  # Amplitude
        self.theta = theta  # Phase shift
        self.sampleFreq = sampleFreq  # Sample Frequency
        self.freq = freq  # Frequency


class Points:  # class for storing points
    def __init__(self, x_points=[], y_points=[], signalType=0, isPeriodic=1, samples=1000):
        self.x_points = x_points  # Points on the X-Axis
        self.y_points = y_points  # Points on the Y-Axis
        self.signalType = signalType  # Wither the signal is Time (0) or Frequency (1)
        self.isPeriodic = isPeriodic  # Wither the signal is Non-Periodic (0) or Periodic (1)
        self.samples = samples


class quantPoints:
    def __init__(self,points = Points(),err = [], levels = [],levelsBin = []):
        self.points = points,
        self.err = err,
        self.levels = levels
        self.levelsBin = levelsBin

class freqPoints:
    def __init__(self,points = [], phasePoints = [], ampPoints = []):
        self.fundFreq = points,
        self.phasePoints = phasePoints,
        self.ampPoints = ampPoints



# functions to optimize code
def getBin(n,l):
    binary = bin(n).split("b")
    length = l - len(binary[1])
    binaryString = ""
    if length > 0:
        for x in range (length):
            binaryString = binaryString + "0"
    binaryString = binaryString + binary[1]
    return binaryString

def generatePoints(wave, startingPos):
    pointsX = []  # initializes an array of 40 indexes
    pointsY = []  # initializes an array of 40 indexes
    for x in range(1000):
        insideCos = 0  # function for the value inside the Cos or Sin
        if wave.trigFunc == "sin":  # if trigFunc is sin will use the sin version of the equation
            insideInsideCos = (2 * np.pi * startingPos * wave.freq) / wave.sampleFreq
            insideCos = np.sin(
                insideInsideCos + np.radians(wave.theta))  # splitting up the function to make it easier to read
        elif wave.trigFunc == "cos":  # if trigFunc is sin will use the sin version of the equation
            insideInsideCos = (2 * np.pi * startingPos * wave.freq) / wave.sampleFreq
            insideCos = np.cos(
                insideInsideCos + np.radians(wave.theta))  # splitting up the function to make it easier to read
        posY = wave.amp * insideCos  # Multiplies amplitude by the
        pointsY.append(posY)  # adds the point at Y to the array to the y-axis
        pointsX.append(startingPos)  # adds the starting point to the x-axis
        startingPos += 1  # increment starting point by 1
    points = Points(pointsX, pointsY)  # adds the values into a class for easier management
    return points  # returns an array of points for graph

