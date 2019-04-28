import pickle
import json
import os
import BoardInfo
import shutil
import time


def LoadingBar(progress, text=""):
	if (progress > 1):
		progress = 1
	if progress < 0:
		progress = 0
		
	Resolution = 100
	progress = progress*Resolution
	os.system("cls")
	bar = "#"*int(progress)
	fill = " "*(Resolution-int(progress))
	print("|"+bar+fill+"|")
	print(text)
	return

def serializer(inputObject):

	return str(inputObject)
def deserializer(inputString):
	if inputString.startswith("b'"):
		outputObject = bytes(inputString[2:-1], 'utf-8')
		#outputObject = inputString

	elif "(" in inputString:
		inputString = inputString.replace('(', '').replace(')', '')
		outputObject = tuple(map(deserializer, inputString.split(', ')))

	elif "." in inputString:
		outputObject = float(inputString)

	else:
		outputObject = int(inputString)
	return outputObject

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
		file.write(str(key)+":"+serializer(value)+"\n")
	file.close()
	return
def DictLoad(address, loadingBarOn=False):
	dictionary = {}
	address += ".txt"

	if loadingBarOn:
		LoadingBar(0, "Loading Dict")

	file = open(address, "r")
	lines = file.readlines()
	file.close()
	
	numberOfLines = len(lines)
	lastOutputTime = time.time()
	if loadingBarOn:
		LoadingBar(0, "Loading dict line: "+str(0)+"/"+str(numberOfLines))

	for loop in range(numberOfLines):
		line = lines[loop][:-1]
		line = line.split(":")
		key = line[0]
		value = deserializer(line[1])
		dictionary[key] = value

		if loadingBarOn and time.time()-lastOutputTime >= 0.5:
			LoadingBar(loop/numberOfLines, "Loading dict line: "+str(loop)+"/"+str(numberOfLines))
			lastOutputTime = time.time()

	if loadingBarOn:
		LoadingBar(1, "Loading dict line: "+str(numberOfLines)+"/"+str(numberOfLines))

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

	NumOfOutputs = 0
	MinOutputSize = 0
	MaxOutputSize = 0
	OutputResolution = 0
	
	def __init__(self, numOfOutputs, minOutputSize, maxOutputSize, outputResolution, datasetAddress):
		self.NumOfOutputs = numOfOutputs
		self.MinOutputSize = minOutputSize
		self.MaxOutputSize = maxOutputSize
		self.OutputResolution = outputResolution
		self.MaxMoveIDs = int(((maxOutputSize-(minOutputSize-1))*(1/outputResolution) )**numOfOutputs)

		self.MoveIDLookUp = []
		for loop in range(self.MaxMoveIDs):
			self.MoveIDLookUp += [self.MoveIDToMove(loop)]
		
		self.DatasetAddress = datasetAddress
		self.DataSetHashTableAddress = datasetAddress+"LookUp//DataSetHashTable"
		self.TableAddress = datasetAddress+"BruteForceDataSet//"
		self.MoveIDLookUpAdress = datasetAddress+"LookUp//"+"MoveIdLookUp"

		self.TableBatchSize = 1000
		self.CanAppendData = False
		self.DataSetHashTable = {}
		self.NewDataSetHashTable = {}
		self.DataSetTables = []
		self.FillingTable = 0
		self.DataSetTablesToSave = {}

		if not os.path.exists(self.TableAddress):
			os.makedirs(self.TableAddress)
		if not os.path.exists(datasetAddress+"LookUp//"):
			os.makedirs(datasetAddress+"LookUp//")
		return

	def SaveDataSet(self):
		if (not ComplexFileExists(self.MoveIDLookUpAdress)):
			ComplexSave(self.MoveIDLookUpAdress, self.MoveIDLookUp)

		if self.CanAppendData:
			DictAppend(self.DataSetHashTableAddress, self.NewDataSetHashTable)
		else:
			DictSave(self.DataSetHashTableAddress, self.NewDataSetHashTable)

		self.NewDataSetHashTable = {}

		for loop in range(len(self.DataSetTables)):
			if (self.DataSetTables[loop].IsLoaded):
				if (loop in self.DataSetTablesToSave):
					self.DataSetTables[loop].Save()
				else:
					self.DataSetTables[loop].Unload()
		self.DataSetTablesToSave = {}
		self.CanAppendData = True
		return
	def LoadDataSet(self):
		LoadingBar(0, "loading tables...")
		self.FillingTable = -1
		self.DataSetTables = []
		numberOfTables = len(os.listdir(self.TableAddress))
		index = 0
		for loop in range(numberOfTables):
			self.DataSetTables += [DataSetTable(self.TableAddress+"Table_"+str(loop), False)]

			self.DataSetTables[index].Load()
			if len(self.DataSetTables[index].Content) < self.TableBatchSize and self.FillingTable == -1:
				self.FillingTable = index
			self.DataSetTables[index].Unload()
			if loop%10 == 0:
				LoadingBar(loop/numberOfTables, "loading table: "+str(loop)+"/"+str(numberOfTables))

			index += 1

		LoadingBar(1, "loading table: "+str(numberOfTables)+"/"+str(numberOfTables))
		if self.FillingTable == -1:
			self.FillingTable = index

		self.DataSetHashTable = DictLoad(self.DataSetHashTableAddress, True)
		self.CanAppendData = True
		return True
	def BackUp(self, backUpAddress):
		if (os.path.exists(backUpAddress)):
			shutil.rmtree(backUpAddress)
		shutil.copytree(self.DatasetAddress, backUpAddress)
		return

