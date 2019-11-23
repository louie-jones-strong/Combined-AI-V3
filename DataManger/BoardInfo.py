import sys
import threading

class BoardInfo():

	def __init__(self, board):
		self.MoveIDOfBestAvgFitness = 0
		self.BestAvgFitness = -sys.maxsize
		self.TotalAvgFitness = -sys.maxsize
		self.TotalTimesPlayed = 0
		self.Moves = {}
		self.PlayedMovesLookUpArray = 0
		self.Finished = False
		self.Lock = threading.Lock()
		self.BeingUsed = False
		self.Board = board
		return

	def __getstate__(self):
		state = {}
		state["Moves"] = self.Moves
		state["MoveIDOfBestAvgFitness"] = self.MoveIDOfBestAvgFitness
		state["BestAvgFitness"] = self.BestAvgFitness
		state["TotalAvgFitness"] = self.TotalAvgFitness
		state["TotalTimesPlayed"] = self.TotalTimesPlayed
		state["PlayedMovesLookUpArray"] = self.PlayedMovesLookUpArray
		state["Finished"] = self.Finished
		state["Board"] = self.Board
		
		self.Lock = threading.Lock()
		self.BeingUsed = False
		return state

	def __setstate__(self, state):
		self.Moves = state["Moves"]
		self.MoveIDOfBestAvgFitness = state["MoveIDOfBestAvgFitness"]
		self.BestAvgFitness = state["BestAvgFitness"]
		self.TotalAvgFitness = state["TotalAvgFitness"]
		self.TotalTimesPlayed = state["TotalTimesPlayed"]
		self.PlayedMovesLookUpArray = state["PlayedMovesLookUpArray"]
		self.Finished = state["Finished"]
		self.Board = state["Board"]

		self.Lock = threading.Lock()
		self.BeingUsed = False
		return
