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
			print("DataSet Saved! Size: " + str(len(self.DataSet)))
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


class BruteForce(object):

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
				
				if not self.DataSetManager.DataSet[key].NumOfTriedMoves < self.DataSetManager.MaxMoveIDs:
					if len(self.DataSetManager.DataSet[key].Moves) == 0:
						print("error!")
						self.DataSetManager.DataSet[key].NumOfTriedMoves = 0

				if self.DataSetManager.DataSet[key].NumOfTriedMoves < self.DataSetManager.MaxMoveIDs:
					moveID = self.DataSetManager.DataSet[key].NumOfTriedMoves
					self.DataSetManager.DataSet[key].Moves += [MoveInfo(MoveID=moveID)]
					self.DataSetManager.DataSet[key].NumOfTriedMoves += 1

				else:
					leastPlayed = self.DataSetManager.DataSet[key].Moves[0].TimesPlayed
					moveID = self.DataSetManager.DataSet[key].Moves[0].MoveID
					pickedItem = 0

					for loop in range(1,len(self.DataSetManager.DataSet[key].Moves)):
						
						if self.DataSetManager.DataSet[key].Moves[loop].TimesPlayed < leastPlayed:
							leastPlayed = self.DataSetManager.DataSet[key].Moves[loop].TimesPlayed
							moveID = self.DataSetManager.DataSet[key].Moves[loop].MoveID
							pickedItem = loop
					
					self.DataSetManager.DataSet[key].Moves[pickedItem].TimesPlayed += 1

			else:
				moveID = 0
				moveInfo = MoveInfo(MoveID=moveID)
				self.DataSetManager.DataSet[key] = BoardInfo(Moves=[moveInfo])




		self.TempDataSet += [{"BoardKey": key, "MoveID": moveID}]
		move = self.DataSetManager.MoveIDLookUp[moveID]
		return move

	def UpdateInvalidMove(self, board, move):
		key = self.BoardToKey(board)
		moveID = self.DataSetManager.MoveIDLookUp.index(move)

		for loop in range(len(self.DataSetManager.DataSet[key].Moves)-1, -1, -1):
			if self.DataSetManager.DataSet[key].Moves[loop].MoveID == moveID:
				del self.DataSetManager.DataSet[key].Moves[loop]
				break

		self.TempDataSet.remove({"BoardKey": key, "MoveID": moveID})
		return
	
	def UpdateData(self, fitness):
		for loop in range(len(self.TempDataSet)):
			key = self.TempDataSet[loop]["BoardKey"]
			moveID = self.TempDataSet[loop]["MoveID"]

			for loop in range(len(self.DataSetManager.DataSet[key].Moves)-1, -1, -1):
				if self.DataSetManager.DataSet[key].Moves[loop].MoveID == moveID:

					newFitness = self.DataSetManager.DataSet[key].Moves[loop].AvgFitness*self.DataSetManager.DataSet[key].Moves[loop].TimesPlayed
					newFitness += fitness
					self.DataSetManager.DataSet[key].Moves[loop].TimesPlayed += 1
					newFitness /= self.DataSetManager.DataSet[key].Moves[loop].TimesPlayed
					self.DataSetManager.DataSet[key].Moves[loop].AvgFitness = newFitness
					break

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
		self.NumOfTriedMoves = NumOfTriedMoves
		self.Moves = Moves
		return

class MoveInfo():
	AvgFitness = 0.0
	TimesPlayed = 1
	MoveID = 0

	def __init__(self, AvgFitness=0.0, TimesPlayed=1, MoveID=0):
		self.AvgFitness = AvgFitness
		self.TimesPlayed = TimesPlayed
		self.MoveID = MoveID
		return
