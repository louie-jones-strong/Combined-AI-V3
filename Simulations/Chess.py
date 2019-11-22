import Simulations.SimulationBase as SimBase

class Simulation(SimBase.SimBase):
	Info = {"MinPlayers":2,"MaxPlayers":2,
			"SimName":"Chess","NumInputs":4,
			"MinInputSize":0,"MaxInputSize":7,
			"Resolution":1,"RenderSetup":True}
	
	def __init__(self):
		return

	def CreateNew(self):
		sim = Simulation()
		return sim
		
	def Start(self):
		self.Board, self.KingPos = NewBoard()
		self.Turn = 1
		self.NumMoves=0
		return self.Board, self.Turn

	def MakeMove(self,inputs):
		if (inputs[0]<0 or inputs[0]>7 or
			inputs[1]<0 or inputs[1]>7 or 
			inputs[2]<0 or inputs[2]>7 or
			inputs[3]<0 or inputs[3]>7):
			return False, self.Board, self.Turn
		
		if inputs[0] == inputs[1] and inputs[2] == inputs[3]:
			return False, self.Board, self.Turn


		if self.Board[ inputs[1] ][ inputs[0] ] == 0:
			return False, self.Board, self.Turn


		if self.Turn == 1 and self.Board[ inputs[1] ][ inputs[0] ] > 0:
			return False, self.Board, self.Turn
		if self.Turn == 2 and self.Board[ inputs[1] ][ inputs[0] ] < 0:
			return False, self.Board, self.Turn


		if self.Turn == 1 and self.Board[ inputs[3] ][ inputs[2] ] < 0:
			return False, self.Board, self.Turn
		if self.Turn == 2 and self.Board[ inputs[3] ][ inputs[2] ] > 0:
			return False, self.Board, self.Turn

		if not (PieceMoveRulesCheck(inputs, self.Board, self.Turn)):
			return False, self.Board, self.Turn

		oldKingPos = [self.KingPos[self.Turn][0], self.KingPos[self.Turn][1]]
		if abs(self.Board[ inputs[1] ][ inputs[0] ]) == 6:
			self.KingPos[self.Turn] = [inputs[3], inputs[2]]

		if abs(self.Board[ inputs[1] ][ inputs[0] ]) == 1 and (inputs[3] == 0 or inputs[3] == 7):
			self.Board[ inputs[1] ][ inputs[0]] = 5*self.Board[ inputs[1] ][ inputs[0] ]

		oldPiece = int(self.Board[ inputs[3] ][ inputs[2] ])

		self.Board[ inputs[3] ][ inputs[2] ] = self.Board[ inputs[1] ][ inputs[0] ]
		self.Board[ inputs[1] ][ inputs[0] ] = 0

		if self.IsInCheck(self.Turn):
			self.Board[ inputs[1] ][ inputs[0] ] = int(self.Board[ inputs[3] ][ inputs[2] ])
			self.Board[ inputs[3] ][ inputs[2] ] = oldPiece

			self.KingPos[self.Turn] = [oldKingPos[0], oldKingPos[1]]

			return False, self.Board, self.Turn

		self.NumMoves += 1

		if self.Turn == 1:
			self.Turn = 2
		else:
			self.Turn = 1

		return True, self.Board, self.Turn

	def CheckFinished(self):
		player1Fitness, player2Fitness = 0,0
		finished = False

		if self.Board[ self.KingPos[1][0] ][ self.KingPos[1][1]] == 0:
			finished = True
			player1Fitness = -5
			player2Fitness = 5
		
		elif self.Board[ self.KingPos[2][0] ][ self.KingPos[2][1]] == 0:
			finished = True
			player1Fitness = 5
			player2Fitness = -5

		elif self.NumMoves >= 1000:
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
		print("   0  1  2  3  4  5  6  7   ")

		for loop in range(8):
			line = ""
			for loop2 in range(8):
				if board[loop][loop2] < 0:
					line += " " + str(board[loop][loop2])
				else:
					line += "  " + str(board[loop][loop2])

			print(str(loop)+" "+str(line)+" "+str(loop))


		print("   0  1  2  3  4  5  6  7   ")
		return

	def ComplexOutputSetup(self):
		import RenderEngine.Piece.ImagePiece as ImagePiece
		super().ComplexOutputSetup()
		self.PieceImageDict = {}
		self.PieceImageDict[-1] = ImagePiece.LoadImage("Assets\\Images\\Chess\\Type1.png")
		self.PieceImageDict[-2] = ImagePiece.LoadImage("Assets\\Images\\Chess\\Type2.png")
		self.PieceImageDict[-3] = ImagePiece.LoadImage("Assets\\Images\\Chess\\Type3.png")
		self.PieceImageDict[-4] = ImagePiece.LoadImage("Assets\\Images\\Chess\\Type4.png")
		self.PieceImageDict[-5] = ImagePiece.LoadImage("Assets\\Images\\Chess\\Type5.png")
		self.PieceImageDict[-6] = ImagePiece.LoadImage("Assets\\Images\\Chess\\Type6.png")

		self.PieceImageDict[1] = ImagePiece.LoadImage("Assets\\Images\\Chess\\Type-1.png")
		self.PieceImageDict[2] = ImagePiece.LoadImage("Assets\\Images\\Chess\\Type-2.png")
		self.PieceImageDict[3] = ImagePiece.LoadImage("Assets\\Images\\Chess\\Type-3.png")
		self.PieceImageDict[4] = ImagePiece.LoadImage("Assets\\Images\\Chess\\Type-4.png")
		self.PieceImageDict[5] = ImagePiece.LoadImage("Assets\\Images\\Chess\\Type-5.png")
		self.PieceImageDict[6] = ImagePiece.LoadImage("Assets\\Images\\Chess\\Type-6.png")

		boardImg = ImagePiece.LoadImage("Assets\\Images\\Board.png")
		scale = [240, 240]
		self.BackGroundpieceList = [ImagePiece.ImagePiece(scale, scale, boardImg)]
		return

	def ComplexBoardOutput(self, board):
		import RenderEngine.Piece.ImagePiece as ImagePiece
		pieceList = super().ComplexBoardOutput(board)

		pieceSize = 20
		gridSize = 30

		grid = [8, 8]
		for x in range(grid[0]):
			for y in range(grid[1]):
				pieceType = board[y][x]

				if pieceType in self.PieceImageDict:
					img = self.PieceImageDict[pieceType]
					pieceList += [ImagePiece.ImagePiece([((x+0.5)-grid[0]/2)*gridSize*2+350, ((y+0.5)-grid[1]/2)
												* gridSize*2+350], [pieceSize, pieceSize], img)]
					
		return pieceList

	def IsInCheck(self, turn):
		kingPosY, kingPosX = self.KingPos[turn]

		KnightChecks = [
			(kingPosX-1, kingPosY-2),
			(kingPosX-2, kingPosY-1),
			(kingPosX+1, kingPosY+2),
			(kingPosX+2, kingPosY+1),
			(kingPosX-1, kingPosY+2),
			(kingPosX-2, kingPosY+1),
			(kingPosX+1, kingPosY-2),
			(kingPosX+2, kingPosY-1)]

		for x, y in KnightChecks:

			if x >= 0 and x < 8 and y >= 0 and y < 8:
				piece = self.Board[y][x]
				if abs(piece) == 2 and IsPieceEnemy(piece, turn):
					return True

		#diagonal check
		for change in range(-7, 8):
			x = kingPosX + change
			y = kingPosY + change

			if x >= 0 and x < 8 and y >= 0 and y < 8:
				if ((abs(piece) == 3 or abs(piece) == 5 or
					(abs(piece) == 1 and change < 0 and turn == 2) or
					(abs(piece) == 1 and change > 0 and turn == 1)) and
					IsPieceEnemy(piece, turn) and
					CheckLineOfSight(self.Board, [kingPosY, kingPosX, y, x])):

					return True

			x = kingPosX - change
			y = kingPosY + change

			if x >= 0 and x < 8 and y >= 0 and y < 8:
				if ((abs(piece) == 3 or abs(piece) == 5 or
					(abs(piece) == 1 and change < 0 and turn == 2) or
					(abs(piece) == 1 and change > 0 and turn == 1)) and
					IsPieceEnemy(piece, turn) and
					CheckLineOfSight(self.Board, [kingPosY, kingPosX, y, x])):

					return True
				

		for loop in range(8):
			
			#horizontal check
			piece = self.Board[kingPosY][loop]

			if ((abs(piece) == 4 or abs(piece) == 5) and 
				IsPieceEnemy(piece, turn) and
				CheckLineOfSight(self.Board, [kingPosY, kingPosX, kingPosY, loop])):

				return True

			#Vertical check
			piece = self.Board[loop][kingPosX]

			if ((abs(piece) == 4 or abs(piece) == 5) and 
				IsPieceEnemy(piece, turn) and
				CheckLineOfSight(self.Board, [kingPosY, kingPosX, loop, kingPosX])):
				
				return True
		return False

