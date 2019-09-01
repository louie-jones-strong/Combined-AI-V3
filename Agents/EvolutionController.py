import time
import sys
import random

class EvolutionController:
	NumberOfDNAInGenration = 10
	
	def __init__(self, dataSetManager, loadData, winningModeON=False):
		self.EvoAgentList = []
		self.LoadData = loadData
		self.DataSetManager = dataSetManager
		self.WinningModeON = winningModeON
		
		self.DNAList = []

		self.DNASeed = None
		if self.LoadData:
			found, weights = self.DataSetManager.LoadNetworkWeights()
			if found:
				self.DNASeed = weights
				self.MakeDNAListFromSeed()
		return

	def RegisterEvoAgent(self, evoAgent, weights):
		evoAgentId = len(self.EvoAgentList)
		self.EvoAgentList += [evoAgent]

		if self.DNASeed == None:
			self.DNASeed = weights
			self.MakeDNAListFromSeed()
			

		return evoAgentId, weights

	def GetNextModelWeights(self, evoAgentId):

		return 

	def MakeDNAListFromSeed(self):
		self.DNAList = []
		for loop in range(self.NumberOfDNAInGenration-1):
			self.DNAList += [ Mutation(self.DNASeed, 1, 4) ]

		self.DNAList += [self.DNASeed]
		return

def Mutation(weights, mutationRate, mutationAmount):

	if hasattr(weights, "__len__"):
		NewWeights = list(map(lambda w: Mutation(w, mutationRate, mutationAmount), weights))

	else:
		if mutationRate >= random.randint(0,100)/100:

			amount = random.randint(-10000,10000)/(10**mutationAmount)
			NewWeights = weights + amount

	return NewWeights



class DNA:
	Weights = []
	Fittness = 0
	AgentId = -1
