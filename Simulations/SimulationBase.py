import RenderEngine.Shape as Shape


class SimBase:
	ComplexOutputSetupDone = False

	def __init__(self):
		return

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
		print(board)
		return

	def ComplexOutputSetup(self):
		self.BackGroundpieceList = []
		self.ComplexOutputSetupDone = True
		return

	def ComplexBoardOutput(self, board):
		if not self.ComplexOutputSetupDone:
			self.ComplexOutputSetup()

		pieceList = []
		pieceList += self.BackGroundpieceList
		return pieceList
