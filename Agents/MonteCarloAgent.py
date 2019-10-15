import Agents.AgentBase as AgentBase
import Agents.SimOutputPredictor as BoardPredictor
import Agents.BoardValuePredictor as BoardValuePredictor
from Shared import OutputFormating as Format
import sys

class Agent(AgentBase.AgentBase):
	AgentType = "MonteCarlo"

	def __init__(self, dataSetManager, loadData, moveAgent, winningModeON=False):
		super().__init__(dataSetManager, loadData, winningModeON)

		self.MoveAgent = moveAgent
		self.AgentType += "("+str(moveAgent.AgentType)+")"

		self.MoveAgent.RecordMoves = False
		self.NumDiffrentMoves = 0

		self.BoardPredictor = BoardPredictor.SimOutputPredictor(dataSetManager, loadData)
		self.ValuePredictor = BoardValuePredictor.BoardValuePredictor(dataSetManager, loadData)

		self.MaxMoveCalDepth = 10
		self.MaxMoveCalTime = 1
		return

	def MoveCal(self, board):
		normalMove = self.MoveAgent.MoveCal(board)

		_, alphaBetaMove = self.AlphaBeta(board)
		
		if normalMove != alphaBetaMove:
			self.NumDiffrentMoves += 1
		
		self.RecordMove(board, alphaBetaMove)
		return alphaBetaMove

	def AlphaBeta(self, board, alpha=-sys.maxsize, beta=sys.maxsize, isMax=True, depth=0):
		minv = sys.maxsize
		maxv = -sys.maxsize
		bestMove = None

		moveList = self.MoveAgent.MoveListCal(board)

		for move in moveList:
			
			predictedBoard = self.BoardPredictor.PredictOutput(board, move)

			if predictedBoard != "GameFinished" and depth < self.MaxMoveCalDepth:
				m, _ = self.AlphaBeta(predictedBoard, alpha=alpha, beta=beta, isMax=not isMax, depth=depth+1)
			else:
				m = self.ValuePredictor.PredictValue(board)

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
		info += "NumDiffrentMoves: "+Format.SplitNumber(self.NumDiffrentMoves)
		return info
