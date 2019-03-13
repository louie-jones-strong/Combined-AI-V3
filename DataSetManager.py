import pickle
import os
import BoardInfo

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
		moves[0] = BoardInfo.MoveInfo()
		self.DataSetTables[index][key] = BoardInfo.BoardInfo(Moves=moves)

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
