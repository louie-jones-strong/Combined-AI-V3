#import Agents.NeuralNetwork as NeuralNetwork
from DataManger.Serializer import BoardToKey
import time
from Shared import OutputFormating as Format
import Predictors.PredictorBase as PredictorBase


class BoardValuePredictor(PredictorBase.PredictorBase):
	TrainedEpochs = 0

	def __init__(self, dataSetManager, loadData, trainingMode=False):
		super().__init__(dataSetManager, loadData)
		return

	def PredictValue(self, board):
		value = 0

		key = BoardToKey(board)
		found, boardInfo = self.DataSetManager.GetBoardInfo(key)

		if found:
			value = boardInfo.TotalAvgFitness
		
		self.NumPredictions += 1
		return value
