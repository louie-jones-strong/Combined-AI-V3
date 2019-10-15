import Agents.AgentBase as AgentBase
import Agents.SimOutputPredictor as BoardPredictor
import sys

class Agent(AgentBase.AgentBase):
	AgentType = "MonteCarlo"

	def __init__(self, dataSetManager, loadData, moveAgent, winningModeON=False):
		super().__init__(dataSetManager, loadData, winningModeON)

		self.MoveAgent = moveAgent
		self.AgentType += "("+str(moveAgent.AgentType)+")"

		self.MoveAgent.RecordMoves = False

		self.BoardPredictor = BoardPredictor.SimOutputPredictor(dataSetManager, loadData)

		self.MaxMoveCalDepth = 10
		self.MaxMoveCalTime = 1
		return

	def MoveCal(self, board):
		_ , move = self.AlphaBeta(board)
		self.RecordMove(board, move)
		return move

	def AlphaBeta(self, board, alpha=-sys.maxsize, beta=sys.maxsize, isMax=True, depth=0):
		minv = sys.maxsize
		maxv = -sys.maxsize
		bestMove = None

		moveList = self.MoveAgent.MoveListCal(board)

		for move in moveList:
			
			predictedBoard = self.BoardPredictor.PredictOutput(board, move)

			if predictedBoard != "GameFinished" and depth < self.MaxMoveCalDepth:
				m, _ = self.AlphaBeta(predictedBoard, alpha=alpha, beta=beta, isMax=not isMax, depth=depth+1)

				if isMax:
					if m > maxv:
						maxv = m
						bestMove = move

						if maxv >= beta:
							return maxv, bestMove
						elif maxv > alpha:
							alpha = maxv
				else:
					if m < minv:
						minv = m

						if minv <= alpha:
							return minv, bestMove

						elif minv < beta:
							beta = minv

		return minv, bestMove

	def AgentInfoOutput(self):
		info = super().AgentInfoOutput()
		info += "\n"
		info += "Monte Carlo info"
		return info
