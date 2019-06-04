import RenderEngine.Shape as Shape
import Simulations.SimulationBase as SimBase


class Simulation(SimBase.SimBase):
	Info = {"MinPlayers":2,"MaxPlayers":2,
	        "SimName":"Draughts","NumInputs":4,
			"MinInputSize":0,"MaxInputSize":7,
			"Resolution":1,"RenderSetup":True}
			
	def __init__(self):
		self.BackGroundpieceList = []
		pieceSize = 30
		boardColor = True
		for x in range(8):
			for y in range(8):

				if boardColor:
					color = [255, 255, 255]
					boardColor = False
				else:
					color = [0, 0, 0]
					boardColor = True

				self.BackGroundpieceList += [Shape.Piece([((x+0.5)-4)*pieceSize*2+350, ((y+0.5)-4)
    	                          * pieceSize*2+350], [pieceSize, pieceSize], Shape.Square(), color)]

			if boardColor:
				boardColor = False
			else:
				boardColor = True
		return

	def Start(self):
		self.Board = NewBoard()
		self.Turn = 1
		self.NumMoves = 0
		self.CanMoveAgain = None
		return self.Board, self.Turn
		
	def MakeMove(self,moveArray):
		selectedPiece = int(self.Board[moveArray[0]][moveArray[1]])

		if [moveArray[0],moveArray[1]] == self.CanMoveAgain \
			and [moveArray[2],moveArray[3]] == self.CanMoveAgain:
			self.NumMoves += 1
			self.CanMoveAgain = None
			if self.Turn == 1:
				self.Turn = 2
			else:
				self.Turn = 1
			return True, self.Board, self.Turn

		if self.Board[moveArray[2]][moveArray[3]] != 0:
			return False, self.Board, self.Turn

		#check if your pick one of your pieces
		if not(((selectedPiece > 0) and self.Turn == 1) \
		or ((selectedPiece < 0) and self.Turn == 2)):
			return False, self.Board, self.Turn

		moves = PossibleMoves(self.Board, moveArray[0], moveArray[1])
		if len(moves) == 0:
			return False, self.Board, self.Turn

		if [moveArray[2],moveArray[3]] not in moves:
			return False, self.Board, self.Turn

		#move the piece
		self.Board[moveArray[2]][moveArray[3]] = selectedPiece
		self.Board[moveArray[0]][moveArray[1]] = 0

		canMoveAgain = False
		#check if attack move if so remove piece in the middle
		if abs(moveArray[2] - moveArray[0]) > 1 or abs(moveArray[3] - moveArray[1]) > 1:
			temp = [moveArray[0]+int((moveArray[2]-moveArray[0])/2),moveArray[1]+int((moveArray[3]-moveArray[1])/2)]
			self.Board[temp[0]][temp[1]] = 0

			if len(AttackMoves(self.Board, moveArray[2], moveArray[3])) > 0:
				canMoveAgain = True
				self.CanMoveAgain = [moveArray[2],moveArray[3]]


		#upgrade the piece
		if selectedPiece == 1 and moveArray[3] == 7:
			self.Board[moveArray[2]][moveArray[3]] = 2

		elif selectedPiece == -1 and moveArray[3] == 0 :
			self.Board[moveArray[2]][moveArray[3]] = -2


		if not canMoveAgain:
			self.NumMoves += 1
			self.CanMoveAgain = None
			if self.Turn == 1:
				self.Turn = 2
			else:
				self.Turn = 1
		return True, self.Board, self.Turn

	def CheckFinished(self):
		finished = False
		player1Fitness = 0
		player2Fitness = 0

		type1Count = 0
		type2Count = 0

		type1Moves = 0
		type2Moves = 0

		for x in range(len(self.Board)):
			for y in range(len(self.Board[x])):

				if IsPieceSameSide(self.Board[x][y], 1):
					type1Count += 1
					if PossibleMoves(self.Board, x, y):
						type1Moves += 1

				elif IsPieceSameSide(self.Board[x][y], -1):
					type2Count += 1
					if PossibleMoves(self.Board, x, y):
						type2Moves += 1
		
		if type1Count == 0 or type1Moves == 0:
			finished = True
			player1Fitness = -5
			player2Fitness = 5

		if type2Count == 0 or type2Moves == 0:
			finished = True
			player1Fitness = 5
			player2Fitness = -5

		#check if progress in last 50 moves if not then draw
		if self.NumMoves >= 250:
			finished = True
			player1Fitness = 3
			player2Fitness = 3



		return finished, [player1Fitness, player2Fitness]

	def FlipBoard(self, board):
		output = []
		for loop in range(len(board)-1,-1,-1):
			temp = []
			for loop2 in range(len(board[loop])-1,-1,-1):
				temp += [board[loop][loop2]*-1]
			output += [temp]

		return output

	def FlipInput(self, move):
		temp = [7-move[0], 7-move[1], 7-move[2], 7-move[3]]
		return temp

	def SimpleBoardOutput(self, board):
		print("   0 1 2 3 4 5 6 7  ")
		for loop in range(8):
			line = ""
			for loop2 in range(8):
				if (board[loop2][loop] == 0):
					line += "  "
				else:
					if board[loop2][loop] < 0:
						line += str(board[loop2][loop])
					else:
						line += " "+str(board[loop2][loop])

			print(str(loop)+" "+str(line)+" "+str(loop))
		print("   0 1 2 3 4 5 6 7  ")
		return
	def ComplexBoardOutput(self, board):
		pieceSize = 20
		gridSize = 30

		pieceList = []
		pieceList += self.BackGroundpieceList
		grid = [8, 8]
		for x in range(grid[0]):
			for y in range(grid[1]):
				if board[x][y] != 0:
					if board[x][y] == 1:
						pieceList += [Shape.Piece([((x+0.5)-grid[0]/2)*gridSize*2+350, ((y+0.5)-grid[1]/2)
    	                                        * gridSize*2+350], [pieceSize, pieceSize], Shape.Circle(), [255, 255, 255])]
					elif board[x][y] == 2:
						pieceList += [Shape.Piece([((x+0.5)-grid[0]/2)*gridSize*2+350, ((y+0.5)-grid[1]/2)
                                                    * gridSize*2+350], [pieceSize, pieceSize], Shape.Circle(), [255, 255, 255])]

						pieceList += [Shape.Piece([((x+0.5)-grid[0]/2)*gridSize*2+350, ((y+0.5)-grid[1]/2)
                                                    * gridSize*2+350], [pieceSize*0.6, pieceSize*0.6], Shape.Crown(), [0, 0, 0])]
					elif board[x][y] == -1:
						pieceList += [Shape.Piece([((x+0.5)-grid[0]/2)*gridSize*2+350, ((y+0.5)-grid[1]/2)
                                                    * gridSize*2+350], [pieceSize, pieceSize], Shape.Circle(), [0, 0, 0])]
					else:
						pieceList += [Shape.Piece([((x+0.5)-grid[0]/2)*gridSize*2+350, ((y+0.5)-grid[1]/2)
    	                                        * gridSize*2+350], [pieceSize, pieceSize], Shape.Circle(), [0, 0, 0])]
						
						pieceList += [Shape.Piece([((x+0.5)-grid[0]/2)*gridSize*2+350, ((y+0.5)-grid[1]/2)
                                                    * gridSize*2+350], [pieceSize*0.6, pieceSize*0.6], Shape.Crown(), [255, 255, 255])]
		return pieceList

