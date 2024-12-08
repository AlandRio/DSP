import math as math

import numpy as np
from files import browseClick, freqFromFile
import points as points
import shared as shared
import menu as menu

def quantClick():
    points_x = []
    points_y = []
    levels = 0
    bits = 0
    if shared.quantype_var.get() == "levels":
        levels = shared.quanum_var.get()
        bits = math.ceil(math.log2(shared.quanum_var.get()))
    elif shared.quantype_var.get() == "bits":
        levels = pow(2,shared.quanum_var.get())
        bits = shared.quanum_var.get()
    print(f"\nLevels: {levels}\n")
    min_point = min(shared.originalPoints.y_points)
    max_point = max(shared.originalPoints.y_points)
    jump = max_point - min_point
    jumpPerLvl = jump / (levels)
    ranges_arr = []
    levels_arr = []
    levelDec_arr = []
    levelBin_arr = []
    error_arr = []
    for x in range(levels + 1):
        ranges_arr.append(round(min_point + (jumpPerLvl*x),3))
        print(f"{ranges_arr[x]}")
    for x in range(levels):
        approx_y = round((ranges_arr[x] + ranges_arr[x + 1])/2,3)
        levels_arr.append(approx_y)
        print(f"Level: ")
    for x in range(len(shared.originalPoints.x_points)):
        for y in range(levels):
            if shared.originalPoints.y_points[x] >= ranges_arr[y] and shared.originalPoints.y_points[x] <= ranges_arr[y + 1]:
                points_x.append(shared.originalPoints.x_points[x])
                points_y.append(levels_arr[y])
                levelDec_arr.append(y + 1)
                levelBin_arr.append(points.getBin(y,bits))
                error_arr.append(round(points_y[x] - shared.originalPoints.y_points[x],3))
                print(f"{levelBin_arr[x]}: ({shared.originalPoints.x_points[x]},{points_y[x]}) and Error = {error_arr[x]}")
                break
    shared.quantizedPoints.points = points.Points(points_x,points_y,shared.originalPoints.signalType,shared.originalPoints.isPeriodic,shared.originalPoints.samples)
    shared.quantizedPoints.levelsBin = levelBin_arr
    shared.quantizedPoints.levels = levelDec_arr
    shared.quantizedPoints.err = error_arr
    shared.postEditPoints = shared.quantizedPoints.points
    menu.createGraph(points_x,points_y,"Quantized Graph","Sample",shared.editedWaveCanvas)
    

def quantizeMenuClick():
    shared.quantype_var.set("levels")
    quantCanvas = menu.createCanvas(shared.root, 0.5, 0.5, 0, 0.5)
    menu.createLabel("Quantize:", quantCanvas, 1, 0.25, 0.1, 0, 0)

    menu.createLabel("Bits?", quantCanvas, 0, 0.15, 0.1, 0.1, 0.2)
    menu.createCheck(shared.quantype_var,"bits","levels",quantCanvas,0.25,0.2)
    menu.createEntry(shared.quanum_var, quantCanvas, 0.6, 0.1, 0.3, 0.2)
    menu.createLabel("Starting Pos:", quantCanvas, 0, 0.2, 0.1, 0.1, 0.3)
    menu.createEntry(shared.startingPos_var, quantCanvas, 0.6, 0.1, 0.3, 0.3)

    menu.createButton("QUANTIZE", quantClick, quantCanvas, 0.2, 0.2, 0.4, 0.5)



def convertFreq():
    amps = []
    phases = []
    fundFreqs = []
    y_points = []
    samp_freq = shared.sampleFreq_var.get()
    nums = len(shared.originalPoints.x_points)
    fund_freq = (2*np.pi)/(nums*(1/samp_freq))
    y_points = shared.originalPoints.y_points
    for x in range(nums):
        real_sum = 0
        imaginary_sum = 0
        for n in range(nums):
            exponent = (-2*np.pi*x*n) / nums
            real_sum = real_sum + y_points[n] * np.cos(exponent)
            imaginary_sum = imaginary_sum + y_points[n] * np.sin(exponent)
        real = np.sum(real_sum)
        imaginary = np.sum(imaginary_sum)
        amp = np.sqrt(np.pow(real, 2) + np.pow(imaginary,2))
        phase = np.atan2(imaginary, real)
        amps.append(amp)
        phases.append(phase)
        fundFreqs.append(fund_freq*x)
        print(f"{x}/{fundFreqs[x]}: amp is {amps[x]} and phase is {phases[x]}")
    if shared.remove_DC_var.get() != 0:
        amps[0] = 0
        phases[0] = 0
    shared.convertPoints.ampPoints = amps
    shared.convertPoints.fundFreq = fundFreqs
    shared.convertPoints.phasePoints = phases
    shared.postEditPoints.x_points = amps
    shared.postEditPoints.y_points = phases
            

def phaseGraph():
    convertFreq()
    menu.createGraph(shared.convertPoints.fundFreq,shared.convertPoints.phasePoints,"Polar Graph","Frequency",shared.editedWaveCanvas)


def ampGraph():
    convertFreq()
    menu.createGraph(shared.convertPoints.fundFreq,shared.convertPoints.ampPoints,"Amplitude Graph","Frequency",shared.editedWaveCanvas)


