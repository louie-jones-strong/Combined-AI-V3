import sys

class BoardInfo():
	MoveIDOfBestAvgFitness = 0
	BestAvgFitness = -sys.maxsize
	Moves = {}
	PlayedMovesLookUpArray = 0

	def __init__(self, Moves={}, moveIDOfBestAvgFitness=0, bestAvgFitness=-sys.maxsize, playedMovesLookUpArray=0):
		self.Moves = Moves
		self.MoveIDOfBestAvgFitness = moveIDOfBestAvgFitness
		self.BestAvgFitness = bestAvgFitness
		self.PlayedMovesLookUpArray = playedMovesLookUpArray
		return

class MoveInfo():
	AvgFitness = 0.0
	TimesPlayed = 1
	MoveOutComes = {}


	def __init__(self, AvgFitness=0.0, TimesPlayed=1):
		self.AvgFitness = AvgFitness
		self.TimesPlayed = TimesPlayed
		self.MoveOutComes = {"GameFinished":0}
		return
# 1) point to the move that is least played
