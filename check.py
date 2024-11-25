import math
from files import browseClick, freqFromFile
import menu as menu
import shared as shared

def SignalSamplesAreEqual(compare_type="edited"):
    file_name = shared.file_var.get()
    samples = []
    if compare_type == "edited":
        samples = shared.postEditPoints.y_points
    elif compare_type == "original":
        samples = shared.originalPoints.y_points
    else:
        return
    expected_indices = []
    expected_samples = []
    with open(file_name, 'r') as f:
        f.readline()
        f.readline()
        f.readline()
        line = f.readline()
        while line:
            # process line
            L = line.strip()
            if len(L.split(' ')) == 2:
                L = line.split(' ')
                V1 = int(L[0])
                V2 = float(L[1])
                expected_indices.append(V1)
                expected_samples.append(V2)
                line = f.readline()
            else:
                break

    test_failed = 0
    if len(expected_samples) != len(samples):
        shared.line_var.set("Test case failed, your signal have different length from the expected one")
        if test_failed == 0:
            print("Test case failed, your signal have different values from the expected one1")
        test_failed = 1
    for i in range(len(expected_samples)):
        try:
            if abs(samples[i] - expected_samples[i]) < 0.01:
                continue
            else:
                shared.line_var.set("Test case failed, your signal have different values from the expected one")
                if test_failed == 0:
                    print("Test case failed, your signal have different values from the expected one2")
                test_failed = 1
        except IndexError:
            shared.line_var.set("Test case failed, your signal have different values from the expected one")
            if test_failed == 0:
                print("Test case failed, your signal have different values from the expected one2")
            test_failed = 1

    if test_failed == 0:
        shared.line_var.set("Test case passed successfully")
        print("Test case passed successfully")

    # creates a label for the note
    menu.createLabel(shared.line_var.get(), shared.root, 0, 0.4, 0.05, 0.05, 0.55)


def compareOriginalClick():
    SignalSamplesAreEqual("original")
    return


def compareEditedClick():
    SignalSamplesAreEqual("edited")
    return

def QuantizationTest1():
    file_name = shared.file_var.get()
    Your_EncodedValues = shared.quantizedPoints.levelsBin
    Your_QuantizedValues = shared.quantizedPoints.points.y_points
    expectedEncodedValues=[]
    expectedQuantizedValues=[]
    test_failed = 0
    with open(file_name, 'r') as f:
        line = f.readline()
        line = f.readline()
        line = f.readline()
        line = f.readline()
        while line:
            # process line
            L=line.strip()
            if len(L.split(' '))==2:
                L=line.split(' ')
                V2=str(L[0])
                V3=float(L[1])
                expectedEncodedValues.append(V2)
                expectedQuantizedValues.append(V3)
                line = f.readline()
            else:
                break
    if( (len(Your_EncodedValues)!=len(expectedEncodedValues)) or (len(Your_QuantizedValues)!=len(expectedQuantizedValues))):
        shared.line_var.set("QuantizationTest1 Test case failed, your signal have different length from the expected one")
        print("QuantizationTest1 Test case failed, your signal have different length from the expected one")
        test_failed = 1
    if test_failed == 0:
        for i in range(len(Your_EncodedValues)):
            if(Your_EncodedValues[i]!=expectedEncodedValues[i]):
                shared.line_var.set("QuantizationTest1 Test case failed, your EncodedValues have different EncodedValues from the expected one")
                print("QuantizationTest1 Test case failed, your EncodedValues have different EncodedValues from the expected one") 
                test_failed = 1
    if test_failed == 0:
        for i in range(len(expectedQuantizedValues)):
            if abs(Your_QuantizedValues[i] - expectedQuantizedValues[i]) < 0.01:
                continue
            else:
                shared.line_var.set("QuantizationTest1 Test case failed, your QuantizedValues have different values from the expected one")
                print("QuantizationTest1 Test case failed, your QuantizedValues have different values from the expected one") 
                test_failed = 1
    
    # creates a label for the note
    if test_failed == 0:
        shared.line_var.set("QuantizationTest1 Test case passed successfully")
        print("QuantizationTest1 Test case passed successfully")
    menu.createLabel(shared.line_var.get(), shared.root, 0, 0.45, 0.05, 0.025, 0.55)


