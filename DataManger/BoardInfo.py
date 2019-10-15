import sys
import threading

class BoardInfo():
	MoveIDOfBestAvgFitness = 0
	BestAvgFitness = -sys.maxsize
	Moves = {}
	PlayedMovesLookUpArray = 0
	Finished = False
	Lock = threading.Lock()
	BeingUsed = False

	def __init__(self):
		self.MoveIDOfBestAvgFitness = 0
		self.BestAvgFitness = -sys.maxsize
		self.Moves = {}
		self.PlayedMovesLookUpArray = 0
		self.Finished = False
		self.Lock = threading.Lock()
		self.BeingUsed = False
		return

	def __getstate__(self):
		state = {}
		state["Moves"] = self.Moves
		state["MoveIDOfBestAvgFitness"] = self.MoveIDOfBestAvgFitness
		state["BestAvgFitness"] = self.BestAvgFitness
		state["PlayedMovesLookUpArray"] = self.PlayedMovesLookUpArray
		state["Finished"] = self.Finished
		
		self.Lock = threading.Lock()
		self.BeingUsed = False
		return state

	def __setstate__(self, state):
		self.Moves = state["Moves"]
		self.MoveIDOfBestAvgFitness = state["MoveIDOfBestAvgFitness"]
		self.BestAvgFitness = state["BestAvgFitness"]
		self.PlayedMovesLookUpArray = state["PlayedMovesLookUpArray"]
		self.Finished = state["Finished"]

		self.Lock = threading.Lock()
		self.BeingUsed = False
		return