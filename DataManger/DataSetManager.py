import os
import DataManger.BoardInfo as BoardInfo
from Shared import LoadingBar as LoadingBar
from Shared import OutputFormating as Format
from Shared import RamUsedInfo as RamInfo
from DataManger.BasicLoadAndSave import *
import shutil
import threading

class DataSetManager:
	MetaData = LockAbleObject()
	MoveIDLookUp = []
	MaxMoveIDs = 0

	Lock = threading.Lock()
	
	def __init__(self, logger, simInfo):
		self.Logger = logger
		self.NumOfOutputs = simInfo["NumInputs"]
		self.MinOutputSize = simInfo["MinInputSize"]
		self.MaxOutputSize = simInfo["MaxInputSize"]
		self.OutputResolution = simInfo["Resolution"]
		self.SimName = simInfo["SimName"]
		self.Lock = threading.Lock()
		self.MetaData = LockAbleObject()

		self.SetupPaths()

		#cal the max move ids from sim info
		self.MaxMoveIDs = int(((self.MaxOutputSize-(self.MinOutputSize-1))*(1/self.OutputResolution) )**self.NumOfOutputs)

		#cal all the moves and given them move ids
		self.MoveIDLookUp = []
		for loop in range(self.MaxMoveIDs):
			self.MoveIDLookUp += [self.MoveIDToMove(loop)]

		self.CanAppendData = False
		self.DataSetHashTable = {}
		self.StartingBoards = {}
		self.NewDataSetHashTable = {}
		self.DataSetTables = []
		self.LoadedDataSetTables = {}
		self.FillingTable = 0
		self.TableBatchSize = 1000
		return
	def SetupPaths(self):
		temp = "DataSets//"+self.SimName
		temp += "//"

		self.DatasetAddress = temp+"Current"

		self.DatasetAddress += "//"
		self.DatasetBackUpAddress = temp+"BackUp//"
		self.DataSetHashTableAddress = self.DatasetAddress+"LookUp//DataSetHashTable"
		self.StartingBoardsAddress = self.DatasetAddress+"LookUp//StartingBoards"
		self.TableAddress = self.DatasetAddress+"BruteForceDataSet//"
		self.AnnDataSetAddress = self.DatasetAddress+"NeuralNetworkData//"
		self.TesnorBoardLogAddress = self.DatasetAddress+"Logs//"
		self.MoveIDLookUpAdress = self.DatasetAddress+"LookUp//"+"MoveIdLookUp"
		return

	def Save(self):
		with self.Lock:
			if (not self.CanAppendData) and os.path.exists(self.DatasetAddress):
				shutil.rmtree(self.DatasetAddress)

			if len(self.NewDataSetHashTable) > 0:
				if self.CanAppendData:
					DictAppend(self.DataSetHashTableAddress, self.NewDataSetHashTable)
				else:
					DictSave(self.DataSetHashTableAddress, self.NewDataSetHashTable)

				self.NewDataSetHashTable = {}

			DictSave(self.StartingBoardsAddress, self.StartingBoards)

			if (not ComplexFileExists(self.MoveIDLookUpAdress)):
				ComplexSave(self.MoveIDLookUpAdress, self.MoveIDLookUp)

			listOfKeys = list(self.LoadedDataSetTables.keys())
			for tableKey in listOfKeys:

				if self.LoadedDataSetTables[tableKey] > 0:
					self.DataSetTables[tableKey].Save()
					self.LoadedDataSetTables[tableKey] = 0
				else:
					self.DataSetTables[tableKey].Unload()
					del self.LoadedDataSetTables[tableKey]



			self.CanAppendData = True
			self.MetaDataSet("SizeOfDataSet", self.GetNumberOfBoards())
			self.MetaDataSet("NumberOfTables", len(self.DataSetTables))
			self.MetaDataSet("FillingTable", self.FillingTable)

		self.SaveMetaData()
		return
	def Clear(self):
		with self.Lock:
			self.CanAppendData = False
			self.DataSetHashTable = {}
			self.StartingBoards = {}
			self.NewDataSetHashTable = {}
			self.DataSetTables = []
			self.LoadedDataSetTables = {}
			self.FillingTable = 0
		return

	def BackUp(self):
		with self.Lock:
			if (os.path.exists(self.DatasetBackUpAddress)):
				shutil.rmtree(self.DatasetBackUpAddress)
			shutil.copytree(self.DatasetAddress, self.DatasetBackUpAddress)
			self.MetaDataSet("LastBackUpTotalTime", self.MetaDataGet("TotalTime"))
		return

	def LoadMetaData(self):
		found = False
		if DictFileExists(self.DatasetAddress+"MetaData"):
			with self.MetaData.Lock:
				self.MetaData.Content = DictLoad(self.DatasetAddress+"MetaData")
			found = True
		return found
	def SaveMetaData(self):
		with self.MetaData.Lock:
			DictSave(self.DatasetAddress+"MetaData", self.MetaData.Content)
		return
	def MetaDataAdd(self, key, value):
		with self.MetaData.Lock:
			self.MetaData.Content[key] += value
		return
	def MetaDataSet(self, key, value):
		with self.MetaData.Lock:
			self.MetaData.Content[key] = value
		return
	def MetaDataGet(self, key, defaultValue=None):
		with self.MetaData.Lock:
			if key in self.MetaData.Content:
				value = self.MetaData.Content[key]
			else:
				value = defaultValue
		return value

	def LoadTableInfo(self):
		with self.Lock:
			if len(self.DataSetHashTable)>0:
				return

			if not DictFileExists(self.DataSetHashTableAddress):
				return

			numberOfTables = self.MetaDataGet("NumberOfTables")

			self.DataSetTables = []
			for loop in range(numberOfTables):
				self.DataSetTables += [DataSetTable(self.TableAddress+"Table_"+str(loop), False)]

			self.FillingTable = self.MetaDataGet("FillingTable")
			self.DataSetHashTable = DictLoad(self.DataSetHashTableAddress, loadingBar=LoadingBar.LoadingBar(self.Logger))
			self.StartingBoards = DictLoad(self.StartingBoardsAddress)
			self.CanAppendData = True
		return

	def AddNewBoard(self, key, board):
		if key in self.DataSetHashTable:
			return

		pickledBoard = pickle.dumps(board)

		with self.Lock:
			index = self.FillingTable
			if (len(self.DataSetTables) <= index):
				self.DataSetTables += [DataSetTable(self.TableAddress+"Table_"+str(index), True)]

			self.DataSetHashTable[key] = (index, pickledBoard)
			self.NewDataSetHashTable[key] = (index, pickledBoard)

			if not self.DataSetTables[index].IsLoaded:
				self.DataSetTables[index].Load()
	
			self.DataSetTables[index].Content[key] = BoardInfo.BoardInfo()
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

			if index not in self.LoadedDataSetTables:
				self.LoadedDataSetTables[index] = 1
			else:
				self.LoadedDataSetTables[index] += 1


			boardInfo = self.DataSetTables[index].Content[key]
			found = True
		
		return found, boardInfo
	
	def UpdateStartingBoards(self, board):
		key = BoardToKey(board)
		if key in self.StartingBoards:
			self.StartingBoards[key] += 1
		else:
			self.StartingBoards[key] = 1
		
		return

	def GetMoveDataSet(self):
		dataSetX = []
		dataSetY = []
		isOneHotEncoding = True

		self.LoadMetaData()
		if (self.MetaDataGet("TotalTime") > self.MetaDataGet("AnnDataMadeFromTotalTime") or
			(not ComplexFileExists(self.AnnDataSetAddress+"XMoveDataSet")) or 
			(not ComplexFileExists(self.AnnDataSetAddress+"YMoveDataSet"))):
			loadingBar = LoadingBar.LoadingBar(self.Logger)
			
			self.LoadTableInfo()
			loop = 0
			for key, value in self.DataSetHashTable.items():
				index = value[0]
				board = pickle.loads(value[1])

				if not self.DataSetTables[index].IsLoaded:
					self.DataSetTables[index].Load()
			
				if key in self.DataSetTables[index].Content:
					boardInfo = self.DataSetTables[index].Content[key]

					dataSetX += [board]
					
					if isOneHotEncoding:
						outputY = []
						for loop2 in range(self.MaxMoveIDs):
							temp = 0
							if loop2 in boardInfo.Moves and boardInfo.BestAvgFitness != 0:
								temp = boardInfo.Moves[loop2].AvgFitness / boardInfo.BestAvgFitness

							outputY += [temp]

						outputY[boardInfo.MoveIDOfBestAvgFitness] = 1
					else:
						outputY = self.MoveIDToMove(boardInfo.MoveIDOfBestAvgFitness)

					dataSetY += [outputY]


				loadingBar.Update(loop/len(self.DataSetHashTable), "building Dataset", loop, len(self.DataSetHashTable))
				loop += 1

			ComplexSave(self.AnnDataSetAddress+"XMoveDataSet", dataSetX)
			ComplexSave(self.AnnDataSetAddress+"YMoveDataSet", dataSetY)
			self.MetaDataSet("AnnDataMadeFromTotalTime", self.MetaDataGet("TotalTime"))
			self.MetaDataSet("NetworkUsingOneHotEncoding", isOneHotEncoding)
			self.Clear()

		elif ComplexFileExists(self.AnnDataSetAddress+"XMoveDataSet") and ComplexFileExists(self.AnnDataSetAddress+"YMoveDataSet"):
			dataSetX = ComplexLoad(self.AnnDataSetAddress+"XMoveDataSet")
			dataSetY = ComplexLoad(self.AnnDataSetAddress+"YMoveDataSet")
			isOneHotEncoding = self.MetaDataGet("NetworkUsingOneHotEncoding")

		return dataSetX, dataSetY

	def GetSimPredictionDataSet(self):
		dataSetX = []
		dataSetY = []

		self.LoadMetaData()
		if (self.MetaDataGet("TotalTime") > self.MetaDataGet("AnnDataMadeFromTotalTime") or
			(not ComplexFileExists(self.AnnDataSetAddress+"XPredictionDataSet")) or 
			(not ComplexFileExists(self.AnnDataSetAddress+"YPredictionDataSet"))):
			
			loadingBar = LoadingBar.LoadingBar(self.Logger)
			
			self.LoadTableInfo()
			loop = 0
			for key, value in self.DataSetHashTable.items():
				index = value[0]
				board = pickle.loads(value[1])

				if not self.DataSetTables[index].IsLoaded:
					self.DataSetTables[index].Load()
			
				if key in self.DataSetTables[index].Content:
					boardInfo = self.DataSetTables[index].Content[key]
					for moveId, moveInfo in boardInfo.Moves.items():

						move = self.MoveIDToMove(moveId)

						dataSetX += [[board, move]]
						
						mostcommonAmount = 0
						mostcommonKey = ""
						for outComeKey, value in boardInfo.Moves.items():
							if value >= mostcommonAmount:
								mostcommonAmount = value
								mostcommonKey = outComeKey

						dataSetY += [[1]]


				loadingBar.Update(loop/len(self.DataSetHashTable), "building Dataset", loop, len(self.DataSetHashTable))
				loop += 1

			ComplexSave(self.AnnDataSetAddress+"XPredictionDataSet", dataSetX)
			ComplexSave(self.AnnDataSetAddress+"YPredictionDataSet", dataSetY)
			#self.MetaDataSet("AnnDataMadeFromTotalTime", self.MetaDataGet("TotalTime"))
			self.Clear()

		elif ComplexFileExists(self.AnnDataSetAddress+"XPredictionDataSet") and ComplexFileExists(self.AnnDataSetAddress+"YPredictionDataSet"):
			dataSetX = ComplexLoad(self.AnnDataSetAddress+"XPredictionDataSet")
			dataSetY = ComplexLoad(self.AnnDataSetAddress+"YPredictionDataSet")

		return dataSetX, dataSetY

	def GetBoardValueDataset(self):
		dataSetX = []
		dataSetY = []

		self.LoadMetaData()
		if (self.MetaDataGet("TotalTime") > self.MetaDataGet("AnnDataMadeFromTotalTime") or
			(not ComplexFileExists(self.AnnDataSetAddress+"XValueDataSet")) or 
			(not ComplexFileExists(self.AnnDataSetAddress+"YValueDataSet"))):
			
			loadingBar = LoadingBar.LoadingBar(self.Logger)
			
			self.LoadTableInfo()
			loop = 0
			for key, value in self.DataSetHashTable.items():
				index = value[0]
				board = pickle.loads(value[1])

				if not self.DataSetTables[index].IsLoaded:
					self.DataSetTables[index].Load()
			
				if key in self.DataSetTables[index].Content:
					boardInfo = self.DataSetTables[index].Content[key]
					dataSetX += [[board]]
					dataSetY += [[boardInfo.TotalAvgFitness]]


				loadingBar.Update(loop/len(self.DataSetHashTable), "building Dataset", loop, len(self.DataSetHashTable))
				loop += 1

			ComplexSave(self.AnnDataSetAddress+"XValueDataSet", dataSetX)
			ComplexSave(self.AnnDataSetAddress+"YValueDataSet", dataSetY)
			#self.MetaDataSet("AnnDataMadeFromTotalTime", self.MetaDataGet("TotalTime"))
			self.Clear()

		elif ComplexFileExists(self.AnnDataSetAddress+"XValueDataSet") and ComplexFileExists(self.AnnDataSetAddress+"YValueDataSet"):
			dataSetX = ComplexLoad(self.AnnDataSetAddress+"XValueDataSet")
			dataSetY = ComplexLoad(self.AnnDataSetAddress+"YValueDataSet")

		return dataSetX, dataSetY

	def SaveNetworkWeights(self, networkType, weights):
		ComplexSave(self.AnnDataSetAddress+str(networkType)+"weights", weights)
		return
	def LoadNetworkWeights(self):
		if ComplexFileExists(self.AnnDataSetAddress+"weights"):
			weights = ComplexLoad(self.AnnDataSetAddress+"weights")
			return True, weights
		else:
			return False, []

	def GetLoadedDataInfo(self):
		loadedTables = 0
		for loop in range(len(self.DataSetTables)):
			if (self.DataSetTables[loop].IsLoaded):
				loadedTables += 1

		return Format.SplitNumber(loadedTables)+"/"+Format.SplitNumber(len(self.DataSetTables))
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
