import pickle
import json
import os
import BoardInfo
import shutil

def SaveObject(address, objectInfo):
	method = 0
	if method == 0:
		pickle.dump(objectInfo, open(address+".p", "wb"))
	elif method == 1:
		file = open(address+".json", "w")
		file.write(json.dumps(objectInfo, indent=4))
		file.close()

	return
def LoadObject(address):
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
def FileExists(address):
	method = 0
	value = False

	if method == 0:
		value = os.path.exists(address+".p")
	elif method == 1:
		value = os.path.exists(address+".json")
	return value

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

		self.DataSet = {}

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
		if (not FileExists(self.MoveIDLookUpAdress)):
			SaveObject(self.MoveIDLookUpAdress, self.MoveIDLookUp)
			#pickle.dump(self.MoveIDLookUp, open(self.MoveIDLookUpAdress + ".p", "wb"))
		
		SaveObject(self.BoardHashLookUpAddress, self.BoardToHashLookUp)
		#pickle.dump(self.BoardToHashLookUp, open(self.BoardHashLookUpAddress + ".p", "wb"))

		SaveObject(self.DataSetHashTableAddress, self.DataSet)
		#pickle.dump(self.DataSet, open(self.DataSetHashTableAddress, "wb"))
		return
	def LoadDataSet(self):
		if not FileExists(self.BoardHashLookUpAddress):
			return False
		self.BoardToHashLookUp = LoadObject(self.BoardHashLookUpAddress)

		self.DataSet = LoadObject(self.DataSetHashTableAddress)
		return True
	def BackUp(self, backUpAddress):
		if (os.path.exists(backUpAddress)):
			shutil.rmtree(backUpAddress)
		shutil.copytree(self.DatasetAddress, backUpAddress)
		return

	def AddNewBoard(self, key):
		if key in self.DataSet:
			return

		moves = {}
		moves[0] = BoardInfo.MoveInfo()
		self.DataSet[key] = BoardInfo.BoardInfo(Moves=moves)

		return
	def GetBoardInfo(self, key):
		boardInfo = None
		found = False

		if key in self.DataSet:
			boardInfo = self.DataSet[key]
			found = True
		
		return found, boardInfo
	def GetNumberOfBoards(self):
		return len(self.DataSet)
	
	def GetCachingInfoString(self):
		return str(1)+"/"+str(1)

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
