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

		self.MaxMoveCalDepth = 3
		self.MaxMoveCalTime = 1
		return

	def MoveCal(self, board):
		move = self.MoveAgent.MoveCal(board)
		
		self.RecordMove(board, move)
		return move

	def AlphaBeta(self, board, alpha=-sys.maxsize, beta=sys.maxsize, isMax=True):
		minv = sys.maxsize
		maxv = -sys.maxsize
		bestMove = None

		moveList = self.MoveAgent.MoveCal(board)

		for tempMove in moveList:
			
			predictedBoard = self.BoardPredictor.PredictOutput(board, tempMove)

			if predictedBoard != "Finished":
				m, tempMove = self.AlphaBeta(predictedBoard, alpha=alpha, beta=beta, isMax=not isMax)


				if isMax:
					if m > maxv:
						maxv = m
						bestMove = tempMove

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
