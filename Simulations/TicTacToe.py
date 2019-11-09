import Simulations.SimulationBase as SimBase


class Simulation(SimBase.SimBase):
	Info = {"MinPlayers":2,"MaxPlayers":2,
	        "SimName":"TicTacToe","NumInputs":1,
			"MinInputSize":0,"MaxInputSize":8,
			"Resolution":1,"RenderSetup":True}

	def __init__(self):
		return

	def Start(self):

		self.Board = [0,0,0,0,0,0,0,0,0]
		self.Turn = 1
		return self.Board, self.Turn

	def MakeMove(self,inputs):
		move = int(inputs[0]) 

		valid = False
		if self.Board[move] == 0:
			self.Board[move] = self.Turn
			valid = True


		if valid:
			if self.Turn == 1:
				self.Turn = 2
			else:
				self.Turn = 1
		return valid, self.Board, self.Turn

	def CheckFinished(self):
		player1Fitness, player2Fitness = 0,0
		finished = False
		
		if CheckWin(self.Board, 1) == True:#win
			finished = True
			player1Fitness = 5
			player2Fitness = -5

		elif CheckWin(self.Board, 2) == True:#loss
			finished = True
			player1Fitness = -5
			player2Fitness = 5

		elif not(0 in self.Board):#draw
			finished = True
			player1Fitness = 3
			player2Fitness = 3
			

		return finished, [player1Fitness, player2Fitness]

	def CreateNew(self):
		sim = Simulation()
		return sim

	def FlipBoard(self, board):
		output = []
		for loop in range(len(board)):
			if board[loop] == 1:
				output += [2]
			elif board[loop] == 2:
				output += [1]
			else:
				output += [0]

		return output

	def FlipInput(self, move):
		return move

	def SimpleBoardOutput(self, board):
		loop = 0
		for y in range(3):
			temp = ""
			for x in range(3):
				if board[loop] == 0:
					temp += " "
				elif board[loop] == 1:
					temp += "X"
				else:
					temp += "O"

				loop += 1
				if x < 2:
					temp += "|"

			print(temp)
			if y < 2:
				print("-+-+-")
		return

	def ComplexOutputSetup(self):
		import RenderEngine.PolygonPiece as Piece
		import RenderEngine.Shape as Shape
		super().ComplexOutputSetup()
		self.BackGroundpieceList += [Piece.PolygonPiece([350,300],[150, 1], Shape.HorizontalLine(), [0, 0, 0])]
		self.BackGroundpieceList += [Piece.PolygonPiece([350,400],[150, 1], Shape.HorizontalLine(), [0, 0, 0])]
		
		self.BackGroundpieceList += [Piece.PolygonPiece([300, 350], [1, 150], Shape.VerticalLine(), [0, 0, 0])]
		self.BackGroundpieceList += [Piece.PolygonPiece([400, 350], [1, 150], Shape.VerticalLine(), [0, 0, 0])]
		return

	def ComplexBoardOutput(self, board):
		import RenderEngine.PolygonPiece as Piece
		import RenderEngine.Shape as Shape
		pieceList = super().ComplexBoardOutput(board)
		pieceSize = 40
		gridSize = 50

		grid = [3, 3]
		loop = 0
		for x in range(grid[0]):
			for y in range(grid[1]):

				if board[loop] != 0:
					if board[loop] == 1:#X
						pieceList += [Piece.PolygonPiece([((x+0.5)-grid[0]/2)*gridSize*2+350, ((y+0.5)-grid[1]/2)* gridSize*2+350], [pieceSize, pieceSize], Shape.Cross(), [0, 0, 0])]
					else:#O
						pieceList += [Piece.PolygonPiece([((x+0.5)-grid[0]/2)*gridSize*2+350, ((y+0.5)-grid[1]/2)* gridSize*2+350], [pieceSize, pieceSize], Shape.Circle(), [0, 0, 0])]
				loop += 1
		return pieceList

def CheckWin(board, player):
	if    (board[0] == player and board[1] == player and board[2] == player) \
	   or (board[3] == player and board[4] == player and board[5] == player) \
	   or (board[6] == player and board[7] == player and board[8] == player) \
	   or (board[0] == player and board[3] == player and board[6] == player) \
	   or (board[1] == player and board[4] == player and board[7] == player) \
	   or (board[2] == player and board[5] == player and board[8] == player) \
	   or (board[0] == player and board[4] == player and board[8] == player) \
	   or (board[6] == player and board[4] == player and board[2] == player):
		return True

	else:
		return False
