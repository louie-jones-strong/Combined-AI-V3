import pickle
import os
import sys
import random

class DataSetManager(object):
	NumberOfCompleteBoards = 0
	MoveIDLookUp = []
	MaxMoveIDs = 0
	
	def __init__(self, numOfOutputs, minOutputSize, maxOutputSize, outputResolution, datasetAddress):
		self.NumOfOutputs = numOfOutputs

		self.MinOutputSize = minOutputSize
		self.MaxOutputSize = maxOutputSize
		self.OutputResolution = outputResolution

		self.MaxMoveIDs = int(((maxOutputSize-(minOutputSize-1))*(1/outputResolution) )**numOfOutputs)
		self.HashTableAddress = datasetAddress+"BruteForceDataSet//DataSetHashTable.p"
		self.TableAddress = datasetAddress+"BruteForceDataSet//"
		self.BoardHashLookUpAddress = datasetAddress+"LookUp//"+"BoardHashLookup"
		self.MoveIDLookUpAdress = datasetAddress+"LookUp//"+"MoveIdLookUp"
		self.TableBatchSize = 20000

		self.DataBaseHashTable = {}
		self.DataSetTables = []
		self.BoardToHashLookUp = {}
		self.FillingTable = 0
		self.TablesToSave = {}

		if not os.path.exists(self.TableAddress):
			os.makedirs(self.TableAddress)
		if not os.path.exists(datasetAddress+"LookUp//"):
			os.makedirs(datasetAddress+"LookUp//")

		self.DataSet = {}
		self.MoveIDLookUp = []
		for loop in range(self.MaxMoveIDs):
			self.MoveIDLookUp += [self.MoveIDToMove(loop)]
		return

	def SaveDataSet(self):
		if (not os.path.exists(self.MoveIDLookUpAdress + ".p")):
			pickle.dump(self.MoveIDLookUp, open(self.MoveIDLookUpAdress + ".p", "wb"))

		pickle.dump(self.BoardToHashLookUp, open(self.BoardHashLookUpAddress + ".p", "wb"))

		for key, value in self.TablesToSave.items():
			pickle.dump(self.DataSetTables[key], open(self.TableAddress+"Table_"+str(key)+".p", "wb"))

		pickle.dump(self.DataBaseHashTable, open(self.HashTableAddress, "wb"))

		return
	def LoadDataSet(self):
		if not os.path.isfile(self.BoardHashLookUpAddress + ".p"):
			return False
		file = open(self.BoardHashLookUpAddress + ".p", "rb")
		self.BoardToHashLookUp = pickle.load(file)
		file.close()

		file = open(self.HashTableAddress, "rb")
		self.DataBaseHashTable = pickle.load(file)
		file.close()
		
		self.DataSetTables = []
		numberOfTables = 0
		for file in os.listdir(self.TableAddress):
			if file.startswith("Table_") and file.endswith(".p"):

				file = open(self.TableAddress+"Table_"+str(numberOfTables)+".p", "rb")
				self.DataSetTables += [pickle.load(file)]
				file.close()
				
				numberOfTables += 1

		self.FillingTable = 0
		for loop in range(len(self.DataSetTables)):
			if len(self.DataSetTables[loop]) >= self.TableBatchSize:
				self.FillingTable += 1
		return True
	
	def AddNewBoard(self, key):
		index = self.FillingTable
		self.DataBaseHashTable[key] = index

		if len(self.DataSetTables) <= index:
			self.DataSetTables += [{}]

		if (index in self.TablesToSave):
			self.TablesToSave[index] += 1
		else:
			self.TablesToSave[index] = 1

		moves = {}
		moves[0] = MoveInfo()
		value = BoardInfo(Moves=moves)
		self.DataSetTables[index][key] = value

		if len(self.DataSetTables[index]) >= self.TableBatchSize:
			self.FillingTable += 1
		return
	def GetBoardInfo(self, key):
		boardInfo = None
		found = False

		if key in self.DataBaseHashTable:
			index = self.DataBaseHashTable[key]
			boardInfo = self.DataSetTables[index][key]
			found = True
			if (index in self.TablesToSave):
				self.TablesToSave[index] += 1
			else:
				self.TablesToSave[index] = 1
		
		return found, boardInfo
	def GetNumberOfBoards(self):
		numberOfBoards = 0
		for loop in range(len(self.DataSetTables)):
			numberOfBoards += len(self.DataSetTables[loop])

		return numberOfBoards

	def MoveIDToMove(self, moveID):
		temp = int((self.MaxOutputSize-(self.MinOutputSize-1))*(1/self.OutputResolution))
		move = []
		for loop in range(self.NumOfOutputs):
			move += [int(moveID / (temp)**((self.NumOfOutputs - loop)-1))]
			moveID = moveID % (temp)**((self.NumOfOutputs - loop)-1)
		return move

	def BoardToKey(self, board):
		key = hash(str(board))

		if not key in self.BoardToHashLookUp:
			self.BoardToHashLookUp[key] = board

		return key

