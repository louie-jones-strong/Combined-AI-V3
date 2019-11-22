import Agents.AgentBase as AgentBase
import Predictors.SimOutputPredictor as BoardPredictor
import Predictors.BoardValuePredictor as BoardValuePredictor
from Shared import OutputFormating as Format
from DataManger.Serializer import BoardToKey
import sys
import time

class Agent(AgentBase.AgentBase):
	AgentType = "MonteCarlo"

	def __init__(self, dataSetManager, loadData, moveAgent, winningModeON=False):
		super().__init__(dataSetManager, loadData, winningModeON)

		self.MoveAgent = moveAgent
		self.MoveAgent.winningModeON = winningModeON
		self.AgentType += "("+str(moveAgent.AgentType)+")"

		self.MoveAgent.RecordMoves = False
		self.NumDiffrentMoves = 0

		self.BoardPredictor = BoardPredictor.SimOutputPredictor(dataSetManager, loadData)
		self.ValuePredictor = BoardValuePredictor.BoardValuePredictor(dataSetManager, loadData)

		self.MaxMoveCalDepth = 10
		self.MaxMoveCalTime = 5

		self.MoveListCalCache = {}
		self.SimOuputCache = {}
		self.ValueCache = {}
		return

	def MoveCal(self, board):
		normalMove = self.MoveAgent.MoveCal(board)

		moveCalStart = time.time()
		_, alphaBetaMove = self.AlphaBeta(board, moveCalStart)
		
		if normalMove != alphaBetaMove:
			self.NumDiffrentMoves += 1
		
		self.RecordMove(board, alphaBetaMove)
		return alphaBetaMove

	def AlphaBeta(self, board, moveCalStart, alpha=-sys.maxsize, beta=sys.maxsize, isMax=True, depth=0):
		minv = sys.maxsize
		maxv = -sys.maxsize
		bestMove = None

		moveList = self.GetAgentMove(board)

		for move in moveList:
			
			predictedBoard = self.CalSimOuput(board, move)

			if (predictedBoard != "GameFinished" and depth < self.MaxMoveCalDepth and 
				time.time()-moveCalStart < self.MaxMoveCalTime):

				m, _ = self.AlphaBeta(predictedBoard, moveCalStart, alpha=alpha, beta=beta, isMax=not isMax, depth=depth+1)
			else:
				m = self.CalBoardValue(board)

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

	def GetAgentMove(self, board):
		key = BoardToKey(board)

		if key in self.MoveListCalCache:
			return self.MoveListCalCache[key]

		moveList = self.MoveAgent.MoveListCal(board)
		self.MoveListCalCache[key] = moveList
		return moveList

	def CalSimOuput(self, board, move):
		key = BoardToKey(board)+","+str(move)

		if key in self.SimOuputCache:
			return self.SimOuputCache[key]

		predictedBoard = self.BoardPredictor.PredictOutput(board, move)
		self.SimOuputCache[key] = predictedBoard
		return predictedBoard

	def CalBoardValue(self, board):
		key = BoardToKey(board)

		if key in self.ValueCache:
			return self.ValueCache[key]

		value = self.ValuePredictor.PredictValue(board)
		self.ValueCache[key] = value
		return value

	def AgentInfoOutput(self):
		info = super().AgentInfoOutput()
		info += "\n"
		info += "NumDiffrentMoves: "+Format.SplitNumber(self.NumDiffrentMoves)
		info += "\n"
		info += "MoveListCalCache size: " + Format.SplitNumber(len(self.MoveListCalCache))
		info += "\n"
		info += "SimOuputCache size: " + Format.SplitNumber(len(self.SimOuputCache))
		info += "\n"
		info += "ValueCache size: " + Format.SplitNumber(len(self.ValueCache))
		return info

	def GameFinished(self, fitness):
		super().GameFinished(fitness)

		self.MoveListCalCache = {}
		self.SimOuputCache = {}
		self.ValueCache = {}
		return

	def UpdateInvalidMove(self, board, move):
		super().UpdateInvalidMove(board, move)

		key = BoardToKey(board)+","+str(move)
		if key in self.SimOuputCache:
			del self.SimOuputCache[key]

		key = BoardToKey(board)
		if key in self.MoveListCalCache:
			del self.MoveListCalCache[key]

		return