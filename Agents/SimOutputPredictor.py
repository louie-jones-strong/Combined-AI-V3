import Agents.NeuralNetwork as NeuralNetwork
from DataManger.BasicLoadAndSave import BoardToKey
import time

class SimOutputPredictor:
	TrainedEpochs = 0

	def __init__(self, dataSetManager, loadData, trainingMode=False):
		self.DataSetManager = dataSetManager

		if loadData:
			self.DataSetManager.LoadTableInfo()

		networkModel, runId, numberOfLayers = NeuralNetwork.MakeModel(self.DataSetManager)
		self.AnnModel = NeuralNetwork.NeuralNetwork(networkModel, numberOfLayers, runId, 5000)

		if loadData:
			found, weights = self.DataSetManager.LoadNetworkWeights()
			if found:
				self.AnnModel.SetWeights(weights)

		if trainingMode:
			self.Train()
		return

	def PredictOutput(self, board, move):
		newBoard = board[:]

		key = BoardToKey(board)
		found, boardInfo = self.DataSetManager.GetBoardInfo(key)

		if found:
			moveID = self.DataSetManager.MoveIDLookUp.index(move)
			moveOutComes = boardInfo[moveID].MoveOutComes
			
			highestTimes = 0
			for outCome, times in moveOutComes.items():
						
				if highestTimes < times:
					newBoard = outCome
					highestTimes = times

		else:
			print("need to code ann for PredictOutput")

		return newBoard

	def Train(self):
		dataSetX = []
		dataSetY = []

		while len(dataSetY) == 0:
			time.sleep(10)
			dataSetX, dataSetY = self.DataSetManager.GetSimPredictionDataSet()

		while True:
			self.TrainedEpochs += self.AnnModel.Train(dataSetX, dataSetY, trainingTime=60)
			
			weights = self.AnnModel.GetWeights()
			self.DataSetManager.SaveNetworkWeights(weights)
			dataSetX, dataSetY = self.DataSetManager.GetSimPredictionDataSet()

		return
