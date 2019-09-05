import Agents.AgentBase as AgentBase
from DataManger.Serializer import BoardToKey
import Agents.NeuralNetwork as NeuralNetwork

class Agent(AgentBase.AgentBase):
	EvoAgentId = -1

	def __init__(self, evoController, dataSetManager, loadData, winningModeON=False):
		super().__init__(dataSetManager, loadData, winningModeON)
		self.EvoController = evoController

		networkModel, runId, numberOfLayers = NeuralNetwork.MakeModel(self.DataSetManager)
		self.AnnModel = NeuralNetwork.NeuralNetwork(networkModel, numberOfLayers, 5000, runId)
		weights = self.AnnModel.GetWeights()

		self.EvoAgentId, weights = self.EvoController.RegisterEvoAgent(self, weights)
		self.AnnModel.SetWeights(weights)
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

	def TournamentFinished(self):
		super().TournamentFinished()
		self.EvoController.GetNextModelWeights(self.EvoAgentId)
		return