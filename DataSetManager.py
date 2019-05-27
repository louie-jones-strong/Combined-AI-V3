import pickle
import json
import os
import BoardInfo
import shutil
import time

class LoadingBar():

	def __init__(self, allowUpdate=True):
		self.CurrentProgress = 0
		self.CurrentText = ""
		self.Resolution = 100
		self.LastUpdateTime = 0
		self.AllowUpdate = allowUpdate
		return

	def Update(self, progress, text=""):
		progress = max(progress, 0)
		progress = min(progress, 1)

		progress = int(progress*self.Resolution)

		if time.time()-self.LastUpdateTime >= 0.15 or progress == self.Resolution:
			if progress != self.CurrentProgress or text != self.CurrentText:
				os.system("cls")
				bar = "#"*progress
				fill = " "*(self.Resolution-progress)
				print("|"+bar+fill+"|")
				print(text)
				self.CurrentProgress = progress
				self.CurrentText = text
				self.LastUpdateTime = time.time()
		return

def serializer(inputObject):
	outputObject = ""

	if type(inputObject) is bytes:
		outputObject = "b("
		for loop in range(len(inputObject)):
			outputObject += str(inputObject[loop])
			if loop < len(inputObject)-1:
				outputObject +=","

		return outputObject + ")"

	elif hasattr(inputObject, "__len__"):
		outputObject = []
		for loop in range(len(inputObject)):
			outputObject += [serializer(inputObject[loop])]

		outputObject = ", ".join(outputObject)
		return "["+outputObject+"]"
	else:
		return str(inputObject)
def deserializer(inputString):
	if inputString.startswith("b("):
		subInputString = inputString[2:-1]
		byteArray = list(map(int, subInputString.split(",")))
		outputObject = bytes(byteArray)

	elif inputString.startswith("["):
		inputString = inputString.replace('[', '').replace(']', '')
		outputObject = tuple(map(deserializer, inputString.split(", ")))

	elif inputString == "True":
		outputObject = True

	elif inputString == "False":
		outputObject = False

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
			file.write(str(key)+":"+serializer(value)+"\n")
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

	loadingBar = LoadingBar(loadingBarOn)
	loadingBar.Update(0, "Loading Dict")

	file = open(address, "r")
	lines = file.readlines()
	file.close()
	
	numberOfLines = len(lines)
	loadingBar.Update(0, "Loading dict line: "+str(0)+"/"+str(numberOfLines))

	for loop in range(numberOfLines):
		line = lines[loop][:-1].split(":")
		key = line[0]
		dictionary[key] = deserializer(line[1])

		loadingBar.Update(loop/numberOfLines, "Loading dict line: "+str(loop)+"/"+str(numberOfLines))

	loadingBar.Update(1, "Loading dict line: "+str(numberOfLines)+"/"+str(numberOfLines))

	return dictionary
def DictFileExists(address):
	return os.path.exists(address+".txt")

def ComplexSave(address, objectInfo):
	pickle.dump(objectInfo, open(address+".p", "wb"))
	return
def ComplexLoad(address):
	file = open(address+".p", "rb")
	objectInfo = pickle.load(file)
	file.close()
	return objectInfo
