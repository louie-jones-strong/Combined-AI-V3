import Agents.AgentBase as AgentBase
from DataManger.Serializer import BoardToKey
import time
import sys

import Agents.NeuralNetwork as NeuralNetwork

class Agent(AgentBase.AgentBase):
	TrainedEpochs = 0

	def __init__(self, dataSetManager, loadData, winningModeON=False):
		super().__init__(dataSetManager, loadData, winningModeON)

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
			outputs += [self.PredictionToMove(networkOutput, boards[loop])]

		if not batch:
			outputs = outputs[0]
			self.RecordMove(boards[0], outputs)
		return outputs

	def PredictionToMove(self, networkOutput, board):
		if self.DataSetManager.MetaDataGet("NetworkUsingOneHotEncoding"):
			key = BoardToKey(board)
			found, boardInfo = self.DataSetManager.GetBoardInfo(key)

			output = self.DataSetManager.MoveIDToMove(0)
			bestValue = -sys.maxsize

			for loop in range(len(networkOutput)):
				invaild = False

				if found:
					if 2**loop & boardInfo.PlayedMovesLookUpArray:
						if loop not in boardInfo.Moves:
							invaild = True

				if networkOutput[loop] >= bestValue and (not invaild):
					bestValue = networkOutput[loop]
					output = self.DataSetManager.MoveIDToMove(loop)

		else:
			output = []
			for loop in range(len(networkOutput)):
				temp = networkOutput[loop]
				temp = temp / self.DataSetManager.OutputResolution
				temp = round(temp)
				temp = temp * self.DataSetManager.OutputResolution

				if temp < self.DataSetManager.MinOutputSize:
					temp = self.DataSetManager.MinOutputSize

				if temp > self.DataSetManager.MaxOutputSize:
					temp = self.DataSetManager.MaxOutputSize

				if self.DataSetManager.OutputResolution == int(self.DataSetManager.OutputResolution):
					temp= int(temp)

				output += [temp]

		return output

	def SaveData(self, fitness):
		super().SaveData(fitness)
		return