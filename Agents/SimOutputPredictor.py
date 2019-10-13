#import Agents.NeuralNetwork as NeuralNetwork
from DataManger.Serializer import BoardToKey
import time
from Shared import OutputFormating as Format

class SimOutputPredictor:
	TrainedEpochs = 0
	NumPredictions = 0
	NumWrongPredictions = 0

	def __init__(self, dataSetManager, loadData, trainingMode=False):
		self.DataSetManager = dataSetManager
		self.Predictions = {}

		if loadData:
			self.DataSetManager.LoadTableInfo()

		#todo
		# networkModel, runId, numberOfLayers = NeuralNetwork.MakeModel(self.DataSetManager)
		# self.AnnModel = NeuralNetwork.NeuralNetwork(networkModel, numberOfLayers, 5000, runId)

		# if loadData:
		# 	found, weights = self.DataSetManager.LoadNetworkWeights()
		# 	if found:
		# 		self.AnnModel.SetWeights(weights)

		# if trainingMode:
		# 	self.Train()
		return

	def PredictOutput(self, board, move):
		newBoard = []

		key = BoardToKey(board)
		found, boardInfo = self.DataSetManager.GetBoardInfo(key)

		if found:
			print(move)
			moveID = self.DataSetManager.MoveIDLookUp.index(move)
			with boardInfo.Lock:
				moveOutComes = boardInfo.Moves[moveID].MoveOutComes

				highestTimes = 0
				for outCome, times in moveOutComes.items():

					if highestTimes < times:
						newBoard = outCome
						highestTimes = times

		else:
			#todo
			print("need to code ann for PredictOutput")

		
		self.Predictions[str(key)+str(move)] = {"BoardKey": key, "Move": move, "Prediction": newBoard}
		self.NumPredictions += 1
		return newBoard

	def UpdateInvalidMove(self, boardKey, move):

		return

	def UpdateMoveOutCome(self, boardKey, move, outComeBoard, finished):

		if str(boardKey)+str(move) in self.Predictions:
			prediction = self.Predictions[str(boardKey)+str(move)]["Prediction"]

			outComeBoardKey = BoardToKey(outComeBoard)
			if finished:
				outComeBoardKey = "GameFinished"

			if prediction != outComeBoardKey:
				self.NumWrongPredictions += 1
		return

	def Train(self):
		dataSetX = []
		dataSetY = []

		while len(dataSetY) == 0:
			time.sleep(10)
			dataSetX, dataSetY = self.DataSetManager.GetSimPredictionDataSet()

		while True:
			self.TrainedEpochs += self.AnnModel.Train(dataSetX, dataSetY, trainingTime=60)
			
			weights = self.AnnModel.GetWeights()
			self.DataSetManager.SaveNetworkWeights("Sim", weights)
			dataSetX, dataSetY = self.DataSetManager.GetSimPredictionDataSet()

		return

	def PredictorInfoOutput(self):
		info = ""
		info += "Number of Wrong predictions: "+Format.SplitNumber(self.NumWrongPredictions)
		info += "\n"
		info += "Number of predictions: "+Format.SplitNumber(self.NumPredictions)
		if self.NumPredictions != 0:
			info += "\n"
			ratio = (1-(self.NumWrongPredictions/self.NumPredictions))*100
			info += "predictions ratio: "+str(round(ratio,ndigits=2))+"%"

		return info
