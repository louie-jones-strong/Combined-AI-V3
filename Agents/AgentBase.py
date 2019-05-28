class AgentBase:

	def __init__(self, dataSetManager, winningModeON=False):
		self.DataSetManager = dataSetManager
		self.WinningModeON = winningModeON

		return

	def UpdateInvalidMove(self, board, move):
		return

	def UpdateMoveOutCome(self, board, move, outComeBoard, gameFinished=False):
		return

	def SaveData(self, fitness):
		return
