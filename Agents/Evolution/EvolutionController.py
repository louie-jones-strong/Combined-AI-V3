import time
import sys
import random
import numpy as np
import Agents.Evolution.DNAObject as DNA

class EvolutionController:
	NumberOfDNAInGenration = 10
	GenrationNum = 0
	
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

		for dna in self.DNAList:
			dna.NumberOfGames = 0
			dna.AgentId = None
			dna.Fittness = 0

		self.GenrationNum += 1
		print("Genration: " + str(self.GenrationNum))
		return

def GetFittness(dna):
	return dna.Fittness

def Mutation(weights, mutationRate, mutationAmount):
	weightType = type(weights)

	if hasattr(weights, "__len__"):
		if weightType == np.ndarray:

			d1 = np.random.random_integers(0, 1, weights.shape)
			d2 = np.random.random_integers(-100, 100, weights.shape)
			mutateArray = ((d1*d2)/1000)+1
			newWeights = weights*mutateArray
			return newWeights
		else:
			newWeights = list()
			for weight in weights:
				newWeights += [Mutation(weight, mutationRate, mutationAmount)]
			return newWeights

		return newWeights

	return newWeights
