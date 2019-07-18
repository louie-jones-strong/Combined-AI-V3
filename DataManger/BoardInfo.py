import sys
import threading

class BoardInfo():
	MoveIDOfBestAvgFitness = 0
	BestAvgFitness = -sys.maxsize
	Moves = {}
	PlayedMovesLookUpArray = 0
	Finished = False
	Lock = threading.Lock()

	def __getstate__(self):
		state = {}
		state["Moves"] = self.Moves
		state["MoveIDOfBestAvgFitness"] = self.MoveIDOfBestAvgFitness
		state["BestAvgFitness"] = self.BestAvgFitness
		state["PlayedMovesLookUpArray"] = self.PlayedMovesLookUpArray
		state["Finished"] = self.Finished
		return state

	def __setstate__(self, state):
		self.Moves = state["Moves"]
		self.MoveIDOfBestAvgFitness = state["MoveIDOfBestAvgFitness"]
		self.BestAvgFitness = state["BestAvgFitness"]
		self.PlayedMovesLookUpArray = state["PlayedMovesLookUpArray"]
		self.Finished = state["Finished"]
		self.Lock = threading.Lock()
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
