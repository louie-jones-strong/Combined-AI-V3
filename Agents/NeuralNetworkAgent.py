import Agents.AgentBase as AgentBase
import time
import sys

import Agents.NeuralNetwork as NeuralNetwork

class Agent(AgentBase.AgentBase):
	TrainedEpochs = 0

	def __init__(self, dataSetManager, loadData, winningModeON=False, trainingMode=False):
		if not trainingMode:
			super().__init__(dataSetManager, loadData, winningModeON)
		else:
			self.DataSetManager = dataSetManager

		self.LoadData = loadData

		self.NetworkModel, self.RunId, self.NumberOfLayers = NeuralNetwork.MakeModel(self.DataSetManager)

		if loadData:
			found, weights = self.DataSetManager.LoadNetworkWeights()
			if found:
				NeuralNetwork.SetWeights(self.NetworkModel, self.NumberOfLayers, weights)

		self.BatchSize = 4520
		self.PredictionCache = {}
		if trainingMode:
			self.Train()
		return

	def MoveCal(self, boards, batch=False):
		if not batch:
			boards = [boards]

		networkOutputs = []
		boardsInCache = True
		for loop in range(len(boards)):
			
			key = self.DataSetManager.BoardToKey(boards[loop])
			if key in self.PredictionCache:
				networkOutputs += [self.PredictionCache[key]]

			else:
				boardsInCache = False
				break

		if not boardsInCache:
			networkOutputs = self.NetworkModel.predict(boards)
			self.PredictionCache = {}



		outputs = []
		for loop in range(len(networkOutputs)):
			
			key = self.DataSetManager.BoardToKey(boards[loop])
			if not boardsInCache:
				self.PredictionCache[key] = networkOutputs[loop]

			networkOutput = list(networkOutputs[loop])
			outputs += [self.PredictionToMove(networkOutput, key)]

		if not batch:
			outputs = outputs[0]
			self.RecordMove(boards[0], outputs)
		return outputs

	def PredictionToMove(self, networkOutput, key):
		if self.DataSetManager.MetaData["NetworkUsingOneHotEncoding"]:

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

	def Train(self):
		dataSetX = []
		dataSetY = []

		while len(dataSetY) == 0:
			time.sleep(10)
			dataSetX, dataSetY = self.DataSetManager.GetMoveDataSet()
		datasetLoadedAtTime = time.time()

		while True:
			epochs = 10
			self.NetworkModel.fit(dataSetX, dataSetY, n_epoch=epochs, batch_size=self.BatchSize, run_id=str(self.RunId), shuffle=True)
			self.TrainedEpochs += epochs

			if time.time() - datasetLoadedAtTime >= 60:
				weights = NeuralNetwork.GetWeights(self.NetworkModel, self.NumberOfLayers)
				self.DataSetManager.SaveNetworkWeights(weights)
				dataSetX, dataSetY = self.DataSetManager.GetMoveDataSet()
				datasetLoadedAtTime = time.time()

		return

	def SaveData(self, fitness):
		super().SaveData(fitness)
		if self.LoadData:
			found, weights = self.DataSetManager.LoadNetworkWeights()
			if found:
				NeuralNetwork.SetWeights(self.NetworkModel, self.NumberOfLayers, weights)
		return