def DFTMenu():
    DFTCanvas = menu.createCanvas(shared.root, 0.5, 0.45, 0, 0.55)
    menu.createLabel("DFT:", DFTCanvas, 1, 0.25, 0.1, 0, 0)

    menu.createLabel("Sampling Frequency:", DFTCanvas, 0, 0.2, 0.1, 0.25, 0.3)
    menu.createEntry(shared.sampleFreq_var, DFTCanvas, 0.2, 0.1, 0.5, 0.3)
    menu.createLabel("Remove DC?:", DFTCanvas, 0, 0.2, 0.1, 0.25, 0.4)
    shared.remove_DC_var.set(0)
    menu.createCheck(shared.remove_DC_var,1,0,DFTCanvas,0.5,0.4)

    menu.createButton("Polar Graph", phaseGraph, DFTCanvas, 0.2, 0.1, 0.25, 0.6)
    menu.createButton("Amp Graph", ampGraph, DFTCanvas, 0.2, 0.1, 0.5, 0.6)



def idftFreq(amp_points, phase_points, samples):
    y = []
    for x in range(samples):
        real_sum = 0
        img_sum = 0
        for n in range(samples):
            amp = amp_points[n]
            phase = phase_points[n]
            real = amp * np.cos(phase)
            imaginary = amp * np.sin(phase)
            exponent = 2*np.pi*x*n
            exponent = exponent/samples
            real = real * np.cos(exponent) / samples
            imaginary = imaginary * np.sin(exponent) / samples
            real_sum = real_sum + real
            img_sum = img_sum + imaginary
        real_sum = round(real_sum,8)
        img_sum = round(img_sum, 8)
        total = real_sum + img_sum
        y.append(total)
    y_points = []
    x_points = []
    y_points.append(round(y[0],4))
    for x in range(samples):
        if x > 0:
            y_points.append(round(y[samples-x],4))
    for x in range(samples):
        x_points.append(x)
        print(f"{x}: {y_points[x]}")
    shared.originalPoints.x_points = x_points
    shared.originalPoints.y_points = y_points
    
    menu.createGraph(x_points,y_points,"IDFT Graph","samples",shared.originalWaveCanvas)


def importFreq():
    amp_points, phase_points, samples = freqFromFile()
    idftFreq(amp_points,phase_points,samples)


def idftClick():
    idftFreq(shared.postEditPoints.x_points,shared.postEditPoints.y_points,len(shared.convertPoints.ampPoints))


def IDFTMenu():
    IDFTCanvas = menu.createCanvas(shared.root, 0.5, 0.45, 0, 0.55)
    menu.createLabel("IDFT:", IDFTCanvas, 1, 0.25, 0.1, 0, 0)
    menu.createLabel("File:", IDFTCanvas, 0, 0.2, 0.1, 0.05, 0.2)
    menu.createEntry(shared.file_var, IDFTCanvas, 0.6, 0.1, 0.25, 0.2)

    menu.createButton("Browse", browseClick, IDFTCanvas, 0.1, 0.1, 0.8, 0.2)
    
    menu.createButton("Import Freq", importFreq, IDFTCanvas, 0.2, 0.1, 0.2, 0.6)
    menu.createButton("IDFT", importFreq, IDFTCanvas, 0.2, 0.1, 0.6, 0.6)


def DCTGraph():
    new_points = []
    samples = len(shared.originalPoints.x_points)
    normalize = np.sqrt(2/samples)
    for k in range(samples):
        new_point = 0
        inside_cos = 0
        for n in range(samples):
            inside_cos = (np.pi/(4*samples)) * (2*n - 1) * (2*k-1)
            inside_cos = np.cos(inside_cos)
            new_point += shared.originalPoints.y_points[n] * inside_cos
        new_point = round(new_point * normalize,9)
        print(f"Point at {k}: {new_point}")
        new_points.append(new_point)
    print("\n")
    shared.postEditPoints.x_points = shared.originalPoints.x_points
    shared.postEditPoints.y_points = new_points 
    menu.createGraph(shared.postEditPoints.x_points,shared.postEditPoints.y_points,"DCT Graph","samples",shared.editedWaveCanvas)


def DCTMenu():
    DCTCanvas = menu.createCanvas(shared.root, 0.5, 0.45, 0, 0.55)
    menu.createLabel("DCT:", DCTCanvas, 1, 0.25, 0.1, 0, 0)

    menu.createLabel("Starting Position:", DCTCanvas, 0, 0.2, 0.1, 0.25, 0.3)
    menu.createEntry(shared.startingPos_var, DCTCanvas, 0.2, 0.1, 0.5, 0.3)

    menu.createButton("DCT", DCTGraph, DCTCanvas, 0.2, 0.1, 0.25, 0.6)


def convertMenuClick():
    compareCanvas = menu.createCanvas(shared.root, 0.5, 0.5, 0, 0.5)
    menu.createLabel("Convert:", compareCanvas, 1, 0.25, 0.1, 0, 0)

    menu.createButton("DFT", DFTMenu, compareCanvas, 0.1, 0.1, 0.4, 0)
    menu.createButton("IDFT", IDFTMenu, compareCanvas, 0.1, 0.1, 0.5, 0)
    menu.createButton("DCT", DCTMenu, compareCanvas, 0.1, 0.1, 0.6, 0)