def ComplexFileExists(address):
	method = 0
	value = False
	value = os.path.exists(address+".p")
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
	MetaData = {}
	MoveIDLookUp = []
	MaxMoveIDs = 0

	SimName = ""
	NumOfOutputs = 0
	MinOutputSize = 0
	MaxOutputSize = 0
	OutputResolution = 0
	
	def __init__(self, numOfOutputs, minOutputSize, maxOutputSize, outputResolution, simName):
		self.NumOfOutputs = numOfOutputs
		self.MinOutputSize = minOutputSize
		self.MaxOutputSize = maxOutputSize
		self.OutputResolution = outputResolution
		self.SimName = simName

		
		temp = "DataSets//"+self.SimName
		if not os.path.exists(temp):
			os.makedirs(temp)
		temp += "//"

		self.DatasetAddress = temp+"Current"
		if not os.path.exists(self.DatasetAddress):
			os.makedirs(self.DatasetAddress)

		self.DatasetAddress += "//"
		self.DatasetBackUpAddress = temp+"BackUp//"
		self.DataSetHashTableAddress = self.DatasetAddress+"LookUp//DataSetHashTable"
		self.TableAddress = self.DatasetAddress+"BruteForceDataSet//"
		self.AnnDataSetAddress = self.DatasetAddress+"NeuralNetworkData//"
		self.MoveIDLookUpAdress = self.DatasetAddress+"LookUp//"+"MoveIdLookUp"


		self.MaxMoveIDs = int(((maxOutputSize-(minOutputSize-1))*(1/outputResolution) )**numOfOutputs)

		self.MoveIDLookUp = []
		for loop in range(self.MaxMoveIDs):
			self.MoveIDLookUp += [self.MoveIDToMove(loop)]

		self.TableBatchSize = 1000
		self.CanAppendData = False
		self.DataSetHashTable = {}
		self.NewDataSetHashTable = {}
		self.DataSetTables = []
		self.FillingTable = 0
		self.DataSetTablesToSave = {}

		if not os.path.exists(self.TableAddress):
			os.makedirs(self.TableAddress)
		if not os.path.exists(self.DatasetAddress+"LookUp//"):
			os.makedirs(self.DatasetAddress+"LookUp//")
		if not os.path.exists(self.AnnDataSetAddress):
			os.makedirs(self.AnnDataSetAddress)

		if (not ComplexFileExists(self.MoveIDLookUpAdress)):
			ComplexSave(self.MoveIDLookUpAdress, self.MoveIDLookUp)
		return

	def SaveDataSet(self):
		if len(self.NewDataSetHashTable) > 0:
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


		self.MetaData["SizeOfDataSet"] = self.GetNumberOfBoards()
		self.SaveMetaData()
		return
	def GetMetaData(self):
		found = False

		if DictFileExists(self.DatasetAddress+"MetaData"):
			self.MetaData = DictLoad(self.DatasetAddress+"MetaData")
			found = True

		return found
	def SaveMetaData(self):
		DictSave(self.DatasetAddress+"MetaData", self.MetaData)
		return

	def LoadDataSet(self):
		loadingBar = LoadingBar()
		loadingBar.Update(0, "loading tables...")
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
			loadingBar.Update(loop/numberOfTables, "loading table: "+str(loop)+"/"+str(numberOfTables))

			index += 1

		loadingBar.Update(1, "loading table: "+str(numberOfTables)+"/"+str(numberOfTables))
		if self.FillingTable == -1:
			self.FillingTable = index

		self.DataSetHashTable = DictLoad(self.DataSetHashTableAddress, True)
		self.CanAppendData = True
		return True
	def BackUp(self):
		if (os.path.exists(self.DatasetBackUpAddress)):
			shutil.rmtree(self.DatasetBackUpAddress)
		shutil.copytree(self.DatasetAddress, self.DatasetBackUpAddress)
		self.MetaData["LastBackUpTotalTime"] = self.MetaData["TotalTime"]
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
		dataSetX = []
		dataSetY = []
		loadingBar = LoadingBar()
		isOneHotEncoding = True

		if (self.MetaData["BruteForceTotalTime"]>self.MetaData["AnnDataMadeFromBruteForceTotalTime"] or 
			not ComplexFileExists(self.AnnDataSetAddress+"XDataSet") or 
			not ComplexFileExists(self.AnnDataSetAddress+"YDataSet")):

			loop = 0
			for key, value in self.DataSetHashTable.items():
				index = value[0]
				board = pickle.loads(value[1])

				if not self.DataSetTables[index].IsLoaded:
					self.DataSetTables[index].Load()
			
				if key in self.DataSetTables[index].Content:
					boardInfo = self.DataSetTables[index].Content[key]

					if boardInfo.NumOfTriedMoves >= self.MaxMoveIDs:
						dataSetX += [board]
						
						if isOneHotEncoding:
							temp = []
							for loop2 in range(self.MaxMoveIDs):
								temp += [0]

							temp[boardInfo.MoveIDOfBestAvgFitness] = 1
						else:
							temp = self.MoveIDToMove(boardInfo.MoveIDOfBestAvgFitness)

						dataSetY += [temp]


				loadingBar.Update(loop/len(self.DataSetHashTable), "building Dataset")
				loop += 1

			ComplexSave(self.AnnDataSetAddress+"XDataSet", dataSetX)
			ComplexSave(self.AnnDataSetAddress+"YDataSet", dataSetY)
			self.MetaData["AnnDataMadeFromBruteForceTotalTime"] = self.MetaData["BruteForceTotalTime"]
			self.MetaData["NetworkUsingOneHotEncoding"] = isOneHotEncoding
			self.SaveMetaData()

		elif ComplexFileExists(self.AnnDataSetAddress+"XDataSet") and ComplexFileExists(self.AnnDataSetAddress+"YDataSet"):
			dataSetX = ComplexLoad(self.AnnDataSetAddress+"XDataSet")
			dataSetY = ComplexLoad(self.AnnDataSetAddress+"YDataSet")
			isOneHotEncoding = self.MetaData["NetworkUsingOneHotEncoding"]

		return dataSetX, dataSetY, isOneHotEncoding

	def SaveNetworkWeights(self, weights):
		ComplexSave(self.AnnDataSetAddress+"weights", weights)
		return

	def LoadNetworkWeights(self):

		return 

	def GetCachingInfoString(self):
		loadedTables = 0
		for loop in range(len(self.DataSetTables)):
			if (self.DataSetTables[loop].IsLoaded):
				loadedTables += 1

		return str(loadedTables)+"/"+str(len(self.DataSetTables))

	def MoveIDToMove(self, moveID):
		if moveID < 0 or moveID > self.MaxMoveIDs-1:
			input("Error!!!")

		temp = int((self.MaxOutputSize-(self.MinOutputSize-1))*(1/self.OutputResolution))
		move = []
		for loop in range(self.NumOfOutputs):
			move += [int(moveID / (temp)**((self.NumOfOutputs - loop)-1))]
			moveID = moveID % (temp)**((self.NumOfOutputs - loop)-1)

		return move
	def BoardToKey(self, board):
		key = str(board)
		#key = hash(key)
		return key
