import RenderEngine.Shape as Shape
import RenderEngine.PolygonPiece as Piece
import RenderEngine.ImagePiece as ImagePiece
import Simulations.SimulationBase as SimBase


class Simulation(SimBase.SimBase):
	Info = {"MinPlayers":2,"MaxPlayers":2,
			"SimName":"Chess","NumInputs":4,
			"MinInputSize":0,"MaxInputSize":7,
			"Resolution":1,"RenderSetup":True}
	
	def __init__(self):
		self.PieceImageDict = {}
		self.PieceImageDict[1] = ImagePiece.LoadImage("RenderEngine\\Images\\Chess\\Type1.png")
		self.PieceImageDict[2] = ImagePiece.LoadImage("RenderEngine\\Images\\Chess\\Type2.png")
		self.PieceImageDict[3] = ImagePiece.LoadImage("RenderEngine\\Images\\Chess\\Type3.png")
		self.PieceImageDict[4] = ImagePiece.LoadImage("RenderEngine\\Images\\Chess\\Type4.png")
		self.PieceImageDict[5] = ImagePiece.LoadImage("RenderEngine\\Images\\Chess\\Type5.png")
		self.PieceImageDict[6] = ImagePiece.LoadImage("RenderEngine\\Images\\Chess\\Type6.png")

		self.PieceImageDict[-1] = ImagePiece.LoadImage("RenderEngine\\Images\\Chess\\Type-1.png")
		self.PieceImageDict[-2] = ImagePiece.LoadImage("RenderEngine\\Images\\Chess\\Type-2.png")
		self.PieceImageDict[-3] = ImagePiece.LoadImage("RenderEngine\\Images\\Chess\\Type-3.png")
		self.PieceImageDict[-4] = ImagePiece.LoadImage("RenderEngine\\Images\\Chess\\Type-4.png")
		self.PieceImageDict[-5] = ImagePiece.LoadImage("RenderEngine\\Images\\Chess\\Type-5.png")
		self.PieceImageDict[-6] = ImagePiece.LoadImage("RenderEngine\\Images\\Chess\\Type-6.png")

		boardImg = ImagePiece.LoadImage("RenderEngine\\Images\\Board.png")
		self.BackGroundpieceList = []
		pieceSize = 30
		grid = [8,8]
		scale = [grid[0]*pieceSize, grid[1]*pieceSize]
		pos = [scale[0], scale[1]]
		self.BackGroundpieceList += [ImagePiece.ImagePiece(pos, scale, boardImg)]
		return

	def CreateNew(self):
		sim = Simulation()
		return sim
		
	def Start(self):
		self.Board = NewBoard()
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

		if not (PiceMoveRulesCheck(inputs, self.Board, self.Turn)):
			return False, self.Board, self.Turn

		self.Board[ inputs[3] ][ inputs[2] ] = self.Board[ inputs[1] ][ inputs[0] ]
		self.Board[ inputs[1] ][ inputs[0] ] = 0
		self.NumMoves += 1
		return True, self.Board, self.Turn

	def CheckFinished(self):
		player1Fitness, player2Fitness = 0,0
		finished = False
		
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

	def ComplexBoardOutput(self, board):
		pieceSize = 20
		gridSize = 30

		pieceList = []
		pieceList += self.BackGroundpieceList
		grid = [8, 8]
		for x in range(grid[0]):
			for y in range(grid[1]):
				pieceType = board[y][x]

				if pieceType in self.PieceImageDict:
					img = self.PieceImageDict[pieceType]
					pieceList += [ImagePiece.ImagePiece([((x+0.5)-grid[0]/2)*gridSize*2+350, ((y+0.5)-grid[1]/2)
												* gridSize*2+350], [pieceSize, pieceSize], img)]
					
		return pieceList

def NewBoard():
	board = [[4,2,3,6,5,3,2,4],
			 [1,1,1,1,1,1,1,1],
			 [0,0,0,0,0,0,0,0],
			 [0,0,0,0,0,0,0,0],
			 [0,0,0,0,0,0,0,0],
			 [0,0,0,0,0,0,0,0],
			 [-1,-1,-1,-1,-1,-1,-1,-1],
			 [-4,-2,-3,-6,-5,-3,-2,-4]]

	return board

def PiceMoveRulesCheck(move, board, turn ):
	pice = board[ move[1] ][ move[0] ]
	if abs(pice) == 6:
		return kingCheck(move, board, turn)

	elif abs(pice) == 5:
		return QueenCheck(move, board, turn)

	elif abs(pice) == 4:
		return RooksCheck(move, board, turn)

	elif abs(pice) == 3:
		return BishopsCheck(move, board, turn)

	elif abs(pice) == 2:
		return KnightsCheck(move, board, turn)

	elif abs(pice) == 1:
		return PawnCheck(move, board, turn)

	else:
		return False

def kingCheck(move, board, turn):
	change_x = abs(move[0] - move[2])
	change_y = abs(move[1] - move[3])
	if change_y > 1 or change_x > 1:
		return False
	else:
		return CheckLineOfSight( board , move)

def QueenCheck(move, board, turn):
	change_x = abs(move[0] - move[2])
	change_y = abs(move[1] - move[3])
	if not( change_x == change_y) and not(change_x == 0) and not(change_y == 0):
		return False
	return CheckLineOfSight( board , move)

def RooksCheck(move, board, turn):
	change_x = abs(move[0] - move[2])
	change_y = abs(move[1] - move[3])
	if not ( change_x == 0 or change_y == 0 ):
		return False
	return CheckLineOfSight( board , move)

def BishopsCheck(move, board, turn):
	change_x = abs(move[0] - move[2])
	change_y = abs(move[1] - move[3])
	if not( change_x == change_y):
		return False
	return CheckLineOfSight( board , move)

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
	if turn == 1 and (change_y <= 0 or change_y > 2):
		return False
	if turn == 2 and (change_y >=0 or change_y < -2):
		return 
	if turn == 1 and change_y == 2 and not(move[1] == 1):
		return False
	if turn == 2 and change_y == -2 and not(move[1] == 6):
		return False
	return CheckLineOfSight( board , move)

def CheckLineOfSight(board, move):
	change_x = move[2] - move[0]
	change_y = move[3] - move[1]
	if abs(change_y) == 0:
		for loop in range( move[1] , move[3] ):
			if not (board[ move[0] ][ loop ] == 0):
				return False
	elif abs(change_x) == 0:
		for loop in range( move[0] , move[2] ):
			if not (board[ loop ][ move[1] ] == 0):
				return False
	elif abs(change_x) == abs(change_y):
		for loop in range(1,abs(change_x)):
			x = loop
			y = loop
			if change_x < 0:
				x = x * -1
			if change_y < 0:
				y = y * -1
			if not (board[ move[1] + y ][ move[0] + x] == 0):
				return False
	return True
