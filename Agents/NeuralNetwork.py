import os
from DataManger.Serializer import BoardToKey
import time
import sys

print("Importing Tflearn...")
import tflearn

class NeuralNetwork:

	def __init__(self, networkModel, numberOfLayers, batchSize, runId):
		self.NetworkModel = networkModel
		self.NumberOfLayers = numberOfLayers
		self.BatchSize = batchSize
		self.RunId = runId
		self.PredictionCache = {}
		self.MaxCacheSize = 10000

		self.NumBetterValueInvailds = 0
		return
	
	def GetWeights(self):
		weightsValue = []
		for loop in range(self.NumberOfLayers):
			temp = tflearn.variables.get_layer_variables_by_name("layer"+str(loop))
			with self.NetworkModel.session.as_default():
				temp[0] = tflearn.variables.get_value(temp[0])
				temp[1] = tflearn.variables.get_value(temp[1])
				weightsValue += [temp]
		return weightsValue

	def SetWeights(self, newWeights):
		for loop in range(self.NumberOfLayers):
			temp = tflearn.variables.get_layer_variables_by_name("layer"+str(loop))
			with self.NetworkModel.session.as_default():
				tflearn.variables.set_value(temp[0],newWeights[loop][0])
				tflearn.variables.set_value(temp[1],newWeights[loop][1])

		self.PredictionCache = {}
		return

	def Predict(self, board):
		key = BoardToKey(board)

		if key in self.PredictionCache:
			output = self.PredictionCache[key]
		else:
			output = self.NetworkModel.predict(board)
			if len(self.PredictionCache) >= self.MaxCacheSize:
				self.PredictionCache = {}
			self.PredictionCache[key] = output

		return output

	def Train(self, dataSetX, dataSetY, trainingTime=60):
		trainedEpochs = 0
		trainingStartTime = time.time()
		
		while trainingTime == None or (time.time()-trainingStartTime) < trainingTime:
			epochs = 10
			self.NetworkModel.fit(dataSetX, dataSetY, n_epoch=epochs, batch_size=self.BatchSize, run_id=self.RunId, shuffle=True)
			trainedEpochs += epochs

		self.PredictionCache = {}
		return trainedEpochs

	def GetInfoOutput(self, numGames, numMoves):
		
		info = "ANN Prediction Cache Size: " + str(len(self.PredictionCache))
		
		perGame = self.NumBetterValueInvailds
		if numGames > 0:
			perGame = self.NumBetterValueInvailds/numGames

		perMove = self.NumBetterValueInvailds
		if numMoves > 0:
			perMove = self.NumBetterValueInvailds/numMoves


		info += "\n"
		info += "Avg NumBetterValueInvailds per Game: "+str(round(perGame))
		info += "\n"
		info += "Avg NumBetterValueInvailds Per move: "+str(round(perMove))
		info += "\n"
		return info

	def PredictionToMove(self, dataSetManager, networkOutput, board):

		if dataSetManager.MetaDataGet("NetworkUsingOneHotEncoding"):
			key = BoardToKey(board)
			found, boardInfo = dataSetManager.GetBoardInfo(key)

			output = dataSetManager.MoveIDToMove(0)
			bestValue = -sys.maxsize

			for loop in range(len(networkOutput)):
				invaild = False

				if found:
					if 2**loop & boardInfo.PlayedMovesLookUpArray:
						if loop not in boardInfo.Moves:
							invaild = True

				if networkOutput[loop] >= bestValue and (not invaild):
					bestValue = networkOutput[loop]
					output = dataSetManager.MoveIDToMove(loop)

			for loop in range(len(networkOutput)):
				if networkOutput[loop] >= bestValue:
					self.NumBetterValueInvailds += 1
			
			self.NumBetterValueInvailds -= 1


		else:
			output = []
			for loop in range(len(networkOutput)):
				temp = networkOutput[loop]
				temp = temp / dataSetManager.OutputResolution
				temp = round(temp)
				temp = temp * dataSetManager.OutputResolution

				if temp < dataSetManager.MinOutputSize:
					temp = dataSetManager.MinOutputSize

				if temp > dataSetManager.MaxOutputSize:
					temp = dataSetManager.MaxOutputSize

				if dataSetManager.OutputResolution == int(dataSetManager.OutputResolution):
					temp= int(temp)

				output += [temp]

		return output

