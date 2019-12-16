import time
import sys
import random
import numpy as np
import Agents.Evolution.DNAObject as DNA

class EvolutionController:
	NumberOfDNAInGenration = 50
	GenrationNum = 0
	FittnessCache = []
	LastGenBestFittness = None
	
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

		if self.EvoAgentList[evoAgentId].WinningModeON:
			agentDna = self.DNAList[len(self.DNAList)-1]
			agentDna.AgentId = evoAgentId

		else:
			for loop in range(len(self.DNAList)):
				dna = self.DNAList[loop]
				self.FittnessCache[loop] = round(dna.Fittness, 3)

				if dna.AgentId == None and dna.NumberOfGames == 0:
					agentDna = dna
					break
		
			if agentDna == None:
				self.CalNextGen()
				agentDna = self.DNAList[0]

			agentDna.AgentId = evoAgentId
		return agentDna

	def MakeDNAListFromSeed(self):
		self.DNAList = []
		for loop in range(self.NumberOfDNAInGenration-1):
			self.DNAList += [DNA.DNAObject(Mutation(self.WeightsSeed))]
			self.FittnessCache += [0]


		self.DNAList += [DNA.DNAObject(self.WeightsSeed)]
		self.FittnessCache += [0]
		return

	def CalNextGen(self):
		self.DNAList.sort(key=GetFittness, reverse=True)
		self.LastGenBestFittness = self.DNAList[0].Fittness

		self.DNAList = self.DNAList[:int(len(self.DNAList)/2)]

		selectionChance = CalSelectionChance(self.DNAList)
		self.DNAList = Breed(self.DNAList, selectionChance)



		for loop in range(len(self.DNAList)):
			self.DNAList[loop].NumberOfGames = 0
			self.DNAList[loop].AgentId = None
			self.DNAList[loop].Fittness = 0
			self.FittnessCache[loop] = 0

		self.GenrationNum += 1
		return

	def ControllerInfoOutput(self):
		info = "Genration: " + str(self.GenrationNum)
		info += "\n"
		
		if self.LastGenBestFittness != None:
			info += "Last Gen Best Fittness: "+str(self.LastGenBestFittness)
			info += "\n"
			
		info += "Fittness: " + str(sorted(self.FittnessCache, reverse=True))
		return info

def GetFittness(dna):
	return dna.Fittness

def Mutation(weights):
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
				newWeights += [Mutation(weight)]
			return newWeights

		return newWeights

	return newWeights


def Breed(dnaList, selectionChance):

	newDnaList = []
	for loop in range(len(dnaList)):
		dna1 = dnaList[loop]
		#todo make sure it can't breed with it's self
		dna2 = np.random.choice(dnaList, p=selectionChance)

		newDnaList += [DNA.DNAObject(Mutation(dna1.Weights))]


		#todo make the better one more important
		newWeights = CrossFadeWithWeights(dna1.Weights, dna2.Weights, [0.5, 0.5])

		newWeights = Mutation(newWeights)
		newDnaList += [DNA.DNAObject(newWeights)]
		
	return newDnaList


def CalSelectionChance(dnaList):

	selectionChance = []
	for dna in dnaList:
		fittness = GetFittness(dna)

		selectionChance += [pow(fittness, 3)]

	selectionChance = selectionChance / np.amax(selectionChance)

	selectionChance = selectionChance / np.sum(selectionChance)
	
	return selectionChance

def CrossFadeWithWeights(dna1, dna2, weights):
	newDna = []
	for loop in range(len(dna1)):
		temp = []
		for loop2 in range(len(dna1[loop])):

			joinArray = np.array([dna1[loop][loop2], dna2[loop][loop2]], dtype=dna1[loop][loop2].dtype)

			temp += [np.average(joinArray, axis=0, weights=weights)]

		newDna += [temp]

	return newDna
