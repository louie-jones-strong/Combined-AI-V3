import os
import pickle


class NeuralNetwork(object):
	DataSetX = []
	DataSetY = []

	def __init__(self, numOfOutputs, minOutputSize, maxOutputSize, outputResolution, dataSetPath):
		self.DataSetPath = dataSetPath
		return

	def ImportDataSet(self):
		if not os.path.isfile(self.DataSetPath + ".p"):
			return

		file = open(self.DataSetPath + ".p", "rb")
		dataSet = pickle.load(file)
		file.close()

		for key, value in dataSet.items():
			self.DataSetX += [key]

			temp = []
			for loop in range(4096):#len of move to move ids list
				if loop in value.Moves:
					temp += [1]
				else:
					temp += [0]

			self.DataSetY += [temp]

		return 

	def SaveDataSet(self):

		return

	def Train(self, epochs):
		
		return

	def Run(self):

		return