def MakeModel(dataSetManager):
	inputShape, structreArray = PredictNetworkStructre(dataSetManager)

	runId = dataSetManager.MetaDataGet("AnnRunId")
	if runId == None:
		runId = 0
		if os.path.exists(dataSetManager.TesnorBoardLogAddress):
			runId = len(os.listdir(dataSetManager.TesnorBoardLogAddress))

		dataSetManager.MetaDataSet("AnnRunId", runId)

	model = ModelMaker(inputShape, structreArray, dataSetManager.TesnorBoardLogAddress, lr=0.001)#, optimizer="sgd")	
	return model, str(runId), len(structreArray)

def PredictNetworkStructre(dataSetManager):

	inputShape = dataSetManager.MetaDataGet("AnnMoveInputShape")
	structreArray = dataSetManager.MetaDataGet("AnnMoveStructreArray")

	if structreArray == None or inputShape == None:
		dataSetX = []
		dataSetY = []

		while len(dataSetY) == 0:
			print("waiting for move dataset")
			time.sleep(10)
			dataSetX, dataSetY = dataSetManager.GetMoveDataSet()

		inputShape = [len(dataSetX[0])]
		if hasattr(dataSetX[0][0], "__len__"):
			inputShape += [len(dataSetX[0][0])]

			if hasattr(dataSetX[0][0][0], "__len__"):
				inputShape += [len(dataSetX[0][0][0])]

				if hasattr(dataSetX[0][0][0][0], "__len__"):
					inputShape += [len(dataSetX[0][0][0][0])]

		inputNodeSum = 1
		for loop in range(len(inputShape)):
			inputNodeSum *= inputShape[loop]


		structreArray = []
		structreArray += [["ann", inputNodeSum*10, "Tanh"]]
		structreArray += [["ann", inputNodeSum*10, "Tanh"]]
		structreArray += [["ann", inputNodeSum*10, "Tanh"]]
		structreArray += [["ann", inputNodeSum*10, "Tanh"]]
		structreArray += [["ann", inputNodeSum*10, "Tanh"]]
		structreArray += [["ann", inputNodeSum*10, "Tanh"]]

		if dataSetManager.MinOutputSize < -1 or dataSetManager.MaxOutputSize > 1:
			structreArray += [["ann", len(dataSetY[0]), "Linear"]]
		elif dataSetManager.MinOutputSize < 0:
			structreArray += [["ann", len(dataSetY[0]), "Tanh"]]
		else:
			structreArray += [["ann", len(dataSetY[0]), "Sigmoid"]]

		dataSetManager.MetaDataSet("AnnMoveInputShape", inputShape)
		dataSetManager.MetaDataSet("AnnMoveStructreArray", structreArray)

	return inputShape, structreArray

def ModelMaker(inputShape, structreArray, tensorBoardAdress, lr=0.01, optimizer="adam"):
	
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
	
	loss = 'mean_square'
	if optimizer != "adam":
		optimizer = tflearn.SGD(learning_rate=lr)
	
	network = tflearn.regression(network, optimizer=optimizer, learning_rate=lr, loss=loss, name="target")
	
	model = tflearn.DNN(network, tensorboard_dir=tensorBoardAdress)
	return model
def LayerMaker(network, structreArray, layerNumber=0):
	layerName = "layer" + str(layerNumber)

	layerInfo = structreArray[layerNumber]

	if layerInfo[0] == "conv":
		network = tflearn.conv_2d(network, layerInfo[1], 3, activation=layerInfo[2], regularizer="L2", name=layerName)

	elif layerInfo[0] == "ann":
		network = tflearn.fully_connected(network, layerInfo[1], activation=layerInfo[2], name=layerName)
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