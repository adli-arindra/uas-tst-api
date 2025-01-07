import numpy as np

class faceData:
    def __init__(self, array, long):
        self.diamond = array[0]
        self.oblong = array[1]
        self.oval = array[2]
        self.pear = array[3]
        # self.rect = array[4]
        self.round = array[4]
        self.square = array[5]
        self.tri = array[6]
        self.long = long

    
    def display(self):
        print(f"diamond    : {round(self.diamond, 2)}")
        print(f"oblong     : {round(self.oblong, 2)}")
        print(f"oval       : {round(self.oval, 2)}")
        print(f"pear       : {round(self.pear, 2)}")
        print(f"round      : {round(self.round, 2)}")
        print(f"square     : {round(self.square, 2)}")
        print(f"triangular : {round(self.tri, 2)}")
    
    def arr(self):
        return [self.diamond, self.oblong, self.oval, self.pear,
               self.round, self.square, self.tri]
    
    def getHeadShape(self):
        maxPercentage = max(self.arr())
        if self.diamond == maxPercentage:
            return "diamond"
        elif self.oblong == maxPercentage:
            return "oblong"
        elif self.oval == maxPercentage:
            return "oval"
        elif self.pear == maxPercentage:
            return "pear"
        elif self.round == maxPercentage:
            return "round"
        elif self.square == maxPercentage:
            return "square"
        elif self.tri == maxPercentage:
            return "triangle"
        return "none"
    
class haircutData:
    def __init__(self, array, long, count = 1):
        self.diamond = array[0]
        self.oblong = array[1]
        self.oval = array[2]
        self.pear = array[3]
        # self.rect = array[4]
        self.round = array[4]
        self.square = array[5]
        self.tri = array[6]
        self.long = long
        self.count = count

    def display(self):
        print(f"diamond    : {round(self.diamond, 2)}")
        print(f"oblong     : {round(self.oblong, 2)}")
        print(f"oval       : {round(self.oval, 2)}")
        print(f"pear       : {round(self.pear, 2)}")
        # print(f"rect       : {round(self.rect, 2)}")
        print(f"round      : {round(self.round, 2)}")
        print(f"square     : {round(self.square, 2)}")
        print(f"triangular : {round(self.tri, 2)}")
    
    def arr(self):
        return [self.diamond, self.oblong, self.oval, self.pear,
               self.round, self.square, self.tri]
    
    def update(self, arr):
        self.diamond = ((self.diamond * self.count) + arr[0]) / (self.count + 1)
        self.oblong = ((self.oblong * self.count) + arr[1]) / (self.count + 1)
        self.oval = ((self.oval * self.count) + arr[2]) / (self.count + 1)
        self.pear = ((self.pear * self.count) + arr[3]) / (self.count + 1)
        # self.rect = ((self.rect * self.count) + arr[4]) / (self.count + 1)
        self.round = ((self.round * self.count) + arr[5]) / (self.count + 1)
        self.square = ((self.square * self.count) + arr[6]) / (self.count + 1)
        self.tri = ((self.tri * self.count) + arr[7]) / (self.count + 1)
        self.count += 1

############## FUNCTIONS #################################

def getSumPoint(face, haircut):
    sum = 0
    for i in range(len(face.arr())):
        sum += face.arr()[i] * haircut.arr()[i]
    return sum

def getHaircut(face):
    returnValue = {}
    for i in haircuts.keys():
        returnValue[i] = 0

    for haircut in returnValue.keys():
        if haircuts[haircut].long and not face.long:
            returnValue[haircut] = 0
        else:
            returnValue[haircut] = getSumPoint(face, haircuts[haircut])
    sortedValue = {k: v for k, v in sorted(returnValue.items(), key=lambda item: item[1], reverse= True)}

    # for i in sortedValue.keys():
        # print (f"{i} : {sortedValue[i]}")

    returnArray = []
    for i in sortedValue.keys():
        returnArray.append(i + ";" + str(sortedValue[i]))
    return returnArray

def normalizePredicted(arr):
    negativePoint = 0
    negativeCount = 0
    for i in range(len(arr)):
        if arr[i] < 0:
            negativePoint += arr[i]
            negativeCount += 1
            arr[i] = 0
    
    negativePoint = negativePoint / (len(arr) - negativeCount)
    for i in range(len(arr)):
        if arr[i] > 0:
            arr[i] += negativePoint
    
    return arr



############### HAIRCUT DATA ##############################

globalCount = 20
# twoBlock = haircutData([0.375, 0.625, 0.5, 0.125, 1, 0.75, 0.25], False, globalCount)
curtains = haircutData([1, 0.375, 0.5, 0.125, 0.25, 0.625, 0.875], True, globalCount)
comma = haircutData([1, 0.75, 0.625, 0.5, 0.125, 0.25, 0.875], False, globalCount)
bowlCut = haircutData([0.125, 0.5, 0.25, 1, 0.875, 0.375, 0.625], False, globalCount)
fauxHawk = haircutData([0.125, 0.875, 0.625, 0.5, 0.375, 0.75, 0.25], True, globalCount)
# undercut
slickedBack = haircutData([0.125, 0.875, 0.75, 0.5, 0.375, 0.625, 0.25], False, globalCount)
pompadour = haircutData([0.25, 0.875, 0.75, 0.375, 0.5, 0.625, 0.125], False, globalCount)
frenchCrop = haircutData([1, 0.875, 0.75, 0.625, 0.25, 0.375, 0.125], False, globalCount)
buzzCut = haircutData([0.125, 0.75, 0.875, 0.375, 0.5, 0.625, 0.25], False, globalCount)
fringe = haircutData([1, 0.375, 0.5, 0.125, 0.25, 0.75, 0.875], False, globalCount)
quiff = haircutData([0.125, 0.875, 0.75, 0.25, 0.625, 0.375, 0.5], False, globalCount)
sideParted = haircutData([0.25, 0.875, 1, 0.375, 0.5, 0.625, 0.125], True, globalCount)
# wolfCut = haircutData([1, 0.5, 0.625, 0.125, 0.75, 0.25, 0.375, 0.875], True, globalCount)
crewCut = haircutData([0.25, 0.75, 0.625, 0.375, 0.5, 0.875, 0.125], False, globalCount)

global haircuts
haircuts = {
    # "twoBlock" : twoBlock,
    "Curtain" : curtains,
    "Comma" : comma,
    "Bowl Cut" : bowlCut,
    "Fauxhawk" : fauxHawk,
    # under cut
    "Slicked Back" : slickedBack,
    "Pompadour" : pompadour,
    "French Crop" : frenchCrop,
    "Buzz Cut" : buzzCut,
    "Fringe" : fringe,
    "Quiff" : quiff,
    "Side Part" : sideParted,
    # "wolfcut" : wolfCut,
    "Crew Cut" : crewCut
}