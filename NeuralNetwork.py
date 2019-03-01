import os
import pickle
import tflearn
import time

class NeuralNetwork(object):
	DataSetX = []
	DataSetY = []

	def __init__(self, numOfOutputs, minOutputSize, maxOutputSize, outputResolution, dataSetPath):
		self.MinOutputSize = minOutputSize
		self.MaxOutputSize = maxOutputSize
		self.OutputResolution = outputResolution

		self.DataSetPath = dataSetPath
		self.LastImportTime = 0

		print("Waiting for DataSet")
		while len(self.DataSetY) == 0:
			self.ImportDataSet()
			if len(self.DataSetY) == 0:
				time.sleep(1)

		inputShape, structreArray = self.PredictNetworkStructre()

		self.RunId = "test2"
		self.NetworkModel = ModelMaker(inputShape, structreArray, batchSize=4520, lr=0.001)#, optimizer="sgd")
		return
	def PredictNetworkStructre(self):
		inputShape = [len(self.DataSetX[0])]
		if hasattr(self.DataSetX[0][0], "__len__"):
			inputShape += [len(self.DataSetX[0][0])]

			if hasattr(self.DataSetX[0][0][0], "__len__"):
				inputShape += [len(self.DataSetX[0][0][0])]

				if hasattr(self.DataSetX[0][0][0][0], "__len__"):
					inputShape += [len(self.DataSetX[0][0][0][0])]

		structreArray = []
		structreArray += [["ann", 1000, "Tanh"]]
		structreArray += [["ann", 1000, "Tanh"]]
		structreArray += [["ann", 1000, "Tanh"]]
		structreArray += [["ann", 1000, "Tanh"]]
		structreArray += [["ann", 1000, "Tanh"]]
		structreArray += [["ann", 1000, "Tanh"]]
		structreArray += [["ann", 9, "Tanh"]]

		if self.MinOutputSize < -1 or self.MinOutputSize > 1:
			structreArray += [["ann", len(self.DataSetY[0]), "Linear"]]
		elif self.MinOutputSize < 0:
			structreArray += [["ann", len(self.DataSetY[0]), "Tanh"]]
		else:
			structreArray += [["ann", len(self.DataSetY[0]), "Sigmoid"]]

		self.NumberOfLayers = len(structreArray)
		return inputShape, structreArray
	def ImportDataSet(self):
		if not os.path.isfile(self.DataSetPath+"Dataset" + ".p"):
			return False
		
		if not os.path.isfile(self.DataSetPath+"BoardHashLookup" + ".p"):
			return False

		if not os.path.isfile(self.DataSetPath+"MoveIdLookUp" + ".p"):
			return False

		if time.time() - self.LastImportTime < 60:
			return False

		if self.LastImportTime >= os.path.getmtime(self.DataSetPath+"Dataset"+".p"):
			return False

		file = open(self.DataSetPath+"Dataset" + ".p", "rb")
		dataSet = pickle.load(file)
		file.close()
		
		file = open(self.DataSetPath+"BoardHashLookup" + ".p", "rb")
		boardToHashLookUp = pickle.load(file)
		file.close()

		file = open(self.DataSetPath+"MoveIdLookUp" + ".p", "rb")
		self.MoveIdLookUp = pickle.load(file)
		file.close()

		self.LastImportTime = time.time()

		loop = 0
		self.DataSetX = []
		self.DataSetY = []
		for key, value in dataSet.items():
			if key in boardToHashLookUp:
				self.DataSetX += [boardToHashLookUp[key]]
			else:
				input("board hash missing")

			temp = self.MoveIdLookUp[value.MoveIDOfBestAvgFitness]

			self.DataSetY += [temp]
			
			if loop % 500 == 0:
				temp = int((loop/len(dataSet))*100)
				os.system("cls")
				print(str(temp)+"% "+str(loop)+"/"+str(len(dataSet)))
			loop += 1
		os.system("cls")
		print("100% "+str(len(dataSet))+"/"+str(len(dataSet)))
		return True

	def MoveCal(self, inputs):
		outputs = self.NetworkModel.predict([inputs])[0]
		

		temp =""
		for loop in range(len(outputs)):
			temp += str(loop)+": "+str(round(outputs[loop],2))+" "
		print(temp)

		largest = 0
		moveId = 0
		for loop in range(len(outputs)):
			if outputs[loop] > largest:
				moveId = loop
				largest = outputs[loop]
		
		outputMove = self.MoveIdLookUp[moveId]
		return outputMove

	def UpdateInvalidMove(self, board, move):
		os.system("cls")
		self.ImportDataSet()
		self.NetworkModel.fit(self.DataSetX, self.DataSetY, n_epoch=10, run_id=self.RunId)
		self.SaveData(0)
		return

	def SaveData(self, fitness):
		weights = GetWeights(self.NetworkModel, self.NumberOfLayers)
		pickle.dump(weights, open(self.DataSetPath+"NetWorkWeights"+".p", "wb"))
		return

	def LoadData(self):
		if os.path.isfile(self.DataSetPath+"NetWorkWeights"+".p"):
			file = open(self.DataSetPath+"NetWorkWeights"+".p", "rb")
			newWeights = pickle.load(file)
			file.close()

			self.NetworkModel = SetWeights(self.NetworkModel, self.NumberOfLayers, newWeights)
		return

