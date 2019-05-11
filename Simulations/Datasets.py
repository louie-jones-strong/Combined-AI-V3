import RenderEngine.Shape as Shape

class Simulation(object):
	Info = {"MinPlayers":1,"MaxPlayers":1,
	        "SimName":"DataSet","NumInputs":1,
			"MinInputSize":0,"MaxInputSize":100,
			"Resolution":1}

	def __init__(self):
		self.DataSetX = [[0],[1],[2],[3],[4],[5],[6]]
		self.DataSetY = [[0],[2],[4],[6],[8],[10],[12]]
		self.BackGroundpieceList = []
		return

	def Start(self):

		self.Move = 0
		self.Board = self.DataSetX[self.Move]
		self.Turn = 1
		self.Fitness = 0
		return self.Board, self.Turn

	def MakeMove(self,inputs):
		valid = False
		if inputs[0] == self.DataSetY[self.Move][0]:
			valid = True
			self.Fitness += 1

			self.Move += 1
			if self.Move < len(self.DataSetX):
				self.Board = self.DataSetX[self.Move]
		
		return valid, self.Board, self.Turn

	def CheckFinished(self):
		finished = False
		if self.Move >= len(self.DataSetX):
			finished = True

		return finished, [self.Fitness]

	def FlipBoard(self, board):
		return board

	def FlipInput(self, move):
		return move

	def SimpleBoardOutput(self, board):
		print(board)
		return

	def ComplexBoardOutput(self, board):
		pieceList = []
		pieceList += self.BackGroundpieceList
		return pieceList
