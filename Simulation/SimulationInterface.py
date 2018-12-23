class Simulation(object):
	Info = {}

	def Start(self):
		self.Board = []
		self.Turn = 1
		self.Finished = False
		return self.Board, self.Turn

	def MakeSelection(self,X,Y):
		valid = True
		return valid, self.Board

	def MakeMove(self,X,Y):
		valid = True
		return valid, self.Board, self.Turn

	def CheckFinished(self):
		player1Fitness, player2Fitness = 0,0
		return self.Finished, [player1Fitness, player2Fitness]

	def FlipBoard(self):

		return self.Board

	def FlipInput(self, move):
		return move