#for Brute Force
	def AddNewBoard(self, key, board):
		if key in self.DataSetHashTable:
			return

		index = self.FillingTable
		if (len(self.DataSetTables) <= index):
			self.DataSetTables += [DataSetTable(self.TableAddress+"Table_"+str(index), True)]

		pickledBoard = pickle.dumps(board)
		self.DataSetHashTable[key] = (index, pickledBoard)
		self.NewDataSetHashTable[key] = (index, pickledBoard)

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
			index = self.DataSetHashTable[key][0]
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
	
#for Neural Network
	def GetDataSet(self):
		maxTablesLoaded = 1000

		dataSetX = []
		dataSetY = []

		loop = 0
		for key, value in self.DataSetHashTable.items():
			index = value[0]
			board = value[1]#pickle.loads(value[1])

			if not self.DataSetTables[index].IsLoaded:
				self.DataSetTables[index].Load()
			
			if key in self.DataSetTables[index].Content:
				boardInfo = self.DataSetTables[index].Content[key]

				if boardInfo.NumOfTriedMoves >= self.MaxMoveIDs:
					dataSetX += [board]
					dataSetY += [self.MoveIDLookUp[boardInfo.MoveIDOfBestAvgFitness]]


			if loop % 10 == 0:
				LoadingBar(loop/len(self.DataSetHashTable), "building Dataset")
			loop += 1

		return dataSetX, dataSetY

	def GetCachingInfoString(self):
		loadedTables = 0
		for loop in range(len(self.DataSetTables)):
			if (self.DataSetTables[loop].IsLoaded):
				loadedTables += 1

		return str(loadedTables)+"/"+str(len(self.DataSetTables))

	def MoveIDToMove(self, moveID):
		temp = int((self.MaxOutputSize-(self.MinOutputSize-1))*(1/self.OutputResolution))
		move = []
		for loop in range(self.NumOfOutputs):
			move += [int(moveID / (temp)**((self.NumOfOutputs - loop)-1))]
			moveID = moveID % (temp)**((self.NumOfOutputs - loop)-1)
		return move

	def BoardToKey(self, board):
		key = str(board)
		key = hash(key)
		return key
