import time
import sys
import random
import numpy
import Agents.Evolution.DNAObject as DNA

class EvolutionController:
	NumberOfDNAInGenration = 10
	
	def __init__(self, dataSetManager, loadData, winningModeON=False):
		self.EvoAgentList = []
		self.LoadData = loadData
		self.DataSetManager = dataSetManager
		self.WinningModeON = winningModeON
		
		self.DNAList = []

		self.WeightsSeed = None
		if self.LoadData:
			found, weights = self.DataSetManager.LoadNetworkWeights()
			if found:
				self.WeightsSeed = weights
				self.MakeDNAListFromSeed()
		return

	def RegisterEvoAgent(self, evoAgent, currentWeights):
		evoAgentId = len(self.EvoAgentList)
		self.EvoAgentList += [evoAgent]

		if self.WeightsSeed == None:
			self.WeightsSeed = currentWeights
			self.MakeDNAListFromSeed()
		
		agentDna = self.GetNextModelWeights(evoAgentId)
		
		return evoAgentId, agentDna

	def GetNextModelWeights(self, evoAgentId):
		agentDna = None
		for loop in range(len(self.DNAList)):
			dna = self.DNAList[loop]
			if dna.AgentId == None and dna.NumberOfGames == 0:
				agentDna = dna
				agentDna.AgentId = evoAgentId
				break
		
		if agentDna == None:
			self.CalNextGen()
			agentDna = self.DNAList[0]

		return agentDna

	def MakeDNAListFromSeed(self):
		self.DNAList = []
		for loop in range(self.NumberOfDNAInGenration-1):
			self.DNAList += [DNA.DNAObject(Mutation(self.WeightsSeed, 1, 0.01))]

		self.DNAList += [DNA.DNAObject(self.WeightsSeed)]
		return

	def CalNextGen(self):
		self.DNAList.sort(key=GetFittness)
		
		return

def GetFittness(dna):
	return dna.Fittness

def Mutation(weights, mutationRate, mutationAmount):
	weightType = type(weights)

	if hasattr(weights, "__len__"):
		if weightType == numpy.ndarray:
			newWeights = numpy.ndarray(weights.shape, dtype=weights.dtype)
		else:
			newWeights = list()

		weightsList = map(lambda w: Mutation(w, mutationRate, mutationAmount), weights)
		for weight in weightsList:
			newWeights += [weight]
			

	else:
		amount = 0
		if mutationRate >= random.randint(0,100)/100:
			amount = random.randint(-mutationAmount*1000,mutationAmount*1000)/1000

		newWeights = weightType(weights*(1+amount))

	return newWeights
