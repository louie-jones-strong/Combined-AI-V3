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

		loop = 0
		for key, value in dataSet.items():
			self.DataSetX += [key]

			temp = []
			for loop2 in range(4096):#len of move to move ids list
				if loop2 in value.Moves:
					temp += [1]
				else:
					temp += [0]

			self.DataSetY += [temp]
			
			if loop % 500 == 0:
				temp = int((loop/len(dataSet))*100)
				os.system("cls")
				print(str(temp)+"% "+str(loop)+"/"+str(len(dataSet)))
			loop += 1

		

		return 

	def SaveDataSet(self, path):
		pickle.dump(self.DataSetX, open(path + "X.p", "wb"))
		pickle.dump(self.DataSetY, open(path + "Y.p", "wb"))
		return

	def Train(self, epochs):
		
		return

	def Run(self):

		return