def NewBoard():
	board = [[4,2,3,6,5,3,2,4],
			 [1,1,1,1,1,1,1,1],
			 [0,0,0,0,0,0,0,0],
			 [0,0,0,0,0,0,0,0],
			 [0,0,0,0,0,0,0,0],
			 [0,0,0,0,0,0,0,0],
			 [-1,-1,-1,-1,-1,-1,-1,-1],
			 [-4,-2,-3,-6,-5,-3,-2,-4]]

	KingPos = {}
	KingPos[2] = [0, 3]
	KingPos[1] = [7, 3]
	return board, KingPos

def PieceMoveRulesCheck(move, board, turn ):
	piece = abs(board[ move[1] ][ move[0] ])
	if piece == 6:
		return kingCheck(move, board, turn)

	elif piece == 5:
		return QueenCheck(move, board, turn)

	elif piece == 4:
		return RooksCheck(move, board, turn)

	elif piece == 3:
		return BishopsCheck(move, board, turn)

	elif piece == 2:
		return KnightsCheck(move, board, turn)

	elif piece == 1:
		return PawnCheck(move, board, turn)

	else:
		return False

def kingCheck(move, board, turn):
	change_x = abs(move[0] - move[2])
	change_y = abs(move[1] - move[3])
	if change_y > 1 or change_x > 1:
		return False
	else:
		return CheckLineOfSight(board, move)

