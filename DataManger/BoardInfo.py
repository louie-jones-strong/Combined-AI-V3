import sys

class BoardInfo():
	MoveIDOfBestAvgFitness = 0
	BestAvgFitness = -sys.maxsize
	Moves = {}
	PlayedMovesLookUpArray = 0
	Finished = False

	def __init__(self):
		self.Moves = {}
		self.MoveIDOfBestAvgFitness = 0
		self.BestAvgFitness = -sys.maxsize
		self.PlayedMovesLookUpArray = 0
		self.Finished = False
		return

class MoveInfo():
	AvgFitness = 0.0
	TimesPlayed = 1
	MoveOutComes = {}


	def __init__(self, AvgFitness=0.0, TimesPlayed=0):
		self.AvgFitness = AvgFitness
		self.TimesPlayed = TimesPlayed
		self.MoveOutComes = {}
		return
# 1) point to the move that is least played