def PossibleMoves(board, X, Y):
	outputList = AttackMoves(board,X,Y)

	if board[X][Y] != -1:
		if X >= 1 and Y <= 6:
			if board[X-1][Y+1] == 0:
				outputList += [[X-1,Y+1]]
		if X <= 6 and Y <= 6:
			if board[X+1][Y+1] == 0:
				outputList += [[X+1,Y+1]]

	if board[X][Y] != 1:
		if X >= 1 and Y >= 1:
			if board[X-1][Y-1] == 0:
				outputList += [[X-1,Y-1]]
		if X <= 6 and Y >= 1:
			if board[X+1][Y-1] == 0:
				outputList += [[X+1,Y-1]]

	return outputList
		
def AttackMoves(board, X, Y):
	outputList = []
	piece = int(board[X][Y])

	if board[X][Y] != 2:
		if X >= 2 and Y <= 5:
			if board[X-2][Y+2] == 0 and IsPieceEnemySide(piece, board[X-1][Y+1]):
				outputList += [[X-2,Y+2]]

		if X <= 5 and Y <= 5:
			if board[X+2][Y+2] == 0 and IsPieceEnemySide(piece, board[X+1][Y+1]):
				outputList += [[X+2,Y+2]]

	if board[X][Y] != 1:
		if X >= 2 and Y >= 2:
			if board[X-2][Y-2] == 0 and IsPieceEnemySide(piece, board[X-1][Y-1]):
				outputList += [[X-2,Y-2]]

		if X <= 5 and Y >= 2:
			if board[X+2][Y-2] == 0 and IsPieceEnemySide(piece, board[X+1][Y-1]):
				outputList += [[X+2,Y-2]]

	return outputList

def IsPieceSameSide(piece1, piece2):
	return (piece1 < 0 and piece2 < 0) or (piece1 > 0 and piece2 > 0)

def IsPieceEnemySide(piece1, piece2):	
	return (piece1 < 0 and piece2 > 0) or (piece1 > 0 and piece2 < 0)

def NewBoard():
	Board = [[1, 0, 1, 0, 0, 0, -1, 0], 
			 [0, 1, 0, 0, 0, -1, 0, -1], 
			 [1, 0, 1, 0, 0, 0, -1, 0], 
			 [0, 1, 0, 0, 0, -1, 0, -1], 
			 [1, 0, 1, 0, 0, 0, -1, 0], 
			 [0, 1, 0, 0, 0, -1, 0, -1], 
			 [1, 0, 1, 0, 0, 0, -1, 0], 
			 [0, 1, 0, 0, 0, -1, 0, -1]]
	return Board
