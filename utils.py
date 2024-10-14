
import numpy as np


class Wave:
    def __init__(self, type, amp, theta, sampleNum, sampleFreq, freq):
        self.type = type
        self.amp = amp
        self.sampleNum = sampleNum
        self.theta = theta
        self.sampleFreq = sampleFreq
        self.freq = freq

def generatePoints(wave):
        points = [0]*wave.sampleNum.get()
        for x in range(wave.sampleNum.get()):
            insideCos = 0;
            if (wave.type.get() == "sin"):
                insideInsideCos = (2 * np.pi * x * wave.freq.get()) / wave.sampleFreq.get()
                insideCos = np.sin(insideInsideCos + np.radians(wave.theta.get()))
            else:
                insideInsideCos = (2 * np.pi * x * wave.freq.get()) / wave.sampleFreq.get()
                insideCos = np.cos(insideInsideCos + np.radians(wave.theta.get()))
            posY = wave.amp.get() * insideCos
            points[x] = posY
        return points