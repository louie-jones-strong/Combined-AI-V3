import os
import DataManger.BoardInfo as BoardInfo
from Shared import LoadingBar as LoadingBar
from Shared import OutputFormating as Format
from DataManger.BasicLoadAndSave import *
import shutil
import sys

class DataSetManager:
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

		self.SetupFoldersAndPaths()

		#cal the max move ids from sim info
		self.MaxMoveIDs = int(((maxOutputSize-(minOutputSize-1))*(1/outputResolution) )**numOfOutputs)

		#cal all the moves and given them move ids
		self.MoveIDLookUp = []
		for loop in range(self.MaxMoveIDs):
			self.MoveIDLookUp += [self.MoveIDToMove(loop)]
		if (not ComplexFileExists(self.MoveIDLookUpAdress)):
			ComplexSave(self.MoveIDLookUpAdress, self.MoveIDLookUp)

		self.CanAppendData = False
		self.DataSetHashTable = {}
		self.NewDataSetHashTable = {}
		self.DataSetTables = []
		self.DataSetTablesToSave = {}
		self.FillingTable = 0
		self.TableBatchSize = 1000
		return
	def SetupFoldersAndPaths(self):
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
		self.TesnorBoardLogAddress = self.DatasetAddress+"Logs//"
		self.MoveIDLookUpAdress = self.DatasetAddress+"LookUp//"+"MoveIdLookUp"

		if not os.path.exists(self.TableAddress):
			os.makedirs(self.TableAddress)
		if not os.path.exists(self.DatasetAddress+"LookUp//"):
			os.makedirs(self.DatasetAddress+"LookUp//")
		if not os.path.exists(self.AnnDataSetAddress):
			os.makedirs(self.AnnDataSetAddress)
		return

	def Save(self):
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
	def Clear(self):
		self.DataSetHashTable = {}
		self.DataSetTables = []
		return

	def BackUp(self):
		if (os.path.exists(self.DatasetBackUpAddress)):
			shutil.rmtree(self.DatasetBackUpAddress)
		shutil.copytree(self.DatasetAddress, self.DatasetBackUpAddress)
		self.MetaData["LastBackUpTotalTime"] = self.MetaData["TotalTime"]
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

	def LoadTableInfo(self):
		if len(self.DataSetHashTable)>0:
			return

		numberOfTables = len(os.listdir(self.TableAddress))

		self.DataSetTables = []
		for loop in range(numberOfTables):
			self.DataSetTables += [DataSetTable(self.TableAddress+"Table_"+str(loop), False)]

		self.FillingTable = 0
		if numberOfTables >= 1:
			self.DataSetTables[numberOfTables-1].Load()
			if len(self.DataSetTables[numberOfTables-1].Content) < self.TableBatchSize:
					self.FillingTable = numberOfTables-1
			else:
				self.FillingTable = numberOfTables

			self.DataSetTables[numberOfTables-1].Unload()

		self.DataSetHashTable = DictLoad(self.DataSetHashTableAddress, True)
		self.CanAppendData = True
		return

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

	def GetMoveDataSet(self):
		dataSetX = []
		dataSetY = []
		loadingBar = LoadingBar.LoadingBar()
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
	def GetSimPredictionDataSet(self):
		dataSetX = []
		dataSetY = []

		return dataSetX, dataSetY

	def SaveNetworkWeights(self, weights):
		ComplexSave(self.AnnDataSetAddress+"weights", weights)
		return

	def LoadNetworkWeights(self):

		return 

	def GetLoadedDataInfo(self):
		loadedTables = 0
		for loop in range(len(self.DataSetTables)):
			if (self.DataSetTables[loop].IsLoaded):
				loadedTables += 1

		ramUsed = 0
		ramUsed += sys.getsizeof(self.DataSetHashTable)
		ramUsed += sys.getsizeof(self.DataSetTables)
		ramUsed += sys.getsizeof(self.MetaData)
		ramUsed += sys.getsizeof(self.MoveIDLookUp)
		ramUsed = Format.SplitNumber(ramUsed)

		return Format.SplitNumber(loadedTables)+"/"+Format.SplitNumber(len(self.DataSetTables)) + " RamUsed: "+ramUsed + " bytes"
	def GetNumberOfBoards(self):
		return len(self.DataSetHashTable)

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
