import menu as menu
import shared as shared
import points as points
import math as math
import numpy as np
import tkinter as tk 

new_new_final_h_coef = []
new_new_final_h_coef_time = []

filterCanvas = tk.Canvas()
resampleCanvas = tk.Canvas()

def convolve():
    # x_signal1 = shared.postEditPoints.x_points
    # y_signal1 = shared.postEditPoints.y_points
    # x_signal2 = new_new_final_h_coef_time
    # y_signal2 = new_new_final_h_coef
    first = shared.postEditPoints.y_points
    first_x = shared.postEditPoints.x_points
    second = new_new_final_h_coef
    second_x = new_new_final_h_coef_time
    new_points = np.convolve(first,second,mode="full")
    min_point = min(first_x) + min(second_x)
    max_point = max(first_x) + max(second_x)
    shared.postEditPoints.x_points = range(int(min_point),int(max_point))
    shared.postEditPoints.y_points = new_points
    menu.createGraph(shared.postEditPoints.x_points, shared.postEditPoints.y_points, "Convolved Wave", "Sample", shared.editedWaveCanvas)


def filter(type):
    global new_new_final_h_coef
    global new_new_final_h_coef_time

    samp_freq = shared.sampleFreq_var.get()
    normalized_trans = shared.transBand_var.get()/samp_freq
    stop_atten = shared.stopAtten_var.get()
    cut_off = shared.cutFreq_var.get()
    cut_off_1 = shared.firstFreq_var.get()
    cut_off_2 = shared.secondFreq_var.get()
    if type == "low":
        cut_off = cut_off + shared.transBand_var.get()/2
    elif type == "high":
        cut_off = cut_off - shared.transBand_var.get()/2
    elif type == "pass":
        cut_off_1 = cut_off_1 - shared.transBand_var.get()/2
        cut_off_2 = cut_off_2 + shared.transBand_var.get()/2
    elif type == "stop":
        cut_off_1 = cut_off_1 + shared.transBand_var.get()/2
        cut_off_2 = cut_off_2 - shared.transBand_var.get()/2
    cut_off = cut_off/samp_freq
    cut_off_2 = cut_off_2/samp_freq
    cut_off_1 = cut_off_1/samp_freq
    omega = cut_off*2*math.pi
    cut_off_1_omega = cut_off_1*2*math.pi
    cut_off_2_omega = cut_off_2*2*math.pi
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
        menu.createLabel("Error Stop attentuation must be between 0-74", filterCanvas, 0, 0.5, 0.1, 0.25, 0)
        return
    big_N = math.ceil(big_N)
    if big_N % 2 == 0:
        big_N = big_N + 1
    h_coef = []
    if type == "high":
        h_d_0 = 1-(2*cut_off)
    elif type == "low":
        h_d_0 = 2*cut_off
    elif type == "pass":
        h_d_0 = 2*(cut_off_2-cut_off_1)
    elif type == "stop":
        h_d_0 = 1 - 2*(cut_off_2-cut_off_1)
    
    h_coef.append(h_d_0 * w_n_0)
    print(f"0 window = {w_n_0},{h_coef[0]}")
    for n in range(1,math.ceil(big_N/2)):
        h_d = 0
        w_n = 0
        if type == "low": 
            h_d = 2*cut_off*(math.sin(n*omega))/(n*omega)
        elif type == "high":
            h_d = -2*cut_off*(math.sin(n*omega))/(n*omega)
        elif type == "pass":
            h_d = 2*cut_off_2*math.sin(n*cut_off_2_omega)/(n*cut_off_2_omega)-2*cut_off_1*math.sin(n*cut_off_1_omega)/(n*cut_off_1_omega)
        elif type=="stop":
            h_d = 2*cut_off_1*math.sin(n*cut_off_1_omega)/(n*cut_off_1_omega)-2*cut_off_2*math.sin(n*cut_off_2_omega)/(n*cut_off_2_omega)
        if window == 0:
            w_n = 1
        elif window == 1:
            w_n = 0.5 + 0.5*math.cos(2*math.pi*n/big_N)
        elif window == 2:
            w_n = 0.54 + 0.46*math.cos(2*math.pi*n/big_N)
        elif window == 3:
            w_inside_cos = math.pi*n/(big_N-1)
            w_n_param_number_1 = 0.5 * (math.cos(2*w_inside_cos))
            w_n_param_number_2 = 0.08 * (math.cos(4*w_inside_cos))
            w_n = 0.42 + w_n_param_number_1 + w_n_param_number_2
        print(f"{n} window: {w_n}")
        h_n = h_d * w_n
        h_coef.append(h_n)
    h_coef_time = np.arange(0,len(h_coef)).tolist()
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
    shared.postEditPoints.x_points = shared.originalPoints.x_points
    shared.postEditPoints.y_points = shared.originalPoints.y_points
    filter("high")

def lowPassClick():
    shared.postEditPoints.x_points = shared.originalPoints.x_points
    shared.postEditPoints.y_points = shared.originalPoints.y_points
    filter("low")


def bandStopClick():
    shared.postEditPoints.x_points = shared.originalPoints.x_points
    shared.postEditPoints.y_points = shared.originalPoints.y_points
    filter("stop")


def bandPassClick():
    shared.postEditPoints.x_points = shared.originalPoints.x_points
    shared.postEditPoints.y_points = shared.originalPoints.y_points
    filter("pass")

