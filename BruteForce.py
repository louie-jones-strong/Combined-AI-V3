import pickle
import os
import sys
import random

class DataSetLoadAndSaver(object):
	def __init__(self, datasetAddress):
		self.HashTableAddress = datasetAddress+"DataSetHashTable.p"
		self.TableAddress = datasetAddress
		self.batchSize = 20000
		self.DataBaseHashTable = {}
		self.DataSetTables = []
		return

	def SaveBruteForceDataSet(self, dataset):
		fillingTable = 0
		for loop in range(len(self.DataSetTables)):
			if len(self.DataSetTables[loop]) >= self.batchSize:
				fillingTable += 1

		tablesToSave = []
		for key, value in dataset.items():

			if key in self.DataBaseHashTable:
				index = self.DataBaseHashTable[key]

			else:
				self.DataBaseHashTable[key] = fillingTable
				index = fillingTable
				if len(self.DataSetTables) <= index:
					self.DataSetTables += [{}]

				if len(self.DataSetTables[index]) >= self.batchSize:
					fillingTable += 1
			
			self.DataSetTables[index][key] = value
			if index not in tablesToSave:
				tablesToSave += [index]

		for loop in range(len(tablesToSave)):
			index = tablesToSave[loop]
			pickle.dump(self.DataSetTables[index], open(self.TableAddress+"Table_"+str(index)+".p", "wb"))

		pickle.dump(self.DataBaseHashTable, open(self.HashTableAddress, "wb"))
		return

	def LoadBruteForceDataSet(self):
		file = open(self.HashTableAddress, "rb")
		self.DataBaseHashTable = pickle.load(file)
		file.close()
		
		numberOfTables = 0
		for file in os.listdir(self.TableAddress):
			if file.startswith("Table_") and file.endswith(".p"):
				numberOfTables += 1


		output = {}
		self.DataSetTables = []
		for loop in range(numberOfTables):
			file = open(self.TableAddress+"Table_"+str(loop)+".p", "rb")
			self.DataSetTables += [pickle.load(file)]
			file.close()
			output.update(self.DataSetTables[loop])
		
		return output

class DataSetManager(object):
	DataSet = {}
	NumberOfCompleteBoards = 0
	MoveIDLookUp = []
	BoardToHashLookUp = {}
	MaxMoveIDs = 0
	BoardsToUpdate = {}
	
	def __init__(self, numOfOutputs, minOutputSize, maxOutputSize, outputResolution, datasetAddress):
		self.NumOfOutputs = numOfOutputs

		self.MinOutputSize = minOutputSize
		self.MaxOutputSize = maxOutputSize
		self.OutputResolution = outputResolution

		self.MaxMoveIDs = int(((maxOutputSize-(minOutputSize-1))*(1/outputResolution) )**numOfOutputs)
		self.DatasetAddress = datasetAddress+"BruteForceDataSet//"
		self.BoardHashLookUpAddress = datasetAddress+"LookUp//"+"BoardHashLookup"
		self.MoveIDLookUpAdress = datasetAddress+"LookUp//"+"MoveIdLookUp"

		if not os.path.exists(datasetAddress+"BruteForceDataSet//"):
			os.makedirs(datasetAddress+"BruteForceDataSet//")
		if not os.path.exists(datasetAddress+"LookUp//"):
			os.makedirs(datasetAddress+"LookUp//")

		self.DataSet = {}
		self.MoveIDLookUp = []
		for loop in range(self.MaxMoveIDs):
			self.MoveIDLookUp += [self.MoveIDToMove(loop)]
			
		self.LoadAndSaver = DataSetLoadAndSaver(self.DatasetAddress)
		return

	def SaveDataSet(self, forceSave=False):
		if (not os.path.exists(self.MoveIDLookUpAdress + ".p")):
			pickle.dump(self.MoveIDLookUp, open(self.MoveIDLookUpAdress + ".p", "wb"))

		pickle.dump(self.BoardToHashLookUp, open(self.BoardHashLookUpAddress + ".p", "wb"))

		if forceSave:
			self.LoadAndSaver.SaveBruteForceDataSet(self.DataSet)
		else:
			boardsToSave = {}
			for key in self.BoardsToUpdate:
				boardsToSave[key] = self.DataSet[key]

			self.LoadAndSaver.SaveBruteForceDataSet(boardsToSave)

		self.BoardsToUpdate = {}
		return
	
	def LoadDataSet(self):
		if not os.path.isfile(self.BoardHashLookUpAddress + ".p"):
			return False

		self.DataSet = self.LoadAndSaver.LoadBruteForceDataSet()

		file = open(self.BoardHashLookUpAddress + ".p", "rb")
		self.BoardToHashLookUp = pickle.load(file)
		file.close()
		return True

	def MoveIDToMove(self, moveID):
		temp = int((self.MaxOutputSize-(self.MinOutputSize-1))*(1/self.OutputResolution))
		move = []
		for loop in range(self.NumOfOutputs):
			move += [int(moveID / (temp)**((self.NumOfOutputs - loop)-1))]
			moveID = moveID % (temp)**((self.NumOfOutputs - loop)-1)
		return move

	def BoardToKey(self, board):
		key = str(board)
		key = key.replace(" ", "")

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

		if self.WinningModeON:
			print("winnning mode!")
			if key in self.DataSetManager.DataSet and len(self.DataSetManager.DataSet[key].Moves) > 0:
				moveID = self.DataSetManager.DataSet[key].MoveIDOfBestAvgFitness

			else:#never played board before
				moveID = random.randint(0,self.DataSetManager.MaxMoveIDs-1)
				print("new Board!")

		else:  # learning mode
			if key in self.DataSetManager.DataSet:
				
				if self.DataSetManager.DataSet[key].NumOfTriedMoves > self.DataSetManager.MaxMoveIDs:
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
		key = self.DataSetManager.BoardToKey(board)
		moveID = self.DataSetManager.MoveIDLookUp.index(move)

		if key in self.DataSetManager.DataSet:
			if moveID in self.DataSetManager.DataSet[key].Moves:
				del self.DataSetManager.DataSet[key].Moves[moveID]

		if str(key)+str(moveID) in self.TempDataSet:
			del self.TempDataSet[str(key)+str(moveID)]
		return
	
	def SaveData(self, fitness):
		for tempKey in self.TempDataSet:
			key = self.TempDataSet[tempKey]["BoardKey"]
			moveID = self.TempDataSet[tempKey]["MoveID"]

			if key in self.DataSetManager.BoardsToUpdate:
				self.DataSetManager.BoardsToUpdate[key] += 1
			else:
				self.DataSetManager.BoardsToUpdate[key] = 1

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
		return

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
# 2) make datasetmanager and datasetloadandsaver in to one to save ram 
# 3) get a single boardinfo for the brute force to work with to cut down on lookups