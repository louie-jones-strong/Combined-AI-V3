import pickle
import json
import os
import BoardInfo
import shutil


def DictAppend(address, dictionary): 
	if (dictionary == {}):
		return

	if (not DictFileExists(address)):
		DictSave(address, dictionary)

	else:
		address += ".txt"
		file = open(address, "a")
		for key, value in dictionary.items():
			file.write(str(key)+":"+str(value)+"\n")
		file.close()

	return
def DictSave(address, dictionary):
	address += ".txt"
	file = open(address, "w")
	for key, value in dictionary.items():
		file.write(str(key)+":"+str(value)+"\n")
	file.close()
	return
def DictLoad(address):
	dictionary = {}
	address += ".txt"

	file = open(address, "r")
	lines = file.readlines()
	file.close()
	for loop in range(len(lines)):
			line = lines[loop][:-1]
			line = line.split(":")
			key = line[0]
			value = line[1]
			if "." in value:
				value = float(value)
			else:
				value = int(value)
			dictionary[key] = value

	return dictionary
def DictFileExists(address):
	return os.path.exists(address+".txt")


def ComplexSave(address, objectInfo):
	method = 0
	if method == 0:
		pickle.dump(objectInfo, open(address+".p", "wb"))
	elif method == 1:
		file = open(address+".json", "w")
		file.write(json.dumps(objectInfo, indent=4))
		file.close()

	return
def ComplexLoad(address):
	method = 0
	if method == 0:
		file = open(address+".p", "rb")
		objectInfo = pickle.load(file)
		file.close()
	elif method == 1:
		file = open(address+".json", "r")
		objectInfo = json.load(file)
		file.close()

	return objectInfo
def ComplexFileExists(address):
	method = 0
	value = False

	if method == 0:
		value = os.path.exists(address+".p")
	elif method == 1:
		value = os.path.exists(address+".json")
	return value

class DataSetTable(object):
	Content = {}
	IsLoaded = False

	def __init__(self, address, isLoaded):
		self.FileAddress = address
		self.IsLoaded = isLoaded
		self.Content = {}
		return

	def Load(self):
		self.Content = ComplexLoad(self.FileAddress)
		self.IsLoaded = True
		return
	def Save(self):
		ComplexSave(self.FileAddress, self.Content)
		return
	def Unload(self):
		self.Content ={}
		self.IsLoaded = False
		return

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
		self.DatasetAddress = datasetAddress
		self.DataSetHashTableAddress = datasetAddress+"BruteForceDataSet//DataSet"
		self.TableAddress = datasetAddress+"BruteForceDataSet//"
		self.BoardHashLookUpAddress = datasetAddress+"LookUp//"+"BoardHashLookup"
		self.MoveIDLookUpAdress = datasetAddress+"LookUp//"+"MoveIdLookUp"

		self.TableBatchSize = 10000
		self.DataSetHashTable = {}
		self.NewDataSetHashTable = {}
		self.DataSetTables = []
		self.FillingTable = 0
		self.DataSetTablesToSave = {}

		if not os.path.exists(self.TableAddress):
			os.makedirs(self.TableAddress)
		if not os.path.exists(datasetAddress+"LookUp//"):
			os.makedirs(datasetAddress+"LookUp//")

		self.BoardToHashLookUp = {}
		self.MoveIDLookUp = []
		for loop in range(self.MaxMoveIDs):
			self.MoveIDLookUp += [self.MoveIDToMove(loop)]
		return

	def SaveDataSet(self):
		if (not ComplexFileExists(self.MoveIDLookUpAdress)):
			ComplexSave(self.MoveIDLookUpAdress, self.MoveIDLookUp)
		ComplexSave(self.BoardHashLookUpAddress, self.BoardToHashLookUp)

		DictAppend(self.DataSetHashTableAddress, self.NewDataSetHashTable)
		self.NewDataSetHashTable = {}

		for loop in range(len(self.DataSetTables)):
			if (self.DataSetTables[loop].IsLoaded):
				if (loop in self.DataSetTablesToSave):
					self.DataSetTables[loop].Save()
				else:
					self.DataSetTables[loop].Unload()
		self.DataSetTablesToSave = {}
		return
	def LoadDataSet(self):
		if not ComplexFileExists(self.BoardHashLookUpAddress):
			return False
		self.BoardToHashLookUp = ComplexLoad(self.BoardHashLookUpAddress)

		self.DataSetHashTable = DictLoad(self.DataSetHashTableAddress)

		self.FillingTable = -1
		self.DataSetTables = []
		index = 0
		for loop in os.listdir(self.TableAddress):
			if loop.startswith("Table_") and "." in loop:
				loop = loop[0:loop.find(".")]
				self.DataSetTables += [DataSetTable(self.TableAddress+loop, False)]
				if len(self.DataSetTables[index].Content) < self.TableBatchSize and self.FillingTable == -1:
					self.FillingTable = index

				index += 1

		if self.FillingTable == -1:
			self.FillingTable = index
		return True
	def BackUp(self, backUpAddress):
		if (os.path.exists(backUpAddress)):
			shutil.rmtree(backUpAddress)
		shutil.copytree(self.DatasetAddress, backUpAddress)
		return

	def AddNewBoard(self, key):
		if key in self.DataSetHashTable:
			return

		index = self.FillingTable
		if (len(self.DataSetTables) <= index):
			self.DataSetTables += [DataSetTable(self.TableAddress+"Table_"+str(index), True)]

		self.DataSetHashTable[key] = index
		self.NewDataSetHashTable[key] = index
		if not self.DataSetTables[index].IsLoaded:
			self.DataSetTables[index].Load()

		moves = {}
		moves[0] = BoardInfo.MoveInfo()
		self.DataSetTables[index].Content[key] = BoardInfo.BoardInfo(Moves=moves)
		if len(self.DataSetTables[index].Content) >= self.TableBatchSize:
			self.FillingTable += 1

		return
	def GetBoardInfo(self, key):
		boardInfo = None
		found = False

		if key in self.DataSetHashTable:
			index = self.DataSetHashTable[key]
			if not self.DataSetTables[index].IsLoaded:
				self.DataSetTables[index].Load()
			
			if (index in self.DataSetTablesToSave):
				self.DataSetTablesToSave[index] += 1
			else:
				self.DataSetTablesToSave[index] = 1

			boardInfo = self.DataSetTables[index].Content[key]
			found = True
		
		return found, boardInfo
	def GetNumberOfBoards(self):
		return len(self.DataSetHashTable)
	
	def GetCachingInfoString(self):
		loadedTables = 0
		for loop in range(len(self.DataSetTables)):
			if (self.DataSetTables[loop].IsLoaded):
				loadedTables += 1

		return str(loadedTables)+"/"+str(len(self.DataSetTables))+str(self.DataSetTablesToSave)

	def MoveIDToMove(self, moveID):
		temp = int((self.MaxOutputSize-(self.MinOutputSize-1))*(1/self.OutputResolution))
		move = []
		for loop in range(self.NumOfOutputs):
			move += [int(moveID / (temp)**((self.NumOfOutputs - loop)-1))]
			moveID = moveID % (temp)**((self.NumOfOutputs - loop)-1)
		return move

	def BoardToKey(self, board):
		key = str(board)
		#key = hash(key)

		if not key in self.BoardToHashLookUp:
			self.BoardToHashLookUp[key] = board

		return key