def QuantizationTest2():
    file_name = shared.file_var.get()
    Your_IntervalIndices = shared.quantizedPoints.levels
    Your_EncodedValues = shared.quantizedPoints.levelsBin
    Your_QuantizedValues = shared.quantizedPoints.points.y_points
    Your_SampledError = shared.quantizedPoints.err
    test_failed = 0
    expectedIntervalIndices=[]
    expectedEncodedValues=[]
    expectedQuantizedValues=[]
    expectedSampledError=[]
    with open(file_name, 'r') as f:
        line = f.readline()
        line = f.readline()
        line = f.readline()
        line = f.readline()
        while line:
            # process line
            L=line.strip()
            if len(L.split(' '))==4:
                L=line.split(' ')
                V1=int(L[0])
                V2=str(L[1])
                V3=float(L[2])
                V4=float(L[3])
                expectedIntervalIndices.append(V1)
                expectedEncodedValues.append(V2)
                expectedQuantizedValues.append(V3)
                expectedSampledError.append(V4)
                line = f.readline()
            else:
                break
    if(len(Your_IntervalIndices)!=len(expectedIntervalIndices)
     or len(Your_EncodedValues)!=len(expectedEncodedValues)
      or len(Your_QuantizedValues)!=len(expectedQuantizedValues)
      or len(Your_SampledError)!=len(expectedSampledError)):
        shared.line_var.set("QuantizationTest2 Test case failed, your signal have different length from the expected one")
        print("QuantizationTest2 Test case failed, your signal have different length from the expected one")
        test_failed = 1
    if test_failed == 0:
        for i in range(len(Your_IntervalIndices)):
            if(Your_IntervalIndices[i]!=expectedIntervalIndices[i]):
                shared.line_var.set("QuantizationTest2 Test case failed, your signal have different indicies from the expected one") 
                print("QuantizationTest2 Test case failed, your signal have different indicies from the expected one") 
                test_failed = 1
    if test_failed == 0:
        for i in range(len(Your_EncodedValues)):
            if(Your_EncodedValues[i]!=expectedEncodedValues[i]):
                shared.line_var.set("uantizationTest2 Test case failed, your EncodedValues have different EncodedValues from the expected one") 
                print("QuantizationTest2 Test case failed, your EncodedValues have different EncodedValues from the expected one") 
                test_failed = 1
    if test_failed == 0: 
        for i in range(len(expectedQuantizedValues)):
            if abs(Your_QuantizedValues[i] - expectedQuantizedValues[i]) < 0.01:
                continue
            else:
                shared.line_var.set("QuantizationTest2 Test case failed, your QuantizedValues have different values from the expected one") 
                print("QuantizationTest2 Test case failed, your QuantizedValues have different values from the expected one") 
                test_failed = 1
    if test_failed == 0:
        for i in range(len(expectedSampledError)):
            if abs(Your_SampledError[i] - expectedSampledError[i]) < 0.01:
                continue
            else:
                shared.line_var.set("QuantizationTest2 Test case failed, your SampledError have different values from the expected one")
                print("QuantizationTest2 Test case failed, your SampledError have different values from the expected one") 
                test_failed = 1
    if test_failed == 0:
        shared.line_var.set("QuantizationTest2 Test case passed successfully")
        print("QuantizationTest2 Test case passed successfully")
    menu.createLabel(shared.line_var.get(), shared.root, 0, 0.45, 0.05, 0.025, 0.55)


#Use to test the Amplitude of DFT and IDFT
def SignalComapreAmplitude(SignalInput = [] ,SignalOutput= []):
    if len(SignalInput) != len(SignalInput):
        return False
    else:
        for i in range(len(SignalInput)):
            if abs(round(SignalInput[i])-round(SignalOutput[i]))>0.001:
                return False
            elif round(SignalInput[i])!=round(SignalOutput[i]):
                return False
        return True


def RoundPhaseShift(P):
    while P<0:
        p+=2*math.pi
    return float(P%(2*math.pi))


#Use to test the PhaseShift of DFT
def SignalComaprePhaseShift(SignalInput = [] ,SignalOutput= []):
    if len(SignalInput) != len(SignalInput):
        return False
    else:
        for i in range(len(SignalInput)):
            A=round(SignalInput[i])
            B=round(SignalOutput[i])
            if abs(A-B)>0.0001:
                return False
            elif A!=B:
                return False
        return True


def polarTest():
    file_amp_points,file_phase_points,file_samples = freqFromFile()
    original_amp_points = shared.convertPoints.ampPoints
    original_phase_points = shared.convertPoints.phasePoints

    isPhaseEqual = SignalComaprePhaseShift(original_phase_points,file_phase_points)
    isAmpEqual = SignalComapreAmplitude(original_amp_points,file_amp_points)

    if isPhaseEqual == 0 and isAmpEqual == 0:
        shared.line_var.set("Amp and Phase are not equal.")
        print("Amp and Phase are not equal.")
    elif isPhaseEqual == 1 and isAmpEqual == 0:
        shared.line_var.set("Amp is not Equal but Phase is Equal")
        print("Amp is not Equal but Phase is Equal")
    elif isPhaseEqual == 0 and isAmpEqual == 1:
        shared.line_var.set("Amp is Equal but Phase is not Equal")
        print("Amp is Equal but Phase is not Equal")
    elif isPhaseEqual == 1 and isAmpEqual == 1:
        shared.line_var.set("Freq Test passed succesfully.")
        print("Freq Test passed succesfully.")
    else:
        shared.line_var.set("Error: Something went wrong with freq TEST")
        print("Error: Something went wrong with freq TEST")
        return
    menu.createLabel(shared.line_var.get(), shared.root, 0, 0.45, 0.05, 0.025, 0.55)

