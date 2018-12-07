class Main(object):

    def Setup(self, numOfOutputs, maxOutputSize, winningModeON=False):
        self.NumOfOutputs = numOfOutputs
        self.MaxOutputSize = maxOutputSize
        self.MaxMoveIDs = maxOutputSize * numOfOutputs
        self.WinningModeON = winningModeON
        self.DataSet = {}
        self.TempDataSet = {}

        return

    def MoveCal(self, board):
        key = BoardToKey(board)
        moveID = 0

        if key in self.DataSet:
            if self.WinningModeON:
                print("winnning mode!")

            else:  # learning mode
                dataSetItem = self.DataSet[key]
                if len(dataSetItem) < self.MaxMoveIDs:
                    moveID = len(dataSetItem)

                else:
                    leastPlayed = dataSetItem[0]["TimesPlayed"]
                    for loop in range(1,len(dataSetItem)):

                        if dataSetItem[loop]["Valid"] and dataSetItem[loop]["TimesPlayed"] < leastPlayed:
                            leastPlayed = dataSetItem[loop]["TimesPlayed"]
                            moveID = loop

        self.TempDataSet[key] = moveID
        return MoveIDToMove(moveID, self.NumOfOutputs, self.MaxOutputSize)
    
    def UpdateInvalidMove(self, board, move):
        print("invalid: " + str(move) + " on board: " + str(board))
        key = BoardToKey(board)
        moveID = MoveToMoveID(move, self.NumOfOutputs, self.MaxOutputSize)

        if key in self.TempDataSet:
            if self.TempDataSet[key] == moveID:
                self.TempDataSet.pop(key)

        self.AddMoveToDataset(key, moveID, 0, valid=False)
        return
    
    def UpdateData(self, fitness):
        #need to code
        return
    
    def AddMoveToDataset(self, key, moveID, fitness, valid=True):
        #self.DataSet[key][moveID] = {"Valid": valid, "TimesPlayed": 1, "Fitness": fitness}
        if key in self.DataSet:
            self.DataSet[key][moveID] = {"Valid": valid, "TimesPlayed": 1, "Fitness": fitness}
        else:
            self.DataSet[key] = {moveID: {"Valid": valid, "TimesPlayed": 1, "Fitness": fitness}}
        return


def MoveIDToMove(moveID, numOfOutputs, maxOutputSize):
    move = []
    for loop in range(numOfOutputs):
        move += [int(moveID / (maxOutputSize)**((numOfOutputs - loop)-1))]
        moveID = moveID % (maxOutputSize)**((numOfOutputs - loop)-1)
    return move

def MoveToMoveID(move, numOfOutputs, maxOutputSize):
    moveID = 0
    for loop in range(len(move)):
        moveID += move[loop]*(maxOutputSize**((numOfOutputs - loop)-1))


    return moveID

def BoardToKey(board):

    return str(board)
