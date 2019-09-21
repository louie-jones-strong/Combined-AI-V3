import Agents.AgentBase as AgentBase
from DataManger.Serializer import BoardToKey
import time
import sys

import Agents.NeuralNetwork as NeuralNetwork

class Agent(AgentBase.AgentBase):
	TrainedEpochs = 0
	AgentType = "NeuralNetwork"

	def __init__(self, dataSetManager, loadData, winningModeON=False, trainingMode=False, trainingStopTime=None):
		self.TrainingMode = trainingMode
		self.TrainingStopTime = trainingStopTime

		if not self.TrainingMode:
			super().__init__(dataSetManager, loadData, winningModeON)
		else:
			self.DataSetManager = dataSetManager

		self.LoadData = loadData

		networkModel, runId, numberOfLayers = NeuralNetwork.MakeModel(self.DataSetManager)
		self.AnnModel = NeuralNetwork.NeuralNetwork(networkModel, numberOfLayers, 5000, runId)

		if loadData:
			found, weights = self.DataSetManager.LoadNetworkWeights()
			if found:
				self.AnnModel.SetWeights(weights)

		if self.TrainingMode:
			self.Train()
			input("finished training hold as not coded this")
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

	def Train(self):
		dataSetX = []
		dataSetY = []

		while len(dataSetY) == 0:
			time.sleep(10)
			dataSetX, dataSetY = self.DataSetManager.GetMoveDataSet()


		self.TrainedEpochs += self.AnnModel.Train(dataSetX, dataSetY, trainingTime=self.TrainingStopTime)
		
		weights = self.AnnModel.GetWeights()
		self.DataSetManager.SaveNetworkWeights("BestMove", weights)
		dataSetX, dataSetY = self.DataSetManager.GetMoveDataSet()

		return

	def SaveData(self, fitness):
		super().SaveData(fitness)
		if self.LoadData:
			found, weights = self.DataSetManager.LoadNetworkWeights()
			if found:
				self.AnnModel.SetWeights(weights)
		return

	def TournamentFinished(self):
		super().TournamentFinished()
		if self.TrainingMode:
			self.Train()
		return
