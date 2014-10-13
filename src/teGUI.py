# -*- coding: iso-8859-15 -*-
'''
Created on 25.02.2014

@author: Mussmann
'''

from Tkinter import *
from tkFileDialog import *
from tkMessageBox import *
import tkFont

import cPickle
import os
import numpy as np

from teConfig import Config
from teMain import Exp

class GUI(Frame):
    def __init__(self,parent):
        self.parent = parent
        self.configFile = "config.pkl"
        self.config = Config()
        self.loadConfig()
        
        self.startExpOnExit = False
        self.resume = False

        parent.columnconfigure(1, weight=1)
        
        # font for the GUI elements
        myFont = tkFont.Font(family="Arial", size=10, weight=tkFont.NORMAL)

        ###############
        # parameters
        ###############
        
        # subject
        self.labelSubject = Label(parent, text="VP", font=myFont)
        self.labelSubject.grid(row=0, column=0, sticky=W, padx=3, pady=3)

        self.subject = StringVar()
        self.inputSubject = Entry(parent, textvariable=self.subject, font=myFont)
        self.inputSubject.grid(row=0, column=1, sticky=W+E, padx=3, pady=3)
        #self.subject.set(self.config.subject)
        
        # Room height and width
        self.labelRoomDims = Label(parent, text="Raum Breite/Höhe [cm]", font=myFont)
        self.labelRoomDims.grid(row=1, column=0, sticky=W, padx=3, pady=3)
        
        self.frameRoomDims = Frame(parent)
        self.frameRoomDims.columnconfigure(0, weight=1)
        self.frameRoomDims.columnconfigure(1, weight=1)
        self.frameRoomDims.grid(row=1, column=1, sticky=W+E)
        
        self.roomWidth = StringVar()
        self.inputRoomWidth = Entry(self.frameRoomDims, textvariable=self.roomWidth, font=myFont)
        self.inputRoomWidth.grid(row=0, column=0, sticky=W+E, padx=3, pady=3)
        self.roomWidth.set("%.1f" % (self.config.roomSize[0]))
        
        self.roomHeight = StringVar()
        self.inputRoomHeight = Entry(self.frameRoomDims, textvariable=self.roomHeight, font=myFont)
        self.inputRoomHeight.grid(row=0, column=1, sticky=W+E, padx=3, pady=3)
        self.roomHeight.set("%.1f" % (self.config.roomSize[1]))
        
        # Door height and width
        self.labelDoorDims = Label(parent, text="Eingang Breite/Höhe [cm]", font=myFont)
        self.labelDoorDims.grid(row=2, column=0, sticky=W, padx=3, pady=3)
        
        self.frameDoorDims = Frame(parent)
        self.frameDoorDims.columnconfigure(0, weight=1)
        self.frameDoorDims.columnconfigure(1, weight=1)
        self.frameDoorDims.grid(row=2, column=1, sticky=W+E)
        
        self.doorWidth = StringVar()
        self.inputDoorWidth = Entry(self.frameDoorDims, textvariable=self.doorWidth, font=myFont)
        self.inputDoorWidth.grid(row=0, column=0, sticky=W+E, padx=3, pady=3)
        self.doorWidth.set("%.1f" % (self.config.doorSize[0]))
        
        self.doorHeight = StringVar()
        self.inputDoorHeight = Entry(self.frameDoorDims, textvariable=self.doorHeight, font=myFont)
        self.inputDoorHeight.grid(row=0, column=1, sticky=W+E, padx=3, pady=3)
        self.doorHeight.set("%.1f" % (self.config.doorSize[1]))
        
        # object size
        self.labelObjectSize = Label(parent, text="Objektdurchmesser [cm]", font=myFont)
        self.labelObjectSize.grid(row=3, column=0, sticky=W, padx=3, pady=3)
        
        self.objectSize = StringVar()
        self.inputObjectSize = Entry(parent, textvariable=self.objectSize, font=myFont)
        self.inputObjectSize.grid(row=3, column=1, sticky=W+E, padx=3, pady=3)
        self.objectSize.set(self.config.objectSize)
        
        # trials header
        self.labelTrials = Label(parent, text="Trials pro Objekt:", font=myFont)
        self.labelTrials.grid(row=4, column=0, sticky=W, padx=3, pady=3)
        
        # practice 1 trials
        self.labelTrialsPractice1 = Label(parent, text="1. Training (für jeden Ausgang)", font=myFont)
        self.labelTrialsPractice1.grid(row=5, column=0, sticky=W, padx=3, pady=3)
        
        self.trialsPractice1 = StringVar()
        self.inputTrialsPractice1 = Entry(parent, textvariable=self.trialsPractice1, font=myFont)
        self.inputTrialsPractice1.grid(row=5, column=1, sticky=W+E, padx=3, pady=3)
        self.trialsPractice1.set(self.config.trialsPractice1)
        
        # practice 2 trials
        self.labelTrialsPractice2 = Label(parent, text="2. Training (pro Block, für einen Ausgang)", font=myFont)
        self.labelTrialsPractice2.grid(row=6, column=0, sticky=W, padx=3, pady=3)
        
        self.trialsPractice2 = StringVar()
        self.inputTrialsPractice2 = Entry(parent, textvariable=self.trialsPractice2, font=myFont)
        self.inputTrialsPractice2.grid(row=6, column=1, sticky=W+E, padx=3, pady=3)
        self.trialsPractice2.set(self.config.trialsPractice2)
        
        # experiment trials
        self.labelTrialsExp = Label(parent, text="Experiment häufig/selten/Start (pro Block)", font=myFont)
        self.labelTrialsExp.grid(row=7, column=0, sticky=W, padx=3, pady=3)
        
        self.frameTrialsExp = Frame(parent)
        self.frameTrialsExp.columnconfigure(0, weight=1)
        self.frameTrialsExp.columnconfigure(1, weight=1)
        self.frameTrialsExp.columnconfigure(2, weight=1)
        self.frameTrialsExp.grid(row=7, column=1, sticky=W+E)
        
        self.trialsExpHigh = StringVar()
        self.inputTrialsExpHigh = Entry(self.frameTrialsExp, textvariable=self.trialsExpHigh, font=myFont)
        self.inputTrialsExpHigh.grid(row=0, column=0, sticky=W+E, padx=3, pady=3)
        self.trialsExpHigh.set(self.config.trialsPerBlockHigh)
        
        self.trialsExpLow = StringVar()
        self.inputTrialsExpLow = Entry(self.frameTrialsExp, textvariable=self.trialsExpLow, font=myFont)
        self.inputTrialsExpLow.grid(row=0, column=1, sticky=W+E, padx=3, pady=3)
        self.trialsExpLow.set(self.config.trialsPerBlockLow)
        
        self.trialsExpStart = StringVar()
        self.inputTrialsExpStart = Entry(self.frameTrialsExp, textvariable=self.trialsExpStart, font=myFont)
        self.inputTrialsExpStart.grid(row=0, column=2, sticky=W+E, padx=3, pady=3)
        self.trialsExpStart.set(self.config.trialsPerBlockStart)
        
        # blocks
        self.labelBlocks = Label(parent, text="Blöcke", font=myFont)
        self.labelBlocks.grid(row=8, column=0, sticky=W, padx=3, pady=3)
        
        self.blocks = StringVar()
        self.inputBlocks = Entry(parent, textvariable=self.blocks, font=myFont)
        self.inputBlocks.grid(row=8, column=1, sticky=W+E, padx=3, pady=3)
        self.blocks.set(self.config.blocks)
        
        # fixation duration
        self.labelFixationDuration = Label(parent, text="Fixationsdauer [s]", font=myFont)
        self.labelFixationDuration.grid(row=9, column=0, sticky=W, padx=3, pady=3)
        
        self.fixationDuration = StringVar()
        self.inputFixationDuration = Entry(parent, textvariable=self.fixationDuration, font=myFont)
        self.inputFixationDuration.grid(row=9, column=1, sticky=W+E, padx=3, pady=3)
        self.fixationDuration.set(self.config.fixationDuration)
        
        # pause at entrance
        self.labelPauseEntrance = Label(parent, text="Pause am Eingang [s]", font=myFont)
        self.labelPauseEntrance.grid(row=10, column=0, sticky=W, padx=3, pady=3)
        
        self.pauseEntrance = StringVar()
        self.inputPauseEntrance = Entry(parent, textvariable=self.pauseEntrance, font=myFont)
        self.inputPauseEntrance.grid(row=10, column=1, sticky=W+E, padx=3, pady=3)
        self.pauseEntrance.set(self.config.entranceDuration)
        
        # pause at exit
        self.labelPauseExit = Label(parent, text="Pause am Ausgang [s]", font=myFont)
        self.labelPauseExit.grid(row=11, column=0, sticky=W, padx=3, pady=3)
        
        self.pauseExit = StringVar()
        self.inputPauseExit = Entry(parent, textvariable=self.pauseExit, font=myFont)
        self.inputPauseExit.grid(row=11, column=1, sticky=W+E, padx=3, pady=3)
        self.pauseExit.set(self.config.exitDuration)
        
        # pause in room
        self.labelPauseInside = Label(parent, text="Pause im Raum [s]", font=myFont)
        self.labelPauseInside.grid(row=12, column=0, sticky=W, padx=3, pady=3)
        
        self.pauseInside = StringVar()
        self.inputPauseInside = Entry(parent, textvariable=self.pauseInside, font=myFont)
        self.inputPauseInside.grid(row=12, column=1, sticky=W+E, padx=3, pady=3)
        self.pauseInside.set(self.config.delay)
        
        # movement duration
        self.labelMovementDuration = Label(parent, text="Bewegungsdauer Eingang/Ausgang [s]", font=myFont)
        self.labelMovementDuration.grid(row=13, column=0, sticky=W, padx=3, pady=3)
        
        self.frameMovementDur = Frame(parent)
        self.frameMovementDur.columnconfigure(0, weight=1)
        self.frameMovementDur.columnconfigure(1, weight=1)
        self.frameMovementDur.grid(row=13, column=1, sticky=W+E)
        
        self.movementDurationEntrance = StringVar()
        self.inputMovementDurationEntrance = Entry(self.frameMovementDur, textvariable=self.movementDurationEntrance, font=myFont)
        self.inputMovementDurationEntrance.grid(row=0, column=0, sticky=W+E, padx=3, pady=3)
        self.movementDurationEntrance.set(self.config.movementDurationEntrance)
        
        self.movementDurationExit = StringVar()
        self.inputMovementDurationExit = Entry(self.frameMovementDur, textvariable=self.movementDurationExit, font=myFont)
        self.inputMovementDurationExit.grid(row=0, column=1, sticky=W+E, padx=3, pady=3)
        self.movementDurationExit.set(self.config.movementDurationExit)
        
        # folder
        self.labelOutputFolder = Label(parent, text="Ausgabeordner", font=myFont)
        self.labelOutputFolder.grid(row=14, column=0, sticky=W, padx=3, pady=3)
        
        self.frameFolder = Frame(parent)
        self.frameFolder.columnconfigure(0, weight=1)
        self.frameFolder.grid(row=14, column=1, sticky=W+E)
        
        self.outputFolder = StringVar()
        self.inputOutputFolder = Entry(self.frameFolder, textvariable=self.outputFolder, font=myFont)
        self.inputOutputFolder.grid(row=0, column=0, sticky=W+E, padx=3, pady=3)
        self.outputFolder.set(self.config.outputFolder)
        
        self.buttonOutputFolder = Button(self.frameFolder, text="Auswählen", font=myFont, command=self.getFolder, width=8)
        self.buttonOutputFolder.grid(row=0, column=1, sticky=E, padx=3, pady=3)
        
        # start button
        self.buttonStart = Button(parent, text="Start", font=myFont, command=self.exit, width=8)
        self.buttonStart.grid(row=15, column=0, sticky=W, padx=3, pady=3)

    def getFolder(self):
        folder = askdirectory(initialdir=".", title="Ausgabeordner für Experiment")
        if folder != "":
            self.outputFolder.set(folder)

    def loadConfig(self):
        try:
            f = open(os.path.join(".",self.configFile),"rb")
            self.config = cPickle.load(f)
            f.close()          

            return True
        except:
            return False

    def saveConfig(self):
        try:
            f = open(os.path.join(".",self.configFile),"wb")
            cPickle.dump(self.config,f)
            f.close()
            
            return True
        except:
            return False
            
    def checkInput(self):
        errorString = ""
        try:
            subject = int(self.subject.get())
            if subject < 0:
                raise Exception()
        except:
            errorString += "Ungültige Vp-Nr.\n"
        try:
            roomDim = [float(self.roomWidth.get()), float(self.roomHeight.get())]
            if roomDim[0] <= 0 or roomDim[1] <= 0:
                raise Exception()
        except:
            errorString += "Ungültige Raumgrösse\n"
        try:
            doorDim = [float(self.doorWidth.get()), float(self.doorHeight.get())]
            if doorDim[0] <= 0 or doorDim[1] <= 0:
                raise Exception()
        except:
            errorString += "Ungültige Eingangsgrösse\n"
        try:
            objectSize = float(self.objectSize.get())
            if objectSize <= 0:
                raise Exception()
        except:
            errorString += "Ungültige Objektgrösse\n"
        try:
            trialsP1 = int(self.trialsPractice1.get())
            trialsP2 = int(self.trialsPractice2.get())
            trialsExpHigh = int(self.trialsExpHigh.get())
            trialsExpLow = int(self.trialsExpLow.get())
            trialsExpStart = int(self.trialsExpStart.get())
            if trialsP1 <= 0 or trialsP2 <= 0 or trialsExpHigh <= 0 or trialsExpLow <= 0 or trialsExpStart <= 0:
                raise Exception()
        except:
            errorString += "Ungültige Trialanzahl\n"
        try:
            blocks = int(self.blocks.get())
            if blocks <= 0:
                raise Exception()
        except:
            errorString += "Ungültige Blockanzahl\n"
        try:
            fixD = float(self.fixationDuration.get())
            if fixD < 0:
                raise Exception()
        except:
            errorString += "Ungültige Fixationsdauer\n"
        try:
            pauseEnt = float(self.pauseEntrance.get())
            pauseExit = float(self.pauseExit.get())
            pauseRoom = float(self.pauseInside.get())
            if pauseEnt < 0 or pauseExit < 0 or pauseRoom < 0:
                raise Exception()
        except:
            errorString += "Ungültige Pausendauer\n"
        try:
            movDEnt = float(self.movementDurationEntrance.get())
            movDEx = float(self.movementDurationExit.get())
            if movDEnt < 0 or movDEx < 0:
                raise Exception()
        except:
            errorString += "Ungültige Bewegungsdauer\n"
        try:
            folder = self.outputFolder.get()
            if not os.path.isdir(folder):
                raise Exception()
        except:
            errorString += "Ungültiger Ordner\n"
        
        if errorString == "":
            self.config.subject = subject
            self.config.roomSize = roomDim
            self.config.doorSize = doorDim
            self.config.objectSize = objectSize
            self.config.trialsPractice1 = trialsP1
            self.config.trialsPractice2 = trialsP2
            self.config.trialsPerBlockHigh = trialsExpHigh
            self.config.trialsPerBlockLow = trialsExpLow
            self.config.trialsPerBlockStart = trialsExpStart
            self.config.blocks = blocks
            self.config.fixationDuration = fixD
            self.config.entranceDuration = pauseEnt
            self.config.exitDuration = pauseExit
            self.config.delay = pauseRoom
            self.config.movementDurationEntrance = movDEnt
            self.config.movementDurationExit = movDEx
            self.config.outputFolder = folder
    
        return errorString
            
    def exit(self):
        errorMessage = self.checkInput()
        if errorMessage == "":
            self.saveConfig()
            if not os.path.exists(os.path.join(self.config.outputFolder, "vp"+str(self.config.subject))):
                os.makedirs(os.path.join(self.config.outputFolder, "vp"+str(self.config.subject)))
                self.startExpOnExit = True
            elif os.path.exists(os.path.join(self.config.outputFolder, "vp"+str(self.config.subject), str(self.config.subject)+"_result_data.txt")):
                ret = askquestion("Info", "Es wurden existierende Daten gefunden, Versuch fortsetzen?", icon=WARNING, type=YESNOCANCEL)
                if ret != 'cancel':
                    self.startExpOnExit = True
                if ret == 'yes':
                    self.resume = True
            else:
                self.startExpOnExit = True

            self.parent.destroy()
        else:
            showerror("Eingabefehler", errorMessage)

root = Tk()
root.wm_title("Konfiguration")
gui = GUI(root)
root.mainloop()

if gui.startExpOnExit:
    exp = Exp(gui.config, gui.resume)
    exp.run()