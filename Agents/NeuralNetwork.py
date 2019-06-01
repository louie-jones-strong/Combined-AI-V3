import Agents.AgentBase as AgentBase
import os

print("Importing Tflearn...")
import tflearn


class Agent(AgentBase.AgentBase):
	TrainedEpochs = 0

	def __init__(self, dataSetManager, loadData, winningModeON=False):
		super().__init__(dataSetManager, loadData, winningModeON)

		self.DataSetX = []
		self.DataSetY = []
		self.IsOneHotEncoding = False

		self.DataSetManager.LoadTableInfo()
		while len(self.DataSetY) == 0:
			self.DataSetX, self.DataSetY, self.IsOneHotEncoding = self.DataSetManager.GetMoveDataSet()

		inputShape, structreArray = self.PredictNetworkStructre()

		self.RunId = 0
		if os.path.exists(self.DataSetManager.TesnorBoardLogAddress):
			self.RunId = len(os.listdir(self.DataSetManager.TesnorBoardLogAddress))

		self.NetworkModel = ModelMaker(inputShape, structreArray, self.DataSetManager.TesnorBoardLogAddress, lr=0.001)#, optimizer="sgd")
		self.BatchSize = 1000
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
		structreArray += [["ann", 50, "Tanh"]]
		structreArray += [["ann", 50, "Tanh"]]

		if self.DataSetManager.MinOutputSize < -1 or self.DataSetManager.MaxOutputSize > 1:
			structreArray += [["ann", len(self.DataSetY[0]), "Linear"]]
		elif self.DataSetManager.MinOutputSize < 0:
			structreArray += [["ann", len(self.DataSetY[0]), "Tanh"]]
		else:
			structreArray += [["ann", len(self.DataSetY[0]), "Sigmoid"]]

		self.NumberOfLayers = len(structreArray)
		return inputShape, structreArray

	def MoveCal(self, inputs, batch=False):
		if not batch:
			inputs = [inputs]

		networkOutputs = self.NetworkModel.predict(inputs)

		outputs = []
		for loop in range(len(networkOutputs)):
			networkOutput = list(networkOutputs[loop])

			if self.IsOneHotEncoding:
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

	def UpdateInvalidMove(self, board, move):
		print("Move was Invalid!! RETRAINING")
		newMove = move[:]
		
		while move == newMove:
			self.TrainNetWork()
			newMove = self.MoveCal(board)

		return

	def TrainNetWork(self):
		epochs = 1000
		self.NetworkModel.fit(self.DataSetX, self.DataSetY, n_epoch=epochs, run_id=str(self.RunId), shuffle=True)
		self.TrainedEpochs += epochs

		if self.TrainedEpochs % (epochs*10) == 0:
			self.SaveData(0)

		correct, total = self.GetAccuracy()
		print("Accuracy: "+str(correct/total)+" "+str(correct)+"/"+str(total))
		return

	def GetAccuracy(self):
		
		outputs = self.MoveCal(self.DataSetX, batch=True)

		correct = 0
		for loop in range(len(self.DataSetX)):

			if outputs[loop] == self.DataSetY[loop]:
				correct += 1

		return correct, len(self.DataSetX)

	def UpdateMoveOutCome(self, board, move, outComeBoard, gameFinished=False):
		
		return

	def SaveData(self, fitness):
		weights = self.GetWeights()
		self.DataSetManager.SaveNetworkWeights(weights)
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
		return

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
	
	loss = loss='mean_square'
	#loss = "categorical_crossentropy"
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
