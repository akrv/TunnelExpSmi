# -*- coding: iso-8859-15 -*-
'''
Created on 25.02.2014

@author: Mussmann
'''

def enum(**enums):
    return type('Enum', (), enums)

class Config:
    roomSize = [20,20]
    roomColor = [-1,-1,-1] # black
    doorSize = [3,0.5]
    doorColor = [1,1,1] # white
    objectSize = 2
    objectColor = [0,0,0]
    objectColorPost = [0.75,0.75,0.75]
    
    fixationDuration = 0.75
    entranceDuration = 1
    exitDuration = 1
    movementDurationEntrance = 1
    movementDurationExit = 2
    delay = 2
    
    subject = None
    outputFolder = "."
    
    shapes = enum(CIRCLE=1, TRIANGLE=2, SQUARE=3, PRACTICE_1=4, PRACTICE_2=5, PRACTICE_3=6)
    exits = enum(DOWN=0, LEFT=1, UP=2, RIGHT=3)
    # main exit for each shape as first in list
    exitsForShape = {shapes.CIRCLE: [exits.UP, exits.LEFT, exits.RIGHT],
                shapes.TRIANGLE: [exits.RIGHT, exits.LEFT, exits.UP],
                shapes.SQUARE: [exits.LEFT, exits.UP, exits.RIGHT],
                shapes.PRACTICE_1: [exits.UP, exits.LEFT, exits.RIGHT],
                shapes.PRACTICE_2: [exits.RIGHT, exits.LEFT, exits.UP],
                shapes.PRACTICE_3: [exits.LEFT, exits.UP, exits.RIGHT]}
    
    # trials for each object, total number per block = (high+2*low+start)*3
    trialsPerBlockHigh = 20
    trialsPerBlockLow = 3
    trialsPerBlockStart = 1
    
    trialsPractice1 = 2 # jedes object 2mal zu jedem ausgang
    trialsPractice2 = 7 # jedes object 10mal zum hauptausgang
    practice2Blocks = 2
    
    blocks = 4
    
    def __init__(self):
        pass