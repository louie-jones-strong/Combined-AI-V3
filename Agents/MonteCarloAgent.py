import Agents.AgentBase as AgentBase
import Agents.SimOutputPredictor as BoardPredictor

class Agent(AgentBase.AgentBase):

	def __init__(self, dataSetManager, loadData, moveAgent, winningModeON=False):
		super().__init__(dataSetManager, loadData, winningModeON)

		self.MoveAgent = moveAgent
		self.MoveAgent.RecordMoves = False

		self.BoardPredictor = BoardPredictor.SimOutputPredictor(dataSetManager, loadData)
		self.Depth = 3
		return

	def MoveCal(self, board):
		move = self.MoveAgent.MoveCal(board)
		
		return move

