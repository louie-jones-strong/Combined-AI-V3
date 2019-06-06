import Agents.AgentBase as AgentBase
import time

#print("Importing Tflearn...")
#import tflearn
import Agents.NeuralNetwork as NeuralNetwork

class Agent(AgentBase.AgentBase):
	TrainedEpochs = 0

	def __init__(self, dataSetManager, loadData, winningModeON=False):
		super().__init__(dataSetManager, loadData, winningModeON)
		self.LoadData = loadData

		self.NetworkModel, self.RunId, self.NumberOfLayers = NeuralNetwork.MakeModel(self.DataSetManager)

		if loadData:
			found, weights = self.DataSetManager.LoadNetworkWeights()
			if found:
				NeuralNetwork.SetWeights(self.NetworkModel, self.NumberOfLayers, weights)

		self.BatchSize = 4520
		return

	def MoveCal(self, inputs, batch=False):
		if not batch:
			inputs = [inputs]

		networkOutputs = self.NetworkModel.predict(inputs)

		outputs = []
		for loop in range(len(networkOutputs)):
			networkOutput = list(networkOutputs[loop])

			if self.DataSetManager.MetaData["NetworkUsingOneHotEncoding"]:
				output = [0] 
				bestValue = 0
				for loop2 in range(len(networkOutput)):
					if networkOutput[loop2] >= bestValue:
						bestValue = networkOutput[loop2]
						output = self.DataSetManager.MoveIDToMove(loop2)

			else:
				output = []
				for loop2 in range(len(networkOutput)):
					temp = networkOutput[loop2]
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

			outputs += [output]

		if not batch:
			outputs = outputs[0]

		return outputs

	def Train(self):
		dataSetX = []
		dataSetY = []

		while len(dataSetY) == 0:
			dataSetX, dataSetY = self.DataSetManager.GetMoveDataSet()
		datasetLoadedAtTime = time.time()

		while True:
			epochs = 100
			self.NetworkModel.fit(dataSetX, dataSetY, n_epoch=epochs, batch_size=self.BatchSize, run_id=str(self.RunId), shuffle=True)
			self.TrainedEpochs += epochs

			if self.TrainedEpochs % (epochs*10) == 0:
				weights = NeuralNetwork.GetWeights(self.NetworkModel, self.NumberOfLayers)
				self.DataSetManager.SaveNetworkWeights(weights)

				if time.time() - datasetLoadedAtTime >= 60*5:
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