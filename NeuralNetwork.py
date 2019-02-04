import os
import pickle
import tflearn


class NeuralNetwork(object):
	DataSetX = []
	DataSetY = []

	def __init__(self, numOfOutputs, minOutputSize, maxOutputSize, outputResolution, dataSetPath):
		self.DataSetPath = dataSetPath
		self.ImportDataSet()

		structreArray = []
		structreArray += [["ann", 100, "Tanh"]]
		structreArray += [["ann", len(self.DataSetY[0]), "Sigmoid"]]

		self.NetworkModel = ModelMaker([len(self.DataSetX[0])], structreArray)
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
		self.NetworkModel.fit(self.DataSetX, self.DataSetY, n_epoch=epochs)
		#self.NetworkModel.fit( X , Y , n_epoch=epochs , validation_set=( testX , testY ) , show_metric=metrics_on , snapshot_epoch=checkpoints_on , run_id=run_ID )
		return

	def Run(self, inputs):
		output = self.NetworkModel.predict(inputs)
		return output

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

	if optimizer == "adam":
		network = tflearn.regression(network, optimizer="adam", learning_rate=lr, batch_size=batchSize, loss='mean_square', name='target')
	else:
		sgd = tflearn.SGD(learning_rate = lr, lr_decay = 0.01 , decay_step=50)
		network = tflearn.regression(network, optimizer=sgd, learning_rate=lr, batch_size=batchSize, loss="mean_square", name="target")
	
	model = tflearn.DNN(network, tensorboard_dir="log")
	return model
def LayerMaker(network, structreArray, layerNumber=0):
	layerName = "layer" + str(layerNumber)

	layerInfo = structreArray[layerNumber]

	if layerInfo[0] == "conv":
		network = tflearn.conv_2d(network, layerInfo[1], 3, activation=layerInfo[2], regularizer="L2", name=layerName)

	elif layerInfo[0] == "ann":
		network = tflearn.fully_connected(network, layerInfo[1] , activation=layerInfo[2], bias=True, bias_init="Normal", name=layerName)
		if len(layerInfo) > 1 and True:
			network = tflearn.dropout(network, 0.8)

	elif layerInfo[0] == "maxpool":
		network = tflearn.max_pool_2d(network, layerInfo[1], name=layerName)

	elif layerInfo[0] == "rnn":
		network = tflearn.simple_rnn(network, layerInfo[1] , activation=layerInfo[2],bias = True, name=layerName)

	elif  layerInfo[0] == "lstm":
		if len(layerInfo) > 2 and layerInfo[3] == "True":
			network = tflearn.lstm(network, layerInfo[1], activation=layerInfo[2] , dropout=0.8 , return_seq=True, name=layerName)
		else:
			network = tflearn.lstm(network, layerInfo[1], activation=layerInfo[2] , return_seq=False, name=layerName)



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
	return weights_value

def SetWeights(model, numberOfLayers, newWeights):

	for loop in range(numberOfLayers):
		temp = tflearn.variables.get_layer_variables_by_name("layer"+str(loop))
		with model.session.as_default():
			tflearn.variables.set_value(temp[0],newWeights[loop][0])
			tflearn.variables.set_value(temp[1],newWeights[loop][1])
	return model
