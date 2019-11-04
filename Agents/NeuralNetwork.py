import os
from DataManger.Serializer import BoardToKey
import time
import sys

import keras

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
		weightsValue = self.NetworkModel.get_weights()
		return weightsValue

	def SetWeights(self, newWeights):
		self.NetworkModel.set_weights(newWeights)
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
	network = keras.models.Sequential()

	network.add(keras.layers.Dense(structreArray[0][1],input_shape=inputShape))

	network = LayerMaker(network, structreArray)

	network.compile(loss=keras.losses.categorical_crossentropy,
              optimizer=keras.optimizers.SGD(lr=0.01, momentum=0.9, nesterov=True))
	return network

def LayerMaker(network, structreArray, layerNumber=0):
	layerInfo = structreArray[layerNumber]

	network.add(keras.layers.Dense(layerInfo[1], activation=layerInfo[2]))

	if len(structreArray) > layerNumber+1:
		network = LayerMaker(network, structreArray, layerNumber=layerNumber+1)

	return network