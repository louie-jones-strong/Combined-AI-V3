import time
import sys

class EvolutionController:

	def __init__(self, loadData, winningModeON=False):
		self.EvoAgentList = []
		return

	def RegisterEvoAgent(self, evoAgent):
		evoAgentId = len(self.EvoAgentList)
		self.EvoAgentList += [evoAgent]

		return evoAgentId

	def GetNextModelWeights(self, evoAgentId):

		return 
