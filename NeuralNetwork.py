import os
import pickle
import tflearn


class NeuralNetwork(object):
	DataSetX = []
	DataSetY = []

	def __init__(self, numOfOutputs, minOutputSize, maxOutputSize, outputResolution, dataSetPath):
		self.DataSetPath = dataSetPath
		self.NetworkModel = 
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

def run_inputs( inputs , model , batch_size ):

    small = 0
    large = len(inputs)%batch_size
    temp = inputs[ small : large ]
    outputs = model.predict(temp).tolist()


    for loop in range( 0 , int(len(inputs)/batch_size) ):
        small = large
        large += batch_size
        temp = inputs[ small : large ]

        temp = model.predict(temp).tolist()
        outputs += temp
    return outputs

def model_maker( input_shape , structre_array , batch_size=20 , lr=0.01 , tensorboard_level=0 , checkpoint_on=False , checkpoint_num=1 , optimizer="adam" ):
    tflearn.config.init_graph (gpu_memory_fraction=0.95, soft_placement=True)
    model_ID = ""

    #makes the input layer
    if len(input_shape) == 1:
        network = tflearn.input_data(shape=[None, input_shape[0] ], name='input')

    elif len(input_shape) == 2:
        network = tflearn.input_data(shape=[None, input_shape[0] , input_shape[1] ], name='input')

    elif len(input_shape) == 3:
        network = tflearn.input_data(shape=[None, input_shape[0] , input_shape[1] , input_shape[2] ], name='input')

    else:
        network = tflearn.input_data(shape=[None, input_shape[0] , input_shape[1] , input_shape[2] , input_shape[3] ], name='input')

    #makes the network with recursion on each layer
    network , model_ID = layers(network,structre_array,model_ID)

    #to pick the optimizer to use to learn the task
    if optimizer == "adam":
        model_ID += "adam"
        network = tflearn.regression( network , optimizer="adam" , learning_rate=lr , batch_size = batch_size , loss='mean_square' , name='target' )

    else:
        model_ID += "sgd"
        sgd = tflearn.SGD(learning_rate = lr, lr_decay = 0.01 , decay_step=50)
        network = tflearn.regression(network, optimizer=sgd, learning_rate=lr , batch_size=batch_size , loss="mean_square", name="target" )
    
    if checkpoint_on:
        model = tflearn.DNN( network , tensorboard_verbose=tensorboard_level , tensorboard_dir='log')
    else:
        model = tflearn.DNN( network , tensorboard_verbose=tensorboard_level , checkpoint_path='tflearn\\model.tfl' , max_checkpoints=checkpoint_num , tensorboard_dir='log' )

    return model , model_ID

def layers( network , structre_array , model_ID , layer_number=0 ):
    layer_name = "layer_" + str(layer_number)

    if structre_array[0][0] == "conv":
        network = tflearn.conv_2d(network, structre_array[0][1], 3, activation=structre_array[0][2], regularizer="L2", name=layer_name)
        model_ID += "c"+str(structre_array[0][1])+"."

    elif structre_array[0][0] == "ann":
        network = tflearn.fully_connected(network, structre_array[0][1] , activation=structre_array[0][2],bias = True,bias_init = "Normal", name=layer_name)
        model_ID += "a"+str(structre_array[0][1])+"."
        if len(structre_array) > 1 and structre_array[0][3] == "True":
            network = tflearn.dropout(network, 0.8)

    elif structre_array[0][0] == "maxpool":
        network = tflearn.max_pool_2d(network, structre_array[0][1], name=layer_name)
        model_ID += "m"+str(structre_array[0][1])+"."

    elif structre_array[0][0] == "rnn":
        network = tflearn.simple_rnn(network, structre_array[0][1] , activation=structre_array[0][2],bias = True, name=layer_name)
        model_ID += "r"+str(structre_array[0][1])+"."

    elif  structre_array[0][0] == "lstm":
        if len(structre_array) > 2 and structre_array[0][3] == "True":
            network = tflearn.lstm(network, structre_array[0][1], activation=structre_array[0][2] , dropout=0.8 , return_seq=True, name=layer_name)
        else:
            network = tflearn.lstm(network, structre_array[0][1], activation=structre_array[0][2] , return_seq=False, name=layer_name)
        model_ID += "l"+str(structre_array[0][1])+"."



    if len(structre_array) > 1:
        network , model_ID = layers(network,structre_array[1:],model_ID,layer_number = layer_number+1)

    return network , model_ID

def train(epochs , model):
    
    try:
        model.fit( X , Y , n_epoch=epochs , validation_set=( testX , testY ) , show_metric=metrics_on , snapshot_epoch=checkpoints_on , run_id=run_ID )
    except:
        print("batch size to big!!")
        print("batch size changed from: " + str(batch_size) + " to: " + str(int(batch_size*0.9)) )
        batch_size = int(batch_size*0.9)
        model , batch_size = train( X , Y , testX , testY , epochs , model , batch_size , run_ID)

    return model , batch_size

def GetWeights( model , number_of_layers ):
    weights_value = []

    for loop in range(number_of_layers):
        temp = tflearn.variables.get_layer_variables_by_name("layer_"+str(loop))
        with model.session.as_default():
            temp[0] = tflearn.variables.get_value(temp[0])
            temp[1] = tflearn.variables.get_value(temp[1])
            weights_value += [temp]

    return weights_value

def SetWeights( model , number_of_layers , new_weights ):

    for loop in range(number_of_layers):
        temp = tflearn.variables.get_layer_variables_by_name("layer_"+str(loop))
        with model.session.as_default():

            tflearn.variables.set_value(temp[0],new_weights[loop][0])
            tflearn.variables.set_value(temp[1],new_weights[loop][1])
    return model
