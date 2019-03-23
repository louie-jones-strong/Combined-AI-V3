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
		self.DataSetAddress = datasetAddress+"BruteForceDataSet//DataSet.p"
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
		if (not os.path.exists(self.MoveIDLookUpAdress + ".p")):
			pickle.dump(self.MoveIDLookUp, open(self.MoveIDLookUpAdress + ".p", "wb"))
		
		pickle.dump(self.BoardToHashLookUp, open(self.BoardHashLookUpAddress + ".p", "wb"))

		pickle.dump(self.DataSet, open(self.DataSetAddress, "wb"))
		return
	def LoadDataSet(self):
		if not os.path.isfile(self.BoardHashLookUpAddress + ".p"):
			return False
		file = open(self.BoardHashLookUpAddress + ".p", "rb")
		self.BoardToHashLookUp = pickle.load(file)
		file.close()

		file = open(self.DataSetAddress, "rb")
		self.DataSet = pickle.load(file)
		file.close()
		return True
	def BackUp(self, datasetAddress):

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
