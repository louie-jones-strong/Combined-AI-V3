import time
import sys

class EvolutionController:

	def __init__(self, dataSetManager, loadData, winningModeON=False):
		self.EvoAgentList = []
		self.LoadData = loadData
		self.DataSetManager = dataSetManager
		self.WinningModeON = winningModeON
		return

	def RegisterEvoAgent(self, evoAgent, weights):
		evoAgentId = len(self.EvoAgentList)
		self.EvoAgentList += [evoAgent]


		if self.LoadData:
			found, tempWeights = self.DataSetManager.LoadNetworkWeights()
			if found:
				return evoAgentId, tempWeights

		return evoAgentId, None

	def GetNextModelWeights(self, evoAgentId):

		return 
