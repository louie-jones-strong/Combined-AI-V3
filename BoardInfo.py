import sys

class BoardInfo():
	NumOfTriedMoves = 1
	MoveIDOfBestAvgFitness = 0
	BestAvgFitness = -sys.maxsize
	Moves = {}

	def __init__(self, NumOfTriedMoves=1, Moves={}, moveIDOfBestAvgFitness=0, bestAvgFitness=-sys.maxsize):
		self.NumOfTriedMoves = NumOfTriedMoves
		self.Moves = Moves
		self.MoveIDOfBestAvgFitness = moveIDOfBestAvgFitness
		self.BestAvgFitness = bestAvgFitness
		return
class MoveInfo():
	AvgFitness = 0.0
	TimesPlayed = 1

	def __init__(self, AvgFitness=0.0, TimesPlayed=1):
		self.AvgFitness = AvgFitness
		self.TimesPlayed = TimesPlayed
		return
# 1) point to the move that is least played
