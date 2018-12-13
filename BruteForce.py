import pickle
import os

class DataSetManager(object):
    DataSet = {}
    MoveIDLookUp = []
    MaxMoveIDs = 0
    
    def __init__(self, numOfOutputs, maxOutputSize, outputResolution=1, loadData=True):
        self.NumOfOutputs = numOfOutputs
        self.MaxOutputSize = maxOutputSize
        self.MaxMoveIDs = maxOutputSize ** numOfOutputs

        self.RunningAIs = []
        self.DataSet = {}
        self.MoveIDLookUp = self.BuildMoveIDLookUp()
        if loadData:
            self.LoadDataSet()

        return

    def BuildMoveIDLookUp(self):
        moveIDLookUp = []
        for loop in range(self.MaxMoveIDs):
            moveIDLookUp += [self.MoveIDToMove(loop)]

        return moveIDLookUp
    
    def SetupNewAI(self):
        AiNumber = len(self.RunningAIs)
        self.RunningAIs += [False]
        return AiNumber
    
    def SaveDataSet(self, AiNumber):
        self.RunningAIs[AiNumber] = True
        canSave = True

        for loop in range(len(self.RunningAIs)):
            if self.RunningAIs[loop] == False:
                canSave = False

        if canSave:
            pickle.dump(self.DataSet, open("DataSet//DataSet.p", "wb"))
            #add a save to save on boards
            for loop in range(len(self.RunningAIs)):
                self.RunningAIs[loop] = False
        return
    
    def LoadDataSet(self):
        if os.path.isfile("DataSet//DataSet.p"):
            self.DataSet = pickle.load(open("DataSet//DataSet.p", "rb"))

        print("DataSet lenght: " + str(len(self.DataSet)))
        return
    
    def MoveIDToMove(self, moveID):
        #maybe make this a lookuptabel in stead but will use more memory
        move = []
        for loop in range(self.NumOfOutputs):
            move += [int(moveID / (self.MaxOutputSize)**((self.NumOfOutputs - loop)-1))]
            moveID = moveID % (self.MaxOutputSize)**((self.NumOfOutputs - loop)-1)
        return move


class Main(object):

    def __init__(self, dataSetManager, winningModeON=False):
        self.DataSetManager = dataSetManager
        self.WinningModeON = winningModeON

        self.TempDataSet = []

        self.AiNumber = self.DataSetManager.SetupNewAI()
        return

    def MoveCal(self, board):
        key = self.BoardToKey(board)

        if self.WinningModeON:
            print("winnning mode!")

        else:  # learning mode
            if key in self.DataSetManager.DataSet:
                dataSetItem = self.DataSetManager.DataSet[key]

                if dataSetItem.NumOfTriedMoves < self.DataSetManager.MaxMoveIDs:
                    moveID = dataSetItem.NumOfTriedMoves
                    dataSetItem.Moves += [MoveInfo(MoveID=moveID)]
                    dataSetItem.NumOfTriedMoves += 1

                else:
                    Moves = dataSetItem.Moves
                    leastPlayed = Moves[0].TimesPlayed
                    moveID = Moves[0].MoveID

                    for loop in range(1,len(Moves)):
                        
                        if Moves[loop].TimesPlayed < leastPlayed:
                            leastPlayed = Moves[loop].TimesPlayed
                            moveID = Moves[loop].MoveID
                            pickedItem = loop
                    
                    dataSetItem.Moves[pickedItem].TimesPlayed += 1
                self.DataSetManager.DataSet[key] = dataSetItem

            else:
                moveID = 0
                self.DataSetManager.DataSet[key] = BoardInfo(Moves=[MoveInfo(MoveID=0)])




        self.TempDataSet += [{"BoardKey": key, "MoveID": moveID}]
        move = self.DataSetManager.MoveIDLookUp[moveID]
        return move

    def UpdateInvalidMove(self, board, move):
        key = self.BoardToKey(board)
        moveID = self.DataSetManager.MoveIDLookUp.index(move)

        moves = self.DataSetManager.DataSet[key].Moves
        for loop in range(len(moves)-1, -1, -1):
            if moves[loop].MoveID == moveID:
                del moves[loop]
                break

        self.TempDataSet.remove({"BoardKey": key, "MoveID": moveID})

        self.DataSetManager.DataSet[key].Moves = moves

        return
    
    def UpdateData(self, fitness):
        for loop in range(len(self.TempDataSet)):
            key = self.TempDataSet[loop]["BoardKey"]
            moveID = self.TempDataSet[loop]["MoveID"]

            datasetItem = self.DataSetManager.DataSet[key].Moves[moveID]
            
            newFitness = datasetItem.AvgFitness*datasetItem.TimesPlayed
            newFitness += fitness
            datasetItem.TimesPlayed += 1
            newFitness /= datasetItem.TimesPlayed
            datasetItem.AvgFitness = newFitness

            self.DataSetManager.DataSet[key].Moves[moveID] = datasetItem

        self.TempDataSet = []
        self.DataSetManager.SaveDataSet(self.AiNumber)
        return

    def BoardToKey(self, board):
        board = str(board)
        return board.replace(" ", "")

class BoardInfo():
    NumOfTriedMoves = 1
    Moves = []

    def __init__(self, NumOfTriedMoves=1, Moves=[]):
        NumOfTriedMoves = NumOfTriedMoves
        Moves = Moves
        return

class MoveInfo():
    AvgFitness = 0.0
    TimesPlayed = 1
    MoveID = 0

    def __init__(self, AvgFitness=0.0, TimesPlayed=1, MoveID=0):
        AvgFitness = AvgFitness
        TimesPlayed = TimesPlayed
        MoveID = MoveID
        return