def QueenCheck(move, board, turn):
	change_x = abs(move[0] - move[2])
	change_y = abs(move[1] - move[3])
	if not( change_x == change_y) and not(change_x == 0) and not(change_y == 0):
		return False
	return CheckLineOfSight(board, move)

def RooksCheck(move, board, turn):
	change_x = abs(move[0] - move[2])
	change_y = abs(move[1] - move[3])
	if change_x != 0 and change_y != 0:
		return False
	return CheckLineOfSight(board, move)

def BishopsCheck(move, board, turn):
	change_x = abs(move[0] - move[2])
	change_y = abs(move[1] - move[3])
	if not( change_x == change_y):
		return False
	return CheckLineOfSight(board, move)

def KnightsCheck(move, board, turn):
	change_x = abs(move[0] - move[2])
	change_y = abs(move[1] - move[3])
	if not(change_x == 2 and change_y == 1) and not(change_x == 1 and change_y == 2):
		return False
	else:
		return True

def PawnCheck(move, board, turn):
	change_x = abs(move[0] - move[2])
	change_y = move[1] - move[3]
	
	if change_x > 1:
		return False
	if abs(change_y) > 2 or change_y == 0:
		return False

	if change_x == 1:
		if board[move[3]][move[2]] == 0:
			return False
		if board[move[3]][move[2]] < 0 and turn == 1:
			return False
		if board[move[3]][move[2]] > 0 and turn == 2:
			return False
	elif board[move[3]][move[2]] != 0:
		return False

	if turn == 1 and change_y <= 0:
		return False
	if turn == 2 and change_y >= 0:
		return False
	
	if abs(change_y) == 2:
		if turn == 1 and not(move[1] == 1):
			return False
		if turn == 2 and not(move[1] == 6):
			return False

	return CheckLineOfSight(board, move)

def CheckLineOfSight(board, move):
	change_x = move[2] - move[0]
	change_y = move[3] - move[1]
	if change_y == 0:
		if move[0] < move[2]:
			for loop in range( move[0] , move[2] ):
				if loop != move[2] and loop != move[0] and board[ move[1] ][ loop ] != 0:
					return False
		else:
			for loop in range( move[2] , move[0] ):
				if loop != move[2] and loop != move[0] and board[ move[1] ][ loop ] != 0:
					return False

	elif change_x == 0:
		if move[1] < move[3]:
			for loop in range( move[1] , move[3] ):
				if loop != move[3] and loop != move[1] and board[ loop ][ move[0] ] != 0:
					return False
		else:
			for loop in range( move[3] , move[1] ):
				if loop != move[3] and loop != move[1] and board[ loop ][ move[0] ] != 0:
					return False

	elif abs(change_x) == abs(change_y):
		for loop in range(1,abs(change_x)):
			x = loop
			y = loop
			if change_x < 0:
				x = x * -1
			if change_y < 0:
				y = y * -1
			if board[ move[1] + y ][ move[0] + x] != 0:
				return False

	return True

def IsPieceEnemy(piece, turn):
	if piece < 0 and turn == 1:
		return False
	if piece > 0 and turn == 2:
		return False
	return True