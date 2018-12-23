import pickle
import os
import sys

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
			if key in self.DataSetManager.DataSet and len(self.DataSetManager.DataSet[key].Moves) > 0:
				bestAvgFitness = -sys.maxsize
				moveID = 0
				for movekey, moveValue in self.DataSetManager.DataSet[key].Moves.items():
					if moveValue.AvgFitness > bestAvgFitness:
						leastPlayed = moveValue.TimesPlayed
						moveID = movekey

			else:#never played board before
				moveID = 0
				print("new Board!")

		else:  # learning mode
			if key in self.DataSetManager.DataSet:
				
				if not self.DataSetManager.DataSet[key].NumOfTriedMoves < self.DataSetManager.MaxMoveIDs:
					if len(self.DataSetManager.DataSet[key].Moves) == 0:
						input("error!!!")

				if self.DataSetManager.DataSet[key].NumOfTriedMoves < self.DataSetManager.MaxMoveIDs:
					moveID = self.DataSetManager.DataSet[key].NumOfTriedMoves
					self.DataSetManager.DataSet[key].Moves[moveID] = MoveInfo(MoveID=moveID)
					self.DataSetManager.DataSet[key].NumOfTriedMoves += 1

				else:#played every board once already
					leastPlayed = sys.maxsize
					moveID = 0
					for movekey, moveValue in self.DataSetManager.DataSet[key].Moves.items():
						if moveValue.TimesPlayed < leastPlayed:
							leastPlayed = moveValue.TimesPlayed
							moveID = movekey
					
					self.DataSetManager.DataSet[key].Moves[moveID].TimesPlayed += 1

			else:#never played board before
				moveID = 0
				moveInfo = {moveID : MoveInfo(MoveID=moveID)}
				self.DataSetManager.DataSet[key] = BoardInfo(Moves=moveInfo)

			#cahnge tempdataset to dict so faster to del for bigger lists
			self.TempDataSet += [{"BoardKey": key, "MoveID": moveID}]


		move = self.DataSetManager.MoveIDLookUp[moveID]
		return move

	def UpdateInvalidMove(self, board, move):
		key = self.BoardToKey(board)
		moveID = self.DataSetManager.MoveIDLookUp.index(move)

		if key in self.DataSetManager.DataSet:
			if moveID in self.DataSetManager.DataSet[key].Moves:
				del self.DataSetManager.DataSet[key].Moves[moveID]
			
		#cahnge tempdataset to dict so faster to del for bigger lists
		if {"BoardKey": key, "MoveID": moveID} in self.TempDataSet:
			self.TempDataSet.remove({"BoardKey": key, "MoveID": moveID})
		return
	
	def UpdateData(self, fitness):
		for loop in range(len(self.TempDataSet)):
			key = self.TempDataSet[loop]["BoardKey"]
			moveID = self.TempDataSet[loop]["MoveID"]

			if moveID in self.DataSetManager.DataSet[key].Moves:
				newFitness = self.DataSetManager.DataSet[key].Moves[moveID].AvgFitness*self.DataSetManager.DataSet[key].Moves[moveID].TimesPlayed
				newFitness += fitness
				self.DataSetManager.DataSet[key].Moves[moveID].TimesPlayed += 1
				newFitness /= self.DataSetManager.DataSet[key].Moves[moveID].TimesPlayed
				self.DataSetManager.DataSet[key].Moves[moveID].AvgFitness = newFitness


		self.TempDataSet = []
		self.DataSetManager.SaveDataSet(self.AiNumber)
		return

	def BoardToKey(self, board):
		board = str(board)
		return board.replace(" ", "")

class BoardInfo():
	NumOfTriedMoves = 1
	MoveIDOfLeastPlayed = 1
	MoveIDOfBestAvgFitness = 0
	BestAvgFitness = -sys.maxsize
	Moves = {}

	def __init__(self, NumOfTriedMoves=1, Moves={}, moveIDOfLeastPlayed=1, moveIDOfBestAvgFitness=0, bestAvgFitness=-sys.maxsize):
		self.NumOfTriedMoves = NumOfTriedMoves
		self.Moves = Moves
		self.MoveIDOfLeastPlayed = moveIDOfLeastPlayed
		self.MoveIDOfBestAvgFitness = moveIDOfBestAvgFitness
		self.BestAvgFitness = bestAvgFitness
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


# 1) point to the move that is least played
# 2) point to the move that has best avg fitness
# 3) speed up tempdataset (maybe dict) so that it can delete item in invalid wiht O(1) instead of O(N)