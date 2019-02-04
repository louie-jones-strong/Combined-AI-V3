import pickle
import os
import sys
import random

class DataSetManager(object):
	DataSet = {}
	NumberOfCompleteBoards = 0
	MoveIDLookUp = []
	MaxMoveIDs = 0
	
	def __init__(self, numOfOutputs, minOutputSize, maxOutputSize, outputResolution, datasetAddress):
		self.NumOfOutputs = numOfOutputs

		self.MinOutputSize = minOutputSize
		self.MaxOutputSize = maxOutputSize
		self.OutputResolution = outputResolution

		self.MaxMoveIDs = int(((maxOutputSize-(minOutputSize-1))*(1/outputResolution) )**numOfOutputs)
		self.DatasetAddress = datasetAddress

		self.RunningAIs = []
		self.DataSet = {}
		self.MoveIDLookUp = self.BuildMoveIDLookUp()
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
			pickle.dump(self.DataSet, open(self.DatasetAddress + ".p", "wb"))
			for loop in range(len(self.RunningAIs)):
				self.RunningAIs[loop] = False
		return
	
	def LoadDataSet(self):
		if os.path.isfile(self.DatasetAddress + ".p"):
			file = open(self.DatasetAddress + ".p", "rb")
			self.DataSet = pickle.load(file)
			file.close()
			
			return True
		else:
			return False

	def MoveIDToMove(self, moveID):
		temp = int((self.MaxOutputSize-(self.MinOutputSize-1))*(1/self.OutputResolution))
		move = []
		for loop in range(self.NumOfOutputs):
			move += [int(moveID / (temp)**((self.NumOfOutputs - loop)-1))]
			moveID = moveID % (temp)**((self.NumOfOutputs - loop)-1)
		return move

class BruteForce(object):

	def __init__(self, dataSetManager, winningModeON=False):
		self.DataSetManager = dataSetManager
		self.WinningModeON = winningModeON

		self.TempDataSet = {}

		self.AiNumber = self.DataSetManager.SetupNewAI()
		return

	def MoveCal(self, board):
		key = self.BoardToKey(board)

		if self.WinningModeON:
			print("winnning mode!")
			if key in self.DataSetManager.DataSet and len(self.DataSetManager.DataSet[key].Moves) > 0:
				moveID = self.DataSetManager.DataSet[key].MoveIDOfBestAvgFitness

			else:#never played board before
				moveID = random.randint(0,self.DataSetManager.MaxMoveIDs-1)
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

					if self.DataSetManager.DataSet[key].NumOfTriedMoves >= self.DataSetManager.MaxMoveIDs:
						self.DataSetManager.NumberOfCompleteBoards += 1

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
			self.TempDataSet[str(key)+str(moveID)] = {"BoardKey": key, "MoveID": moveID}


		move = self.DataSetManager.MoveIDLookUp[moveID]
		return move

	def UpdateInvalidMove(self, board, move):
		key = self.BoardToKey(board)
		moveID = self.DataSetManager.MoveIDLookUp.index(move)

		if key in self.DataSetManager.DataSet:
			if moveID in self.DataSetManager.DataSet[key].Moves:
				del self.DataSetManager.DataSet[key].Moves[moveID]

		if str(key)+str(moveID) in self.TempDataSet:
			del self.TempDataSet[str(key)+str(moveID)]
		return
	
	def UpdateData(self, fitness):
		for tempKey in self.TempDataSet:
			key = self.TempDataSet[tempKey]["BoardKey"]
			moveID = self.TempDataSet[tempKey]["MoveID"]

			if moveID in self.DataSetManager.DataSet[key].Moves:
				newFitness = self.DataSetManager.DataSet[key].Moves[moveID].AvgFitness*self.DataSetManager.DataSet[key].Moves[moveID].TimesPlayed
				newFitness += fitness
				self.DataSetManager.DataSet[key].Moves[moveID].TimesPlayed += 1
				newFitness /= self.DataSetManager.DataSet[key].Moves[moveID].TimesPlayed
				self.DataSetManager.DataSet[key].Moves[moveID].AvgFitness = newFitness

				if newFitness > self.DataSetManager.DataSet[key].BestAvgFitness:
					self.DataSetManager.DataSet[key].MoveIDOfBestAvgFitness = moveID
					self.DataSetManager.DataSet[key].bestAvgFitness = newFitness



		self.TempDataSet = {}
		self.DataSetManager.SaveDataSet(self.AiNumber)
		return

	def BoardToKey(self, board):
		#board = str(board)
		#board = board.replace(" ", "")
		return board

class BoardInfo():
	NumOfTriedMoves = 1
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
