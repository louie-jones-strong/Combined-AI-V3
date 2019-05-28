import RenderEngine.Shape as Shape


class SimBase:
	
	def Start(self, numPlayers):

		self.Board = []
		self.Turn = 1
		return self.Board, self.Turn


	def MakeMove(self, inputs):
		valid = False

		return valid, self.Board, self.Turn

	def CheckFinished(self):
		player1Fitness, player2Fitness = 0, 0
		finished = True
		return finished, [player1Fitness, player2Fitness]

	def FlipBoard(self, board):

		return board

	def FlipInput(self, move):
		return move

	def SimpleBoardOutput(self, board):

		return

	def ComplexBoardOutput(self, board):
		pieceList = []
		pieceList += self.BackGroundpieceList
		return pieceList
