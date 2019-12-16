import Agents.AgentBase as AgentBase
from DataManger.Serializer import BoardToKey
import time
import sys

import Agents.NeuralNetwork as NeuralNetwork

class Agent(AgentBase.AgentBase):
	TrainedEpochs = 0
	AgentType = "NeuralNetwork"

	def __init__(self, dataSetManager, loadData, trainingMode=False):
		super().__init__(dataSetManager, loadData, True)
		
		self.TrainingMode = trainingMode

		networkModel, runId, numberOfLayers = NeuralNetwork.MakeModel(self.DataSetManager)
		self.AnnModel = NeuralNetwork.NeuralNetwork(self.DataSetManager, networkModel, numberOfLayers, 5000, runId)

		if loadData:
			found, weights = self.DataSetManager.LoadNetworkWeights()
			if found:
				self.AnnModel.SetWeights(weights)

		if self.TrainingMode:
			self.Train()
		return

	def MoveCal(self, boards):
		boards = [boards]

		networkOutputs = self.AnnModel.Predict(boards)

		outputs = []
		for loop in range(len(networkOutputs)):
			networkOutput = list(networkOutputs[loop])
			outputs += [self.AnnModel.PredictionToMove(self.DataSetManager, networkOutput, boards[loop])]

		outputs = outputs[0]
		self.RecordMove(boards[0], outputs)
		return outputs

	def Train(self):
		dataSetX = []
		dataSetY = []

		while len(dataSetY) == 0:
			time.sleep(10)
			dataSetX, dataSetY = self.DataSetManager.GetMoveDataSet()


		self.TrainedEpochs += self.AnnModel.Train(dataSetX, dataSetY)
		
		weights = self.AnnModel.GetWeights()
		self.DataSetManager.SaveNetworkWeights("BestMove", weights)

		return

	def TournamentFinished(self):
		super().TournamentFinished()
		if self.TrainingMode:
			self.Train()
		return

	def AgentInfoOutput(self):
		info = super().AgentInfoOutput()
		info += "\n"
		info += self.AnnModel.GetInfoOutput(self.NumGames, self.NumMoves)

		return info
