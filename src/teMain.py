# -*- coding: iso-8859-15 -*-
'''
Created on 25.02.2014

@author: Mussmann
'''

from psychopy import visual, core, event, monitors
import numpy as np
import os
import math
from iViewXAPI import *            #iViewX library


class Exp():
    def __init__(self,config,resume):
        self.config = config
        self.resume = resume

        self.trialIdx = 0
        self.trial = 1
        self.practiceStartBlock = 0-self.config.practice2Blocks
        self.startBlock = 1
        self.resultData = np.zeros(shape=((self.config.trialsPerBlockHigh+2*self.config.trialsPerBlockLow+self.config.trialsPerBlockStart)*3*self.config.blocks + self.config.trialsPractice2*3*self.config.practice2Blocks, 10), dtype=np.float64)
        self.save = False

        self.currentPhase = 0
        self.resumeBlock = 0
        if self.resume:
            self.loadExistingData()

        mon = monitors.Monitor('myMonitor1')
        self.window = visual.Window(size=mon.getSizePix(), color=(1,1,1), colorSpace='rgb', fullscr=True, monitor=mon, units='cm')

        self.posForExit = {self.config.exits.DOWN: [0, (-1)*(self.config.roomSize[1]/2.0 + self.config.objectSize/2 + 0.5)],
                        self.config.exits.LEFT: [(-1)*(self.config.roomSize[0]/2.0 + self.config.objectSize/2 + 0.5), 0],
                        self.config.exits.UP: [0, self.config.roomSize[1]/2.0 + self.config.objectSize/2 + 0.5],
                        self.config.exits.RIGHT: [self.config.roomSize[0]/2.0 + self.config.objectSize/2 + 0.5, 0]}

        self.insidePosForExit = {self.config.exits.DOWN: [0, (-1)*(self.config.roomSize[1]/2.0 - self.config.objectSize/2 - 0.1)],
                        self.config.exits.LEFT: [(-1)*(self.config.roomSize[0]/2.0 - self.config.objectSize/2), 0],
                        self.config.exits.UP: [0, self.config.roomSize[1]/2.0 - self.config.objectSize/2],
                        self.config.exits.RIGHT: [self.config.roomSize[0]/2.0 - self.config.objectSize/2, 0]}

        self.exitForKey = {'down': self.config.exits.DOWN,
                        'left': self.config.exits.LEFT,
                        'up': self.config.exits.UP,
                        'right': self.config.exits.RIGHT}

        # visual objects
        self.room = visual.Rect(win=self.window, width=self.config.roomSize[0], height=self.config.roomSize[1], lineColor=self.config.roomColor,
                                lineColorSpace='rgb', fillColor=self.config.roomColor, fillColorSpace='rgb', pos=[0,0], interpolate=True)
        self.doors = [];
        self.doors.append(visual.Rect(win=self.window, width=self.config.doorSize[0], height=self.config.doorSize[1], lineColor=self.config.doorColor,
                                lineColorSpace='rgb', pos=[0, (-1)*self.config.roomSize[1]/2.0 + self.config.doorSize[1]/2.0], interpolate=True))
        self.doors.append(visual.Rect(win=self.window, width=self.config.doorSize[1], height=self.config.doorSize[0], lineColor=self.config.doorColor,
                                lineColorSpace='rgb', pos=[(-1)*self.config.roomSize[0]/2.0 + self.config.doorSize[1]/2.0, 0], interpolate=True))
        self.doors.append(visual.Rect(win=self.window, width=self.config.doorSize[0], height=self.config.doorSize[1], lineColor=self.config.doorColor,
                                lineColorSpace='rgb', pos=[0, self.config.roomSize[1]/2.0 - self.config.doorSize[1]/2.0], interpolate=True))
        self.doors.append(visual.Rect(win=self.window, width=self.config.doorSize[1], height=self.config.doorSize[0], lineColor=self.config.doorColor,
                                lineColorSpace='rgb', pos=[self.config.roomSize[0]/2.0 - self.config.doorSize[1]/2.0, 0], interpolate=True))
        fixationX = visual.Line(win=self.window, lineColor=(1,1,1), lineColorSpace='rgb', start=(-0.25,0), end=(0.25,0), interpolate=True)
        fixationY = visual.Line(win=self.window, lineColor=(1,1,1), lineColorSpace='rgb', start=(0,-0.25), end=(0,0.25), interpolate=True)
        self.fixation = [fixationX, fixationY]


        circle = visual.Circle(win=self.window, radius=self.config.objectSize/2.0, lineColor=self.config.objectColor, lineColorSpace='rgb', fillColor=self.config.objectColor, fillColorSpace='rgb', pos=self.posForExit[self.config.exits.DOWN], interpolate=True)
        triangle = visual.Polygon(win=self.window, edges=3, radius=1.1*self.config.objectSize/2.0, lineColor=self.config.objectColor, lineColorSpace='rgb', fillColor=self.config.objectColor, fillColorSpace='rgb', pos=self.posForExit[self.config.exits.DOWN], ori=180, interpolate=True)
        square = visual.Rect(win=self.window, width=self.config.objectSize, height=self.config.objectSize, lineColor=self.config.objectColor, lineColorSpace='rgb', fillColor=self.config.objectColor, fillColorSpace='rgb', pos=self.posForExit[self.config.exits.DOWN], interpolate=True)

        practice1 = visual.Rect(win=self.window, width=self.config.objectSize/math.sqrt(2), height=self.config.objectSize/math.sqrt(2), lineColor=self.config.objectColor, lineColorSpace='rgb', fillColor=self.config.objectColor, fillColorSpace='rgb', pos=self.posForExit[self.config.exits.DOWN], ori=45, interpolate=True)
        practice21 = visual.Rect(win=self.window, width=self.config.objectSize, height=self.config.objectSize/3, lineColor=self.config.objectColor, lineColorSpace='rgb', fillColor=self.config.objectColor, fillColorSpace='rgb', pos=self.posForExit[self.config.exits.DOWN], interpolate=True)
        practice22 = visual.Rect(win=self.window, width=self.config.objectSize, height=self.config.objectSize/3, lineColor=self.config.objectColor, lineColorSpace='rgb', fillColor=self.config.objectColor, fillColorSpace='rgb', pos=self.posForExit[self.config.exits.DOWN], ori=90, interpolate=True)
        practice31 = visual.Polygon(win=self.window, edges=3, radius=self.config.objectSize/2.0, lineColor=self.config.objectColor, lineColorSpace='rgb', fillColor=self.config.objectColor, fillColorSpace='rgb', pos=self.posForExit[self.config.exits.DOWN], interpolate=True)
        practice32 = visual.Polygon(win=self.window, edges=3, radius=self.config.objectSize/2.0, lineColor=self.config.objectColor, lineColorSpace='rgb', fillColor=self.config.objectColor, fillColorSpace='rgb', pos=self.posForExit[self.config.exits.DOWN], ori=180, interpolate=True)

        self.shapeVis = {self.config.shapes.CIRCLE: [circle],
                         self.config.shapes.TRIANGLE: [triangle],
                         self.config.shapes.SQUARE: [square],
                         self.config.shapes.PRACTICE_1: [practice1],
                         self.config.shapes.PRACTICE_2: [practice21, practice22],
                         self.config.shapes.PRACTICE_3: [practice31, practice32]}

        self.warningEarly = visual.TextStim(win=self.window, text=u'Zu früh', color=(1, -1, -1), colorSpace='rgb', height=1, pos=[0, self.config.roomSize[1]/2.0 + self.config.objectSize + 1], bold=True)
        self.warningLate = visual.TextStim(win=self.window, text=u'Zu spät', color=(1, -1, -1), colorSpace='rgb', height=1, pos=[0, self.config.roomSize[1]/2.0 + self.config.objectSize + 1], bold=True)
        self.warningExitReaction = visual.TextStim(win=self.window, text=u'Falsch reagiert', color=(1, -1, -1), colorSpace='rgb', height=1, pos=[0, self.config.roomSize[1]/2.0 + self.config.objectSize + 1], bold=True)

        imgStart1 = visual.SimpleImageStim(win=self.window, image="..\\img\\aufgabe1.png")
        imgStart2 = visual.SimpleImageStim(win=self.window, image="..\\img\\aufgabe2.png")
        imgStart3 = visual.SimpleImageStim(win=self.window, image="..\\img\\aufgabe3.png")
        imgPractice1 = visual.SimpleImageStim(win=self.window, image="..\\img\\training1.png")
        imgPractice2 = visual.SimpleImageStim(win=self.window, image="..\\img\\training2.png")
        imgExperiment = visual.SimpleImageStim(win=self.window, image="..\\img\\versuch.png")
        self.NoisyBG = visual.ImageStim(win=self.window, image="..\\img\\howToNameThisPattern.png") #importing background noise image

        self.instructions = {'start1': imgStart1,
                             'start2': imgStart2,
                             'start3': imgStart3,
                             'practice1': imgPractice1,
                             'practice2': imgPractice2,
                             'experiment': imgExperiment}
        #=======================================================================
        # SMI Handling
        # filefolder should be common for both the computers???
        #=======================================================================
        pathOnLaptop = 'D:\\Renker\\TunnelExpD\\data\\'
        Filename = str(self.config.subject)+'_SMI_'
        self.outputfile = pathOnLaptop + Filename + str(self.config.subject)
        self.outputfilecalib = pathOnLaptop+ Filename + '_Calib' + str(self.config.subject)

        # ---------------------------------------------
        #---- connect to iViewX
        # ---------------------------------------------
        listenip='169.254.154.119'  #Eyetracker laptop IP
        targetip='169.254.154.5'   #psychoPy computer IP

        res = iViewXAPI.iV_SetLogger(c_int(1), c_char_p("iViewXSDK_TrackerTest.txt"))
        res = iViewXAPI.iV_Connect(c_char_p(targetip), c_int(4444), c_char_p(listenip), c_int(5555))

        print 'res:' +str(res)
        res = iViewXAPI.iV_GetSystemInfo(byref(systemData))
        print "iV_GetSystemInfo: " + str(res)
        print "Samplerate: " + str(systemData.samplerate)
        print "iViewX Version: " + str(systemData.iV_MajorVersion) + "." + str(systemData.iV_MinorVersion) + "." + str(systemData.iV_Buildnumber)
        print "iViewX API Version: " + str(systemData.API_MajorVersion) + "." + str(systemData.API_MinorVersion) + "." + str(systemData.API_Buildnumber)
        # ---------------------------------------------
        #---- configure and start calibration
        # ---------------------------------------------
        self.useSMI = True

    def calibration(self,calibrate):
        '''
        # SMI calibration method
        '''
        if calibrate:
            cali=1
            while cali==1:
                calibrationData = CCalibration(9, 1, 1, 0, 1, 250, 220, 2, 20, b"")
                accuracyData = CValidation(-1,-1,-1,-1)
                res = iViewXAPI.iV_SetupCalibration(byref(calibrationData))
                print "iV_SetupCalibration " + str(res)
                res = iViewXAPI.iV_Calibrate()
                print "iV_Calibrate " + str(res)
                res = iViewXAPI.iV_Validate()
                print "iV_Validate " + str(res)

                res = iViewXAPI.iV_GetAccuracy(byref(accuracyData), 0)
                print "iV_GetAccuracy " + str(res)
                print "deviationXLeft " + str(accuracyData.deviationLX) + " deviationYLeft " + str(accuracyData.deviationLY)
                print "deviationXRight " + str(accuracyData.deviationRX) + " deviationYRight " + str(accuracyData.deviationRX)
                res = iViewXAPI.iV_SaveCalibration(self.outputfilecalib)
                print "Saving Calibration data " + str(res)
                self.showText('w - Wiederholen, Leertaste - Akzeptiert')

        else :
            print "no calibaration"


    def drawNoisyBackground(self):
        '''Method to draw noise background
        '''
        self.NoisyBG.draw()
        #self.window.flip()



    def drawRoom(self):

        self.room.draw()
        for d in self.doors:
            d.draw()


    def drawFixation(self):
        for f in self.fixation:
            f.draw()


    def drawShape(self, shape):
        for s in shape:
            s.draw()


    def setShapePos(self, shape, pos):
        for s in shape:
            s.setPos(pos)


    def setShapeColor(self, shape, color):
        for s in shape:
            s.lineColor = color
            s.fillColor = color


    def changeShapeOrientation(self, shape, angle):
        for s in shape:
            s.ori += angle


    def showText(self, txt):
        textObj = visual.TextStim(win=self.window, text=txt, color=(-1,-1,-1), colorSpace='rgb', height=2, bold=True, wrapWidth=50)
        textObj.draw()
        self.window.flip()

        key = event.waitKeys(keyList=['space','escape'])
        if key[0] == 'escape':
            self.quit()
        self.window.flip()


    def showImage(self, img):
        img.draw()
        self.window.flip()

        key = event.waitKeys(keyList=['space','escape'])
        if key[0] == 'escape':
            self.quit()
        self.window.flip()


    def move(self, obj, oldPos, newPos, perc):
        currentPos = (oldPos[0]+perc*(newPos[0]-oldPos[0]), oldPos[1]+perc*(newPos[1]-oldPos[1]))
        for o in obj:
            o.setPos(currentPos)


    def saveData(self):
        filename = os.path.join(self.config.outputFolder, "vp"+str(self.config.subject), str(self.config.subject)+"_result_data.txt")
        np.savetxt(filename,self.resultData,fmt='%-10.1i\t%-10.1i\t%-10.1i\t%-10.1i\t%-10.1i\t%-10.1i\t%-10.6f\t%-10.1i\t%-10.6f\t%-10.1i',
            delimiter='\t',header='Subject\tBlock\tTrial\tObject_Type\tExit\tResponse\tRT\tExit_Response\tExit_RT\tChanged_Color',comments='')


    def runTrial(self, shape, target, changeColor):
        shapeObject = self.shapeVis[shape]

        error = False
        acceptingInput = False
        tooEarly = False
        tooLate = False
        tooEarlyStart = 0
        inputStartTime = 0

        exitChosen = -1
        reactionTime = -1
        exitChosen2 = -1
        reactionTime2 = -1

        event.clearEvents()
        self.drawNoisyBackground()
        self.setShapeColor(shapeObject, self.config.objectColor)
        self.drawRoom()
        self.drawFixation()
        self.window.flip()

        core.wait(self.config.fixationDuration)

        #shapeObject.setPos(self.posForExit[self.config.exits.DOWN])
        #shapeObject.draw()
        self.drawNoisyBackground()
        self.setShapePos(shapeObject, self.posForExit[self.config.exits.DOWN])
        self.drawShape(shapeObject)
        self.drawRoom()
        self.window.flip()

        core.wait(self.config.entranceDuration)
        keys = event.getKeys(keyList=['left','right','up','down','escape'])
        if len(keys) > 0:
            if keys[0] == 'escape':
                self.quit()
            else:
                tooEarly = True
                error = True
                tooEarlyStart = core.getTime()

            event.clearEvents()

        # move inside
        startTime = core.getTime()
        currentTime = startTime
        while currentTime < startTime + self.config.movementDurationEntrance:
            relTime = currentTime-startTime
            self.move(shapeObject, self.posForExit[self.config.exits.DOWN], self.insidePosForExit[self.config.exits.DOWN], relTime/self.config.movementDurationEntrance)
            currentTime = core.getTime()

            if not acceptingInput and shapeObject[0].pos[1]-self.config.objectSize/2 >= (-1)*self.config.roomSize[1]/2:
                acceptingInput = True
                inputStartTime = core.getTime()

            keys = event.getKeys(keyList=['left','right','up','down','escape'])
            if len(keys) > 0:
                if keys[0] == 'escape':
                    self.quit()
                elif acceptingInput:
                    exitChosen = self.exitForKey[keys[0]]
                    reactionTime = core.getTime() - inputStartTime
                    tooEarly = False
                else:
                    tooEarly = True
                    error = True
                    tooEarlyStart = core.getTime()

                event.clearEvents()

            if core.getTime() - tooEarlyStart > 1:
                tooEarly = False
            self.drawNoisyBackground()
            self.drawShape(shapeObject)
            self.drawRoom()
            if tooEarly:
                # show warning
                self.warningEarly.draw()
            self.window.flip()

        if changeColor:
            self.setShapeColor(shapeObject, self.config.objectColorPost)

        if not acceptingInput:
            inputStartTime = core.getTime()

        # wait inside
        startTime = core.getTime()
        currentTime = startTime
        while currentTime < startTime + self.config.delay:
            keys = event.getKeys(keyList=['left','right','up','down','escape'])
            if len(keys) > 0:
                if keys[0] == 'escape':
                    self.quit()
                else:
                    exitChosen = self.exitForKey[keys[0]]
                    reactionTime = core.getTime() - inputStartTime
                event.clearEvents()

            if currentTime - tooEarlyStart > 1:
                tooEarly = False
            self.drawNoisyBackground()
            self.drawShape(shapeObject)
            self.drawRoom()
            if tooEarly:
                # show warning
                self.warningEarly.draw()
            self.window.flip()

            currentTime = core.getTime()

        if exitChosen == -1 and not error:
            tooLate = True
            error = True

        # rotate shape
        if target == self.config.exits.LEFT:
            self.changeShapeOrientation(shapeObject, -90)
        elif target == self.config.exits.RIGHT:
            self.changeShapeOrientation(shapeObject, 90)
        elif target == self.config.exits.DOWN:
            self.changeShapeOrientation(shapeObject, 180)

        # move out
        startTime = core.getTime()
        currentTime = startTime
        inputStartTime = startTime
        while currentTime < startTime + self.config.movementDurationExit:
            relTime = currentTime-startTime
            self.move(shapeObject, self.insidePosForExit[target], self.posForExit[target], relTime/self.config.movementDurationExit)
            currentTime = core.getTime()

            keys = event.getKeys(keyList=['left','right','up','down','escape'])
            if len(keys) > 0:
                if keys[0] == 'escape':
                    self.quit()
                else:
                    exitChosen2 = self.exitForKey[keys[0]]
                    reactionTime2 = core.getTime() - inputStartTime
                event.clearEvents()

            if relTime > 1:
                tooLate = False
            self.drawNoisyBackground()
            self.drawShape(shapeObject)
            self.drawRoom()
            if tooLate:
                # show warning
                self.warningLate.draw()
            self.window.flip()
        self.drawNoisyBackground()
        self.drawShape(shapeObject)
        self.drawRoom()
        if not error and ((exitChosen2 != target and changeColor) or (exitChosen2 != -1 and not changeColor)):
            self.warningExitReaction.draw();
        self.window.flip()

        core.wait(self.config.exitDuration)

        # undo rotation
        if target == self.config.exits.LEFT:
            self.changeShapeOrientation(shapeObject, 90)
        elif target == self.config.exits.RIGHT:
            self.changeShapeOrientation(shapeObject, -90)
        elif target == self.config.exits.DOWN:
            self.changeShapeOrientation(shapeObject, -180)

        if error:
            exitChosen = -1
            reactionTime = -1
            exitChosen2 = -1
            reactionTime2 = -1

        return exitChosen, reactionTime, exitChosen2, reactionTime2


    # Run trial block <blockNum> with given list of trials
    def runBlock(self,blockNum,trialList):
        for i in np.arange(trialList.shape[0]):
            if self.useSMI:
                #tobii.setTrigger(self.trial)
                iViewXAPI.iV_SendImageMessage(c_char_p('Trigger '+ str(self.trial)))
            resp, rt, exitResp, exitRT = self.runTrial(*trialList[i])

            if self.save:
                self.resultData[self.trialIdx,:] = [self.config.subject, blockNum, self.trial, trialList[i,0], trialList[i,1], resp, rt, exitResp, exitRT, trialList[i,2]]
                self.trialIdx += 1
                self.trial += 1
                self.saveData()


    # Creates randomized list to match shapes (first column) with exits (second column)
    def createTrialList(self, listType):
        if listType == "practice1" or listType == "practice2":
            shapeList = [self.config.shapes.PRACTICE_1, self.config.shapes.PRACTICE_2, self.config.shapes.PRACTICE_3]
        else:
            shapeList = [self.config.shapes.CIRCLE, self.config.shapes.TRIANGLE, self.config.shapes.SQUARE]
        exitList = [self.config.exits.LEFT, self.config.exits.UP, self.config.exits.RIGHT]

        if listType == "practice1":
            trialList = np.zeros(shape=(self.config.trialsPractice1*3*len(shapeList),3),dtype=np.float64)
            # for each shape
            for i in np.arange(len(shapeList)):
                startIdx = i*self.config.trialsPractice1*3
                endIdx = (i+1)*self.config.trialsPractice1*3
                trialList[startIdx:endIdx, 0] = shapeList[i]

                # for each exit
                for j in np.arange(len(exitList)):
                    trialList[startIdx+j*self.config.trialsPractice1*3/len(exitList):startIdx+(j+1)*self.config.trialsPractice1*3/len(exitList), 1] = exitList[j]

        elif listType == "practice2":
            trialList = np.zeros(shape=(self.config.trialsPractice2*len(shapeList),3),dtype=np.float64)
            # for each shape
            for i in np.arange(len(shapeList)):
                startIdx = i*self.config.trialsPractice2
                endIdx = (i+1)*self.config.trialsPractice2
                trialList[startIdx:endIdx, 0] = shapeList[i]
                # shape always uses main exit
                trialList[startIdx:endIdx, 1] = self.config.exitsForShape[shapeList[i]][0]

        elif listType == "experiment":
            blockLength = (self.config.trialsPerBlockHigh+2*self.config.trialsPerBlockLow+self.config.trialsPerBlockStart)*len(shapeList)
            trialList = np.zeros(shape=(blockLength,3),dtype=np.float64)
            # for each shape
            for i in np.arange(len(shapeList)):
                startIdx = i*blockLength/len(shapeList)
                endIdx = (i+1)*blockLength/len(shapeList)
                trialList[startIdx:endIdx, 0] = shapeList[i]

                trialList[startIdx:startIdx+self.config.trialsPerBlockHigh, 1] = self.config.exitsForShape[shapeList[i]][0]
                trialList[startIdx+self.config.trialsPerBlockHigh:startIdx+self.config.trialsPerBlockHigh+self.config.trialsPerBlockLow, 1] = self.config.exitsForShape[shapeList[i]][1]
                trialList[startIdx+self.config.trialsPerBlockHigh+self.config.trialsPerBlockLow:startIdx+self.config.trialsPerBlockHigh+2*self.config.trialsPerBlockLow, 1] = self.config.exitsForShape[shapeList[i]][2]
                trialList[endIdx-1, 1] = self.config.exits.DOWN

        # change color in 50% of trials
        changeColor = np.zeros(shape=(trialList.shape[0],1),dtype=np.float64)
        changeColor[:changeColor.shape[0]/2] = 1
        np.random.shuffle(changeColor)
        trialList[:,2] = changeColor[:,0]
        acc = False
        while not acc:
            idx = np.where((trialList[:,1] == 0) & (trialList[:,2] == 1))[0]
            if np.size(idx) > 0:
                np.random.shuffle(changeColor)
                trialList[:,2] = changeColor[:,0]
            else:
                acc = True

        # shuffle list
        np.random.shuffle(trialList)

        return trialList


    def run(self):
        if self.resume:
            self.showText("Versuch wird fortgesetzt")

        if self.useSMI and not self.resume:
            self.showText("Kalibrierung")
            self.calibration(self.useSMI)
            #tobii.showCalibrationResultNet()
            event.waitKeys()


        if not (self.resume and self.resumeBlock != 0):
            self.showImage(self.instructions["start1"])
            self.showImage(self.instructions["start2"])
            self.showImage(self.instructions["start3"])

            # practice 1
            trials = self.createTrialList("practice1")
            self.showImage(self.instructions["practice1"])
            self.showText("Block 1")
            self.runBlock(0, trials)

        self.save = True


        # practice 2
        if self.resume:
            if self.resumeBlock < 0:
                self.showImage(self.instructions["practice2"])
                self.practiceStartBlock = self.resumeBlock
            else:
                self.practiceStartBlock = 0
        else:
            self.showImage(self.instructions["practice2"])

        for b in np.arange(self.practiceStartBlock, 0):
            trials = self.createTrialList("practice2")
            self.showText("Block "+str(b+1+self.config.practice2Blocks))
            if self.useSMI:
                iViewXAPI.iV_StartRecording()
            self.runBlock(b, trials)
            if self.useSMI:
                iViewXAPI.iV_PauseRecording() #pause recording until start of next trial
            # feedback
            blockIdx = np.nonzero(self.resultData[:,1] == b)[0]
            correctIdx = np.nonzero(self.resultData[blockIdx,4] == self.resultData[blockIdx,5])[0]
            self.showText(str(np.round(100*float(np.size(correctIdx))/float(np.size(blockIdx)), 2))+"% richtig")


        self.trial = 1

        # experiment
        if self.resume and self.resumeBlock > 0:
            self.startBlock = self.resumeBlock
        self.showImage(self.instructions["experiment"])
        for b in np.arange(self.startBlock,self.config.blocks+1):
            trials = self.createTrialList("experiment")
            self.showText("Block "+str(b))
            if self.useSMI:
                iViewXAPI.iV_StartRecording()
            self.runBlock(b,trials)
            if self.useSMI:
                iViewXAPI.iV_PauseRecording() #pause recording until start of next trial
            # feedback
            blockIdx = np.nonzero(self.resultData[:,1] == b)[0]
            correctIdx = np.nonzero(self.resultData[blockIdx,4] == self.resultData[blockIdx,5])[0]
            self.showText(str(np.round(100*float(np.size(correctIdx))/float(np.size(blockIdx)), 2))+"% richtig")

        self.showText("Versuch abgeschlossen")

        self.quit()

    def quit(self):
        self.window.close()
        if self.useSMI:
            iViewXAPI.iV_StopRecording() #stop eye tracker
            res = iViewXAPI.iV_SaveData(str(self.outputfile), str('TunnelExpSmi'), str(self.config.subject), 0)
            iViewXAPI.iV_Disconnect() # disconnect the eyetracker connection
            ## saving files while using quit method
            ##tobii._gazeProcessor.closeFiles()
        core.quit()

    def loadExistingData(self):
        exData = np.loadtxt(os.path.join(self.config.outputFolder, "vp"+str(self.config.subject), str(self.config.subject)+"_result_data.txt"), skiprows=1, dtype=np.float64)
        idx = np.nonzero(exData[:,1] != 0)[0]
        if np.size(idx) > 0:
            lastBlock = int(exData[idx[-1],1])
            idxBlock = np.nonzero(exData[:,1] == lastBlock)[0]
            if lastBlock < 0:
                if np.size(idxBlock) < self.config.trialsPractice2*3:
                    exData[idxBlock,:] = 0
                    self.resumeBlock = lastBlock
                else:
                    self.resumeBlock = lastBlock+1
                    if self.resumeBlock == 0:
                        self.resumeBlock = 1
            else:
                if np.size(idxBlock) < (self.config.trialsPerBlockHigh+2*self.config.trialsPerBlockLow+self.config.trialsPerBlockStart)*3:
                    exData[idxBlock,:] = 0
                    self.resumeBlock = lastBlock
                else:
                    self.resumeBlock = lastBlock+1

            self.trialIdx = np.nonzero(exData[:,2] == 0)[0][0]
            if self.resumeBlock < 0:
                self.trial = self.trialIdx+1
            else:
                self.trial = self.trialIdx+1 - self.config.trialsPractice2*3*self.config.practice2Blocks

            self.resultData = exData