def Shift_Fold_Signal():
    file_name = shared.file_var.get()
    Your_indices = shared.postEditPoints.x_points
    Your_samples = shared.postEditPoints.y_points      
    expected_indices=[]
    expected_samples=[]
    with open(file_name, 'r') as f:
        line = f.readline()
        line = f.readline()
        line = f.readline()
        line = f.readline()
        while line:
            # process line
            L=line.strip()
            if len(L.split(' '))==2:
                L=line.split(' ')
                V1=int(L[0])
                V2=float(L[1])
                expected_indices.append(V1)
                expected_samples.append(V2)
                line = f.readline()
            else:
                break
    print("Current Output Test file is: ")
    print(file_name)
    print("\n")
    isCorrect = 1
    if (len(expected_samples)!=len(Your_samples)) and (len(expected_indices)!=len(Your_indices)):
        shared.line_var.set("Shift_Fold_Signal Test case failed, your signal have different length from the expected one")
        print("Shift_Fold_Signal Test case failed, your signal have different length from the expected one")
        isCorrect = 0
    else:
        for i in range(len(Your_indices)):
            if(Your_indices[i]!=expected_indices[i]):
                shared.line_var.set("Shift_Fold_Signal Test case failed, your signal have different indicies from the expected one")
                print("Shift_Fold_Signal Test case failed, your signal have different indicies from the expected one") 
                isCorrect = 0
                break
        for i in range(len(expected_samples)):
            if abs(Your_samples[i] - expected_samples[i]) < 0.01:
                continue
            else:
                shared.line_var.set("Shift_Fold_Signal Test case failed, your signal have different values from the expected one")
                print("Shift_Fold_Signal Test case failed, your signal have different values from the expected one") 
                isCorrect = 0
                break
    if isCorrect == 1:
        shared.line_var.set("Shift_Fold_Signal Test case passed successfully")
        print("Shift_Fold_Signal Test case passed successfully")
    menu.createLabel(shared.line_var.get(), shared.root, 0, 0.45, 0.05, 0.025, 0.55)

def ConvTest(): 
    """
    Test inputs
    InputIndicesSignal1 =[-2, -1, 0, 1]
    InputSamplesSignal1 = [1, 2, 1, 1 ]
    
    InputIndicesSignal2=[0, 1, 2, 3, 4, 5 ]
    InputSamplesSignal2 = [ 1, -1, 0, 0, 1, 1 ]
    """
    Your_indices = shared.postEditPoints.x_points
    Your_samples = shared.postEditPoints.y_points
    expected_indices=[-2, -1, 0, 1, 2, 3, 4, 5, 6]
    expected_samples = [1, 1, -1, 0, 0, 3, 3, 2, 1 ]

    correct = 1
    if (len(expected_samples)!=len(Your_samples)) and (len(expected_indices)!=len(Your_indices)):
        shared.line_var.set("Conv Test case failed, your signal have different length from the expected one")
        print("Conv Test case failed, your signal have different length from the expected one")
        correct = 0
    for i in range(len(Your_indices)):
        if(Your_indices[i]!=expected_indices[i]):
            shared.line_var.set("Conv Test case failed, your signal have different indicies from the expected one")
            print("Conv Test case failed, your signal have different indicies from the expected one") 
            correct = 0
            break
    for i in range(len(expected_samples)):
        if abs(Your_samples[i] - expected_samples[i]) < 0.01:
            continue
        else:
            shared.line_var.set("Conv Test case failed, your signal have different values from the expected one")
            print("Conv Test case failed, your signal have different values from the expected one") 
            correct = 0
            break
    
    if (correct == 1):
        shared.line_var.set("Conv Test case passed successfully")
        print("Conv Test case passed successfully")
    menu.createLabel(shared.line_var.get(), shared.root, 0, 0.45, 0.05, 0.025, 0.55)



def compareMenuClick():
    compareCanvas = menu.createCanvas(shared.root, 0.5, 0.5, 0, 0.5)
    menu.createLabel("Compare:", compareCanvas, 1, 0.25, 0.1, 0, 0)

    menu.createLabel("File:", compareCanvas, 0, 0.2, 0.1, 0.1, 0.2)
    menu.createEntry(shared.file_var, compareCanvas, 0.4, 0.1, 0.3, 0.2)
    menu.createButton("Browse", browseClick, compareCanvas, 0.2, 0.1, 0.7, 0.2)
    menu.createButton("Compare OG", compareOriginalClick, compareCanvas, 0.2, 0.1, 0.1, 0.4)
    menu.createButton("Compare ED", compareEditedClick, compareCanvas, 0.2, 0.1, 0.3, 0.4)
    menu.createButton("QN Test 1", QuantizationTest1, compareCanvas, 0.2, 0.1, 0.5, 0.4)
    menu.createButton("QN Test 2", QuantizationTest2, compareCanvas, 0.2, 0.1, 0.7, 0.4)
    menu.createButton("Freq Test", polarTest, compareCanvas, 0.2, 0.1, 0.1, 0.6)
    menu.createButton("Shift/Fold Test", Shift_Fold_Signal, compareCanvas, 0.2, 0.1, 0.3, 0.6)
    menu.createButton("Conv Test", ConvTest, compareCanvas, 0.2, 0.1, 0.5, 0.6)