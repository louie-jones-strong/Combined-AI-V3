
class SimOutputPredictor:

	def __init__(self, dataSetManager, loadData):
		self.DataSetManager = dataSetManager
		self.TempDataSet = {}

		if loadData:
			self.DataSetManager.LoadTableInfo()
		return

	def PredictOutput(self, board, move):
		newBoard = board[:]

		key = self.DataSetManager.BoardToKey(board)
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