def ModelMaker(inputShape, structreArray, batchSize=20, lr=0.01, optimizer="adam"):
	tflearn.config.init_graph(gpu_memory_fraction=0.95, soft_placement=True)

	if len(inputShape) == 1:
		network = tflearn.input_data(shape=[None, inputShape[0] ], name='input')
	elif len(inputShape) == 2:
		network = tflearn.input_data(shape=[None, inputShape[0] , inputShape[1] ], name='input')
	elif len(inputShape) == 3:
		network = tflearn.input_data(shape=[None, inputShape[0] , inputShape[1] , inputShape[2] ], name='input')
	else:
		network = tflearn.input_data(shape=[None, inputShape[0] , inputShape[1] , inputShape[2] , inputShape[3] ], name='input')

	network = LayerMaker(network, structreArray)
	
	loss = loss='mean_square'
	#loss = "categorical_crossentropy"
	if optimizer == "adam":
		network = tflearn.regression(network, optimizer="adam", learning_rate=lr, batch_size=batchSize, loss=loss, name='target')
	else:
		sgd = tflearn.SGD(learning_rate = lr)
		network = tflearn.regression(network, optimizer=sgd, learning_rate=lr, batch_size=batchSize, loss=loss, name="target")
	
	model = tflearn.DNN(network, tensorboard_dir="log")
	return model
def LayerMaker(network, structreArray, layerNumber=0):
	layerName = "layer" + str(layerNumber)

	layerInfo = structreArray[layerNumber]

	if layerInfo[0] == "conv":
		network = tflearn.conv_2d(network, layerInfo[1], 3, activation=layerInfo[2], regularizer="L2", name=layerName)

	elif layerInfo[0] == "ann":
		network = tflearn.fully_connected(network, layerInfo[1], activation=layerInfo[2], bias=True, name=layerName)
		#network = tflearn.dropout(network, 0.8)

	elif layerInfo[0] == "maxpool":
		network = tflearn.max_pool_2d(network, layerInfo[1], name=layerName)

	elif layerInfo[0] == "rnn":
		network = tflearn.simple_rnn(network, layerInfo[1], activation=layerInfo[2], bias=True, name=layerName)

	elif  layerInfo[0] == "lstm":
		if len(layerInfo) > 2 and layerInfo[3] == "True":
			network = tflearn.lstm(network, layerInfo[1], activation=layerInfo[2], dropout=0.8, return_seq=True, name=layerName)
		else:
			network = tflearn.lstm(network, layerInfo[1], activation=layerInfo[2], return_seq=False, name=layerName)



	if len(structreArray) > layerNumber+1:
		network = LayerMaker(network, structreArray, layerNumber=layerNumber+1)

	return network

def GetWeights(model, numberOfLayers):
	weightsValue = []

	for loop in range(numberOfLayers):
		temp = tflearn.variables.get_layer_variables_by_name("layer"+str(loop))
		with model.session.as_default():
			temp[0] = tflearn.variables.get_value(temp[0])
			temp[1] = tflearn.variables.get_value(temp[1])
			weightsValue += [temp]
	return weightsValue
def SetWeights(model, numberOfLayers, newWeights):

	for loop in range(numberOfLayers):
		temp = tflearn.variables.get_layer_variables_by_name("layer"+str(loop))
		with model.session.as_default():
			tflearn.variables.set_value(temp[0],newWeights[loop][0])
			tflearn.variables.set_value(temp[1],newWeights[loop][1])
	return model