class BruteForce(object): 

	def __init__(self, dataSetManager, winningModeON=False):
		self.DataSetManager = dataSetManager
		self.WinningModeON = winningModeON

		self.TempDataSet = {}
		return

	def MoveCal(self, board):
		key = self.DataSetManager.BoardToKey(board)
		found, boardInfo = self.DataSetManager.GetBoardInfo(key)

		if self.WinningModeON:
			print("winnning mode!")
			if found and len(boardInfo.Moves) > 0:
				moveID = boardInfo.MoveIDOfBestAvgFitness

			else:#never played board before
				moveID = random.randint(0,self.DataSetManager.MaxMoveIDs-1)
				print("new Board!")
		else:  # learning mode
			if found:
				if boardInfo.NumOfTriedMoves > self.DataSetManager.MaxMoveIDs:
					if len(boardInfo.Moves) == 0:
						input("error!!!")

				if boardInfo.NumOfTriedMoves < self.DataSetManager.MaxMoveIDs:
					moveID = boardInfo.NumOfTriedMoves
					boardInfo.Moves[moveID] = MoveInfo()
					boardInfo.NumOfTriedMoves += 1

					if boardInfo.NumOfTriedMoves >= self.DataSetManager.MaxMoveIDs:
						self.DataSetManager.NumberOfCompleteBoards += 1

				else:#played every move once already
					leastPlayed = sys.maxsize
					moveID = 0
					for movekey, moveValue in boardInfo.Moves.items():
						if moveValue.TimesPlayed < leastPlayed:
							leastPlayed = moveValue.TimesPlayed
							moveID = movekey
					
					boardInfo.Moves[moveID].TimesPlayed += 1

			else:#never played board before
				moveID = 0
				self.DataSetManager.AddNewBoard(key)

			self.TempDataSet[str(key)+str(moveID)] = {"BoardKey": key, "MoveID": moveID}


		move = self.DataSetManager.MoveIDLookUp[moveID]
		return move

	def UpdateInvalidMove(self, board, move):
		key = self.DataSetManager.BoardToKey(board)
		moveID = self.DataSetManager.MoveIDLookUp.index(move)

		found, boardInfo = self.DataSetManager.GetBoardInfo(key)

		if found:
			if moveID in boardInfo.Moves:
				del boardInfo.Moves[moveID]

		if str(key)+str(moveID) in self.TempDataSet:
			del self.TempDataSet[str(key)+str(moveID)]
		return
	
	def SaveData(self, fitness):
		for tempKey in self.TempDataSet:
			key = self.TempDataSet[tempKey]["BoardKey"]
			moveID = self.TempDataSet[tempKey]["MoveID"]

			found, boardInfo = self.DataSetManager.GetBoardInfo(key)
			if moveID in boardInfo.Moves:
				newFitness = boardInfo.Moves[moveID].AvgFitness*boardInfo.Moves[moveID].TimesPlayed
				newFitness += fitness
				boardInfo.Moves[moveID].TimesPlayed += 1
				newFitness /= boardInfo.Moves[moveID].TimesPlayed
				boardInfo.Moves[moveID].AvgFitness = newFitness

				if newFitness > boardInfo.BestAvgFitness:
					boardInfo.MoveIDOfBestAvgFitness = moveID
					boardInfo.bestAvgFitness = newFitness



		self.TempDataSet = {}
		return

class BoardInfo():
	NumOfTriedMoves = 1
	MoveIDOfBestAvgFitness = 0
	BestAvgFitness = -sys.maxsize
	Moves = {}

	def __init__(self, NumOfTriedMoves=1, Moves={}, moveIDOfBestAvgFitness=0, bestAvgFitness=-sys.maxsize):
		self.NumOfTriedMoves = NumOfTriedMoves
		self.Moves = Moves
		self.MoveIDOfBestAvgFitness = moveIDOfBestAvgFitness
		self.BestAvgFitness = bestAvgFitness
		return

class MoveInfo():
	AvgFitness = 0.0
	TimesPlayed = 1

	def __init__(self, AvgFitness=0.0, TimesPlayed=1):
		self.AvgFitness = AvgFitness
		self.TimesPlayed = TimesPlayed
		return

# 1) point to the move that is least played
