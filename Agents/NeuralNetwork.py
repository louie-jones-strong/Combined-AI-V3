import os

print("Importing Tflearn...")
import tflearn

def GetWeights(networkModel, numberOfLayers):
	weightsValue = []

	for loop in range(numberOfLayers):
		temp = tflearn.variables.get_layer_variables_by_name("layer"+str(loop))
		with networkModel.session.as_default():
			temp[0] = tflearn.variables.get_value(temp[0])
			temp[1] = tflearn.variables.get_value(temp[1])
			weightsValue += [temp]
	return weightsValue
def SetWeights(networkModel, numberOfLayers, newWeights):

	for loop in range(numberOfLayers):
		temp = tflearn.variables.get_layer_variables_by_name("layer"+str(loop))
		with networkModel.session.as_default():
			tflearn.variables.set_value(temp[0],newWeights[loop][0])
			tflearn.variables.set_value(temp[1],newWeights[loop][1])
	return


def MakeModel(dataSetManager):
	inputShape, structreArray = PredictNetworkStructre(dataSetManager)

	runId = 0
	if os.path.exists(dataSetManager.TesnorBoardLogAddress):
		runId = len(os.listdir(dataSetManager.TesnorBoardLogAddress))

	model = ModelMaker(inputShape, structreArray, dataSetManager.TesnorBoardLogAddress, lr=0.001)#, optimizer="sgd")	
	return model, runId, len(structreArray)

def PredictNetworkStructre(dataSetManager):

	inputShape = dataSetManager.MetaData["AnnMoveInputShape"]
	structreArray = dataSetManager.MetaData["AnnMoveStructreArray"]

	if structreArray == None or inputShape == None:
		dataSetX = []
		dataSetY = []

		while len(dataSetY) == 0:
			dataSetX, dataSetY = dataSetManager.GetMoveDataSet()

		inputShape = [len(dataSetX[0])]
		if hasattr(dataSetX[0][0], "__len__"):
			inputShape += [len(dataSetX[0][0])]

			if hasattr(dataSetX[0][0][0], "__len__"):
				inputShape += [len(dataSetX[0][0][0])]

				if hasattr(dataSetX[0][0][0][0], "__len__"):
					inputShape += [len(dataSetX[0][0][0][0])]

		structreArray = []
		structreArray += [["ann", 50, "Tanh"]]
		structreArray += [["ann", 50, "Tanh"]]

		if dataSetManager.MinOutputSize < -1 or dataSetManager.MaxOutputSize > 1:
			structreArray += [["ann", len(dataSetY[0]), "Linear"]]
		elif dataSetManager.MinOutputSize < 0:
			structreArray += [["ann", len(dataSetY[0]), "Tanh"]]
		else:
			structreArray += [["ann", len(dataSetY[0]), "Sigmoid"]]

		dataSetManager.MetaData["AnnMoveInputShape"] = inputShape
		dataSetManager.MetaData["AnnMoveStructreArray"] = structreArray

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
