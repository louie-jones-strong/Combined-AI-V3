import Agents.NeuralNetwork as NeuralNetwork
from DataManger.BasicLoadAndSave import BoardToKey

class SimOutputPredictor:

	def __init__(self, dataSetManager, loadData, trainingMode=False):
		self.DataSetManager = dataSetManager

		if loadData:
			self.DataSetManager.LoadTableInfo()
		return

	def PredictOutput(self, board, move):
		newBoard = board[:]

		key = BoardToKey(board)
		found, boardInfo = self.DataSetManager.GetBoardInfo(key)

		if found:
			moveID = self.DataSetManager.MoveIDLookUp.index(move)
			moveOutComes = boardInfo[moveID].MoveOutComes
			
			highestTimes = 0
			for outCome, times in moveOutComes.items():
						
				if highestTimes < times:
					newBoard = outCome
					highestTimes = times

		else:
			print("need to code ann for PredictOutput")

		return newBoard