def firMenuClick():
    global filterCanvas
    filterCanvas = menu.createCanvas(shared.root, 0.5, 0.45, 0, 0.55)
    menu.createLabel("Filter:", filterCanvas, 1, 0.25, 0.1, 0, 0)
    menu.createButton("Convolve", convolve, filterCanvas, 0.25, 0.1, 0.75, 0)

    menu.createLabel("Sample Frequency:", filterCanvas, 0, 0.2, 0.1, 0.1, 0.1)
    menu.createEntry(shared.sampleFreq_var, filterCanvas, 0.6, 0.1, 0.3, 0.1)
    menu.createLabel("Trans Frequency:", filterCanvas, 0, 0.2, 0.1, 0.1, 0.2)
    menu.createEntry(shared.transBand_var, filterCanvas, 0.6, 0.1, 0.3, 0.2)
    menu.createLabel("Stop Attenuation:", filterCanvas, 0, 0.2, 0.1, 0.1, 0.3)
    menu.createEntry(shared.stopAtten_var, filterCanvas, 0.6, 0.1, 0.3, 0.3)
    menu.createLabel("Cut-off Frequency:", filterCanvas, 0, 0.2, 0.1, 0.1, 0.4)
    menu.createEntry(shared.cutFreq_var, filterCanvas, 0.6, 0.1, 0.3, 0.4)
    menu.createLabel("First Freq:", filterCanvas, 0, 0.2, 0.1, 0.1, 0.5)
    menu.createEntry(shared.firstFreq_var, filterCanvas, 0.6, 0.1, 0.3, 0.5)
    menu.createLabel("Second Freq:", filterCanvas, 0, 0.2, 0.1, 0.1, 0.6)
    menu.createEntry(shared.secondFreq_var, filterCanvas, 0.6, 0.1, 0.3, 0.6)

    menu.createButton("Low pass", lowPassClick, filterCanvas, 0.2, 0.1, 0.1, 0.8)
    menu.createButton("High pass", highPassClick, filterCanvas, 0.2, 0.1, 0.3, 0.8)
    menu.createButton("Band pass", bandPassClick, filterCanvas, 0.2, 0.1, 0.5, 0.8)
    menu.createButton("Band stop", bandStopClick, filterCanvas, 0.2, 0.1, 0.7, 0.8)

def upsample():
    very_small_n = shared.L_var.get() - 1
    points_x = shared.originalPoints.x_points
    points_y = shared.originalPoints.y_points
    new_x = []
    new_y = []
    for x in range(len(points_x)):
        new_x.append(points_x[x])
        new_y.append(points_y[x])
        if x != len(points_x) - 1:
            for n in range(very_small_n):
                new_y.append(0)
                the_new_x = points_x[x]+((n+1)/(very_small_n+1))
                new_x.append(the_new_x)
    print(f"{new_x}\n{new_y}")
    print(f"{len(new_x)}:{len(new_y)}")
    print(f"small n: {very_small_n}")
    shared.postEditPoints.x_points = new_x
    shared.postEditPoints.y_points = new_y


def downsample():
    small_n = shared.M_var.get()
    points_x = shared.postEditPoints.x_points
    points_y = shared.postEditPoints.y_points
    print(f"{len(points_x)}:{len(points_y)}")
    new_x = []
    new_y = []
    for x in points_x[::small_n]:
        new_x.append(float(x))
    for y in points_y[::small_n]:
        new_y.append(float(y))
    for x in range(len(new_y)):
        try:
            print(f"{new_x[x]}: {new_y[x]}")
        except:
            print(f"the x is: {x}")
    print(f"{len(new_x)}:{len(new_y)}")
    shared.postEditPoints.x_points = new_x
    shared.postEditPoints.y_points = new_y
    menu.createGraph(shared.postEditPoints.x_points, shared.postEditPoints.y_points, "Convolved Wave", "Sample", shared.editedWaveCanvas)


def sampleClick():
    if shared.L_var.get() <= 0 and shared.M_var.get() <= 0:
        menu.createLabel("Error Stop attentuation must be between 0-74", filterCanvas, 0, 0.5, 0.1, 0.25, 0)
        return
    if shared.L_var.get() > 0:
        upsample()
    filter("low")
    convolve()
    if shared.M_var.get() > 0:
        downsample()

        


def resampleMenuClick():
    global resampleCanvas
    resampleCanvas = menu.createCanvas(shared.root, 0.5, 0.45, 0, 0.55)
    menu.createLabel("Resample:", resampleCanvas, 1, 0.25, 0.1, 0, 0)

    menu.createLabel("L:", resampleCanvas, 0, 0.2, 0.1, 0.1, 0.3)
    menu.createEntry(shared.L_var, resampleCanvas, 0.6, 0.1, 0.3, 0.3)
    menu.createLabel("M:", resampleCanvas, 0, 0.2, 0.1, 0.1, 0.4)
    menu.createEntry(shared.M_var, resampleCanvas, 0.6, 0.1, 0.3, 0.4)
    menu.createButton("Sample", sampleClick, resampleCanvas, 0.2, 0.1, 0.4, 0.8)

def filtersMenuClick():
    # creates a canvas for edit menu
    filtersMenuCanvas = menu.createCanvas(shared.root, 0.5, 0.5, 0, 0.5)
    # creates a label on the corner for edit
    menu.createLabel("Edit:", filtersMenuCanvas, 1, 0.25, 0.1, 0, 0)
    # Buttons for edit menu
    menu.createButton("FIR", firMenuClick, filtersMenuCanvas, 0.2, 0.1, 0.3, 0)
    menu.createButton("Resample", resampleMenuClick, filtersMenuCanvas, 0.1, 0.1, 0.5, 0)