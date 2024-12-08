import menu as menu
import shared as shared
import points as points
import math as math
import numpy as np

new_new_final_h_coef = []
new_new_final_h_coef_time = []

def convolve():
    first = shared.originalPoints
    second_y = new_new_final_h_coef
    second_x = new_new_final_h_coef_time
    new_points = np.convolve(first.y_points,second_y,mode="full")
    min_point = min(first.x_points) + min(second_x)
    max_point = max(first.x_points) + max(second_x)
    shared.postEditPoints.x_points = range(min_point,max_point)
    shared.postEditPoints.y_points = new_points
    for x in range(shared.postEditPoints.x_points):
        print(f"{shared.postEditPoints.x_points[x]}: {shared.postEditPoints.y_points[x]}")
    menu.createGraph(shared.postEditPoints.x_points, shared.postEditPoints.y_points, "Convolved Wave", "Sample", shared.editedWaveCanvas)


def filter(type):
    global new_new_final_h_coef
    global new_new_final_h_coef_time

    samp_freq = shared.sampleFreq_var.get()
    normalized_trans = shared.transBand_var.get()/samp_freq
    stop_atten = shared.stopAtten_var.get()
    cut_off = shared.cutFreq_var.get()
    if type == "high" or type == "low":
        cut_off = cut_off + shared.transBand_var.get()/2
    cut_off = cut_off/samp_freq
    
    omega = cut_off*2*math.pi
    window = 0
    w_n_0 = 0
    big_N = 0
    if stop_atten <= 21:
        window = 0
        big_N = 0.9/normalized_trans
        w_n_0 = 1
    elif stop_atten <= 44:
        window = 1
        big_N = 3.1/normalized_trans
        w_n_0 = 0.5 + 0.5*math.cos(0)
    elif stop_atten <= 53:
        window = 2
        big_N = 3.3/normalized_trans
        w_n_0 = 0.54+ 0.46*math.cos(0)
    elif stop_atten <= 74:
        window = 3
        big_N = 5.5/normalized_trans
        w_n_0 = 0.42 + 0.5*math.cos(0)+0.08*math.cos(0)
    else:
        menu.createLabel("Error Stop attentuation must be between 0-74", shared.root, 0, 0.45, 0.05, 0.025, 0.55)
        return
    big_N = math.ceil(big_N)
    if big_N % 2 == 0:
        big_N = big_N + 1
    h_coef = []
    if type == "high":
        h_d_0 = 1-(2*cut_off)
    elif type == "low":
        h_d_0 = 2*cut_off
    h_coef.append(h_d_0 * w_n_0)
     
    for n in range(1,math.ceil(big_N/2)):
        h_d = 0
        w_n = 0
        if type == "high" or type == "low": 
            h_d = 2*cut_off*(math.sin(n*omega))/(n*omega)
        if type == "high":
            h_d = h_d * -1
        if window == 0:
            w_n = 1
        elif window == 1:
            w_n = 0.5 + 0.5*math.cos(2*math.pi*n/big_N)
        elif window == 2:
            w_n = 0.54 + 0.46*math.cos(2*math.pi*n/big_N)
        elif window == 3:
            w_n = 0.42 + 0.5*math.cos(2*math.pi*n/(big_N-1))+0.08*math.cos(4*math.pi*n/(big_N-1))
        h_n = h_d * w_n
        h_coef.append(h_n)
    h_coef_time = np.arange(0,len(h_coef)).tolist()
    print(f"{h_coef_time}")
    h_coef.reverse()
    h_coef_time.reverse()
    new_h_coef = np.copy(h_coef)
    new_h_coef_time = np.multiply(np.copy(h_coef_time), -1)
    h_coef_time.reverse()
    h_coef.reverse()
    h_coef.pop(0)
    h_coef_time.pop(0)
    new_new_final_h_coef = np.concatenate((new_h_coef,h_coef),axis=0)
    new_new_final_h_coef_time = np.concatenate((new_h_coef_time,h_coef_time),axis=0)
    for x in range(len(new_new_final_h_coef)):
        print(f"{new_new_final_h_coef_time[x]}: {new_new_final_h_coef[x]}")



def highPassClick():
    filter("high")

def lowPassClick():
    filter("low")


def bandStopClick():
    filter("stop")


def bandPassClick():
    filter("pass")



def filtersMenuClick():
    filterCanvas = menu.createCanvas(shared.root, 0.5, 0.5, 0, 0.5)
    menu.createLabel("Filter:", filterCanvas, 1, 0.25, 0.1, 0, 0)

    menu.createLabel("Sample Frequency:", filterCanvas, 0, 0.2, 0.1, 0.1, 0.1)
    menu.createEntry(shared.sampleFreq_var, filterCanvas, 0.6, 0.1, 0.3, 0.1)
    menu.createLabel("Cut-off Frequency:", filterCanvas, 0, 0.2, 0.1, 0.1, 0.2)
    menu.createEntry(shared.cutFreq_var, filterCanvas, 0.6, 0.1, 0.3, 0.2)
    menu.createLabel("first freq:", filterCanvas, 0, 0.2, 0.1, 0.1, 0.3)
    menu.createEntry(shared.firstFreq_var, filterCanvas, 0.6, 0.1, 0.3, 0.3)
    menu.createLabel("Second Freq:", filterCanvas, 0, 0.2, 0.1, 0.1, 0.4)
    menu.createEntry(shared.secondFreq_var, filterCanvas, 0.6, 0.1, 0.3, 0.4)
    menu.createLabel("Trans Frequency:", filterCanvas, 0, 0.2, 0.1, 0.1, 0.5)
    menu.createEntry(shared.transBand_var, filterCanvas, 0.6, 0.1, 0.3, 0.5)
    menu.createLabel("Stop Attenuation:", filterCanvas, 0, 0.2, 0.1, 0.1, 0.6)
    menu.createEntry(shared.stopAtten_var, filterCanvas, 0.6, 0.1, 0.3, 0.6)

    menu.createButton("Low pass", lowPassClick, filterCanvas, 0.2, 0.1, 0.1, 0.8)
    menu.createButton("High pass", highPassClick, filterCanvas, 0.2, 0.1, 0.3, 0.8)
    menu.createButton("Band pass", bandPassClick, filterCanvas, 0.2, 0.1, 0.5, 0.8)
    menu.createButton("Band stop", bandStopClick, filterCanvas, 0.2, 0.1, 0.7, 0.8)
    menu.createButton("Convolve", convolve, filterCanvas, 0.2, 0.1, 0.8, 0)