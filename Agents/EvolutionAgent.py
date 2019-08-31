import Agents.AgentBase as AgentBase
from DataManger.Serializer import BoardToKey
import time
import sys

import Agents.NeuralNetwork as NeuralNetwork

class Agent(AgentBase.AgentBase):
	TrainedEpochs = 0

	def __init__(self, evoController, dataSetManager, loadData, winningModeON=False):
		super().__init__(dataSetManager, loadData, winningModeON)
		self.EvoController = evoController

		networkModel, runId, numberOfLayers = NeuralNetwork.MakeModel(self.DataSetManager)
		self.AnnModel = NeuralNetwork.NeuralNetwork(networkModel, numberOfLayers, 5000, runId)
		self.NetworkWeights = []

		if loadData:
			found, weights = self.DataSetManager.LoadNetworkWeights()
			if found:
				self.AnnModel.SetWeights(weights)

		self.NetworkWeights += [self.AnnModel.GetWeights()]
		return

	def MoveCal(self, boards, batch=False):
		if not batch:
			boards = [boards]

		networkOutputs = self.AnnModel.Predict(boards)

		outputs = []
		for loop in range(len(networkOutputs)):
			networkOutput = list(networkOutputs[loop])
			outputs += [NeuralNetwork.PredictionToMove(self.DataSetManager, networkOutput, boards[loop])]

		if not batch:
			outputs = outputs[0]
			self.RecordMove(boards[0], outputs)
		return outputs

	def SaveData(self, fitness):
		super().SaveData(fitness)
		return